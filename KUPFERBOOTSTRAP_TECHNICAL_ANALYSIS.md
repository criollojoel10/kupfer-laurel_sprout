# Kupferbootstrap - Análisis Técnico Completo para Mi A3

**Fecha**: 21 de Abril de 2026  
**Estado**: Investigación en profundidad  

---

## 1. ¿QUÉ ES KUPFERBOOTSTRAP?

**Kupferbootstrap** es la **herramienta oficial de Kupfer** para construir imágenes de SO personalizadas para dispositivos móviles Qualcomm.

### Características Clave

```
Entrada:  PKGBUILDs + configs de dispositivo
          ↓
        [kupferbootstrap]
          ↓
Salida:  Imagen lista para flashear (boot.img, system.img, etc)
```

### Flujo de Trabajo

```
1. Pacstrap           → Instala paquetes base
2. Compilation        → Compila paquetes de dispositivo
3. Mkinitcpio         → Crea initramfs
4. Mkfs               → Crea sistema de archivos
5. Mkbootimg          → Empacar Image + initramfs + DTB
6. Fastboot Flash     → Flashear al dispositivo
```

---

## 2. ARQUITECTURA Y COMPONENTES

### Struktura de kupferbootstrap

```
kupferbootstrap/
├── kupferbootstrap/
│   ├── cli.py                  # CLI principal
│   │   ├── main()
│   │   ├── config()
│   │   ├── packages()
│   │   ├── image()
│   │   └── flash()
│   │
│   ├── config.py              # Gestión de configuración
│   │   ├── load_config()
│   │   ├── save_config()
│   │   └── get_device_config()
│   │
│   ├── packages.py            # Gestión de paquetes
│   │   ├── prepare_pacstrap()
│   │   ├── compile_packages()
│   │   └── resolve_deps()
│   │
│   ├── image.py               # Builder de imágenes
│   │   ├── create_rootfs()
│   │   ├── mkinitcpio()
│   │   ├── mkbootimg()
│   │   └── mkfs()
│   │
│   └── utils.py               # Utilidades
│       ├── run_cmd()
│       ├── get_device_info()
│       └── validate_config()
│
├── docs/                      # Documentación
│   ├── README.md
│   ├── INSTALLATION.md
│   ├── DEVICES.md
│   └── CONTRIBUTING.md
│
└── config.json.example
```

---

## 3. INSTALACIÓN Y CONFIGURACIÓN

### 3.1 Requerimientos Previos

```bash
# Sistema base
- Arch Linux (o compatible)
- Python 3.8+
- Git

# Herramientas de compilación
- gcc, make, binutils
- bc, bison, flex (para kernel)
- dtc (device tree compiler)
- mkinitcpio
- mkbootimg

# Paquetes Kupfer
- devicepkg-helpers
- pacman-contrib
```

### 3.2 Instalación

```bash
# Clonar repositorio
git clone https://gitlab.com/kupfer/kupferbootstrap.git
cd kupferbootstrap

# Crear virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalar en modo desarrollo
pip install -e .

# O instalar desde PyPI (cuando esté disponible)
pip install kupferbootstrap
```

### 3.3 Configuración Inicial

```bash
# Inicializar configuración
kupferbootstrap config init

# Editar configuración
nano ~/.config/kupferbootstrap/config.json
```

**Estructura de config.json**:

```json
{
  "device": {
    "codename": "sdm670-xiaomi-laurel",
    "name": "Xiaomi Mi A3",
    "manufacturer": "Xiaomi",
    "arch": "aarch64",
    "soc": "sdm670"
  },
  
  "build": {
    "flavor": "phosh",
    "branch": "dev",
    "rootfs_type": "ext4",
    "rootfs_size_mb": 2048,
    "jobs": 4
  },
  
  "paths": {
    "pkgbuilds": "/path/to/kupfer-pkgbuilds",
    "cache": "~/.cache/kupferbootstrap",
    "output": "~/kupfer-images"
  },
  
  "packages": {
    "base": [
      "base",
      "linux-sdm670",
      "device-sdm670-xiaomi-laurel",
      "firmware-sdm670-xiaomi-laurel"
    ],
    "extra": [
      "phosh",
      "networkmanager",
      "gedit"
    ]
  },
  
  "fastboot": {
    "enabled": true,
    "device_serial": "auto"
  }
}
```

