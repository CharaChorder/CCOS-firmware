# CCOS Issue Repo

## Getting Updates

The latest firmware for each device is now available on https://charachorder.io/ccos/

_Note: pre-2.1.0 changelogs are incomplete and located at [CHANGELOG.md](./CHANGELOG.md) instead of directly on the update page._

- [CharaChorder One](https://docs.charachorder.com/CharaChorder%20One.html#updating-the-firmware)
- [CharaChorder Two](https://docs.charachorder.com/CharaChorder%20One.html#updating-the-firmware)
- [CharaChorder Lite](https://docs.charachorder.com/CharaChorder_Lite.html#updating-the-firmware)
- [CharaChorder X](https://docs.charachorder.com/CharaChorder%20X.html#updating-the-firmware)

## Developer Notes

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

