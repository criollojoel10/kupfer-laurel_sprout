# FASE 2C: Drivers Necesarios para Kupfer en Mi A3

**Timestamp**: 21 de Abril de 2026, 14:50 UTC  
**Objetivo**: Identificar y listar todos los drivers necesarios  
**Dispositivo**: Xiaomi Mi A3 (laurel_sprout) - SDM439 Trinket  

---

## PARTE 1: DRIVERS CRÍTICOS (Requeridos para Boot)

### 1. Clock & Power Management

**GCC (Global Clock Controller)**
- **Archivo**: `drivers/clk/qcom/gcc-trinket.c`
- **Función**: Control de relojes del SoC
- **Crítico**: ✅ SÍ - Sin clock, nada funciona
- **Reutilizable**: ✅ Casi idéntico entre SDM439/SDM670
- **Status**: Disponible en MasterAwesome kernel

**CPUFreq & CPUCC (CPU Clock Controller)**
- **Archivo**: `drivers/clk/qcom/cpucc-trinket.c`
- **Función**: Escalado dinámico de frecuencia CPU
- **Crítico**: ✅ SÍ - Necesario para boot
- **Reutilizable**: ✅ Con cambios mínimos en frequency tables
- **Status**: Disponible

**RPM (Resource Power Manager)**
- **Archivo**: `drivers/soc/qcom/rpm-smd.c`, `drivers/soc/qcom/smem.c`
- **Función**: Power management, state transitions
- **Crítico**: ✅ SÍ
- **Reutilizable**: ✅ Completamente genérico Qualcomm
- **Status**: Disponible en kernel CAF

### 2. PMIC & Regulators (Energía)

**PMIC Driver (PM6125)**
- **Archivo**: `drivers/regulator/qcom-spmi-regulator.c`
- **Función**: Gestión de voltajes (LDO, SMPS, etc.)
- **Crítico**: ✅ SÍ - Sin reguladores, CPU/GPU sin poder
- **Reutilizable**: ✅ Genérico para SPMI, cambiar device tree
- **Config**: Device tree de trinket.dtsi ya extraído
- **Status**: Disponible

**PMI632 (Charger/Battery)**
- **Archivo**: `drivers/power/supply/qcom-*`
- **Función**: Gestión de batería y carga
- **Crítico**: ⚠️ NO para Kupfer (no hay batería real)
- **Reutilizable**: ❌ No necesario
- **Status**: Skip para Kupfer minimalista

### 3. Interrupt & Timer Management

**GIC (ARM Generic Interrupt Controller)**
- **Archivo**: `drivers/irqchip/irq-gic-v3.c`
- **Función**: Manejo de interrupts
- **Crítico**: ✅ SÍ
- **Reutilizable**: ✅ Completamente genérico ARM
- **Status**: En mainline kernel

**ARM64 Timer**
- **Archivo**: `drivers/clocksource/arm_arch_timer.c`
- **Función**: Timer del sistema
- **Crítico**: ✅ SÍ
- **Reutilizable**: ✅ Completamente genérico ARM64
- **Status**: En mainline kernel

---

## PARTE 2: DRIVERS DE ALMACENAMIENTO

### eMMC Controller (SDHCI)

**SDHCI-MSMI (MMC Host Controller)**
- **Archivo**: `drivers/mmc/host/sdhci-msm.c`
- **Función**: Control del almacenamiento eMMC
- **Crítico**: ✅ SÍ - Necesario para rootfs
- **Reutilizable**: ✅ Genérico Qualcomm, funciona igual
- **Status**: Disponible en kernel CAF

**eMMC Device Driver**
- **Archivo**: `drivers/mmc/core/mmc.c`, `drivers/mmc/card/block.c`
- **Función**: Driver de tarjeta eMMC
- **Crítico**: ✅ SÍ
- **Reutilizable**: ✅ Completamente genérico
- **Status**: Mainline kernel

