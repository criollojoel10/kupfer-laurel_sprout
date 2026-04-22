# PHASE 4A: Kupfer Build System Setup
## Objetivo: Preparar el entorno de compilación para el kernel de laurel_sprout

### Estado: EN PROGRESO

---

## 1. Análisis de Requisitos

### 1.1 Herramientas Necesarias
- ✅ gcc (ARM64 cross-compiler)
- ✅ make, binutils
- ✅ bc, bison, flex
- ✅ openssl
- ✅ ccache
- ✅ adb, fastboot

### 1.2 Directorios de Trabajo
```
/home/joel/kupfer-work/
├── device/       (30 MB) - CLONADO
├── vendor/       (77 MB) - CLONADO
├── kernel/       (?) - PENDIENTE DESCARGAR
├── tools/        (?) - Por setup
├── output/       (?) - Para compilación
└── downloads/    (?) - Para descargas
```

### 1.3 Estructura Esperada Kupfer
Kupfer es un derivado de Arch Linux ARM, por lo que:
- Usa PKGBUILD para definición de paquetes
- Soporta cross-compilation con makepkg
- Puede usar defconfig de kernel estándar

---

## 2. Variables de Compilación

### 2.1 ARM64 Toolchain
```bash
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-
export KBUILD_BUILD_USER=joel
export KBUILD_BUILD_HOST=kupfer-dev
```

### 2.2 Paths Kritisks
```bash
KERNEL_DIR=/home/joel/kupfer-work/kernel
DEVICE_DIR=/home/joel/kupfer-work/device
VENDOR_DIR=/home/joel/kupfer-work/vendor
OUTPUT_DIR=/home/joel/kupfer-work/out
```

### 2.3 Defconfig Location
Esperado en: `arch/arm64/configs/` o directamente en el kernel source

---

## 3. Pasos Próximos

1. [ ] Descargar kernel completo
2. [ ] Verificar estructura
3. [ ] Crear defconfig personalizado
4. [ ] Setup toolchain si necesario
5. [ ] Crear scripts de compilación

---

## 4. Comandos Referencia

```bash
# Listar configuraciones disponibles
find $KERNEL_DIR/arch/arm64/configs -name "*.config"

# Generar defconfig para SDM439 (Trinket)
make ARCH=arm64 trinket_defconfig

# Compilar kernel
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)
```

---

