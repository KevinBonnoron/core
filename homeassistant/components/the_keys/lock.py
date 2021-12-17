"""The Keys Lock device."""
from homeassistant.components.lock import LockEntity

from . import TheKeysDevice
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up TheKeys lock devices."""
    data = hass.data[DOMAIN]

    entities = []

    for device in await hass.async_add_executor_job(data.thekeys.get_devices):
        entities.append(TheKeysLock(data, device))

    async_add_entities(entities)


class TheKeysLock(TheKeysDevice, LockEntity):
    """TheKeys lock device implementation."""

    def lock(self, **kwargs):
        """Lock the device."""
        self.thekeys_device.lock()

    def unlock(self, **kwargs):
        """Unlock the device."""
        self.thekeys_device.unlock()

    def update(self) -> None:
        """Update the device."""
        self.thekeys_device.update()

    @property
    def is_locked(self):
        """Return true if device is on."""
        return self.thekeys_device.is_locked
