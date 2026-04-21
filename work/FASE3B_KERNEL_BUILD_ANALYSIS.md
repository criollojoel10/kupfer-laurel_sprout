# FASE 3B: Análisis Kernel Source Tree y Configuración

**Timestamp**: 21 de Abril de 2026, 15:00 UTC  
**Status**: En construcción (esperando clone del kernel)  
**Objetivo**: Analizar estructura de compilación del kernel 4.14 para Kupfer

---

## Estructura esperada en android_kernel_xiaomi_laurel_sprout

### Directorios principales

```
kernel/
├── arch/
│   ├── arm64/
│   │   ├── boot/
│   │   │   ├── dts/qcom/         ← Device trees (DTB, DTS)
│   │   │   │   ├── trinket.dts   ← Board base (laurel_sprout)
│   │   │   │   ├── trinket.dtsi  ← SoC base (SDM439)
│   │   │   │   ├── trinket-sde.dtsi   ← Display config
│   │   │   │   ├── trinket-wcd.dtsi   ← Audio config
│   │   │   │   ├── trinket-thermal.dtsi ← Thermal config
│   │   │   │   └── trinket-usb.dtsi    ← USB config
│   │   │   └── Makefile           ← DTS compilation rules
│   │   ├── configs/
│   │   │   ├── vendor/laurel_sprout-perf_defconfig  ← MAIN CONFIG
│   │   │   └── vendor/laurel_sprout-debug_defconfig ← Alternativo
│   │   ├── Makefile               ← ARM64 architecture build
│   │   └── Kconfig               ← Kernel configuration options
│   ├── arm/                       ← 32-bit ARM support (menor)
│   └── x86/                       ← Descartado para Mi A3
│
├── drivers/
│   ├── clk/qcom/
│   │   ├── gcc-trinket.c          ← Global Clock Controller
│   │   ├── cpucc-trinket.c        ← CPU Clock Controller
│   │   ├── dispcc-qcom.c          ← Display Clock Controller
│   │   ├── gpucc-qcom.c           ← GPU Clock Controller
│   │   └── videocc-qcom.c         ← Video Clock Controller
│   │
│   ├── gpu/drm/msm/
│   │   ├── mdss.c                 ← Mobile Display SubSystem
│   │   ├── dsi/                   ← DSI interface
│   │   │   ├── dsi.c
│   │   │   ├── dsi_host.c
│   │   │   └── truly_td4330.c    ← Panel driver (TD4330)
│   │   └── Makefile
│   │
│   ├── mmc/host/
│   │   ├── sdhci-msm.c            ← eMMC/SD controller
│   │   └── Makefile
│   │
│   ├── usb/
│   │   ├── dwc3/
│   │   │   ├── core.c
│   │   │   ├── gadget.c
│   │   │   └── dwc3-qcom.c       ← Qualcomm glue
│   │   └── Makefile
│   │
│   ├── regulator/
│   │   ├── qcom-spmi-regulator.c  ← PMIC regulators (PM6125)
│   │   └── Makefile
│   │
│   ├── soc/qcom/
│   │   ├── rpm-smd.c              ← Resource Power Manager
│   │   ├── smem.c                 ← Shared memory IPC
│   │   └── Makefile
│   │
│   ├── thermal/
│   │   ├── qcom/
│   │   │   ├── tsens*.c           ← Thermal sensors
│   │   │   └── Makefile
│   │   └── thermal_core.c
│   │
│   ├── input/
│   │   └── keyboard/
│   │       └── gpio_keys.c        ← Power/Volume buttons
│   │
│   └── ... (otros drivers)
│
├── sound/
│   ├── soc/qcom/
│   │   ├── qdsp6/
│   │   │   ├── q6adm.c            ← Audio DSP manager
│   │   │   └── Makefile
│   │   └── Makefile
│   │
│   └── soc/codecs/
│       ├── wcd938x.c              ← WCD938x codec
│       └── Makefile
│
├── Makefile                        ← TOP-LEVEL build rules
├── Kconfig                        ← Top-level kernel config
└── scripts/
    ├── kconfig/                   ← Menuconfig scripts
    ├── dtc/                       ← Device tree compiler
    └── mkbootimg.py              ← Boot image creation
```

---

## Archivo de Configuración Principal

### Ruta: `arch/arm64/configs/vendor/laurel_sprout-perf_defconfig`

Este archivo contiene las opciones de kernel compiladas para Mi A3.
Esperado: ~5900 líneas de configuración

### Opciones críticas esperadas:

