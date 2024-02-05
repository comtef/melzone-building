# Melzone Building for Home Assistant

[![HACS Badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License](https://img.shields.io/github/license/comtef/melzone-building?style=for-the-badge)](https://github.com/comtef/melzone-building/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/comtef/melzone-building?style=for-the-badge)](https://github.com/comtef/melzone-building/releases)
[![Size](https://img.badgesize.io/https:/github.com/comtef/melzone-building/releases/latest/download/melzone-building?style=for-the-badge)](https://github.com/comtef/melzone-building/releases)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=comtef&repository=melzone-building&category=integration)
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=melzone_building)

The `melzone_building` integration integrates Mitsubishi Electric's Melzone Building devices into Home Assistant. It leverages the Colibri virtual remote control API.

<img alt="Colibri virtual remote control" src="assets/colibri.png" width="400px">

## Features

- Integrates Colibri virtual remote control API
  - Auto discovery of enabled features not supported
- Provides `climate` and `sensor` platforms.

### Climate

The following parameters can be controlled for the `climate` platform entities:

- Power (using HVAC mode)
- Target temperature
- Operation mode (HVAC mode)

### Sensor

The following attributes are available for `sensor` platform entities:

- Room temperature
- Target temperature


## Configuration

After installing Auto Backup via [HACS](https://hacs.xyz/), it can then be setup via the UI, by going to **Configuration** → **Devices & Services** → **Add Integration** → **Melzone Building** or by clicking the button below.

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=melzone_building)
