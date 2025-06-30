# CCOS Issue Repo

## General Troubleshooting Steps

Hardware can be weird sometimes. Before reporting an issue, make sure you

1. Unplug your device
2. Wait at least 30 seconds while leaving your device unplugged to make sure nothing gets left in RAM
3. Plug your device back in

## Getting Updates

The latest firmware for each device is now available on https://charachorder.io/ccos/

_Note: pre-2.1.0 changelogs are incomplete and located at [CHANGELOG.md](./CHANGELOG.md) instead of directly on the update page._

- M4G aka [Master Forge](https://docs.charachorder.com/Master%20Forge.html#updating-the-firmware)
- CC2 aka [CharaChorder Two](https://docs.charachorder.com/CharaChorder%20Two.html#updating-the-firmware)
- CC1 aka [CharaChorder One](https://docs.charachorder.com/CharaChorder%20One.html#updating-the-firmware)
- CCL aka [CharaChorder Lite](https://docs.charachorder.com/CharaChorder_Lite.html#updating-the-firmware)
  - _Note: due to a chip shortage at the time CCL has both M0 and S2 variants._
- CCX aka [CharaChorder X](https://docs.charachorder.com/CharaChorder%20X.html#updating-the-firmware)

## Developer Notes

Devices are split into the following categories by hardware

- M0 (SAMD21)
  - `cc1_m0` (CharaChorder One)
  - `ccl_m0` (CharaChorder Lite pre-shortage)
- S2 (ESP32S2)
  - `ccl_s2` (CharaChorder Lite post-shortage)
  - `ccx_s2` (CharaChorder X)
  - `engine_s2` (CharaChorder Engine)
- S3 (ESP32S3)
  - `cc2_s3` (CharaChorder Two)
  - `m4g_s3` (Master Forge Left Half)
  - `m4gr_s3` (Master Forge Right Half)
  - `t4g_s3` (Forge Trackball)

M0 Limitations:

- A maximum of 16k chords due to RAM limitations
- No support for one-click updates (UF2 only)
- Updates reset layout & settings

### Serial API

Serial API docs can be found at https://docs.charachorder.com/SerialAPI.html.

A reference implementation in TypeScript for the web is also available as part of https://charachorder.io/ on
https://github.com/CharaChorder/DeviceManager/blob/master/src/lib/serial/device.ts.

### Firmware Meta API

Firmware Meta API is an important part for developing tooling that interacts with CCOS and used by https://charachorder.io/.

It allows you to get the following data in JSON format:

- [`https://charachorder.io/firmware/`](https://charachorder.io/firmware/) Available CCOS devices
- [`https://charachorder.io/firmware/{device}/`](https://charachorder.io/firmware/m4g_s3/) Publicly Available Builds
- [`https://charachorder.io/firmware/{device}/{version}/meta.json`](https://charachorder.io/firmware/m4g_s3/2.1.0/meta.json) Firmware Specific Meta, such as
  - Version Name and commit date
  - List of firmware files
  - Factory Settings, Chords and Layout
  - Changelog
  - Detailed list of all action codes
  - Detailed list of all settings

Some of this metadata may not be available for older versions and refer to the [device manager implementation](https://github.com/CharaChorder/DeviceManager/tree/master/src/lib/meta).

### Communal Source Program

Right now we provide access to the CCOS source code repository to select applicants.
