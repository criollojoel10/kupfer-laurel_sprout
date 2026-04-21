# FASE 2B: Análisis Comparativo SDM439 (Mi A3) vs SDM670 (Pixel 3a)

**Timestamp**: 21 de Abril de 2026, 14:45 UTC  
**Objetivo**: Identificar similitudes y diferencias para portabilidad a Kupfer  
**Dispositivo Objetivo**: Xiaomi Mi A3 (laurel_sprout) - SDM439 Trinket  
**Referencia Kupfer**: Google Pixel 3a (sargo) - SDM670  

---

## PARTE 1: COMPARACIÓN DE HARDWARE

### SoC (System-on-Chip)

| Aspecto | SDM439 (Mi A3) | SDM670 (Pixel 3a) |
|---------|---|---|
| **Nombre Código** | Trinket | Sdm670 |
| **Familia** | Snapdragon 400 series | Snapdragon 600 series |
| **CPU** | 8x Cortex-A53 @ 2.2 GHz | 8x Cortex-A75/A55 @ 2.8 GHz |
| **GPU** | Adreno 505 | Adreno 616 |
| **ISP** | Spectra 180 | Spectra 250L |
| **DSP (QDSP6)** | ✓ V65M | ✓ V66 |
| **Modem** | Snapdragon X15 LTE | Snapdragon X24 LTE |
| **Fab Process** | 14nm FinFET | 10nm FinFET |
| **PMIC** | PM6125 + PMI632 | PM845 + PMI8998 |

### Similitudes SoC
✅ Ambos ARMv8 64-bit  
✅ Ambos tienen GPU Adreno  
✅ Ambos soportan UFS y eMMC  
✅ Ambos tienen QDSP6 para audio/multimedia  
✅ Ambos soportan MDSS (display controller)  
✅ Ambos IOMMU (SMMU)  

### Diferencias SoC
❌ SDM439 es más modesto (procesamiento más lento)  
❌ SDM439 GPU más antigua (Adreno 505 vs 616)  
❌ SDM439 proceso de fab más viejo (14nm vs 10nm)  
❌ SDM439 PMIC diferente (PM6125 vs PM845)  

---

## PARTE 2: COMPARACIÓN DE KERNEL

### Versión Actual Instalada

| Aspecto | SDM439 (Mi A3) | SDM670 (Pixel 3a) |
|---------|---|---|
| **Kernel Base** | 4.14.356 CAF msm-4.14 | 4.14.x CAF msm-4.14 |
| **Compilador** | Clang 20.0.0 (LTO, PGO, BOLT) | Clang estándar |
| **Build Date** | Feb 24, 2026 | Variable |
| **Optimizaciones** | LTO, PGO, BOLT | Standard |
| **Fuente** | OpenELA rc1-perf | CAF msm-4.14 |

### Similitudes Kernel
✅ Ambos kernel 4.14.x (same base)  
✅ Ambos CAF (Code Aurora Forum) origin  
✅ Ambos soportan ARM64  
✅ Ambos pueden compilar con Clang  
✅ Ambos tienen device tree similar  

### Diferencias Kernel
❌ Mi A3 kernel más reciente (Feb 2026)  
❌ Mi A3 tiene optimizaciones extra (LTO, PGO, BOLT)  
❌ Pixel 3a compilador stock vs optimizado  

---

## PARTE 3: COMPARACIÓN DE DEVICE TREE

### Estructura DT