---

## 4. FLUJO DE COMPILACIÓN CON KUPFERBOOTSTRAP

### Paso a Paso

```bash
# 1. Inicializar paquetes
kupferbootstrap packages init

# Output esperado:
# - Clona kupfer/packages/pkgbuilds
# - Configura caché local
# - Prepara ambiente de compilación

# 2. Compilar paquetes específicos del dispositivo
kupferbootstrap packages build device-sdm670-xiaomi-laurel

# Output esperado:
# - Busca PKGBUILD en ~/.local/share/kupferbootstrap/pkgbuilds
# - Resuelve dependencias
# - Compila device-sdm670-common (dependencia)
# - Compila device-sdm670-xiaomi-laurel
# - Genera .pkg.tar.zst en caché

# 3. Compilar imagen raíz (rootfs)
kupferbootstrap image prepare-rootfs

# Output esperado:
# - Crea root filesystem
# - Ejecuta pacstrap con paquetes base
# - Instala device packages
# - Instala UI (phosh, sxmo, etc)

# 4. Crear initramfs
kupferbootstrap image create-initramfs

# Output esperado:
# - Ejecuta mkinitcpio
# - Incluye módulos del kernel necesarios
# - Genera initramfs.img

# 5. Compilar device trees (si no existen)
kupferbootstrap image compile-dtbs

# Output esperado:
# - Compila arch/arm64/boot/dts/qcom/*.dtb
# - Copia a ~/kupfer-images/

# 6. Crear boot.img
kupferbootstrap image create-bootimg

# Output esperado:
# mkbootimg \
#   --kernel vmlinuz \
#   --ramdisk initramfs.img \
#   --dtb sm6125-xiaomi-laurel.dtb \
#   --cmdline "clk_ignore_unused" \
#   --pagesize 4096 \
#   --base 0x00000000 \
#   --kernel_offset 0x00008000 \
#   --ramdisk_offset 0x01000000 \
#   --output boot.img

# 7. Crear imagen de sistema
kupferbootstrap image create-system-img

# Output esperado:
# mkfs.ext4 -F system.img
# Copia rootfs a imagen

# 8. Flashear al dispositivo
kupferbootstrap device flash

# Output esperado:
# fastboot flash boot boot.img
# fastboot flash system system.img
# fastboot flash vbmeta vbmeta.img
# fastboot reboot
```

---

## 5. INTEGRACIÓN CON KERNEL COMPILADO

### Opción A: Compilar Kernel a través de kupferbootstrap

```bash
# 1. kupferbootstrap compila linux-sdm670 automáticamente
#    si está listado en packages -> base

# 2. Configurar versión en PKGBUILD
nano ~/.local/share/kupferbootstrap/pkgbuilds/linux/sdm670/PKGBUILD
# Cambiar pkgver, _commit, sha256sums según necesidad

# 3. La compilación ocurre durante:
kupferbootstrap packages build device-sdm670-xiaomi-laurel
# Porque device-sdm670-common depende de linux-sdm670
```

### Opción B: Usar Kernel Pre-compilado

Si ya tienes `Image.gz` compilado:

```bash
# 1. Copiar kernel a ubicación conocida
cp /home/joel/kupfer-work/kernel/arch/arm64/boot/Image.gz \
   ~/.cache/kupferbootstrap/linux-sdm670/boot/vmlinuz

# 2. Crear PKGBUILD local que referencia el binario
nano ~/.local/share/kupferbootstrap/pkgbuilds/linux/sdm670/PKGBUILD

# Modificar para usar binario local:
source=(
    "file:///home/joel/kupfer-work/kernel/arch/arm64/boot/Image.gz"
)

# 3. El resto del flujo es igual
kupferbootstrap packages build device-sdm670-xiaomi-laurel
```

