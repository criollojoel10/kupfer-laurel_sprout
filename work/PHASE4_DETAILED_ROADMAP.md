# PHASE 4: Build System & Device Definition - Roadmap Detallado

## Estado General: 70% → 85% (después de esta fase)

---

## PHASE 4A: Setup Kernel Build System
**Tiempo estimado**: 4-6 horas
**Status**: En progreso (clonando kernel)

### A1. Descargar & Verificar Kernel ✅ EN PROGRESO
```bash
# En progreso: https://github.com/LineageOS/android_kernel_xiaomi_sm6125.git
# Tamaño esperado: ~500 MB (descargado con --depth=1)
# Ubicación final: /home/joel/kupfer-work/kernel/
```

### A2. Verificar Estructura Kernel (PRÓXIMO)
```bash
cd /home/joel/kupfer-work/kernel

# Verificar directorios críticos:
ls arch/arm64/boot/dts/qcom/           # Device Trees
ls arch/arm64/configs/                  # Defconfigs
ls drivers/                              # Drivers
ls kernel/                               # Kernel source

# Buscar defconfig para SM6125/Trinket:
find . -name "*trinket*" -o -name "*sm6125*" | grep -i config

# Verificar versión kernel:
cat Makefile | grep "^VERSION\|^PATCHLEVEL\|^SUBLEVEL"
```

### A3. Analizar Defconfig Disponible
**Ubicación esperada**: `arch/arm64/configs/trinket_defconfig` o similar

**Contenido crítico a verificar**:
```
CONFIG_ARM64=y
CONFIG_ARCH_QCOM=y
CONFIG_ARCH_SM6125=y (o TRINKET)
CONFIG_QUALCOMM_*=y (para drivers específicos)
```

### A4. Setup ARM64 Toolchain
**Verificar instalación**:
```bash
aarch64-linux-gnu-gcc --version  # Debe estar disponible
which aarch64-linux-gnu-as
which aarch64-linux-gnu-ld
```

**Si falta**:
```bash
sudo pacman -S arm-linux-gnueabihf-gcc arm-linux-gnueabihf-binutils
# O para ARM64:
sudo pacman -S aarch64-linux-gnu-gcc aarch64-linux-gnu-binutils
```

### A5. Crear Build Environment Script
**Archivo**: `/home/joel/kupfer-work/build_env.sh`

```bash
#!/bin/bash
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-
export KBUILD_BUILD_USER=joel
export KBUILD_BUILD_HOST=kupfer-dev
export KBUILD_BUILD_TIMESTAMP=$(date)
export KERNEL_DIR=/home/joel/kupfer-work/kernel
export DEVICE_DIR=/home/joel/kupfer-work/device
export VENDOR_DIR=/home/joel/kupfer-work/vendor
export OUTPUT_DIR=/home/joel/kupfer-work/out
export PATH=$KERNEL_DIR/scripts:$PATH

# Crear output dir si no existe
mkdir -p $OUTPUT_DIR

echo "Build environment configured for SM6125 (Trinket) kernel compilation"
echo "ARCH=$ARCH"
echo "CROSS_COMPILE=$CROSS_COMPILE"
echo "KERNEL_DIR=$KERNEL_DIR"
```

---

## PHASE 4B: Device Definition for Kupfer
**Tiempo estimado**: 3-5 horas
**Status**: Pendiente

### B1. Analizar Estructura Device Actual
```bash
cd /home/joel/kupfer-work/device

# Estructura típica:
# ├── BoardConfig.mk     ← Configuración kernel
# ├── device.mk          ← Paquetes/módulos
# ├── init/              ← Scripts init
# ├── dtbo.img           ← Device tree overlay
# ├── recovery.fstab     ← Particiones
# └── properties/        ← Propiedades sistema
```

### B2. Crear Directorio Kupfer Device
**Estructura esperada**:
```
/home/joel/kupfer-work/kupfer-device/
├── PKGBUILD                    ← Definición paquete Arch
├── kernel-config               ← Defconfig personalizado
├── device-tree/
│   ├── trinket.dtsi            ← Device tree source
│   └── laurel_sprout.dts       ← Overlay específico
├── init/
│   ├── init.kupfer.rc          ← Init script Kupfer
│   └── init.laurel_sprout.rc   ← Init específico dispositivo
├── boot/
│   └── boot.img               ← Imagen boot compilada
└── modules/
    └── (módulos compilados)
```

### B3. Crear PKGBUILD para Kupfer
**Archivo**: `/home/joel/kupfer-work/kupfer-device/PKGBUILD`

```bash
pkgname=kupfer-linux-sm6125
pkgver=4.14.356
pkgrel=1
pkgdesc="Kernel Linux 4.14 para SM6125 (Trinket) - Xiaomi Mi A3"
arch=('aarch64')
url="https://github.com/LineageOS/android_kernel_xiaomi_sm6125"
license=('GPL2')
depends=('busybox' 'kmod')
makedepends=('base-devel' 'bc' 'bison' 'flex' 'openssl' 'ccache')

build() {
  cd "$srcdir"
  make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)
}

package() {
  cd "$srcdir"
  # Copiar kernel compilado
  install -Dm644 arch/arm64/boot/Image.gz \
    "$pkgdir/boot/Image.gz"
  
  # Copiar módulos
  make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- \
    INSTALL_MOD_PATH="$pkgdir" modules_install
}
```

