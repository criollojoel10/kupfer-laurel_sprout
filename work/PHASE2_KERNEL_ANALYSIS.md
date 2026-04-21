# FASE 2: Análisis de Kernel y Device Tree

**Timestamp**: 21 de Abril de 2026, 13:00 UTC  
**Estado**: EN PROGRESO  
**Dispositivo**: Xiaomi Mi A3 (laurel_sprout, SDM439/Trinket)

## 1. Información del Kernel Actual

### Kernel Build
```
Version: Linux 4.14.356-openela-rc1-perf-g9eacaaff21e8
Compiler: Android Clang 20.0.0
Build Date: Tue Feb 24 05:51:54 UTC 2026
Optimization: LTO + PGO + BOLT
Base: CAF (Code Aurora Forum) msm-4.14
```

### Configuración del Kernel (Líneas Significativas)
```
CONFIG_ARM64=y              # ARMv8 64-bit
CONFIG_SMP=y                # Soporte multi-core
CONFIG_SWIOTLB=y            # Software I/O TLB (IOMMU)
CONFIG_KERNEL_MODE_NEON=y   # NEON SIMD instructions
CONFIG_LOCALVERSION="-perf" # Version string
CONFIG_AUDIT=y              # Auditing support
CONFIG_SPARSE_IRQ=y         # Sparse IRQ layout
CONFIG_NO_HZ_IDLE=y         # Tickless (dynticks)
CONFIG_HIGH_RES_TIMERS=y    # HR timers support
```

### Parámetros del Bootloader (Extraído del Boot.img)
```
console=ttyMSM0           # Debug console UART
video=vfb:640x400         # Framebuffer virtual 640x400
swiotlb=1                 # IOMMU buffer
loop.max_part=7           # Loop device partitions
lpm_levels.sleep_disabled=1  # Sleep levels (power management)
```

## 2. Hardware del Dispositivo (En Vivo)

### Información de CPU (extraída de /proc/cpuinfo)
```
Procesadores: 8 cores ARM Cortex-A53 ARMv8 64-bit
CPU implementer: 0x51 (Qualcomm)
CPU variant: 0xa
CPU part: 0x801 (Cortex-A53) y 0x800 (Little cluster)
CPU revision: 4 y 2

Features soportadas:
- fp (Floating Point)
- asimd (NEON SIMD)
- evtstrm (Event Stream)
- aes (AES crypto)
- pmull (PMULL crypto)
- sha1, sha2 (SHA crypto)
- crc32 (CRC checksum)
- cpuid (CPUID)

BogoMIPS: 38.40 (por core)
```

### SoC: Snapdragon 439 (SM6125/Trinket)
```
Nombre interno: TRINKET
Arquitectura: ARMv8 64-bit (4 Cortex-A53 @ 2.2 GHz + 4 @ menor freq)
GPU: Adreno 505
IOMMU: IOMMU (Software TLB via swiotlb)
```

### Memoria del Sistema
```
Total: 3.5 GB LPDDR4X
Libre: 175 MB (actualmente)
Disponible: 1.7 GB (con cache)
CMA (Contiguous Memory Allocator): 221 MB (actualmente 0 libre)
Swap: 3 GB
```

### Almacenamiento
```
Dispositivo: /dev/sda (eMMC 5.1)
Tamaño total: 120 GB
Particiones principales (extraídas de /proc/partitions):
- sda1-15: Múltiples particiones
- sde (4 GB): UFS controller
- sdc: UFS metadata

Punto de montaje observado:
- /data: 108 GB (2.1 GB usado)
- /vendor: 992 MB (612 MB usado)
- /system/product: Montado vía dm-crypt/dm-verity
```

## 3. Subsistema de Interrupts y Dispositivos

### Interrupts Principales
```
IRQ 2 (mpm):        1198/440/616... (arch_timer/system clock)
IRQ 5 (arch_timer): 68549/69938... (Timer de arquitectura)
IRQ 7 (mem_timer):  22678/15386... (Memory timer)
IRQ 13 (UFS):       30494/11777... (Almacenamiento)
IRQ 50 (SD):        1976 (microSD)
IRQ 51 (SDHCI):     310 (SD controller)
IRQ 52-67 (Modem/Radio): IPA, GSI, ADC, sensors
```

### Controladores Detectados
```
- mpm-gic: MPM GIC interrupt controller
- arm-pmu: Performance Monitoring Unit
- tsens: Thermal sensor (temp monitoring)
- glink-native: QCom Glink IPC
- smp2p: Shared Memory Point-to-Point IPC
- ufshc: Universal Flash Storage Host Controller
- sdhci: Secure Digital Host Controller
- pmic_arb: PMIC arbitrator (PM6125)
- modem/adsp/cdsp: DSP cores (Modem, Audio DSP, Compute DSP)
```

## 4. Device Tree Structure (En /sys/firmware/devicetree)

### Componentes Identificados
```
/energy-costs/          - CPU energy model (big.LITTLE)
/soc/qcom,rpm-smd/      - RPM (Resource Power Manager)
  - rpm-regulator-*     - Voltage regulators (LDO, SMPS)
    - regulator-l7      - LDO 7 (ejemplo)
    - regulator-l17     - LDO 17
```

