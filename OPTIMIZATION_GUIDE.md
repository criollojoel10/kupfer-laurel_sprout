# Optimization Guide - Kupfer Port Xiaomi Mi A3

## Quick Commands

### Kernel Build
```bash
# View build progress
tail -5 /tmp/kernel_build*.log

# Check if make is running
ps aux | grep make

# Check kernel output
ls -lh ~/kupfer-work/kernel/arch/arm64/boot/Image.gz
```

### ADB Device
```bash
# Check device connection
adb devices

# Get kernel version from device
adb shell "uname -r"

# Extract config from running kernel
adb shell "su -c 'zcat /proc/config.gz'" > ~/kupfer-work/kernel/.config
```

### Resume Build (after error)
```bash
cd ~/kupfer-work/kernel
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j4 2>&1 | tee /tmp/kernel_buildNEW.log
```

## Common Errors & Solutions

| Error | Fix |
|-------|-----|
| NOHZ_BALANCE_KICK | Enable CONFIG_NO_HZ_COMMON=y in .config |
| FULL_THROTTLE_BOOST | Use device config: `adb shell "su -c 'zcat /proc/config.gz'"` |
| MMC errors | Disable CONFIG_MMC in .config temporarily |
| hostname not found | Install `inetutils` or add to PATH |

## Build Workflow

1. **Start**: `make -j4`
2. **Monitor**: `tail -f /tmp/kernel_build.log`
3. **Fix errors**: Edit .config or source code
4. **Check output**: `ls arch/arm64/boot/Image.gz`
5. **Build DTBs**: `make dtbs`

## Useful Aliases
```bash
alias kbuild='make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j4'
alias klog='tail -20 /tmp/kernel_build*.log'
alias kstatus='ls -lh ~/kupfer-work/kernel/arch/arm64/boot/Image.gz 2>/dev/null || echo "Building..."'
```