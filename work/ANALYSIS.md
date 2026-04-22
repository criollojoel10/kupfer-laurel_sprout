# Xiaomi Mi A3 (laurel_sprout) - Kupfer Port Analysis

## Current conclusion

The device is `SM6125 / Trinket`, not SDM439 or SDM670. The right strategy is to use postmarketOS as the packaging reference and LineageOS as the boot baseline.

## What matters now

- `deviceinfo` shape from postmarketOS
- `modules-initfs` and machine info mapping
- firmware/blob packaging
- `boot.img` creation and validation

## Next step

Translate the postmarketOS device metadata into Kupfer PKGBUILDs and prepare the first test boot.
