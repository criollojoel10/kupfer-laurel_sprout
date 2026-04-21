# Kupfer Port Project: Xiaomi Mi A3 (laurel_sprout)

**Objetivo**: Portar **Kupfer (Arch Linux ARM)** al Xiaomi Mi A3 como dispositivo oficial compatible.

**Estado**: Fase 1 completada - Investigación y extracción de datos ✅

---

## 📋 Contenido del Proyecto

### Root Directory
```
/
├── boot.img                 (64 MB) - Kernel + Ramdisk de LineageOS
├── dtbo.img                 (8 MB)  - Device Tree Overlays
├── vbmeta.img               (4 KB)  - Android Verified Boot metadata
├── lineage-23.0-...-.zip   (1.1 GB) - ROM LineageOS 23.0 nightly
├── tue_apr_21_2026_...json  (189 KB) - Thread de conversación previa
├── README.md                (Este archivo)
└── work/                    (136 MB) - Análisis e extracciones
```

### Directorio `/work/` - Análisis Técnico

#### Documentación
```
work/
├── RESUMEN_EJECUTIVO.md
│   └─ Resumen ejecutivo de estado, progreso, próximos pasos
│
├── TECHNICAL_SPECIFICATION.md
│   └─ Especificación técnica completa de hardware
│       ├─ SoC: SDM439 (Snapdragon 439)
│       ├─ Kernel: Linux 4.14.356-openela-rc1-perf
│       ├─ Device Tree: Configuración MDSS/DSI/Audio/Sensores
│       └─ Drivers requeridos identificados
│
├── ANALYSIS.md
│   └─ Análisis detallado de arquitectura
│       ├─ Boot chain
│       ├─ Referencias técnicas
│       └─ Comandos de referencia
│
└── extract_boot_img.py
    └─ Script Python para extraer boot.img (kernel + ramdisk)
```

#### Archivos Extraídos
```
work/extracts/
├── boot/
│   ├── kernel                  (17.5 MB) - Kernel Linux comprimido (gzip)
│   ├── kernel_decompressed     (43 MB)   - Kernel descomprimido
│   ├── ramdisk.cpio            (16.7 MB) - Sistema ramdisk
│   └── ramdisk/                (77K archivos)
│       ├── bin/ → /system/bin
│       ├── dev/ - Nodos de dispositivo
│       ├── etc/ - Configuración
│       ├── system/ - Sistema Android completo
│       ├── data/ - Datos de usuario
│       ├── prop.default - Propiedades predeterminadas
│       └── init.rc - Scripts de inicialización
│
└── dtbo_extract/
    └── dtb_0.dtb               (221 KB) - Device Tree Blob extraído
        ├── qcom,trinket-qrd (board match)
        ├── Display config (5 paneles MIPI DSI)
        ├── Audio config (WCD938x codec)
        └── Thermal zones
```

#### Directorios para Futuros Trabajos
```
work/
├── kernels/          (Para clonar repos de kernel)
├── device_tree/      (Para análisis DTB/DTS)
├── analysis/         (Para scripts de análisis adicionales)
└── docs/            (Para documentación adicional)
```

---

## 🔍 Información del Hardware Extraída

### SoC: Qualcomm Snapdragon 439 (SM6125)
| Componente | Especificación |
|-----------|-----------------|
| **CPU** | 8x ARM Cortex-A53 @ 2.2 GHz |
| **GPU** | Adreno 505 |
| **RAM** | LPDDR4X (4 GB) |
| **Storage** | eMMC 5.1 (128 GB) |
| **ISP** | Qualcomm Spectra 180 |
| **UART** | ttyMSM0 (debug serial) |

### Kernel Actual
```
Linux version 4.14.356-openela-rc1-perf-g9eacaaff21e8
Compiler: Android Clang 20.0.0
Build: Tue Feb 24 05:51:54 UTC 2026
Base: CAF (Code Aurora Forum) msm-4.14
Config: SMP PREEMPT, modversions enabled
```

### Bootloader Cmdline (key params for Kupfer)
```
console=ttyMSM0 (serial output)
video=vfb:640x400,bpp=32,memsize=3072000 (framebuffer)
swiotlb=1 (software IOMMU)
loop.max_part=7 (loop devices)
lpm_levels.sleep_disabled=1 (power management)
```

### Device Tree Identifiers
```
qcom,trinket-qrd (exact board match)
qcom,trinket (fallback)
qcom,qrd (generic QRD)
```

### Display Panels Soportados
- Truly TD4330 (Command Mode & Video Mode)
- Truly HX83112A (Video Mode)  
- Truly NT36672 (Video Mode)
- Simulator Panel (for testing)

**Interface**: MIPI DSI → MDSS (Mobile Display SubSystem)

