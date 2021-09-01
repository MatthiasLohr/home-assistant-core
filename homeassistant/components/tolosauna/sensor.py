"""TOLO Sauna sensor controls ()."""

from typing import Callable, List

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    STATE_CLOSED,
    STATE_OPEN,
    TEMP_CELSIUS,
    TIME_MINUTES,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import StateType

from . import ToloSaunaCoordinatorEntity
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[List[Entity]], None],
) -> None:
    """Set up sensors for TOLO Sauna."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    await coordinator.async_config_entry_first_refresh()
    async_add_entities(
        [
            FanTimerSensor(coordinator, entry),
            PowerTimerSensor(coordinator, entry),
            SaltBathTimerSensor(coordinator, entry),
            TankTemperatureSensor(coordinator, entry),
            WaterFlowInSensor(coordinator, entry),
            WaterFlowOutSensor(coordinator, entry),
            WaterLevelSensor(coordinator, entry),
        ]
    )


class FanTimerSensor(ToloSaunaCoordinatorEntity, SensorEntity):
    """Sensor for fan timer."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_fan_timer" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Return name."""
        return "Fan Timer"

    @property
    def icon(self) -> str:
        """Return frontend icon."""
        return "mdi:fan"

    @property
    def state(self) -> StateType:
        """Return state."""
        return self.status.fan_timer

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement."""
        return TIME_MINUTES


class PowerTimerSensor(ToloSaunaCoordinatorEntity, SensorEntity):
    """Sensor for power timer."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_power_timer" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Return name."""
        return "Power Timer"

    @property
    def icon(self) -> str:
        """Return frontend icon."""
        return "mdi:power"

    @property
    def state(self) -> StateType:
        """Return state."""
        return self.status.power_timer

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement."""
        return TIME_MINUTES


class SaltBathTimerSensor(ToloSaunaCoordinatorEntity, SensorEntity):
    """Sensor for salt bath timer."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_salt_bath_timer" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Return name."""
        return "Salt Bath Timer"

    @property
    def icon(self) -> str:
        """Return frontend icon."""
        return "mdi:spray"

    @property
    def state(self) -> StateType:
        """Return state."""
        return self.status.salt_bath_timer

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement."""
        return TIME_MINUTES


class TankTemperatureSensor(ToloSaunaCoordinatorEntity, SensorEntity):
    """Sensor for water tank temperature."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_tank_temperature" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Return name."""
        return "Tank Temperature"

    @property
    def icon(self) -> str:
        """Return frontend icon."""
        return "mdi:coolant-temperature"

    @property
    def state(self) -> StateType:
        """Return state."""
        return self.status.tank_temperature

    @property
    def device_class(self) -> str:
        """Return device class."""
        return "temperature"

    @property
    def unit_of_measurement(self) -> str:
        """Return unit of measurement."""
        return TEMP_CELSIUS


class WaterFlowInSensor(ToloSaunaCoordinatorEntity, SensorEntity):
    """Sensor for water flow in."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_water_flow_in" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Return name."""
        return "Water Flow In"

    @property
    def icon(self) -> str:
        """Return frontend icon."""
        if self.status.flow_in:
            return "mdi:valve-open"
        else:
            return "mdi:valve-closed"

    @property
    def state(self) -> StateType:
        """Return state."""
        if self.status.flow_in:
            return STATE_OPEN
        else:
            return STATE_CLOSED


class WaterFlowOutSensor(ToloSaunaCoordinatorEntity, SensorEntity):
    """Sensor for water flow out."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_water_flow_out" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Return name."""
        return "Water Flow Out"

    @property
    def icon(self) -> str:
        """Return frontend icon."""
        if self.status.flow_out:
            return "mdi:valve-open"
        else:
            return "mdi:valve-closed"

    @property
    def state(self) -> StateType:
        """Return state."""
        if self.status.flow_out:
            return STATE_OPEN
        else:
            return STATE_CLOSED


class WaterLevelSensor(ToloSaunaCoordinatorEntity, SensorEntity):
    """Water level sensor."""

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "%s_water_level" % self._config_entry.entry_id

    @property
    def name(self) -> str:
        """Return name."""
        return "Water Level"

    @property
    def icon(self) -> str:
        """Return frontend icon."""
        if self.status.water_level == 1:
            return "mdi:gauge-low"
        elif self.status.water_level == 2:
            return "mdi:gauge"
        elif self.status.water_level == 3:
            return "mdi:gauge-full"
        else:
            return "mdi:gauge-empty"

    @property
    def state(self) -> StateType:
        """Return current water level."""
        return round(100 / 3 * self.status.water_level)

    @property
    def unit_of_measurement(self) -> str:
        """Return unif of measurement."""
        return PERCENTAGE