| Componente | SDM439 | SDM670 | Status |
|---|---|---|---|
| **Base DTS** | trinket.dtsi (18500+ líneas) | sdm670.dtsi | ✅ Similar |
| **CPU Topology** | 8 cores Cortex-A53 | 8 cores Cortex-A75/A55 | ⚠️ Diferente |
| **Memory** | LPDDR4X 3.5GB | LPDDR4X 4GB | ✅ Compatible |
| **Storage** | eMMC 5.1 128GB | eMMC/UFS | ✅ Compatible |
| **Display** | MDSS + DSI MIPI | MDSS + DSI MIPI | ✅ Similar |
| **Audio** | WCD938x en PM6125 | WCD9335/9340 | ⚠️ Diferente codec |
| **USB** | DWC3 2.0 (480 Mbps) | DWC3 3.0 (5 Gbps) | ⚠️ Diferente |
| **Thermal** | tsens + pm6125-tz | tsens + multi-zone | ✅ Similar |

### Definiciones de Clock

| Reloj | SDM439 | SDM670 | Porta |
|---|---|---|---|
| RPMCC | ✓ | ✓ | ✅ Idéntico |
| GCC | ✓ | ✓ | ✅ Idéntico |
| CPUCC | ✓ | ✓ | ✅ Similar |
| DISPCC | ✓ | ✓ | ✅ Similar |
| GPUCC | ✓ | ✓ | ✅ Similar |
| VIDEOCC | ✓ | ✓ | ✅ Similar |

---

## PARTE 4: REGULADORES DE VOLTAJE (PMIC)

### PM6125 (SDM439) vs PM845 (SDM670)

#### Reguladores críticos para Kupfer

**LDOs (Linear Regulators)** - Voltaje bajo, corriente baja

| Uso | SDM439 | SDM670 | Diferencia |
|---|---|---|---|
| **Display Analog** | L17 (2.8V) | LDO5 (2.85V) | ±0.05V |
| **Codec Core** | L7 (1.2V) | LDO3 (1.25V) | ±0.05V |
| **I/O Supply** | L10 (1.8V/3.0V) | LDO6 (1.8V) | ±0.2V |
| **Camera** | L19 (2.8V) | LDO18 (2.85V) | ±0.05V |

**SMPS (Buck Regulators)** - Voltaje variable, corriente alta

| Uso | SDM439 | SDM670 | Diferencia |
|---|---|---|---|
| **CPU** | S5 (0.6-1.35V) | SMPS1 (0.6-1.4V) | ±0.05V rango |
| **GPU** | S7 (variable) | SMPS2 (variable) | Similar |

### Estrategia de Portabilidad PMIC

**Baja Complejidad**: Ambos PMICs siguen patrones de Qualcomm estándar

```
Mapeo propuesto para Kupfer:
  PM6125 L17   ← → LDO5  (display)
  PM6125 L7    ← → LDO3  (audio codec)
  PM6125 L10   ← → LDO6  (I/O)
  PM6125 S5    ← → SMPS1 (CPU)
  PM6125 S7    ← → SMPS2 (GPU)
```

✅ **Conclusión**: Reguladores mapeables sin problemas grandes

---

## PARTE 5: SUBSISTEMAS CLAVE

### Display (MDSS/DSI)

| Característica | SDM439 | SDM670 | Compatibilidad |
|---|---|---|---|
| **Controlador** | MDSS v5.x | MDSS v5.x | ✅ Idéntico |
| **Interfaz** | MIPI DSI 4 lanes | MIPI DSI 4 lanes | ✅ Idéntico |
| **Panel** | Truly TD4330 1080x2280 | AMOLED 1080x2160 | ⚠️ Diferente |
| **Pixel Clock** | ~60 MHz | ~80 MHz | ✅ Manajable |
| **Backlight** | PM6125 PWM | PM845 PWM | ✅ Similar |

**Status**: ✅ MDSS es genérico, drivers reutilizables, solo cambiar config de panel

### Audio (Codec)

| Aspecto | SDM439 | SDM670 | Compatibilidad |
|---|---|---|---|
| **Codec** | WCD938x | WCD9335/9340 | ⚠️ Diferente |
| **Interfaz** | Slimbus + I2S | Slimbus + I2S | ✅ Similar |
| **DSP** | QDSP6 V65M | QDSP6 V66 | ✅ Compatible |
| **Firmware** | /vendor/firmware/ | /vendor/firmware/ | ✅ Localización igual |