### Audio Configuration
- **Codec**: WCD938x (embedded in PMIC)
- **Interface**: I2S/TDM
- **DSP**: QDSP for audio processing
- **MICs**: Multiple inputs via PMIC
- **Speaker**: Mono via PMIC

---

## 🛠️ Herramientas Instaladas en Arch Linux

✅ **adb** v37.0.0 (Android Debug Bridge)  
✅ **fastboot** (vía android-sdk-platform-tools)  
✅ **base-devel** (gcc, make, binutils)  
✅ **git** (control de versiones)  
✅ **bc, bison, flex** (compilación kernel)  
✅ **openssl** (criptografía)  
✅ **ccache** (aceleración compilación)  
✅ **unzip, binutils** (análisis de archivos)  

**Instaladas en**: `/opt/android-sdk/platform-tools/`

---

## 📚 Próximos Pasos (Fases 2-4)

### ⏳ Fase 2: Análisis de Kernel & Device Tree (3-5 días)
```bash
git clone https://github.com/MasterAwesome/android_kernel_xiaomi_laurel_sprout
git clone https://github.com/MasterAwesome/android_device_xiaomi_laurel_sprout
```
- Comparar con Google Pixel 3a (SDM670) en Kupfer
- Identificar drivers necesarios
- Preparar configuración

### ⏳ Fase 3: Repositorio GitHub Público (Inmediato)
- Crear repo: `kupfer-laurel_sprout`
- Documentación de porting
- Setup de issues y colaboración

### ⏳ Fase 4: Primera Compilación (3-5 días)
- Kernel minimalista
- Ramdisk Arch Linux ARM básico
- Prueba en dispositivo
- Debug de arranque

### ⏳ Fase 5: Hardware Enablement (1-2 semanas)
- Display (MDSS/DSI)
- Input (touchscreen, botones)
- Storage (eMMC)
- Audio
- Wifi/Bluetooth

---

## 🔗 Referencias Técnicas

### Repositorios Clave
- **LineageOS Kernel**: https://github.com/MasterAwesome/android_kernel_xiaomi_laurel_sprout
- **LineageOS Device Tree**: https://github.com/MasterAwesome/android_device_xiaomi_laurel_sprout
- **Vendor Blobs**: https://github.com/MasterAwesome/android_vendor_xiaomi_laurel_sprout
- **Dumps**: https://github.com/catrielmuller/xiaomi_laurel_sprout_dump

### Kupfer Reference (Google Pixel 3a - SDM670)
- **Link**: https://kupfer.gitlab.io/devices/dev/sdm670-google-sargo.html
- **Similitudes**: SDM670 es primo cercano de SDM439, similar arquitectura

### PostmarketOS Wiki
- **Mi A3 (laurel_sprout)**: https://wiki.postmarketos.org/wiki/Xiaomi_Mi_A3_%28xiaomi-laurel%29

---

## 📊 Estimación de Esfuerzo

| Fase | Duración | Complejidad | Status |
|------|----------|-----------|--------|
| **1. Investigación** | 1 día | Alta | ✅ HECHA |
| **2. Kernel & DTB** | 3-5 días | Alta | ⏳ PRÓXIMA |
| **3. Build System** | 2-3 días | Media | ⏳ |
| **4. Compilación** | 2-3 días | Alta | ⏳ |
| **5. Hardware** | 1-2 sem | Muy Alta | ⏳ |
| **6. Docs** | Continuo | Baja | ⏳ |

**Total estimado**: 2-3 semanas para primer boot | 4-6 semanas para funcional

---

## ✅ Conclusión de Fase 1

**Completado**:
- ✓ Kernel completo extraído y analizado
- ✓ Device Tree completo extraído  
- ✓ Ramdisk descomprimido
- ✓ Hardware identificado (SDM439/trinket-qrd)
- ✓ Herramientas instaladas
- ✓ Documentación técnica completa
- ✓ Referencias y comparaciones establecidas

**Capacidad**: La información técnica disponible es suficiente para proceder sin conectar el dispositivo físico hasta fase 4 (compilación/testing).

**Riesgo**: Bajo. Bootloader es reversible, dispositivo A/B permite recuperación.

---

## 📝 Notas

- **Contraseña Arch Linux**: `240223` (para comandos sudo)
- **adb está disponible en**: `/opt/android-sdk/platform-tools/adb`
- **Fuente: LineageOS Nightly** de Feb 24, 2026 (versión muy reciente)
- **Dispositivo actual**: LineageOS 23.0, Android 16, root disponible

---

**Proyecto iniciado**: 21 de Abril de 2026  
**Actualizado**: 21 de Abril de 2026  
**Fase**: 1 - Investigación (✅ COMPLETADA)