```
# Boot & Core
CONFIG_ARM64=y
CONFIG_ARM64_VA_BITS=39
CONFIG_ARM64_MODULE_CODESIZE_PLTS=y
CONFIG_SMP=y
CONFIG_NR_CPUS=8
CONFIG_PREEMPT=y

# Clock & Power Management
CONFIG_COMMON_CLK=y
CONFIG_COMMON_CLK_QCOM=y
CONFIG_QCOM_RPM_SMD=y
CONFIG_QCOM_PM=y
CONFIG_QCOM_SMEM=y

# PMIC & Regulators
CONFIG_REGULATOR=y
CONFIG_REGULATOR_QCOM_SPMI=y
CONFIG_REGULATOR_QCOM_RPM=y
CONFIG_MFD_SPMI_PMIC=y
CONFIG_POWER_RESET_QCOM=y

# Memory
CONFIG_SWIOTLB=y
CONFIG_IOMMU_SUPPORT=y
CONFIG_IOMMU_IOVA=y
CONFIG_CMA=y
CONFIG_CMA_SIZE_MBYTES=256

# MMC/Storage
CONFIG_MMC=y
CONFIG_MMC_BLOCK=y
CONFIG_MMC_SDHCI=y
CONFIG_MMC_SDHCI_MSM=y
CONFIG_SCSI=y
CONFIG_BLK_DEV_SD=y

# USB
CONFIG_USB=y
CONFIG_USB_GADGET=y
CONFIG_USB_GADGET_SERIAL=y
CONFIG_USB_DWC3=y
CONFIG_USB_DWC3_QCOM=y
CONFIG_USB_PHY=y
CONFIG_QCOM_USB_PHY=y

# Display/DRM
CONFIG_DRM=y
CONFIG_DRM_KMS_HELPER=y
CONFIG_DRM_MSM=y
CONFIG_DRM_QCOM_DSI=y
CONFIG_BACKLIGHT_CLASS_DEVICE=y
CONFIG_BACKLIGHT_PWM=y

# Input
CONFIG_INPUT=y
CONFIG_INPUT_KEYBOARD=y
CONFIG_KEYBOARD_GPIO=y
CONFIG_TOUCHSCREEN=y

# Serial/UART
CONFIG_SERIAL_CORE=y
CONFIG_SERIAL_QCOM=y
CONFIG_SERIAL_QCOM_GENI=y
CONFIG_SERIAL_EARLYCON=y

# Timer/RTC
CONFIG_RTC_CLASS=y
CONFIG_RTC_DRV_QCOM_POWEROFF=y

# Thermal
CONFIG_THERMAL=y
CONFIG_THERMAL_QCOM=y
CONFIG_QCOM_TSENS=y

# Audio (opcional para Fase 1)
CONFIG_SOUND=y
CONFIG_SND=y
CONFIG_SND_SOC=y
CONFIG_SND_SOC_QCOM_QDSP6=y
CONFIG_PINCTRL=y
CONFIG_PINCTRL_QCOM=y

# Crypto (seguridad)
CONFIG_CRYPTO=y
CONFIG_CRYPTO_QCOM=y
```

---

## Proceso de Compilación Kernel

### 1. Limpieza Previa
```bash
make ARCH=arm64 mrproper      # Limpiar completamente
make ARCH=arm64 distclean     # Distribución limpia
```

### 2. Configuración
```bash
# Opción A: Usar defconfig existing
make ARCH=arm64 \
  CROSS_COMPILE=aarch64-linux-gnu- \
  vendor/laurel_sprout-perf_defconfig

# Opción B: Generar menuconfig (interactive)
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- menuconfig
```

### 3. Compilación de Device Tree
```bash
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- dtbs

# Output: arch/arm64/boot/dts/qcom/trinket.dtb
```

### 4. Compilación Kernel
```bash
make ARCH=arm64 \
  CROSS_COMPILE=aarch64-linux-gnu- \
  CROSS_COMPILE_COMPAT=arm-linux-gnueabihf- \
  -j$(nproc) \
  Image.gz-dtb    # Kernel + DTB incluido

# Output: arch/arm64/boot/Image.gz-dtb
```

### 5. Compilación Módulos (si CONFIG_MODULES=y)
```bash
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- modules

# Output: *.ko files
```

### 6. Boot Image Creation
```bash
mkbootimg \
  --kernel arch/arm64/boot/Image.gz-dtb \
  --ramdisk ramdisk.img \
  --header_version 1 \
  --base 0x00000000 \
  --pagesize 4096 \
  --kernel_offset 0x00008000 \
  --ramdisk_offset 0x01000000 \
  --tags_offset 0x00000100 \
  --cmdline "console=ttyMSM0,115200n8 ..." \
  -o boot.img
```

---

## Cambios Necesarios para Kupfer

### 1. Remover Dependencias Android
```bash
# Remover en defconfig:
CONFIG_ANDROID=n
CONFIG_ANDROID_LOGGER=n
CONFIG_ANDROID_BINDER=n
CONFIG_ANDROID_PARANOID_NETWORK=n

# Agregar para Kupfer:
CONFIG_UNIX98_PTYS=y         # PTY support para terminal
CONFIG_DEVPTS_MULTIPLE_INSTANCES=y
CONFIG_VT=y                  # Virtual terminals
CONFIG_VT_CONSOLE=y
```