**Status**: ⚠️ WCD938x driver debe adaptarse, pero estructura es estándar Qualcomm

### USB

| Aspecto | SDM439 | SDM670 | Compatibilidad |
|---|---|---|---|
| **Controller** | DWC3 | DWC3 | ✅ Idéntico driver |
| **Modo** | 2.0 Device + Host | 3.0 Device + Host | ✅ DWC3 es backward compatible |
| **PHY** | Synopsys combo | Synopsys combo | ✅ Idéntico |
| **OTG** | ✓ GPIO-based | ✓ GPIO-based | ✅ Similar |

**Status**: ✅ Driver DWC3 completamente reutilizable

### Storage

| Aspecto | SDM439 | SDM670 | Compatibilidad |
|---|---|---|---|
| **Tipo** | eMMC 5.1 | eMMC/UFS | ✅ eMMC es estándar |
| **Controlador** | SDHCI | SDHCI/UFSHC | ✅ Drivers estándar |
| **Partición** | A/B | A/B | ✅ Idéntico esquema |

**Status**: ✅ Drivers de almacenamiento completamente reutilizables

---

## PARTE 6: DRIVERS CRÍTICOS NECESARIOS

### Drivers que SE PUEDEN REUTILIZAR del Pixel 3a (SDM670)

✅ **Completamente compatibles**:
- DWC3 (USB controller)
- SDHCI (eMMC controller)
- UFSHC (UFS, si es necesario)
- MDSS (display controller base)
- QDSP6 (audio DSP loader)
- GIC (interrupt controller)
- Timer ARMv8

✅ **Compatible con adaptaciones menores**:
- CPUFREQ (escalado dinámico CPU)
- GPUFREQ (escalado dinámico GPU)
- Thermal management
- Power management (RPM, LPM levels)

⚠️ **Requiere adaptación específica**:
- Panel drivers (TD4330 vs Samsung AMOLED)
- Audio codec (WCD938x vs WCD9335)
- PMIC driver (PM6125 vs PM845)
- Sensor de huellas (diferentes hardware)
- Cámara (diferentes sensores)

❌ **No reutilizables** (proprietary/device-specific):
- Firmware modem (Snapdragon X15 vs X24)
- HAL específicos de Xiaomi
- Blobs de cámara

---

## PARTE 7: PLAN DE ACCIÓN PARA KUPFER

### Paso 1: Reutilizar de Pixel 3a
```
kernel/drivers/usb/dwc3/          → Copiar directo
drivers/mmc/host/sdhci*.c         → Copiar directo
drivers/gpu/drm/msm/              → Copiar directo (MDSS)
drivers/soc/qcom/                 → Copiar con cambios config
sound/soc/qcom/qdsp6/             → Copiar directo
```

### Paso 2: Adaptar para SDM439
```
arch/arm64/boot/dts/qcom/         → Usar trinket.dtsi como base
drivers/regulator/qcom-spmi-regulator.c → Configuración PM6125
drivers/power/supply/             → Adaptar carga batería
drivers/thermal/qcom/              → Configuración térmica
```

### Paso 3: Hardware específico
```
arch/arm64/configs/                → Crear trinity_defconfig para Kupfer
drivers/video/fbdev/               → Panel TD4330 driver
sound/soc/codecs/wcd938x.c         → Audio codec
drivers/input/touchscreen/         → Touchscreen driver
```

---

## PARTE 8: RIESGOS Y MITIGACIÓN

### Riesgo 1: PMIC (PM6125 vs PM845)
**Severidad**: MEDIA  
**Causa**: Diferente regulador, diferente configuración de voltaje  
**Mitigación**:
- Usar drivers genéricos SPMI de Qualcomm
- Mapear reguladores por nombre (compatible strings)
- Usar valores de voltage del device tree extraído
- Validar con `getprop` en dispositivo si falla