### B4. Adaptar Device Tree
**Tareas**:
- [ ] Copiar trinket.dtsi del kernel
- [ ] Crear overlay para laurel_sprout específico
- [ ] Compilar DTB (Device Tree Blob)
- [ ] Verificar compatibilidad con hardware

### B5. Crear Scripts Init
**Archivo**: init.laurel_sprout.rc
- [ ] Montar filesystems (/dev, /proc, /sys)
- [ ] Cargar módulos críticos (reguladores, pmic, etc.)
- [ ] Inicializar GPIO (panel detection)
- [ ] Setup de permisos

---

## PHASE 4C: Preparar Compilación
**Tiempo estimado**: 1-2 horas
**Status**: Pendiente

### C1. Generar Defconfig Personalizado
```bash
cd /home/joel/kupfer-work/kernel

# Copiar defconfig base
cp arch/arm64/configs/trinket_defconfig .config

# O generar desde zero
make ARCH=arm64 trinket_defconfig

# Verificar opciones críticas:
grep "CONFIG_ARM64\|CONFIG_QCOM\|CONFIG_SPMI\|CONFIG_REGULATOR" .config
```

### C2. Deshabilitar Módulos Innecesarios
Para Kupfer (minimalista), deshabilitar:
- [ ] CONFIG_ANDROID_*=y → n
- [ ] CONFIG_HID_* innecesarios
- [ ] CONFIG_MEDIA_* innecesarios
- [ ] CONFIG_SOUND_* (primero, no necesario)

### C3. Habilitar Módulos Críticos
Según FASE2C_DRIVERS_NEEDED.md:
- [ ] CONFIG_SPMI=y (Power management)
- [ ] CONFIG_QCOM_SPMI_PMIC=y
- [ ] CONFIG_QCOM_SMBB_CHARGER=y
- [ ] CONFIG_GPIO_QPNP_PIN=y
- [ ] CONFIG_QCOM_TSENS=y (thermal)
- [ ] CONFIG_DRM_MSM=y (display)
- [ ] CONFIG_USB_DWC3=y

### C4. Crear Script de Compilación
**Archivo**: `/home/joel/kupfer-work/compile.sh`

```bash
#!/bin/bash
set -e

source ./build_env.sh

echo "=== Compilando kernel para SM6125 ==="
cd $KERNEL_DIR

# Limpiar compilaciones previas
make ARCH=arm64 CROSS_COMPILE=$CROSS_COMPILE clean

# Generar .config
make ARCH=arm64 CROSS_COMPILE=$CROSS_COMPILE trinket_defconfig

# Compilar
time make ARCH=arm64 CROSS_COMPILE=$CROSS_COMPILE \
    -j$(nproc) 2>&1 | tee /tmp/build.log

# Compilar módulos
make ARCH=arm64 CROSS_COMPILE=$CROSS_COMPILE \
    -j$(nproc) modules 2>&1 | tee -a /tmp/build.log

# Copiar salida
mkdir -p $OUTPUT_DIR
cp arch/arm64/boot/Image.gz $OUTPUT_DIR/
cp arch/arm64/boot/dts/qcom/trinket.dtb $OUTPUT_DIR/

echo "=== Compilación completada ==="
ls -lah $OUTPUT_DIR/
```

---

## Checklist Completitud PHASE 4

### Parte A: Setup Build System
- [ ] Kernel clonado (EN PROGRESO)
- [ ] Estructura verificada
- [ ] Defconfig localizado
- [ ] Toolchain ARM64 verificado
- [ ] Build env script creado

### Parte B: Device Definition
- [ ] Estructura Kupfer device creada
- [ ] PKGBUILD escrito
- [ ] Device tree copiado/adaptado
- [ ] Scripts init creados
- [ ] Defconfig personalizado

### Parte C: Compilación Preparada
- [ ] Defconfig generado
- [ ] Módulos críticos habilitados
- [ ] Módulos innecesarios deshabilitados
- [ ] Script compilación creado
- [ ] Variables entorno documentadas

---

## Archivos Generados/Creados en PHASE 4

1. ✅ `PHASE4_DETAILED_ROADMAP.md` ← Este archivo
2. 📝 `PHASE4A_BUILD_SYSTEM_SETUP.md`
3. 📝 `/home/joel/kupfer-work/build_env.sh` (a crear)
4. 📝 `/home/joel/kupfer-work/kupfer-device/PKGBUILD` (a crear)
5. 📝 `/home/joel/kupfer-work/kupfer-device/kernel-config` (a crear)
6. 📝 `/home/joel/kupfer-work/compile.sh` (a crear)

---

## Tiempo Total Estimado

| Parte | Tarea | Tiempo |
|-------|-------|--------|
| 4A | Kernel + Verificación | 1-2h |
| 4B | Device Definition | 3-5h |
| 4C | Compilación Prep | 1-2h |
| **4 Total** | **Setup + Definition** | **5-9h** |

**Siguiente**: PHASE 5 (Compilación real + Testing)

---

## NOTAS IMPORTANTES

1. El kernel SM6125 es el correcto para laurel_sprout (MI A3)
2. Versión kernel: Linux 4.14.x (estable pero antiguo)
3. CAF (Code Aurora Forum) mantiene el source actualizado
4. Kupfer usa Arch Linux ARM como base → PKGBUILD es el standard
5. No necesitamos compilar todo Android, solo kernel + ramdisk