### 2. Agregar Soporte Arch Linux ARM
```bash
# Filesystem
CONFIG_EXT4_FS=y
CONFIG_EXT4_FS_POSIX_ACL=y
CONFIG_TMPFS=y
CONFIG_TMPFS_POSIX_ACL=y

# General
CONFIG_PRINTK=y              # Mensajes de kernel
CONFIG_PRINTK_TIME=y
CONFIG_MAGIC_SYSRQ=y         # Debug via sysrq

# Networking (básico)
CONFIG_NET=y
CONFIG_INET=y
CONFIG_IPV6=y
CONFIG_NETFILTER=y

# Security
CONFIG_CAPABILITY=y
CONFIG_UID16=n
```

### 3. Remover Blobs Propietarios
```bash
# Remover en defconfig:
CONFIG_QCOM_FIRMWARE_LOADER=n
CONFIG_QCOM_SUBSYSTEM_RESTART=n  # Modem firmware

# Mantener:
CONFIG_QCOM_SCM=y            # Security subsystem
CONFIG_QCOM_SCM_DOWNLOAD_MODE_DEFAULT=n  # No auto-download
```

---

## Variables de Compilación Importantes

### CROSS_COMPILE
```bash
CROSS_COMPILE=aarch64-linux-gnu-      # GCC standard
CROSS_COMPILE=aarch64-linux-musl-     # musl (más pequeño)
```

### CROSS_COMPILE_COMPAT (para binarios 32-bit)
```bash
CROSS_COMPILE_COMPAT=arm-linux-gnueabihf-
```

### O (Output Directory)
```bash
O=../build/                           # Compilar en directorio separado
```

### CC (Compiler)
```bash
CC=aarch64-linux-gnu-gcc              # GCC (estándar)
CC=clang-15                           # Clang (si disponible)
```

---

## Herramientas Necesarias

### Instaladas en Arch Linux
```bash
base-devel             # gcc, make, binutils
arm-linux-gnueabihf-gcc  # 32-bit ARM compiler
aarch64-linux-gnu-gcc  # 64-bit ARM compiler
clang                  # LLVM compiler (opcional)
lld                    # LLVM linker (opcional)
dtc                    # Device tree compiler
```

### Verificación
```bash
aarch64-linux-gnu-gcc --version
aarch64-linux-gnu-gcc --print-sysroot
aarch64-linux-gnu-ld --version
aarch64-linux-gnu-objcopy --version
dtc --version
```

---

## Timeline Estimado

| Tarea | Tiempo | Notas |
|---|---|---|
| Limpiar + config | 5 min | mrproper + defconfig |
| Compilar DTB | 10 min | Solo device trees |
| Compilar kernel | 30-60 min | Depende CPU (4-8 cores) |
| Compilar módulos | 15 min | Si CONFIG_MODULES=y |
| Crear boot.img | 5 min | mkbootimg |
| **Total** | **65-90 min** | Con compilación paralela |

---

## Proceso para Kupfer

### Paso 1: Checkout rama compatible
```bash
cd kernel
git log --oneline | head -10      # Ver commits recientes
git checkout <commit-hash>        # Si es necesario

# O usar rama específica:
git branch -a | grep lineage      # Ver ramas disponibles
git checkout lineage-20.0          # Si existe
```

### Paso 2: Preparar para compilación
```bash
# Copiar defconfig
cp arch/arm64/configs/vendor/laurel_sprout-perf_defconfig .config

# O generar from scratch
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- defconfig
```

### Paso 3: Modificar config para Kupfer
```bash
# Opción A: Editar .config directamente
nano .config

# Opción B: Usar menuconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- menuconfig
```

### Paso 4: Compilar
```bash
make ARCH=arm64 \
  CROSS_COMPILE=aarch64-linux-gnu- \
  CROSS_COMPILE_COMPAT=arm-linux-gnueabihf- \
  -j4 \
  Image.gz-dtb modules

make modules_install INSTALL_MOD_PATH=/mnt/kupfer/
```

### Paso 5: Crear boot.img
```bash
# Obtener ramdisk de Kupfer
mkbootimg \
  --kernel arch/arm64/boot/Image.gz-dtb \
  --ramdisk ramdisk.cpio.gz \
  --header_version 1 \
  --base 0x00000000 \
  --pagesize 4096 \
  --kernel_offset 0x00008000 \
  --ramdisk_offset 0x01000000 \
  --tags_offset 0x00000100 \
  --cmdline "root=/dev/mmcblk0p10 rw console=ttyMSM0,115200" \
  -o /boot/boot.img
```

---

## Próximos Pasos

1. Completar descarga de kernel
2. Analizar defconfig actual
3. Crear versión Kupfer del defconfig
4. Compilar kernel minimalista para prueba
5. Flash en dispositivo

