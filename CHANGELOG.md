# Change Log

## Main Releases

### Version 1.1.1 Main (2023-06-13)

#### Fixes
- On the Lite, setting LED related variables through the Serial API correctly updates the variable values.

#### Changes
- On the Lite, disables arpeggiates by default.
- Removes single quote as a separator.
- Adds left and right parentheses as separators; note, these must be activated directly, not with a shift key.
- On the Lite, adds an on/off variable for the LEDs that is separate from brightness.
- On the Lite, adds a submenu in the GTM for the LEDs.


### Version 1.1.0 Main (2023-05-31)

#### Features
- Adds the chording and spurring timeouts to the GTM.
- Adds custom integer types to optimize memory usage tailored to each device hardware's need in order to maximize available ram and chordmap lookups.
- Adds check on chord outputs. If the action code value is above 126, then no space character is added.
- Adds initial migration of the CC Engine into CCOS.

#### Fixes
- Fixes detection of perfectly pressed chords.
- Fixes incorrect behavior of the chord backspacing timeouts.
- Fixes extraneous outputs in the response of successful Serial API CML C4 commands.
- Fixes missing space in the response of successful Serial API CML C2 commands.
- Fixes return of the correct number of hexadecimal action codes in the response of Serial API CML C2 commands when there are multi-byte action codes in the chord output.
- Fixes the startup output of CharaChorder is Ready to not use the delete key, which caused multiple issues including entering the BIOS on some computers during startup.
- Fixes extraneous logging commands that interfered with the SerialAPI and were not flagged as logging outputs.
- Fixes an issue with lingering old chordmaps that caused the device to think that the chord output was extremely long, which could not fit into memory and would lock up the device. These are flagged and the chord output lengths set to zero.
- Fixed the resources in the GTM to only output hyperlinks through keyboard output for non Windows OSes where Ctrl+R does not have a meaning.
- Fixes spacing issue with functional keymaps with number positions and backspace or delete.

#### Changes
- Changes the startup chords to remove 'sa' for 'saw' which was overwriting 'as' for 'as'.
- Changes the hard coded DUP+g chordmap in the CharaChorder One. This still remains in the CharaChorder Lite.
- Changes HID keyboard reports to be non-blocking in a buffer so that if a relatively high keystroke delay is used (ie above 1000us), the keystroke delay will not block incoming key press and release actions that could affect chord detection. A high keystroke delay may be necessary for a host OS that has a low power mode enabled.
- Changes the GTM to output correctly with the non-blocking keystroke delay buffer.
- Changes the learning resources in the GTM from launchpad to iq-eq.io.
- Changes the default arpeggiate timeout from 800ms to 600ms.
- Changes the default debounce on the CharaChorder Lite from 20ms to 12ms.


### Version 1.0.1 Main (2023-03-09)

#### Features
- Adds mouse backward button (560) and forward button (561) capabilities.

#### Fixes
- Fixes issue on M0 devices for mouse right click where it would only do a left click.


### Version 1.0.0 Main (2023-03-08)

### Features
- Adds left shift and right shift as a chord for capslock toggle, available through the RST FUNC command through the Serial API.

### Fixes
- Fixes issue for reporting version number and type with the Serial API VERSION command
- Fixes RST FUNC commands for the CC1 where numbers are used for backspace, delete, and left and rigth arrow keys to use the default primary layout's characters instead of numbers which are on the num-shift layer

### Changes
- Sets the default for enable compound chording to false while this feature is developed in beta releases


## Beta Releases

### 1.0.5 Beta (2023-05-05)

#### Fixes
- Fixes detection of perfectly pressed chords.


### 1.0.4 Beta (2023-04-27)

#### Features
- Adds initial migration of the CC Engine into CCOS

#### Fixes
- Fixes incorrect behavior of the chord backspacing timeouts.
- Fixes extraneous outputs in the response of successful Serial API CML C4 commands.
- Fixes missing space in the response of successful Serial API CML C2 commands.
- Fixes return of the correct number of hexadecimal action codes in the response of Serial API CML C2 commands when there are multi-byte action codes in the chord output.

#### Changes
- Changes the startup chords to remove 'sa' for 'saw' which was overwriting 'as' for 'as'.


### 1.0.3 Beta (2023-04-20)

