# Xiaomi Mi A3 (laurel_sprout) - Technical Specification for Kupfer Port

## Hardware Specifications

### SoC & Architecture
- **SoC**: Qualcomm Snapdragon 439 (SM6125 variant, codenamed "trinket" internally)
- **CPU**: 8x ARM Cortex-A53 @ up to 2.2GHz
- **GPU**: Adreno 505
- **ISP**: Qualcomm Spectra 180
- **Memory Interface**: LPDDR4X (supports up to 4GB)
- **Storage Interface**: eMMC 5.1 (supports up to 256GB)

### Boot & Memory Layout (from boot.img analysis)
- **Boot Magic**: ANDROID! (standard Android format)
- **Page Size**: 4096 bytes (standard ARM)
- **Kernel Address**: 0x00008000
- **Ramdisk Address**: 0x01000000
- **Tags Address**: 0x00000100
- **Boot Header Version**: 2 (supports vendor bootconfig)

### Kernel Information (Extracted from LineageOS)
**Linux Kernel**: 4.14.356-openela-rc1-perf-g9eacaaff21e8
- **Base**: CAF (Code Aurora Forum) msm-4.14
- **Compiler**: Android Clang 20.0.0 (LTO, PGO, BOLT optimized)
- **Build Date**: Tue Feb 24 05:51:54 UTC 2026
- **Config**: SMP PREEMPT enabled, module support enabled
- **Firmware Location**: `/lib/firmware/4.14.356-openela-rc1-perf-g9eacaaff21e8/`

### Kernel Bootloader Command Line (from boot.img)
```
console=null 
androidboot.hardware=qcom 
androidboot.console=ttyMSM0 
lpm_levels.sleep_disabled=1 
video=vfb:640x400,bpp=32,memsize=3072000 
msm_rtb.filter=0x237 
service_locator.enable=1 
swiotlb=1 
loop.max_part=7 
cgroup.memory=nokmem,nosocket 
buildvariant=user 
androidboot.init_fatal_reboot_target=recovery
```

**Key Parameters for Kupfer**:
- `console=ttyMSM0` - Serial console on UART (MSM proprietary)
- `video=vfb:640x400` - Framebuffer video device (virtual framebuffer)
- `swiotlb=1` - Software IOMMU for DMA
- `loop.max_part=7` - Loop device partition support

## Device Tree Architecture

### DTBO.img Analysis
- **Format**: Device Tree Blob with overlay support
- **Size**: 8 MB (contains full overlay configuration)
- **Main Board**: `qcom,trinket-qrd` (Qualcomm Trinket QRD reference design)
- **Fallback**: `qcom,trinket` (Generic Trinket), `qcom,qrd` (Generic QRD)

### Display Configuration (from DTB)
Multiple display panel support configured:
- `qcom,mdss_dsi_td4330_truly_cmd` - Truly TD4330 Command Mode
- `qcom,mdss_dsi_td4330_truly_video` - Truly TD4330 Video Mode
- `qcom,mdss_dsi_hx83112a_truly_video` - Truely HX83112A Video Mode
- `qcom,mdss_dsi_nt36672_truly_video` - Truly NT36672 Video Mode
- `qcom,mdss_dsi_sim_video` - Simulator panel for testing

All panels use MIPI DSI (Display Serial Interface) connected to MDSS (Mobile Display SubSystem)

### Audio Configuration (from DTB)
- **Codec**: Qualcomm WCD938x (embedded in PMIC)
- **Interface**: I2S/TDM to WCD938x
- **DSP**: QDSP (Qualcomm DSP) for audio processing
- **Microphone**: Multiple mic inputs via PMIC
- **Speaker**: Mono speaker via PMIC

### Sensor Support (from DTB)
- PMI632-TZ: Thermal zone management
- Multiple thermal trips configured for battery protection
- Cooling maps for thermal throttling

## Ramdisk Structure (from extracted ramdisk.cpio.gz)

### Root filesystem structure:
```
/bin → /system/bin (symlink)
/dev/ - Device node definitions
/system/ - Full Android system
/data/ - User data partition
/data_mirror/ - Data mirror for A/B partitions
/apex/ - APEX modules (Android Pony EXpress)
/bootstrap-apex/ - Bootstrap APEX modules
/config/ - Configuration directory
/debug_ramdisk/ - Debug ramdisk
/prop.default - Default properties
```