### Reguladores de Voltaje Detectados
```
LDO 7:  min=1200 µV, max=1200 µV (FIXED)
LDO 17: min=? µV, max=? µV
SMPS (múltiples):configuradas por RPM
```

## 5. Servicios Android Relacionados (Kernel)

### Drivers/Servicios de Hardware
```
Detectados en dmesg:
- CCI (Camera Control Interface): hw_version = 0x10060000
- Sensores de cámara:
  - laurus_sunny_imx586 (principal)
  - laurus_imx586_sunny
  - laurus_ov02a10_sunny (secundaria)
  - laurus_s5kgd1_sunny
  - laurus_s5k4h7
- thermal-engine: Motor de gestión térmica
- DPM: Dynamic Power Management
- media subsystem: Audio/video HAL
- wificond: WiFi condition daemon
```

## 6. Análisis Comparativo: SDM439 vs SDM670 (Pixel 3a)

### Similitudes
```
✓ Ambos usa CAF (Code Aurora Forum) kernel base
✓ Soporte IOMMU (swiotlb)
✓ Ambos ARMv8 64-bit
✓ MDSS para display
✓ Audio DSP (adsp)
✓ Modem Qualcomm
```

### Diferencias
```
SDM670 (Pixel 3a): 8x Cortex-A75 @ 2.8 GHz (más potente)
SDM439: 8x Cortex-A53 @ 2.2 GHz (más modesto)

SDM670: Adreno 616
SDM439: Adreno 505

SDM670: Kernel más reciente típicamente
SDM439: Kernel 4.14 (estable pero más antiguo)
```

### Estrategia de Portabilidad
```
⚠️ Muchos drivers serán reutilizables
⚠️ Device tree será significativamente diferente
⚠️ Reguladores de voltaje: PM6125 vs PM845
⚠️ Configuración de frecuencias: será diferente
```

## 7. Problemas Identificados para Kupfer

### CRÍTICO: Kernel Base
```
Problema: Kernel 4.14 es bastante antiguo (stable desde 2021)
Impacto: Falta de drivers modernos, parches de seguridad limitados
Solución: 
  - Usar CAF patches para SDM439
  - Backport critical drivers desde kernels más nuevos
  - Verificar soporte en mainline kernel
```

### CRÍTICO: Display (MDSS)
```
5 paneles detectados:
  1. Truly TD4330 (command mode + video mode)
  2. HX83112A
  3. NT36672
  4. Simulator
  5. [Posible 5to panel]

Desafío: Detectar dinámicamente qué panel está instalado
Solución: Implementar panel detection en Device Tree
```

### CRÍTICO: Audio (WCD938x)
```
Codec: WCD938x en PMIC PM6125
Interfaz: I2S/TDM
Desafío: Requiere driver ASoC específico
Solución: Usar CAF ASoC drivers o mainline wcd938x
```

### CRÍTICO: Modem/Cellular
```
Detectado: Modem Qualcomm
Interfaz: QMI, IPA (Internet Packet Accelerator)
Desafío: Blobs propietarios necesarios
Solución: Extraer de imagen LineageOS actual
```

### CRÍTICO: Thermal Management
```
Detectado: tsens (Thermal Sensor), thermal-engine
Desafío: Configuración específica de TZ (Thermal Zones)
Solución: Extraer del device tree actual
```

## 8. Próximos Pasos para Fase 2

### 8.1 Extracción de Fuentes
```
TODO:
- [ ] Clonar kernel: https://github.com/MasterAwesome/android_kernel_xiaomi_laurel_sprout
- [ ] Clonar device tree: https://github.com/MasterAwesome/android_device_xiaomi_laurel_sprout
- [ ] Extraer vendor blobs (si es necesario)
- [ ] Analizar defconfig y fragments
```

### 8.2 Análisis de Device Tree
```
TODO:
- [ ] Comparar .dts con Pixel 3a reference
- [ ] Mapear reguladores de voltaje
- [ ] Identificar clock sources
- [ ] Documentar panel detection
```

### 8.3 Identificación de Drivers Necesarios
```
TODO:
- [ ] Display: MDSS + DSI panels
- [ ] Audio: ASoC + WCD938x codec
- [ ] Input: Touchscreen, buttons
- [ ] Sensors: Accelerometer, gyro, proximity, etc.
- [ ] Modem: QCom modem driver
- [ ] Networking: WiFi, Bluetooth, USB
```

### 8.4 Preparación para Kupfer
```
TODO:
- [ ] Crear device definition para Kupfer
- [ ] Preparar toolchain ARM 64-bit
- [ ] Estudiar proceso de compilación de Kupfer
- [ ] Crear estructura de archivos de configuración
```

## Referencias

- [PostmarketOS Xiaomi Mi A3](https://wiki.postmarketos.org/wiki/Xiaomi_Mi_A3_%28xiaomi-laurel%29)
- [MasterAwesome kernel](https://github.com/MasterAwesome/android_kernel_xiaomi_laurel_sprout)
- [MasterAwesome device tree](https://github.com/MasterAwesome/android_device_xiaomi_laurel_sprout)
- CAF (Code Aurora Forum) msm-4.14 documentation
- Qualcomm Trinket SDM439 datasheets

---

**Estado**: Documento en construcción mientras se investigan fuentes adicionales.  
**Siguiente revisión**: Después de analizar kernel source y device tree de MasterAwesome.
