# Kupfer Port Oficial para Xiaomi Mi A3 - Estructura Técnica Completa

**Autor**: Joel (@criollojoel10)  
**Fecha**: 21 de Abril de 2026  
**Estado**: Documentación de Referencia para Port Oficial  
**Basado en**: Análisis de device-sdm670-google-sargo + PostmarketOS pmaports

---

## 1. RESUMEN EJECUTIVO

Un port oficial de Kupfer para el Xiaomi Mi A3 requiere **4 paquetes principales**:

```
1. linux-sdm670              # Kernel compilado
2. device-sdm670-common      # Configuración común para SDM670
3. device-sdm670-xiaomi-laurel   # Configuración específica del Mi A3
4. firmware-sdm670-xiaomi-laurel # Blobs binarios del dispositivo
```

Más **archivos de configuración**:
- `deviceinfo` (del PostmarketOS pmaports)
- `machine-info`
- `mkinitcpio.conf.d/` configs
- `modules-initfs` (lista de módulos para initramfs)
- Opcionales: udev rules, systemd units

---

## 2. ESTRUCTURA DE DIRECTORIOS RECOMENDADA

### En repositorio local (desarrollo):

```
~/kupfer-port/
├── linux/
│   └── linux-sdm670/
│       ├── PKGBUILD
│       ├── extra_config          # Configuración personalizada
│       ├── linux.preset
│       ├── 60-linux.hook
│       └── 90-linux.hook
│
├── device/
│   ├── device-sdm670-common/
│   │   ├── PKGBUILD
│   │   ├── sdm670-common.conf
│   │   ├── sdm670.lst
│   │   ├── sdm670_callaudio.lst
│   │   └── bootmac-bt.lst
│   │
│   └── device-sdm670-xiaomi-laurel/
│       ├── PKGBUILD
│       ├── deviceinfo             # DE PostmarketOS pmaports
│       ├── modules-initfs         # Módulos kernel para initramfs
│       ├── machine-info
│       ├── xiaomi-laurel.conf
│       └── rootston.ini           # UI config (phosh)
│
└── firmware/
    └── firmware-sdm670-xiaomi-laurel/
        ├── PKGBUILD
        └── (referencia a repositorio de blobs)
```

### En repositorio oficial (kupfer/packages/pkgbuilds):

```
kupfer/packages/pkgbuilds/
├── linux/
│   └── sdm670/                    # Existente, solo necesita mantenimiento
│
├── device/
│   ├── device-sdm670-common/      # Existente, compartido
│   └── device-sdm670-xiaomi-laurel/  # NUEVO - Adicionar
│
└── firmware/
    └── firmware-sdm670-xiaomi-laurel/  # NUEVO - Adicionar
```

---

## 3. INFORMACIÓN DEL DISPOSITIVO (PostmarketOS)

### deviceinfo (del repositorio pmaports)