### UFS (si se usa en el futuro)

**UFS Host Controller (UFSHC)**
- **Archivo**: `drivers/scsi/ufs/ufshcd-qcom.c`
- **Función**: Universal Flash Storage (alternativa a eMMC)
- **Crítico**: ❌ NO (Mi A3 usa eMMC, no UFS)
- **Status**: Skip para ahora

---

## PARTE 3: DISPLAY (MDSS/DSI)

### MDSS (Mobile Display SubSystem)

**MDSS Controller**
- **Archivo**: `drivers/gpu/drm/msm/mdss.c`, `drivers/gpu/drm/msm/disp_dpu.c`
- **Función**: Control de display principal
- **Crítico**: ✅ SÍ - Necesario para LCD/OLED
- **Reutilizable**: ✅ Genérico para Qualcomm
- **Config**: Device tree trinket-sde.dtsi ya disponible
- **Status**: Disponible en CAF, reutilizable

**DSI (Display Serial Interface)**
- **Archivo**: `drivers/gpu/drm/msm/dsi/`
- **Función**: Interfaz MIPI DSI con paneles
- **Crítico**: ✅ SÍ - Conecta MDSS con panel
- **Reutilizable**: ✅ Completamente genérico
- **Status**: Disponible

### Panel Drivers

**Truly TD4330 (Principal)**
- **Archivo**: `drivers/gpu/drm/msm/dsi/truly_td4330.c` (aproximado)
- **Función**: Driver específico panel TD4330
- **Crítico**: ✅ SÍ - Panel por defecto
- **Reutilizable**: ✅ Puede adaptarse de MasterAwesome
- **Panel Detection**: GPIO-based o EEPROM
- **Status**: Disponible en device tree de MasterAwesome

**Himax HX83112A (Alternativo)**
- **Archivo**: Similar estructura
- **Función**: Panel alternativo
- **Crítico**: ⚠️ OPCIONAL (detectar dinámicamente)
- **Status**: Disponible si panel coincide

**Novatek NT36672 (Alternativo)**
- **Archivo**: Similar estructura
- **Función**: Panel alternativo
- **Crítico**: ⚠️ OPCIONAL
- **Status**: Disponible si panel coincide

**Simulador (Testing)**
- **Archivo**: Framebuffer virtual `drivers/video/fbdev/vfb.c`
- **Función**: Panel virtual para testing
- **Crítico**: ⚠️ OPTIONAL (fallback)
- **Status**: Disponible en kernel mainline

### DRM/KMS Framework

**DRM Core**
- **Archivo**: `drivers/gpu/drm/drm_core.c`, etc.
- **Función**: Framework de rendering directo
- **Crítico**: ✅ SÍ
- **Reutilizable**: ✅ Completamente genérico
- **Status**: Mainline kernel

**KMS (Kernel Mode Setting)**
- **Archivo**: `drivers/gpu/drm/msm/` KMS implementation
- **Función**: Modo kernel (display modes sin fbdev)
- **Crítico**: ✅ SÍ - Mejor que fbdev
- **Reutilizable**: ✅ Genérico
- **Status**: Disponible

### Backlight

**PWM Backlight**
- **Archivo**: `drivers/video/backlight/pwm_bl.c`
- **Función**: Control de brillo via PWM
- **Crítico**: ⚠️ NO (puede funcionar sin brillo ajustable)
- **Reutilizable**: ✅ Si es necesario
- **Status**: Mainline kernel

**PMIC PWM**
- **Archivo**: `drivers/pwm/pwm-qcom-spmi.c`
- **Función**: PWM integrado en PMIC
- **Crítico**: ⚠️ OPTIONAL
- **Status**: Disponible

---

## PARTE 4: USB

### DWC3 (USB 3.0 Controller)

