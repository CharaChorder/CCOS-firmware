# [Changelog](CHANGELOG.md)

Read about the latest changes [here](CHANGELOG.md).

# Firmware downloads

| Device | Latest Main Release | Latest Beta Release|
| ----------- | ----------- | ----------- |
| CharaChorder One | [v1.1.3](CharaChorder_One/M0/Main/CCOS_One_M0_v1.1.3) | (none) |
| CharaChorder Lite M0 | [v1.1.3](CharaChorder_Lite/M0/Main/CCOS_Lite_M0_v1.1.3) | (none) |
| CharaChorder Lite S2 | [v1.1.3](CharaChorder_Lite/S2/Main/CCOS_Lite_S2_v1.1.3) | (none) |
| CharaChorder X S2 | [v1.1.3](CharaChorder_X/S2/Main/CCOS_X_S2_v1.1.3) | (none) |
| CharaChorder Engine S2 | [v1.1.3](CharaChorder_Engine/S2/Main/CCOS_Engine_S2_v1.1.3) | (none) |

=======

# Update instructions

> *Note*: If your device shipped before 2023 and has not been migrated to CCOS, you must do that [here](https://www.charachorder.com/pages/migrating-to-ccos) before following these steps.

1. Using Google Chrome, or a Chromium based browser, go to your device manager: https://www.iq-eq.io/#/manager
2. Click “Connect”.
3. Select your device, then click the blue "Connect" button in the pop-up
4. Click “Bootloader”. Your CharaChorder will appear as an external storage device (for example, “Drive F:” on Windows or “Arduino” on Mac)
5. Download your update file from this repository.

> *Note:* If you have a CharaChorder Lite that was delivered before October 1st, 2022 you will need to use the file which corresponds to the MO chipset. Otherwise CharaChorder Lite users should use the S2 chipset.
6. Drag and drop the new `CURRENT.UF2` update file to your CharaChorder (Drive F:, etc) and overwrite the existing file. While your device reboots, place your cursor into a text editor and wait to see 'CCOS is ready' 
> *Note:* the file MUST be named `CURRENT.UF2`. For example, `CURRENT.UF2(1)` will NOT work