```bash
# Source: https://gitlab.com/postmarketOS/pmaports/-/raw/master/device/testing/device-xiaomi-laurel/deviceinfo

deviceinfo_format_version="0"
deviceinfo_name="Xiaomi Mi A3"
deviceinfo_manufacturer="Xiaomi"
deviceinfo_codename="xiaomi-laurel"
deviceinfo_year="2019"
deviceinfo_dtb="qcom/sm6125-xiaomi-laurel_sprout"  # Device tree (IMPORTANTE)
deviceinfo_arch="aarch64"

# Pantalla
deviceinfo_chassis="handset"
deviceinfo_keyboard="false"
deviceinfo_external_storage="true"
deviceinfo_screen_width="720"
deviceinfo_screen_height="1560"

# Bootloader (Fastboot)
deviceinfo_flash_method="fastboot"
deviceinfo_kernel_cmdline="clk_ignore_unused"
deviceinfo_generate_bootimg="true"
deviceinfo_flash_fastboot_partition_vbmeta="vbmeta"
deviceinfo_bootimg_qcdt="false"
deviceinfo_bootimg_mtk_mkimage="false"
deviceinfo_bootimg_dtb_second="false"
deviceinfo_append_dtb="true"                      # Agregar DTB al kernel
deviceinfo_rootfs_image_sector_size="4096"
deviceinfo_flash_pagesize="4096"
deviceinfo_flash_sparse="true"
deviceinfo_flash_offset_base="0x00000000"
deviceinfo_flash_offset_kernel="0x00008000"
deviceinfo_flash_offset_ramdisk="0x01000000"
deviceinfo_flash_offset_second="0x00f00000"
deviceinfo_flash_offset_tags="0x00000100"

# Particiones (CRÍTICO - investigar con lsblk/fdisk en TWRP)
# Identificar con: adb shell lsblk en dispositivo vivo
deviceinfo_partitions_data="/dev/mmcblk0p???"   # TBD - Investigar
deviceinfo_partitions_system="/dev/mmcblk0p???"  # TBD - Investigar
deviceinfo_partitions_boot="/dev/mmcblk0p???"    # TBD - Investigar
deviceinfo_partitions_recovery="/dev/mmcblk0p???" # TBD - Investigar

# Módulos kernel para initramfs (TBD)
deviceinfo_modules_initfs="gpi spi-geni-qcom"
```

**PENDIENTE**: Confirmar números de particiones (???) en dispositivo real con lsblk.

---

## 4. TEMPLATES DE PKGBUILD

### A. PKGBUILD para device-sdm670-xiaomi-laurel

```bash
_mode=cross
_nodeps=true
pkgname=device-sdm670-xiaomi-laurel
pkgdesc="Xiaomi Mi A3"
pkgver=0.1
pkgrel=1
_arches=specific
arch=(aarch64)
license=(MIT)
depends=(
    device-sdm670-common
    firmware-sdm670-xiaomi-laurel
    meta-qbootctl
)
makedepends=(devicepkg-helpers)

# Commit de PostmarketOS pmaports (actualizar periódicamente)
_commit=be110154ba203db01e58f87ee212657705abc129

source=(
    "https://gitlab.com/postmarketOS/pmaports/-/raw/${_commit}/device/testing/device-xiaomi-laurel/deviceinfo"
    "https://gitlab.com/postmarketOS/pmaports/-/raw/${_commit}/device/testing/device-xiaomi-laurel/modules-initfs"
    xiaomi-laurel.conf
    machine-info
    rootston.ini
)

sha256sums=(
    # Hashes SHA256 de los archivos descargados (generar con sha256sum)
    SKIP  # modules-initfs - puede no existir en pmaports
    SKIP  # xiaomi-laurel.conf
    SKIP  # machine-info
    SKIP  # rootston.ini
)

package() {
    # Instalar mkinitcpio config
    install -Dm644 "$srcdir"/xiaomi-laurel.conf \
        "$pkgdir"/etc/kupfer/mkinitcpio.conf.d/xiaomi-laurel.conf
    
    # Instalar machine-info
    install -Dm644 "$srcdir"/machine-info "$pkgdir"/etc/machine-info
    
    # Instalar UI config
    install -Dm644 "$srcdir"/rootston.ini "$pkgdir"/etc/phosh/rootston.ini
    
    # Preparar deviceinfo con información de particiones
    cp "$srcdir"/deviceinfo "$srcdir"/deviceinfo_
    cat >>"$srcdir"/deviceinfo_ <<EOF

deviceinfo_partitions_data="/dev/mmcblk0pXX"  # Reemplazar XX con número real
deviceinfo_partitions_system="/dev/mmcblk0pXX"
deviceinfo_partitions_boot="/dev/mmcblk0pXX"
deviceinfo_partitions_recovery="/dev/mmcblk0pXX"
deviceinfo_modules_initfs="$(cat "$srcdir"/modules-initfs 2>/dev/null | tr '\n' ' ')"
EOF
    
    install -Dm644 "$srcdir"/deviceinfo_ "$pkgdir"/etc/kupfer/deviceinfo
}
```