### Init Scripts Available
- Standard Android init.rc
- device-specific init scripts for SDM439
- SELinux policy enforcement
- Device-specific bootanimation

## Critical Files for Kupfer Port

### Extracted Files
1. **Kernel**: `/work/extracts/boot/kernel` (17.5 MB)
   - Compressed with gzip
   - When decompressed: 43 MB raw kernel binary
   - Contains initramfs with busybox+init

2. **Device Tree**: `/work/extracts/dtbo_extract/dtb_0.dtb` (221 KB)
   - Full device tree with all hardware definitions
   - Overlay support for runtime configuration
   - Panel configurations and thermal zones

3. **Ramdisk**: `/work/extracts/boot/ramdisk/` (extracted structure)
   - Full init system
   - Device configuration
   - SELinux policies

## Required Kernel Drivers for Boot (from cmdline & DTB analysis)

### Essential for initial boot:
1. **TTY/Serial**: ttyMSM0 (MSM UART driver)
2. **Framebuffer**: Virtual framebuffer (vfb) for display
3. **Block**: eMMC/MMC support (mmc_block)
4. **Filesystem**: EXT4 (for rootfs)
5. **IOMMU**: MSM IOMMU + SWIOTLB
6. **Memory**: LPDDR4X controller (msm-core)

### For full functionality:
1. **Display**: MDSS, MIPI DSI, panel drivers
2. **Input**: Touchscreen (I2C), GPIO buttons
3. **Power**: PMIC (PM6125), regulator framework
4. **Thermal**: Thermal zone driver
5. **USB**: XHCI controller (DWC3)
6. **Storage**: eMMC driver, UFS (if supported)

## Partition Layout

### From LineageOS A/B scheme:
- **Bootloader partition**: Primary bootloader (ROM)
- **boot_a / boot_b**: Kernel + ramdisk (A/B slots)
- **dtbo_a / dtbo_b**: Device tree overlay (A/B slots)
- **system_a / system_b**: System partition (A/B slots)
- **vendor_a / vendor_b**: Vendor partition (A/B slots)
- **metadata**: Partition metadata
- **userdata**: User data
- **misc**: Bootloader flags

## Compatibility Notes

### With Google Pixel 3a (sargo) - SDM670
- **Similarities**: 
  - Same ARMv8 64-bit architecture
  - Similar MDSS/DSI display subsystem
  - Similar PMIC architecture (PM6125 in both)
  - Same thermal zone implementation
  
- **Differences**:
  - SDM670 has 2x ARM Cortex-A75 (higher performance)
  - SDM670 has Adreno 615 (vs 505 on SDM439)
  - Slightly different memory controller

### With Snapdragon 660/665
- Close cousin (sm6xxx series)
- Better kernel compatibility than older SDM variants
- Similar DTB structure

## Known Issues from Android to Linux Migration

1. **Verified Boot**: vbmeta.img has dm-verity - needs unsigned mode
2. **SELinux**: Android SELinux policy must be adapted/disabled
3. **PMIC/Regulator**: Complex PMIC initialization sequence
4. **Thermal Zones**: Must be initialized before temperature readings
5. **Display Panels**: May need firmware/config updates
6. **USB**: Needs OTG mode detection

## Next Phase: Kernel Source Analysis

Required repositories to clone:
```bash
# LineageOS kernel (4.14 base)
git clone https://github.com/MasterAwesome/android_kernel_xiaomi_laurel_sprout

# LineageOS device tree
git clone https://github.com/MasterAwesome/android_device_xiaomi_laurel_sprout

# Alternative newer kernels (5.x base)
git clone https://github.com/FlopKernel-Series/flop_trinket-mi_kernel
git clone https://github.com/Evolution-XYZ-Devices/kernel_xiaomi_laurel_sprout

# Vendor blobs
git clone https://github.com/MasterAwesome/android_vendor_xiaomi_laurel_sprout
```

## References for Kupfer Build System Integration

Based on comparison with Google Pixel 3a (sargo):
1. Create `/usr/share/kupfer/devices/xiaomi-laurel_sprout.toml`
2. Define bootloader type: `fastboot`
3. Set kernel flavor: `linux-xiaomi-laurel_sprout` (custom package)
4. Include PMIC initialization firmware in initrd
5. Create display panel database for runtime detection