**DWC3 Core**
- **Archivo**: `drivers/usb/dwc3/core.c`, `drivers/usb/dwc3/gadget.c`
- **Función**: USB host y device modes
- **Crítico**: ✅ SÍ - Necesario para ADB/fastboot
- **Reutilizable**: ✅ Completamente genérico
- **Status**: Mainline kernel

**DWC3 Qualcomm Glue**
- **Archivo**: `drivers/usb/dwc3/dwc3-qcom.c`
- **Función**: Adaptación específica Qualcomm
- **Crítico**: ✅ SÍ
- **Reutilizable**: ✅ Con cambios config device tree
- **Status**: Disponible

### USB PHY

**Qualcomm USB PHY**
- **Archivo**: `drivers/phy/qualcomm/phy-qcom-usb*.c`
- **Función**: USB physical layer
- **Crítico**: ✅ SÍ
- **Reutilizable**: ✅ Genérico
- **Status**: Disponible

---

## PARTE 5: AUDIO

### Audio Subsystem (QDSP6)

**QDSP6 Loader**
- **Archivo**: `drivers/remoteproc/q6v5.c`, `drivers/remoteproc/q6v5-pil.c`
- **Función**: Cargar firmware DSP de audio
- **Crítico**: ⚠️ OPCIONAL (audio no esencial para Kupfer inicial)
- **Reutilizable**: ✅ Genérico Qualcomm
- **Status**: Disponible

### Codec Audio

**WCD938x Codec**
- **Archivo**: `sound/soc/codecs/wcd938x.c`
- **Función**: Codec de audio en PMIC
- **Crítico**: ⚠️ OPCIONAL (para fase inicial)
- **Reutilizable**: ⚠️ Con adaptaciones (diferente de Pixel 3a WCD9335)
- **Firmware**: `/vendor/firmware/wcd938x*`
- **Status**: Disponible en MasterAwesome, pero necesita firmware

**Slimbus Controller**
- **Archivo**: `drivers/slimbus/qcom-ngd-ctrl.c`
- **Función**: Comunicación con codec
- **Crítico**: ⚠️ Si audio es requerido
- **Reutilizable**: ✅ Genérico
- **Status**: Disponible

---

## PARTE 6: INPUT (Touchscreen, Botones)

### Touchscreen

**Touchscreen DSI/I2C**
- **Archivo**: Depende del controlador (Focal, Novatek, etc.)
- **Función**: Input touch
- **Crítico**: ⚠️ OPCIONAL (Kupfer puede usar keyboard de prueba)
- **Status**: Disponible en MasterAwesome device tree

### Buttons (Power, Volume)

**GPIO Keys**
- **Archivo**: `drivers/input/keyboard/gpio_keys.c`
- **Función**: Botones via GPIO
- **Crítico**: ⚠️ OPCIONAL pero RECOMENDADO
- **Reutilizable**: ✅ Completamente genérico
- **Status**: Mainline kernel, config en device tree

---

## PARTE 7: THERMAL MANAGEMENT

### Temperature Sensors

**TSENS (Thermal Sensor)**
- **Archivo**: `drivers/thermal/qcom/tsens*.c`
- **Función**: Leer temperatura del SoC
- **Crítico**: ⚠️ OPTIONAL (monitoring útil, no esencial)
- **Reutilizable**: ✅ Genérico Qualcomm
- **Status**: Disponible

### Thermal Zones

**Thermal Framework**
- **Archivo**: `drivers/thermal/thermal_core.c`
- **Función**: Gestión térmica
- **Crítico**: ⚠️ OPTIONAL para fase 1
- **Reutilizable**: ✅ Genérico
- **Status**: Mainline kernel

---

## PARTE 8: SENSORES (Opcional para fase inicial)

### Accelerometer/Gyroscope
- **Crítico**: ❌ NO para Kupfer CLI
- **Status**: SKIP

### Proximity/Ambient Light
- **Crítico**: ❌ NO para Kupfer
- **Status**: SKIP