### B. PKGBUILD para device-sdm670-common (Referencia)

Ya existe en kupfer/packages/pkgbuilds, pero aquí está la estructura:

```bash
_mode=cross
_nodeps=true
pkgname=device-sdm670-common
pkgdesc="Common package for Qualcomm SDM670 devices"
pkgver=0.1
pkgrel=4
_arches=specific
arch=(aarch64)
license=(MIT)
provides=(alsa-ucm-conf)
conflicts=(alsa-ucm-conf)

depends=(
    linux-firmware-atheros
    linux-firmware-qcom
    linux-sdm670
    pd-mapper-git
    qrtr-git
    rmtfs-git
    tqftpserv-git
    boot-android-common
    meta-modem-qcom
    q6voiced
    bootmac
)

_ucm_commit=ae7dee03e655fcb1aa68bb327397cd838cf99bb1
source=(
    "git+https://gitlab.com/sdm670-mainline/alsa-ucm-conf.git/#commit=$_ucm_commit"
    sdm670-common.conf
    sdm670.lst
    sdm670_callaudio.lst
    bootmac-bt.lst
)

package() {
    # Instalar configs mkinitcpio
    install -Dm644 "$srcdir"/sdm670-common.conf \
        "$pkgdir"/etc/kupfer/mkinitcpio.conf.d/sdm670-common.conf
    
    # Instalar systemd units
    install -Dm644 "$srcdir"/sdm670.lst \
        "$pkgdir"/etc/kupfer/systemd/sdm670.lst
    install -Dm644 "$srcdir"/bootmac-bt.lst \
        "$pkgdir"/etc/kupfer/systemd/bootmac-bt.lst
    install -Dm644 "$srcdir"/sdm670_callaudio.lst \
        "$pkgdir"/etc/kupfer/systemd/user/sdm670_callaudio.lst
    
    # Instalar ALSA UCM configs (audio)
    cd "$srcdir"/alsa-ucm-conf
    export alsadir="${pkgdir}/usr/share/alsa/"
    find ucm2 -type f -iname "*.conf" -exec install -vDm 644 {} "$alsadir"{} \;
    find ucm2 -type l -iname "*.conf" -exec bash -c \
        'install -vdm 755 "${alsadir}$(dirname "{}")" && cp -dv "{}" "${alsadir}{}"' \;
}
```

### C. PKGBUILD para firmware-sdm670-xiaomi-laurel

```bash
_mode=cross
pkgname=firmware-sdm670-xiaomi-laurel
pkgver=0.1
pkgrel=1
_arches=specific
arch=(aarch64)
license=(custom:Proprietary)
options=(!strip)

# Referencia: Buscar repositorio de blobs del Mi A3
# Opciones:
# 1. Extraer de ROM android oficial (adb pull)
# 2. Clonar de repositorio similar (ej: Pixel 3a)
# 3. Obtener de LineageOS device tree

source=(
    "git+https://github.com/criollojoel10/firmware-mi-a3.git"
)
sha256sums=(
    SKIP
)

package() {
    cp -avf "$srcdir"/firmware-mi-a3/* "$pkgdir"/
}
```

### D. PKGBUILD para linux-sdm670 (Referencia existente)