### Opción C: Bypass Manual (Desarrollo Rápido)

Para desarrollo rápido sin recompilar:

```bash
# 1. Crear estructura manual de rootfs
mkdir -p ~/kupfer-mi-a3-build
cd ~/kupfer-mi-a3-build

# 2. Pacstrap manual
sudo pacstrap -C /etc/pacman.conf -c rootfs \
  base \
  linux-sdm670 \
  device-sdm670-xiaomi-laurel \
  firmware-sdm670-xiaomi-laurel

# 3. Crear initramfs
mkinitcpio -r rootfs -c /etc/mkinitcpio.conf -o initramfs.img

# 4. Crear boot.img
mkbootimg \
  --kernel /home/joel/kupfer-work/kernel/arch/arm64/boot/Image.gz \
  --ramdisk initramfs.img \
  --dtb /home/joel/kupfer-work/kernel/arch/arm64/boot/dts/qcom/sm6125-xiaomi-laurel_sprout.dtb \
  --output boot.img

# 5. Flashear
fastboot flash boot boot.img
```

---

## 6. CONFIGURACIÓN ESPECÍFICA PARA MI A3

### Archivo device-specific config

```bash
# ~/.config/kupferbootstrap/devices/sdm670-xiaomi-laurel.conf

DEVICE_CODENAME="sdm670-xiaomi-laurel"
DEVICE_NAME="Xiaomi Mi A3"
DEVICE_ARCH="aarch64"
DEVICE_SOC="sdm670"
DEVICE_VARIANT="f9s"

# Bootloader config
FASTBOOT_ENABLED="true"
FASTBOOT_PARTITION_BOOT="boot"
FASTBOOT_PARTITION_SYSTEM="system"
FASTBOOT_PARTITION_VBMETA="vbmeta"

# Kernel cmdline
KERNEL_CMDLINE="clk_ignore_unused"

# Particiones
PARTITION_DATA="/dev/mmcblk0pXX"      # Investigar
PARTITION_SYSTEM="/dev/mmcblk0pXX"    # Investigar
PARTITION_BOOT="/dev/mmcblk0pXX"      # Investigar

# Modules para initramfs
MODULES_INITFS="gpi spi-geni-qcom"

# UI
UI_FLAVOR="phosh"

# Tamaños
ROOTFS_SIZE_MB=2048
CACHE_SIZE_MB=512
```

---

## 7. TROUBLESHOOTING COMÚN

### Problema: "Config file not found"

```bash
# Solución
kupferbootstrap config init
# Luego editar:
nano ~/.config/kupferbootstrap/config.json
```

### Problema: "device-sdm670-common not found"

```bash
# Solución: Asegurar que pkgbuilds está actualizado
kupferbootstrap packages update
# O apuntar a repositorio local:
kupferbootstrap packages init \
  --pkgbuilds-source=file:///home/joel/kupfer-port
```

### Problema: "Kernel modules not found"

```bash
# Solución: Asegurar que linux-sdm670 está compilado con CONFIG_MODULES=y
grep CONFIG_MODULES /home/joel/kupfer-work/kernel/.config
# Debe mostrar: CONFIG_MODULES=y

# Si no, reconfigurar y recompilar
cd /home/joel/kupfer-work/kernel
make ARCH=arm64 menuconfig
# Enable: Loadable module support -> Module support
```

### Problema: "mkbootimg: command not found"

```bash
# Solución: Instalar herramienta
sudo pacman -S android-tools
# O compilar desde source
git clone https://github.com/osm0sis/mkbootimg
```

---

