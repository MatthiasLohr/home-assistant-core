"""TOLO Sauna climate controls (main sauna control)."""

from typing import Any, Callable, List, Optional

from tololib.const import Calefaction

from homeassistant.components.climate import (
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    ClimateEntity,
)
from homeassistant.components.climate.const import (
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    CURRENT_HVAC_OFF,
    FAN_OFF,
    FAN_ON,
    SUPPORT_FAN_MODE,
    SUPPORT_TARGET_HUMIDITY,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, PRECISION_WHOLE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from . import ToloSaunaCoordinatorEntity
from .const import (
    DEFAULT_MAX_HUMIDITY,
    DEFAULT_MAX_TEMP,
    DEFAULT_MIN_HUMIDITY,
    DEFAULT_MIN_TEMP,
    DOMAIN,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[List[Entity]], None],
) -> None:
    """Set up climate controls for TOLO Sauna."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([SaunaClimate(coordinator, entry)])


class SaunaClimate(ToloSaunaCoordinatorEntity, ClimateEntity):
    """Sauna climate control."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_climate" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Return name."""
        return "Sauna Climate"

    @property
    def temperature_unit(self) -> str:
        """Return temperature uni."""
        return TEMP_CELSIUS

    @property
    def precision(self) -> float:
        """Return precision."""
        return PRECISION_WHOLE

    @property
    def current_temperature(self) -> int:
        """Return current temperature."""
        return self.status.current_temperature

    @property
    def current_humidity(self) -> int:
        """Return current humidity."""
        return self.status.current_humidity

    @property
    def target_temperature(self) -> int:
        """Return target temperature."""
        return self.settings.target_temperature

    @property
    def target_humidity(self) -> int:
        """Return target humidity."""
        return self.settings.target_humidity

    @property
    def max_temp(self) -> int:
        """Return maximum supported temperature."""
        return DEFAULT_MAX_TEMP

    @property
    def min_temp(self) -> int:
        """Return minimum supported temperature."""
        return DEFAULT_MIN_TEMP

    @property
    def max_humidity(self) -> int:
        """Return maximum supported humidity."""
        return DEFAULT_MAX_HUMIDITY

    @property
    def min_humidity(self) -> int:
        """Return minimum supported humidity."""
        return DEFAULT_MIN_HUMIDITY

    @property
    def hvac_mode(self) -> str:
        """Get current HVAC mode."""
        if self.status.power_on:
            return HVAC_MODE_HEAT
        else:
            return HVAC_MODE_OFF

    @property
    def hvac_action(self) -> Optional[str]:
        """Execute HVAC action."""
        if self.status.calefaction == Calefaction.HEAT:
            return CURRENT_HVAC_HEAT
        elif self.status.calefaction == Calefaction.KEEP:
            return CURRENT_HVAC_IDLE
        elif self.status.calefaction == Calefaction.INACTIVE:
            return CURRENT_HVAC_OFF
        return None

    @property
    def hvac_modes(self) -> List[str]:
        """Return supported HVAC modes."""
        return [HVAC_MODE_OFF, HVAC_MODE_HEAT]

    @property
    def preset_mode(self) -> None:
        """Return current preset mode."""
        return None

    @property
    def preset_modes(self) -> None:
        """Return supported preset modes."""
        return None

    @property
    def fan_mode(self) -> str:
        """Return current fan mode."""
        if self.status.fan_on:
            return FAN_ON
        else:
            return FAN_OFF

    @property
    def fan_modes(self) -> List[str]:
        """Return supported fan modes."""
        return [FAN_ON, FAN_OFF]

    @property
    def swing_mode(self) -> None:
        """Return current swing mode (None supported)."""
        return None

    @property
    def swing_modes(self) -> None:
        """Return supported swing modes (None)."""
        return None

    @property
    def supported_features(self) -> int:
        """Return supported features."""
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_TARGET_HUMIDITY | SUPPORT_FAN_MODE

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        """Set HVAC mode."""
        if hvac_mode == HVAC_MODE_OFF:
            await self.hass.async_add_executor_job(self.client.set_power_on, False)
        elif hvac_mode == HVAC_MODE_HEAT:
            await self.hass.async_add_executor_job(self.client.set_power_on, True)
        else:
            pass  # TODO raise error for unsupported HVAC mode
        await self.coordinator.async_refresh()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set fan mode."""
        if fan_mode == FAN_OFF:
            await self.hass.async_add_executor_job(self.client.set_fan_on, False)
        elif fan_mode == FAN_ON:
            await self.hass.async_add_executor_job(self.client.set_fan_on, True)
        else:
            pass  # TODO raise error for unsupported fan mode
        await self.coordinator.async_refresh()

    async def async_set_humidity(self, humidity: float) -> None:
        """Set desired target humidity."""
        await self.hass.async_add_executor_job(
            self.client.set_target_humidity, int(humidity)
        )
        await self.coordinator.async_refresh()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set desired target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        await self.hass.async_add_executor_job(
            self.client.set_target_temperature, int(temperature)
        )
        await self.coordinator.async_refresh()
