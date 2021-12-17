"""The Keys integration."""
from __future__ import annotations

from the_keyspy import TheKeyApi

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS = ["lock"]


class TheKeysSystem:
    """TheKeys System class."""

    def __init__(self, thekeys):
        """Init the system class."""
        self.thekeys = thekeys


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up The Keys from a config entry."""
    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    thekeys = await hass.async_add_executor_job(
        TheKeyApi, entry.data.get(CONF_USERNAME), entry.data.get(CONF_PASSWORD)
    )

    hass.data[DOMAIN] = TheKeysSystem(thekeys)
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.pop(DOMAIN)

    return unload_ok


class TheKeysEntity(Entity):
    """Base Hassio the_keys entity class."""

    def __init__(self, data):
        """Init a TheKeys entity."""
        self._data = data
        self._available = True

    @property
    def available(self):
        """Return the available state."""
        return self._available


class TheKeysDevice(TheKeysEntity):
    """Base Hassio the_keys device class."""

    def __init__(self, data, device):
        """Init a TheKeys device."""
        super().__init__(data)
        self.thekeys_device = device

    @property
    def name(self):
        """Return the name of the device."""
        return self.thekeys_device.name

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self.thekeys_device.identifier

    @property
    def device_info(self):
        """Return the device_info of the device."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "manufacturer": "The Keys",
            "name": self.name,
            "device_type": "Lock",
        }
