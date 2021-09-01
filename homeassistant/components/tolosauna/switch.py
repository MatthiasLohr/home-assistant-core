"""TOLO Sauna switch controls ()."""

from typing import Any, Callable, List

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from . import ToloSaunaCoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[List[Entity]], None],
) -> None:
    """Set up switches for TOLO Sauna."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    await coordinator.async_config_entry_first_refresh()
    async_add_entities(
        [
            PowerSwitch(coordinator, entry),
            FanSwitch(coordinator, entry),
            AromaTherapySwitch(coordinator, entry),
            SweepSwitch(coordinator, entry),
            SaltBathSwitch(coordinator, entry),
        ]
    )


class PowerSwitch(ToloSaunaCoordinatorEntity, SwitchEntity):
    """Power switch."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_power" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Switch name."""
        return "Power"

    @property
    def icon(self) -> str:
        """Icon to use in frontend."""
        return "mdi:power"

    @property
    def is_on(self) -> bool:
        """Return if power is turned on."""
        return self.status.power_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on power."""
        await self.hass.async_add_executor_job(self.client.set_power_on, True)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off power."""
        await self.hass.async_add_executor_job(self.client.set_power_on, False)
        await self.coordinator.async_refresh()


class FanSwitch(ToloSaunaCoordinatorEntity, SwitchEntity):
    """Fan switch."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_fan" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Switch name."""
        return "Fan"

    @property
    def icon(self) -> str:
        """Icon to use in frontend."""
        return "mdi:fan"

    @property
    def is_on(self) -> bool:
        """Return if fan is turned on."""
        return self.status.fan_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on fan."""
        await self.hass.async_add_executor_job(self.client.set_fan_on, True)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off fan."""
        await self.hass.async_add_executor_job(self.client.set_fan_on, False)
        await self.coordinator.async_refresh()


class AromaTherapySwitch(ToloSaunaCoordinatorEntity, SwitchEntity):
    """Switch for aroma therapy."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_aroma_therapy" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Switch name."""
        return "Aroma Therapy"

    @property
    def icon(self) -> str:
        """Icon to use in frontend."""
        return "mdi:bottle-tonic"

    @property
    def is_on(self) -> bool:
        """Return if aroma therapy is on."""
        return self.status.aroma_therapy_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on aroma therapy."""
        await self.hass.async_add_executor_job(self.client.set_aroma_therapy_on, True)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off aroma therapy."""
        await self.hass.async_add_executor_job(self.client.set_aroma_therapy_on, False)
        await self.coordinator.async_refresh()


class SweepSwitch(ToloSaunaCoordinatorEntity, SwitchEntity):
    """Sweep switch."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_sweep" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Switch name."""
        return "Sweep"

    @property
    def icon(self) -> str:
        """Icon to use in frontend."""
        return "mdi:broom"

    @property
    def is_on(self) -> bool:
        """Return if sweep is enabled."""
        return self.status.sweep_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on sweep."""
        await self.hass.async_add_executor_job(self.client.set_sweep_on, True)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn of sweep."""
        await self.hass.async_add_executor_job(self.client.set_sweep_on, False)
        await self.coordinator.async_refresh()


class SaltBathSwitch(ToloSaunaCoordinatorEntity, SwitchEntity):
    """Switch for enabling/disabling salt bath."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_salt_bath" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Switch name."""
        return "Salt Bath"

    @property
    def icon(self) -> str:
        """Icon to use in frontend."""
        return "mdi:spray"

    @property
    def is_on(self) -> bool:
        """Return if salt bath switch is on."""
        return self.status.salt_bath_on

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on salt bath switch."""
        await self.hass.async_add_executor_job(self.client.set_salt_bath_on, True)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off salt bath switch."""
        await self.hass.async_add_executor_job(self.client.set_salt_bath_on, False)
        await self.coordinator.async_refresh()
