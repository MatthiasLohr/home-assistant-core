"""TOLO Sauna light controls (sauna lights)."""

from typing import Any, Callable, List, Set

from tololib.const import LampMode

from homeassistant.components.light import (
    ATTR_EFFECT,
    COLOR_MODE_ONOFF,
    SUPPORT_EFFECT,
    LightEntity,
)
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
    """Set up lights for TOLO Sauna."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([SaunaLight(coordinator, entry)])


class SaunaLight(ToloSaunaCoordinatorEntity, LightEntity):
    """Sauna light."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_lights" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Return name."""
        return "Lights"

    @property
    def effect(self) -> str:
        """Return the currently activated effect."""
        return str(self.settings.lamp_mode.name).capitalize()

    @property
    def effect_list(self) -> List[str]:
        """Return list of supported effects for lamp."""
        return [str(mode.name).capitalize() for mode in LampMode]

    @property
    def is_on(self) -> bool:
        """Return if lamp is turned on."""
        return self.status.lamp_on

    @property
    def supported_color_modes(self) -> Set[str]:
        """Return the supported color modes of this light."""
        return set(COLOR_MODE_ONOFF)

    @property
    def supported_features(self) -> int:
        """Return features of this light."""
        return SUPPORT_EFFECT

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on light."""
        if kwargs.get(ATTR_EFFECT) is not None:
            await self.hass.async_add_executor_job(
                self.client.set_lamp_mode,
                LampMode[str(kwargs.get(ATTR_EFFECT)).upper()],
            )
        await self.hass.async_add_executor_job(self.client.set_lamp_on, True)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off light."""
        await self.hass.async_add_executor_job(self.client.set_lamp_on, False)
        await self.coordinator.async_refresh()
