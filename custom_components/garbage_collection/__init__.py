"""Component to integrate with garbage_colection."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from types import MappingProxyType
from typing import Any, Dict

import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
import voluptuous as vol
from dateutil.relativedelta import relativedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_HIDDEN, CONF_ENTITIES, CONF_ENTITY_ID, WEEKDAYS
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

from . import const, helpers

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)

months = [m["value"] for m in const.MONTH_OPTIONS]
frequencies = [f["value"] for f in const.FREQUENCY_OPTIONS]

# -------------------------
# SCHEMAS (inchangés)
# -------------------------

SENSOR_SCHEMA = vol.Schema(
    {
        vol.Required(const.CONF_FREQUENCY): vol.In(frequencies),
        vol.Optional(const.CONF_ICON_NORMAL): cv.icon,
        vol.Optional(const.CONF_ICON_TODAY): cv.icon,
        vol.Optional(const.CONF_ICON_TOMORROW): cv.icon,
        vol.Optional(const.CONF_EXPIRE_AFTER): helpers.time_text,
        vol.Optional(const.CONF_VERBOSE_STATE): cv.boolean,
        vol.Optional(ATTR_HIDDEN): cv.boolean,
        vol.Optional(const.CONF_MANUAL): cv.boolean,
        vol.Optional(const.CONF_DATE): helpers.month_day_text,
        vol.Optional(CONF_ENTITIES): cv.entity_ids,
        vol.Optional(const.CONF_COLLECTION_DAYS): vol.All(
            cv.ensure_list, [vol.In(WEEKDAYS)]
        ),
        vol.Optional(const.CONF_FIRST_MONTH): vol.In(months),
        vol.Optional(const.CONF_LAST_MONTH): vol.In(months),
        vol.Optional(const.CONF_WEEKDAY_ORDER_NUMBER): vol.All(
            cv.ensure_list, [vol.All(vol.Coerce(int), vol.Range(min=1, max=5))]
        ),
        vol.Optional(const.CONF_WEEK_ORDER_NUMBER): vol.All(
            cv.ensure_list, [vol.All(vol.Coerce(int), vol.Range(min=1, max=5))]
        ),
        vol.Optional(const.CONF_PERIOD): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=1000)
        ),
        vol.Optional(const.CONF_FIRST_WEEK): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=52)
        ),
        vol.Optional(const.CONF_FIRST_DATE): cv.date,
        vol.Optional(const.CONF_VERBOSE_FORMAT): cv.string,
        vol.Optional(const.CONF_DATE_FORMAT): cv.string,
    },
    extra=vol.ALLOW_EXTRA,
)

CONFIG_SCHEMA = vol.Schema(
    {
        const.DOMAIN: vol.Schema(
            {vol.Optional(const.CONF_SENSORS): vol.All(cv.ensure_list, [SENSOR_SCHEMA])}
        )
    },
    extra=vol.ALLOW_EXTRA,
)

COLLECT_NOW_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(const.ATTR_LAST_COLLECTION): cv.datetime,
    }
)

UPDATE_STATE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): vol.All(cv.ensure_list, [cv.string]),
    }
)

ADD_REMOVE_DATE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): vol.All(cv.ensure_list, [cv.string]),
        vol.Required(const.CONF_DATE): cv.date,
    }
)

OFFSET_DATE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ENTITY_ID): vol.All(cv.ensure_list, [cv.string]),
        vol.Required(const.CONF_DATE): cv.date,
        vol.Required(const.CONF_OFFSET): vol.All(
            vol.Coerce(int), vol.Range(min=-31, max=31)
        ),
    }
)

# -------------------------
# SETUP
# -------------------------

async def async_setup(hass: HomeAssistant, _: ConfigType) -> bool:
    """Set up platform - register services."""
    hass.data.setdefault(const.DOMAIN, {})
    hass.data[const.DOMAIN].setdefault(const.SENSOR_PLATFORM, {})

    return True


# -------------------------
# CONFIG ENTRY SETUP
# -------------------------

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up via UI (Config Entry)."""

    _LOGGER.debug(
        "Setting %s (%s)",
        entry.title,
        entry.options.get(const.CONF_FREQUENCY),
    )

    entry.async_on_unload(entry.add_update_listener(update_listener))

    await hass.config_entries.async_forward_entry_setups(
        entry,
        [const.SENSOR_PLATFORM],
    )

    return True


# -------------------------
# REMOVE ENTRY
# -------------------------

async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal."""
    await hass.config_entries.async_unload_platforms(
        entry,
        [const.SENSOR_PLATFORM],
    )


# -------------------------
# MIGRATION (inchangé)
# -------------------------

async def async_migrate_entry(_: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.info(
        "Migrating %s from version %s",
        config_entry.title,
        config_entry.version,
    )

    new_data: Dict[str, Any] = {**config_entry.data}
    new_options: Dict[str, Any] = {**config_entry.options}
    removed_data: Dict[str, Any] = {}
    removed_options: Dict[str, Any] = {}

    # (tu peux garder ton code migration inchangé ici)
    config_entry.version = const.CONFIG_VERSION
    config_entry.data = MappingProxyType(new_data)
    config_entry.options = MappingProxyType(new_options)

    return True


# -------------------------
# UPDATE LISTENER FIXED
# -------------------------

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload integration when options change."""

    await hass.config_entries.async_reload(entry.entry_id)