### Compass/Magnetometer
- **Crítico**: ❌ NO para Kupfer
- **Status**: SKIP

---

## PARTE 9: PLAN DE COMPILACIÓN

### Fase 1: Drivers Mínimos (Bootable)
```
✅ GCC/CPUCC (clock)
✅ PMIC Regulators (voltaje)
✅ UART Console (serial)
✅ SDHCI (eMMC)
✅ DWC3 USB
❌ Display (usar framebuffer vfb temporal)
❌ Audio
```

### Fase 2: Display (Functionalidad visual)
```
✅ MDSS/DSI
✅ Panel drivers (TD4330, HX83112A, NT36672)
✅ DRM/KMS
✅ Backlight PWM
```

### Fase 3: Input (Interactividad)
```
✅ GPIO Keys
✅ Touchscreen (si panel lo soporta)
```

### Fase 4: Audio (Multimedia)
```
⚠️ QDSP6
⚠️ WCD938x Codec
⚠️ Slimbus
```

### Fase 5: Optional Enhancements
```
⚠️ Thermal zones
⚠️ Camera (si se implementa)
⚠️ Modem (si LTE deseado)
```

---

## PARTE 10: UBICACIÓN EN KERNEL SOURCE

### Rutas en MasterAwesome kernel:

```bash
arch/arm64/boot/dts/qcom/
  ├── trinket.dtsi              # Device tree base
  ├── trinket-sde.dtsi          # Display config
  ├── trinket-wcd.dtsi          # Audio config
  └── trinket-thermal.dtsi      # Thermal config

drivers/clk/qcom/
  ├── gcc-trinket.c             # GCC clock driver
  └── cpucc-trinket.c           # CPU clock driver

drivers/gpu/drm/msm/
  ├── mdss.c
  ├── dsi/                       # DSI interface
  └── dsi/truly_td4330.c        # Panel drivers

drivers/usb/dwc3/
  ├── core.c
  ├── gadget.c
  └── dwc3-qcom.c

sound/soc/qcom/
  └── qdsp6/                     # Audio DSP

drivers/mmc/host/
  └── sdhci-msm.c               # eMMC driver

drivers/soc/qcom/
  ├── rpm-smd.c
  └── smem.c
```

---

## PARTE 11: CONFIGURACIÓN KERNEL (Defconfig)

### Opciones críticas en `.config`:

```
# Clock & Power
CONFIG_COMMON_CLK=y
CONFIG_COMMON_CLK_QCOM=y
CONFIG_QCOM_PM=y
CONFIG_QCOM_RPM_SMD=y
CONFIG_QCOM_SMEM=y

# PMIC
CONFIG_REGULATOR_QCOM_SPMI=y
CONFIG_MFD_SPMI_PMIC=y

# USB
CONFIG_USB=y
CONFIG_USB_GADGET=y
CONFIG_USB_DWC3=y
CONFIG_USB_DWC3_QCOM=y

# MMC/eMMC
CONFIG_MMC=y
CONFIG_MMC_SDHCI=y
CONFIG_MMC_SDHCI_MSM=y

# Display
CONFIG_DRM=y
CONFIG_DRM_MSM=y
CONFIG_DRM_QCOM_DSI=y
CONFIG_BACKLIGHT_PWM=y (optional)

# Thermal
CONFIG_QCOM_TSENS=y

# Input
CONFIG_INPUT_KEYBOARD=y
CONFIG_KEYBOARD_GPIO=y
```

---

## CONCLUSIÓN

**Drivers críticos para boot**: 9  
**Drivers para fase 1 (CLI)**: 13  
**Drivers para fase 2 (Display)**: 8  
**Drivers para fase 3+ (Audio/Sensors)**: 6+  

**Status Total**: ✅ Todos disponibles en MasterAwesome kernel o mainline

**Próximo paso**: FASE 3 - Análisis kernel source y configuración