## 8. ALTERNATIVA: COMPILAR MANUALMENTE (SIN KUPFERBOOTSTRAP)

Para casos de emergencia o desarrollo rápido:

```bash
#!/bin/bash
# manual_build.sh

KERNEL_DIR="/home/joel/kupfer-work/kernel"
DEVICE_ARCH="aarch64"
CROSS_COMPILE="aarch64-linux-gnu-"
OUTPUT_DIR="/tmp/kupfer-mi-a3"

mkdir -p $OUTPUT_DIR

# 1. Compilar kernel
cd $KERNEL_DIR
make ARCH=$DEVICE_ARCH CROSS_COMPILE=$CROSS_COMPILE -j6 Image.gz modules dtbs

# 2. Instalar modules
mkdir -p $OUTPUT_DIR/lib/modules
make ARCH=$DEVICE_ARCH CROSS_COMPILE=$CROSS_COMPILE \
  INSTALL_MOD_PATH=$OUTPUT_DIR modules_install

# 3. Crear initramfs
mkinitcpio \
  -c /etc/mkinitcpio.conf \
  -r $OUTPUT_DIR \
  -o $OUTPUT_DIR/initramfs.img

# 4. Crear boot.img
mkbootimg \
  --kernel $KERNEL_DIR/arch/arm64/boot/Image.gz \
  --ramdisk $OUTPUT_DIR/initramfs.img \
  --dtb $KERNEL_DIR/arch/arm64/boot/dts/qcom/sm6125-xiaomi-laurel_sprout.dtb \
  --cmdline "clk_ignore_unused" \
  --pagesize 4096 \
  --base 0x00000000 \
  --kernel_offset 0x00008000 \
  --ramdisk_offset 0x01000000 \
  --output $OUTPUT_DIR/boot.img

# 5. Flashear
fastboot flash boot $OUTPUT_DIR/boot.img
fastboot reboot
```

---

## 9. CHECKLIST PRE-CONSTRUCCIÓN

Antes de ejecutar `kupferbootstrap image build`:

- [ ] Kernel compilado (Image.gz, modules, dtbs generados)
- [ ] PKGBUILD de device-sdm670-xiaomi-laurel creado y validado
- [ ] PKGBUILD de firmware-sdm670-xiaomi-laurel existente
- [ ] device-sdm670-common disponible en repositorio
- [ ] Archivo deviceinfo con particiones correctas
- [ ] Archivo machine-info creado
- [ ] Archivo rootston.ini configurado para Phosh
- [ ] Módulos kernel identificados (modules-initfs)
- [ ] Config de kupferbootstrap actualizado
- [ ] Espacio suficiente en disco (mínimo 5GB)
- [ ] Dispositivo en fastboot mode y USB conectado

---

## 10. FLUJO COMPLETO ESTIMADO

```
TIEMPO                      ACTIVIDAD
────────────────────────────────────────────
Ahora                  ✅ Compilación kernel (EN PROGRESO)
Ahora+30min            ✅ Validar Image.gz
+1h                    📋 Crear PKGBUILDs (device, firmware)
+2h                    📋 Validar PKGBUILDs con namcap
+3h                    📋 Instalar kupferbootstrap
+4h                    🔧 kupferbootstrap image build
+5h                    ⚡ fastboot flash
+5h30min               ✨ Testing en dispositivo
+6h                    📊 Documentación final
+6h30min               🚀 Envío a repositorio oficial
```

---

## CONCLUSIÓN

**Kupferbootstrap** automatiza todo el proceso de construcción, pero entender el flujo manual es crucial para:

1. ✅ Debugging cuando algo falla
2. ✅ Optimización de compilación
3. ✅ Desarrollo rápido
4. ✅ Adaptación a variantes de hardware

**Recomendación**: 
- Primero, completar compilación manual del kernel
- Luego, crear PKGBUILDs paso a paso
- Finalmente, integrar todo con kupferbootstrap para automatización