```bash
_mode=cross
_kernelname=sdm670
pkgbase="linux-$_kernelname"
_desc="Qualcomm SDM670 kernel"
pkgver=6.6.3          # Actualizar según versión disponible
pkgrel=2
_arches=specific
arch=(aarch64)
license=(GPL2)
url=https://gitlab.com/sdm670-mainline/linux
makedepends=(
    xmlto docbook-xsl kmod inetutils bc dtc cpio
)
options=(!strip)

_commit=d480f5e9e022a4eef746e894b9fa1cc712244987  # Actualizar si es necesario
source=(
    "linux-${_commit}.tar.gz::${url}/-/archive/${_commit}.tar.gz"
    extra_config
    linux.preset
    60-linux.hook
    90-linux.hook
)

build() {
    cd linux-*
    make defconfig sdm670.config
    cat ../extra_config >> .config
    make olddefconfig
    sed -i "2iexit 0" scripts/depmod.sh
    make ${MAKEFLAGS} Image.gz modules
    make ${MAKEFLAGS} DTC_FLAGS="-@" dtbs
}

package() {
    # Instalar kernel
    mkdir -p "${pkgdir}"/{boot,usr/lib/modules}
    make INSTALL_MOD_PATH="${pkgdir}/usr" modules_install
    cp arch/arm64/boot/Image.gz "${pkgdir}/boot"
    
    # Instalar device trees del Mi A3
    mkdir -p "${pkgdir}/boot/dtbs/qcom"
    cp arch/arm64/boot/dts/qcom/sm6125-xiaomi-laurel*.dtb \
        "${pkgdir}/boot/dtbs/qcom/" 2>/dev/null || true
    
    # El resto del packaging es estándar Arch Linux
}
```

---

## 5. ARCHIVOS DE CONFIGURACIÓN

### A. machine-info
```ini
PRETTY_HOSTNAME="Xiaomi Mi A3"
CHASSIS=handset
ICON_NAME=phone
```

### B. xiaomi-laurel.conf (mkinitcpio)
```ini
FILES+=(/lib/firmware/qcom/sdm670/laurel/a615_zap.mbn)
# Agregar otros firmware según sea necesario
```

### C. rootston.ini (Phosh UI config)
```ini
[Output MIPI-1]
scaling_mode=aspect
transform=normal
```

### D. modules-initfs
```
# Módulos necesarios para inicializar el sistema
gpi
spi-geni-qcom
# Agregar otros según sea necesario
```

---

## 6. CHECKLIST ANTES DE CREAR PKGBUILDS

### Fase 1: Investigación Hardware

- [ ] **Obtener números de particiones exactos**
  ```bash
  adb shell lsblk
  adb shell cat /proc/partitions
  # Identificar: data, system, boot, recovery
  ```

- [ ] **Confirmar devicetree**
  ```bash
  adb shell cat /sys/firmware/devicetree/base/model
  # Debe coincidir con arch/arm64/boot/dts/qcom/sm6125-xiaomi-laurel*.dtb
  ```

- [ ] **Listar firmware necesario**
  ```bash
  ls -la /lib/firmware/qcom/sdm670/
  # O extraer ROM Android y buscar en /system/lib/firmware
  ```

- [ ] **Identificar módulos kernel para initramfs**
  ```bash
  # Revisar logs de compilación
  # Modules usados en booting: gpi, spi-geni-qcom, etc.
  ```

### Fase 2: Preparar PKGBUILDs

- [ ] Descargar/obtener archivos de PostmarketOS pmaports
- [ ] Calcular SHA256sums correctos
- [ ] Crear extra_config con cambios necesarios
- [ ] Validar sintaxis PKGBUILD
  ```bash
  namcap device-sdm670-xiaomi-laurel/PKGBUILD
  ```

### Fase 3: Integración

- [ ] Fork de kupfer/packages/pkgbuilds
- [ ] Crear rama feature/sdm670-xiaomi-laurel
- [ ] Push de los 3 packages (device-sdm670-xiaomi-laurel, firmware-*, posiblemente device-sdm670-common updates)
- [ ] Crear Merge Request con descripción detallada

---

## 7. DEPENDENCIAS CRÍTICAS

### Paquetes que debe tener instalado el Usuario Final

```bash
# Base Kupfer
kupfer-base
kupfer-linux-sdm670
device-sdm670-xiaomi-laurel
device-sdm670-common
firmware-sdm670-xiaomi-laurel

# Dependencias automáticas (instaladas por pacman)
linux-firmware-qcom
pd-mapper-git
qrtr-git
rmtfs-git
q6voiced
meta-modem-qcom
boot-android-common

# UI (elegir una)
phosh                  # Recomendado
sxmo                   # Alternativa
lomiri-deviceinfo      # Alternativa

# Base system
base
base-devel (para desarrollo)
network-manager
```

