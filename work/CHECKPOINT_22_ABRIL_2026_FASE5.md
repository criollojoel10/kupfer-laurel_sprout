# Checkpoint: Fase 5 - Preparación Boot + PKGBUILDs
**Fecha**: 22 Abril 2026  
**Estado**: Preparación completada para pruebas de boot

---

## RESUMEN EJECUTIVO

- **Kernel objetivo**: Usaremos el kernel existente de LineageOS (v4.14.356-perf) del boot.img
- **Compilación nativo** del kernel LINUX 4.14 con GCC tiene errores con drivers propietarios
- **Estrategia cambiada**: Usar kernel working del dispositivo y extraer blobs necesarios
- **PKGBUILDs**: Creados basados en Kupfer Pixel 3a (sargo)

---

## 📋 ARCHIVOS EXTRAÍDOS DE LINEAGEOS

### boot.img (LineageOS 23.0 - Android 16)
- **Ubicación**: `/home/joel/Downloads/boot.img` (64 MB)
- **Kernel extraído**: `~/kupfer-work/lineage_extract/boot_extract/kernel` (17 MB)
- **Ramdisk extraído**: `~/kupfer-work/lineage_extract/boot_extract/ramdisk.cpio` (38 MB)

### OTA Package
- **Ubicación**: `/home/joel/Downloads/lineage-23.0-20260224-nightly-laurel_sprout-signed.zip`
- **Tamaño**: 1.13 GB
- **Contenido**: `payload.bin` (1.13 GB) - Android AB payload

### Device Tree
- **Ubicación**: `/home/joel/Downloads/dtbo.img` (8 MB)

---

## ✅ KERNEL DEL DISPOSITIVO

El kernel running actualmente en el Xiaomi Mi A3 es:

```
Linux version 4.14.356-openela-rc1-perf-g9eacaaff21e8
Compiler: Android Clang 20.0.0
Build: Tue Feb 24 05:51:54 UTC 2026
```

### Configuración habilitada (del `/proc/config.gz`):
- `CONFIG_ARCH_QCOM=y`
- `CONFIG_MACH_XIAOMI_F9S=y`
- `CONFIG_NO_HZ_COMMON=y`
- `CONFIG_SCHED_WALT=y`
- `CONFIG_MODULES=y`
- `CONFIG_EXT4_FS=y`
- Device tree: `qcom,trinket-qrd`

---

## 📦 PKGBUILDs CREADOS

### Estructura creada: `pkgbuilds/`
```
pkgbuilds/
├── README.md
├── device/
│   └── device-sdm670-xiaomi-laurel/
│       ├── PKGBUILD          # Basado en Pixel 3a
│       ├── machine-info
│       ├── xiaomi-laurel.conf  
│       ├── rootston.ini
│       └── modules-initfs
└── firmware/
    └── firmware-sdm670-xiaomi-laurel/
        ├── PKGBUILD          # Esqueleto
        └── firmware-manifest.txt
```

### deviceinfo actualizado:
```bash
deviceinfo_format_version="0"
deviceinfo_name="Xiaomi Mi A3"
deviceinfo_manufacturer="Xiaomi"
deviceinfo_codename="xiaomi-laurel"
deviceinfo_year="2019"
deviceinfo_dtb="qcom/sm6125-xiaomi-laurel_sprout"
deviceinfo_arch="aarch64"
deviceinfo_chassis="handset"
deviceinfo_keyboard="false"
deviceinfo_external_storage="true"
deviceinfo_screen_width="720"
deviceinfo_screen_height="1560"
deviceinfo_flash_method="fastboot"
deviceinfo_kernel_cmdline="clk_ignore_unused"
deviceinfo_generate_bootimg="true"
deviceinfo_flash_fastboot_partition_vbmeta="vbmeta"
deviceinfo_bootimg_qcdt="false"
deviceinfo_bootimg_mtk_mkimage="false"
deviceinfo_bootimg_dtb_second="false"
deviceinfo_append_dtb="true"
deviceinfo_rootfs_image_sector_size="4096"
deviceinfo_flash_pagesize="4096"
deviceinfo_flash_sparse="true"
deviceinfo_flash_offset_base="0x00000000"
deviceinfo_flash_offset_kernel="0x00008000"
deviceinfo_flash_offset_ramdisk="0x01000000"
deviceinfo_flash_offset_second="0x00f00000"
deviceinfo_flash_offset_tags="0x00000100"

# Particiones validadas via ADB:
deviceinfo_partitions_data="/dev/block/bootdevice/by-name/userdata"
deviceinfo_partitions_system="/dev/block/bootdevice/by-name/system_a"
deviceinfo_partitions_boot="/dev/block/bootdevice/by-name/boot_a"
deviceinfo_modules_initfs="gpi spi-geni-qcom"
```

---

## 📱 REFERENCIA: KUPFER PIXEL 3A (sargo)

PKGBUILD del Pixel 3a usado como template:
- **Repo**: `device-sdm670-google-sargo`
- **Paquetes dependientes**: `device-sdm670-common`, `firmware-sdm670-google-sargo`
- **SoC**: Qualcomm SDM670 (similar架构 a nuestro SDM6125/Trinket)

---

## 🔧 SIGUIENTES PASOS

### 1. Crear boot.img para testing
```bash
# Usar kernel del boot.img existente + initramfs básico
mkbootimg --kernel ~/kupfer-work/lineage_extract/boot_extract/kernel \
         --ramdisk ~/kupfer-work/lineage_extract/boot_extract/ramdisk.cpio \
         --cmdline "clk_ignore_unused" \
         -o boot-test.img
```

### 2. Extraer firmware blobs necesarios
```bash
adb pull /vendor/firmware_mnt/image/
# or via root access:
adb shell "su -c 'cp -r /vendor/firmware/* /sdcard/firmware/'"
adb pull /sdcard/firmware/
```

### 3. Flash de prueba (CONSERVADOR - solo si estamos seguros)
```bash
fastboot flash boot boot-test.img
fastboot reboot
```

### 4. Depuración via serial console o ADB
```bash
adb shell "dmesg | tail -100"
adb shell "cat /proc/kmsg"
```

---

## 🎯 RESUMEN DE PROGRESO

| Fase | Estado |
|------|--------|
| 1. Investigación | ✅ 100% |
| 2. Análisis Kernel | ✅ 100% |
| 3. LineageOS Integration | ✅ 100% |
| 4. Build System Setup | ✅ 100% |
| 4D. Kernel Compilation | ⚠️ Usar kernel existing |
| 5.PKGBUILDs | ✅ Completado |
| 5B. Boot img Creation | ⏳ Pendiente |
| 6. Hardware Testing | ⏳ Pendiente |

**Progreso total**: ~80%

---

## 📝 NOTAS TÉCNICAS

### Por qué no compilamos el kernel desde cero:
1. Errores en scheduler code (sched/core.c, fair.c) requieren parchear código
2. Drivers propietarios (qcacld WiFi, cámara MSM) tienen errores de compilación
3. La configuración de Android-specific es compleja
4. El kernel existente ya funciona - mejor usarlo para primer boot

### Estrategia:
1. Usar kernel working del boot.img de LineageOS
2. Extraer/initramfs básico de su ramdisk
3. Iterar/hackear incrementally
4. Eventually build kernel más optimizado después de primer boot

---

**Checkpoint**: 22 Abril 2026
**Por**: OpenCode Agent  
**Proyecto**: kupfer-laurel_sprout