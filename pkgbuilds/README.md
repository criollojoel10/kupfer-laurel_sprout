# Kupfer PKGBUILDs for Xiaomi Mi A3

This directory tracks packaging work for the next project phases.

## Current packages

- `device/device-sdm670-xiaomi-laurel`
  - Device package template adapted from Kupfer SDM670 style.
  - Includes `deviceinfo` merge with validated partition mapping via ADB.

- `firmware/firmware-sdm670-xiaomi-laurel`
  - Placeholder package scaffold.
  - Waiting for legal firmware blob extraction and install rules.

## Notes

- The kernel build phase (4D) is still blocked by scheduler config inconsistencies in the current source tree and minimal `.config`.
- Partition mapping was validated on connected device `fc178bb9491e` using `/dev/block/bootdevice/by-name`.