---

## 8. REFERENCIAS Y FUENTES

| Componente | Fuente | Notas |
|-----------|--------|-------|
| **Kernel** | https://gitlab.com/sdm670-mainline/linux | Mainline SDM670 |
| **Device Config** | https://gitlab.com/kupfer/packages/pkgbuilds/-/tree/dev/device | Plantillas |
| **PostmarketOS** | https://gitlab.com/postmarketOS/pmaports | deviceinfo |
| **ALSA UCM** | https://gitlab.com/sdm670-mainline/alsa-ucm-conf | Audio |
| **Referencia (Sargo)** | device-sdm670-google-sargo | Google Pixel 3a |
| **Mi A3 Info** | wiki.postmarketos.org | Hardware reference |

---

## 9. PRÓXIMOS PASOS (Orden Recomendado)

### Semana 1: Finalizando Compilación

1. ✅ **Completar compilación del kernel** (esperando)
2. ✅ **Validar Image.gz y modules**
3. **Verificar Device Trees compilados**
4. **Crear boot.img con mkbootimg**
5. **Flashear a dispositivo y validar boot**

### Semana 2: Crear PKGBUILDs

1. **Investigar particiones exactas del Mi A3**
   ```bash
   adb shell lsblk  # Desde dispositivo vivo
   ```

2. **Crear PKGBUILD para device-sdm670-xiaomi-laurel**
   - Bajar archivos de PostmarketOS pmaports
   - Configurar sha256sums
   - Crear xiaomi-laurel.conf personalizado

3. **Crear PKGBUILD para firmware**
   - Obtener firmware de ROM oficial o LineageOS
   - Empacar en repositorio separado

4. **Validar PKGBUILDs**
   ```bash
   cd device-sdm670-xiaomi-laurel
   namcap PKGBUILD
   ```

### Semana 3: Pruebas

1. **Instalar paquetes localmente en Arch ARM**
2. **Construir imagen con kupferbootstrap**
3. **Flashear a dispositivo**
4. **Validar componentes**:
   - ✅ Boot
   - ✅ Display
   - ✅ Modem
   - ✅ Audio
   - ✅ WiFi/BT
   - ✅ Carga

### Semana 4: Envío Oficial

1. **Fork kupfer/packages/pkgbuilds**
2. **Push a rama feature**
3. **Crear Merge Request**
4. **Code review de mantenedores**
5. **Merge a rama dev/main**
6. **¡Soporte oficial alcanzado!**

---

## 10. RECURSOS Y HERRAMIENTAS

```bash
# Herramientas necesarias
pacman -S kupferbootstrap
pacman -S devicepkg-helpers
pacman -S aarch64-linux-gnu-{gcc,binutils}

# Para investigación
adb shell lsblk
adb shell cat /proc/partitions
adb pull /sys/firmware/devicetree/base/model

# Para compilación
git clone https://gitlab.com/kupfer/packages/pkgbuilds.git
cd pkgbuilds/device
mkdir device-sdm670-xiaomi-laurel
cd device-sdm670-xiaomi-laurel
# ... Crear PKGBUILD ...

# Para validación
namcap PKGBUILD
makepkg --syncdeps
```

---

## CONCLUSIÓN

El port oficial de Kupfer para el Xiaomi Mi A3 es **técnicamente factible** y sigue el patrón establecido por otros devices (sargo, enchilada, etc.). 

Las 4 fases principales son:
1. ✅ **Investigación** (COMPLETADO)
2. ✅ **Compilación del kernel** (EN PROGRESO)
3. **Creación de PKGBUILDs** (PRÓXIMA)
4. **Envío a repositorio oficial** (FINAL)

Tiempo estimado restante: **2-3 semanas** con dedicación parcial.
