# Xiaomi Mi A3 (laurel_sprout) - Technical Specification for Kupfer

## Hardware

- SoC: Qualcomm `SM6125 / Trinket`
- CPU: 8x Cortex-A53
- GPU: Adreno 505
- RAM: LPDDR4X
- Storage: eMMC 5.1

## Boot baseline

- Kernel: `4.14.356-openela-rc1-perf`
- DTB board match: `qcom,trinket-qrd`
- Bootloader: fastboot / A/B

## Kupfer direction

- `device` package: derived from postmarketOS `device-xiaomi-laurel`
- `firmware` package: blobs mínimos para hardware básico
- `boot` package or image: built from the verified LineageOS baseline first

## Next phase

Convert the postmarketOS device metadata into Kupfer package metadata and validate a first boot image.