#### Features
- Adds the chording and spurring timeouts to the GTM.
- Adds custom integer types to optimize memory usage tailored to each device hardware's need in order to maximize available ram and chordmap lookups.

#### Fixes
- Fixes the startup output of CharaChorder is Ready to not use the delete key, which caused multiple issues including entering the BIOS on some computers during startup.
- Fixes extraneous logging commands that interfered with the SerialAPI and were not flagged as logging outputs.
- Fixes an issue with lingering old chordmaps that caused the device to think that the chord output was extremely long, which could not fit into memory and would lock up the device. These are flagged and the chord output lengths set to zero.
- Fixed the resources in the GTM to only output hyperlinks through keyboard output for non Windows OSes where Ctrl+R does not have a meaning.

#### Changes
- Changes the hard coded DUP+g chordmap in the CharaChorder One. This still remains in the CharaChorder Lite.
- Changes HID keyboard reports to be non-blocking in a buffer so that if a relatively high keystroke delay is used (ie above 1000us), the keystroke delay will not block incoming key press and release actions that could affect chord detection. A high keystroke delay may be necessary for a host OS that has a low power mode enabled.
- Changes the GTM to output correctly with the non-blocking keystroke delay buffer.
- Changes the learning resources in the GTM from launchpad to iq-eq.io.
- Changes the default arpeggiate timeout from 800ms to 600ms.
- Changes the default debounce on the CharaChorder Lite from 20ms to 12ms.



### 1.0.2 Beta (2023-03-09)

#### Features
- Adds check on chord outputs. If the action code value is above 126, then no space character is added.

#### Fixes
- Fixes spacing issue with functional keymaps with number positions and backspace or delete.



### 0.9.17 Beta (2023-03-04)

#### Features
- Adds horizontal mouse scroll capabilities to the CC1 M0 and the CC Lite M0.
- Adds Serial API command, RST FUNC, which writes backspace, delete, and left and right arrow key repeat chordmaps.

#### Fixes
- Fixes incorrect backspacing of incorrect chorded input, especially when the number of incorrect input keys is more than 12.
- Fixes the issue where left shift remains pressed when returning to the primary keymap while a shifted character had yet to be released.
- Fixes the default on position 1 of the secondary keymap (num-shift) for the CC One to the forward slash key. Previously the default was incorrectly set to backslash.
- Fixes the default mouse scroll keys on the secondary keymap (num-shift) for the CC One. Previously the default was incorrectly set only to arrow move, like in the primary keymap. Mouse scroll remains available through 3D press combined with mouse move keys.
- Fixes the default secondary keymap for the CC Lite. Previous versions had some incorrect offsets based on older keymapings.

#### Changes
- Sets the default mouse scrolling speed to 2, since with a default of 1, the half speed integer divides to 0.
- Sets mouse scroll polling rate to 1/4th that of mouse move update polling rate to allow for more control over the large scroll detent implemented on the host OS.



### 0.9.16 Beta (2023-03-02)

#### Features
- Adds 12 Key Rollover
- Adds chord breakers with any CTRL or ALT key.
- Adds synchronization of capslock with the host OS on the CC Lite S2.
- Adds double brightness LED lighting of the capslock key using the capslock state on the CC Lite S2.

#### Fixes
- Fixes incorrect character count when exiting the impulse chording interface.
- Fixes incorrect backspacing on chords with more than 6 key inputs.
- Fixes unexpected behavior when using media key actions. However, the host OS still may not process the media keys in this format.

#### Changes
- Increases the logical maximum of the keyboard usage table from 115 to 255 for devices with the M0 chipset.


### 0.9.15 Beta (2023-02-14)

#### Features
- Adds exclamation arpeggiate.
- Adds human readable Impulse chord inputs.

#### Fixes
- Fixes spacing issues on exiting Impulse chording.
- Fixes unintended enter key press on Impulse chord confirmation.
- Fixes pulling in chords with modifiers into the Impulse chording interface.
- Fixes backspacing on chords with more than 6 key inputs (due to HID report limitations).
- Fixes arpeggiate tense mappings on the CC Lite.
- Fixes spacing on arpeggiate tense modifiers in the CC Lite that use either spacebar.

#### Changes
- Increases the maximum microsecond delay from 2560us to 10240us with 40us increments.
- Increases default microsecond delay increased from 250us to 480us.
- Reduces default LED brightness on the CC Lite from 16 to 5 keep it under 100mA for mobile device use.