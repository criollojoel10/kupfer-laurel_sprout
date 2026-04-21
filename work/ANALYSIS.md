# Xiaomi Mi A3 (laurel_sprout) - Kupfer Port Analysis

## Device Specifications
- **Device**: Xiaomi Mi A3 (laurel_sprout)
- **SoC**: Snapdragon 439 (SDM439, Qualcomm SM6125)
- **Architecture**: ARMv8 (64-bit)
- **Cores**: 8x ARM Cortex-A53 (octa-core)
- **GPU**: Adreno 505
- **RAM**: 4GB LPDDR4X
- **Storage**: 128GB eMMC
- **Current OS**: LineageOS 23.0 (Android 16) Nightly
- **Bootloader**: Fastboot (AOSP-based)

## Files Extracted & Analyzed

### 1. boot.img Analysis
**File**: boot.img (64 MB)
- **Magic**: ANDROID! (valid Android boot image)
- **Header version**: 2 (supports v2 headers with vendor bootconfig)
- **Page size**: 4096 bytes
- **Kernel size**: 17.5 MB (Linux kernel with initramfs)
- **Ramdisk size**: 16.7 MB (compressed with gzip, CPIO format)
- **Kernel address**: 0x00008000
- **Ramdisk address**: 0x01000000
- **Tags address**: 0x00000100
- **OS Version**: 262144.26.2 (decoded as 10.26.2)

### 2. Ramdisk Extraction
**Contents extracted from ramdisk.cpio.gz** (76,731 blocks):
- Full `/bin`, `/system`, `/etc` structure
- Device node definitions in `dev/`
- Init scripts and property configurations
- SELinux policies
- Key insight: This is a full system ramdisk from LineageOS A/B partition scheme

### 3. dtbo.img Analysis
**File**: dtbo.img (8 MB)
- Device tree overlay blob
- Contains hardware-specific device tree overlays
- Used for dynamic hardware configuration

### 4. vbmeta.img Analysis  
**File**: vbmeta.img (4 KB)
- Android Verified Boot metadata
- Contains dm-verity hashes and signatures
- For this project, may need to be flashed in unsigned mode

### 5. LineageOS ROM (OTA)
**File**: lineage-23.0-20260224-nightly-laurel_sprout-signed.zip (1.1 GB)
- **Format**: OTA update package (payload.bin based)
- Contains:
  - `payload.bin` (1.1 GB) - Main system image with A/B partitions
  - `payload_properties.txt` - Update metadata
  - `META-INF/` - Certificate and metadata
- **Status**: Requires OTA payload decoder to extract full ROM

## Architecture Overview

### Bootloader Chain
```
Bootloader → boot.img (kernel + ramdisk) → Android System (LineageOS)
                ↓
           Device Tree Blob (dtbo.img)
                ↓
           Verified Boot (vbmeta.img)
```

### For Kupfer Port - Required Components
1. **Kernel** (already extracted): `/work/extracts/boot/kernel`
   - msm-4.14 kernel base
   - Device tree sources available in LineageOS repos
   
2. **Device Tree** (to extract from repos):
   - arch/arm64/boot/dts/qcom/sm6125.dtsi (base SoC)
   - arch/arm64/boot/dts/qcom/laurel_sprout.dts (device specific)
   - Device tree overlays from dtbo.img

3. **Drivers & Firmware** (from vendor blobs):
   - GPU drivers (Adreno 505)
   - Modem/Radio firmware (if needed for initial boot)
   - Audio HAL
   - Sensors HAL
   - Display drivers

4. **Bootloader Config**:
   - Fastboot compatible
   - Verified boot parameters (can be disabled for testing)

## Key References & Resources

### Device Tree & Kernel Sources
- **LineageOS Device Tree**: https://github.com/MasterAwesome/android_device_xiaomi_laurel_sprout
- **LineageOS Kernel**: https://github.com/MasterAwesome/android_kernel_xiaomi_laurel_sprout
- **Alternative Kernels**:
  - FlopKernel: https://github.com/FlopKernel-Series/flop_trinket-mi_kernel
  - HemantSachdeva: https://github.com/HemantSachdeva/kernel_xiaomi_laurel_sprout
  - Evolution-XYZ: https://github.com/Evolution-XYZ-Devices/kernel_xiaomi_laurel_sprout

### Vendor Blobs
- https://github.com/MasterAwesome/android_vendor_xiaomi_laurel_sprout
- https://github.com/HemantSachdeva/vendor_xiaomi_laurel_sprout

### Device Dumps
- https://github.com/catrielmuller/xiaomi_laurel_sprout_dump

## Kupfer Reference Implementation

### Google Pixel 3a (sargo) - SDM670 - REFERENCE
- **Kupfer device**: google-sargo
- **Architecture**: Similar ARMv8 with SDM670 (close cousin of SDM439)
- **URL**: https://kupfer.gitlab.io/devices/dev/sdm670-google-sargo.html
- **Resources**: https://wiki.postmarketos.org/wiki/Xiaomi_Mi_A3_%28xiaomi-laurel%29

## PostmarketOS Wiki Info (laurel_sprout)
- Existing community documentation for Mi A3
- Contains relevant hardware information
- Notes on bootloader, partitions, and known issues

## Next Steps

### Phase 1: Kernel & Device Tree Setup
1. Clone MasterAwesome kernel + device tree repos
2. Compare with Google Pixel 3a kernel configuration
3. Identify SDM439-specific drivers and configuration
4. Extract bootconfig from boot.img for cmdline params

### Phase 2: Build System Integration with Kupfer
1. Create device definition for Kupfer
2. Adapt build PKGBUILDs for sdm439
3. Configure cross-compilation toolchain

### Phase 3: Initial Boot Testing
1. Create minimal Kupfer rootfs for testing
2. Package kernel with Kupfer ramdisk
3. Flash test image to device
4. Debug bootloader and kernel messages

### Phase 4: Hardware Enablement
1. Port drivers incrementally
2. Enable display (display subsystem)
3. Enable input (touchscreen, buttons)
4. Enable storage (eMMC drivers)
5. Enable networking (USB)

## Commands for Future Reference

```bash
# Extract kernel from boot image
python3 work/extract_boot_img.py boot.img work/extracts/boot

# Extract OTA payload (needs brotli-tools)
/path/to/update_payload_extractor.py payload.bin

# Clone kernel sources
git clone https://github.com/MasterAwesome/android_kernel_xiaomi_laurel_sprout
git clone https://github.com/MasterAwesome/android_device_xiaomi_laurel_sprout

# Compile kernel for ARM64
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- laurel_sprout_defconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)

# Flash via fastboot (when ready)
adb reboot bootloader
fastboot flash boot custom_boot.img
fastboot flash dtbo custom_dtbo.img
fastboot flash vbmeta --disable-verification vbmeta.img
fastboot reboot
```

## Risk Mitigation
- **Bootloader unlock**: Verify device supports OEM unlock before proceeding
- **Data backup**: All data should be backed up from Termux/LineageOS before testing
- **Serial console**: Optional but highly recommended for kernel debugging
- **Test builds**: Use incremental testing with custom boot images only initially