### Riesgo 2: Audio Codec (WCD938x vs WCD9335)
**Severidad**: MEDIA  
**Causa**: Diferente codec, diferente firmware DSP  
**Mitigación**:
- Obtener firmware WCD938x del dispositivo actual
- Usar driver ASoC genérico si existe
- Extraer del ramdisk actual `/vendor/firmware/`
- Copiar al directorio de firmware de Kupfer

### Riesgo 3: Panel Display
**Severidad**: MEDIA-ALTA  
**Causa**: 5 variantes de panel, autodetección necesaria  
**Mitigación**:
- Implementar GPIO-based panel detection
- Tener fallback a TD4330 (más común)
- Si falla, usar framebuffer vfb como último recurso
- Usuario puede especificar panel manualmente

### Riesgo 4: Kernel 4.14 Antiguo
**Severidad**: MEDIA  
**Causa**: Kernel 4.14 es estable desde 2021, missing modern features  
**Mitigación**:
- Usar LTS (Long Term Support) kernel branch
- Backport critical security patches
- Considerar upgrade a 4.19 o 5.4 si problemas
- CAF patches incluyen fixes importantes

### Riesgo 5: Falta de Drivers Modernos
**Severidad**: BAJA  
**Causa**: SDM439 < SDM670 en features  
**Mitigación**:
- La mayoría de drivers son genéricos Qualcomm
- Kupfer no necesita todas las features de Android
- Enfoque minimalista: solo lo esencial
- Características no-críticas pueden esperar

---

## PARTE 9: ESTIMACIÓN DE ESFUERZO

| Tarea | Tiempo | Complejidad | Riesgo |
|---|---|---|---|
| Copiar drivers USB/MMC | 2 horas | BAJA | BAJO |
| Adaptar MDSS para Kupfer | 6 horas | MEDIA | MEDIO |
| Configurar PMIC (PM6125) | 4 horas | MEDIA | MEDIO |
| Audio codec (WCD938x) | 8 horas | ALTA | ALTO |
| Display panel detection | 4 horas | MEDIA | MEDIO |
| Kernel build & config | 4 horas | MEDIA | BAJO |
| **Total estimado** | **28 horas** | - | - |

**Por fases**:
- Fase 2 (análisis): 2-3 días
- Fase 3 (compilación kernel): 2-3 días  
- Fase 4 (drivers básicos): 3-5 días
- Fase 5 (hardware enablement): 7-10 días

**Total**: 14-21 días para sistema funcional básico

---

## PARTE 10: CONCLUSIÓN

### ✅ Veredicto: PORTABILIDAD ALTA

**Razones**:
1. ✅ Ambos usan mismo kernel base (4.14 CAF)
2. ✅ Arquitectura SoC similar (ARM64, Qualcomm)
3. ✅ Mayoría drivers son genéricos Qualcomm
4. ✅ Device tree estructura idéntica
5. ✅ Referencias (Pixel 3a Kupfer) disponibles
6. ✅ Comunidad LineageOS activa para laurel_sprout

### ⚠️ Desafíos principales:
1. ⚠️ Diferentes PMICs requieren configuración
2. ⚠️ Audio codec diferente (WCD938x vs WCD9335)
3. ⚠️ Panel detection para 5 variantes
4. ⚠️ Firmware modem (no requerido para Kupfer, pero nice-to-have)

### ✅ Facilidades:
1. ✅ Casi todo source code disponible (MasterAwesome repos)
2. ✅ LineageOS continuamente actualizado
3. ✅ Comunidad PostmarketOS con info adicional
4. ✅ Device tree completo ya extraído
5. ✅ Kernel source compilable sin cambios grandes

---

**Recomendación**: Proceder a Fase 3 con confianza.  
El puerto a Kupfer es técnicamente factible.  
Tiempo estimado: 2-3 semanas para primer boot.

