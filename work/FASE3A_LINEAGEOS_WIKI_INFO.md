# FASE 3A: Información LineageOS Wiki - Xiaomi Mi A3

**Timestamp**: 21 de Abril de 2026, 14:55 UTC  
**Fuente**: https://wiki.lineageos.org/devices/laurel_sprout/  
**Status**: Device no longer maintained (pero código disponible)

---

## INFO IMPORTANTE: Especificaciones vs Reportadas

### CORRECCIÓN: GPU
**Wiki reporta**: Adreno 610  
**Dispositivo real**: Adreno 505  
**Kernel actual**: Adreno 505

⚠️ **Nota**: Wiki puede estar desactualizada. Confiar en reportes del dispositivo real.

---

## Especificaciones Técnicas (De Wiki)

### SoC
```
Qualcomm SM6125 Snapdragon 665 (PERO El dispositivo reporta SDM439/Trinket)
CPU: Octa-core Kryo @ 2.0 GHz + 1.8 GHz (asimetric)
GPU: Adreno 610 (reportada), pero real es Adreno 505
Arquitectura: arm64
```

### Memoria
```
RAM: 4/6 GB opciones
Storage: 64/128 GB eMMC
SD Card: Hasta 256 GB microSD
```

### Pantalla
```
6.09" (154.69 mm diagonal)
720x1560 píxeles (282 PPI)
Super AMOLED
Max: 60 Hz refresh rate
Tecnología: AMOLED (NO LCD como pensábamos)
```

⚠️ **CRITICAL NOTE**: Wiki dice AMOLED pero kernel config dice DSI panels. Posible que sea LCD MIPI DSI.

### Conectividad
```
2G: GSM
3G: UMTS
4G: LTE
WiFi: 802.11 a/b/g/n/ac (5 GHz + 2.4 GHz)
Bluetooth: 5.0 con A2DP + aptX HD
USB: OTG soportado
```

### Periféricos
```
✓ 3.5mm jack (audio)
✓ Fingerprint reader (lector de huellas)
✓ IR blaster (control remoto)
✓ Dual SIM
✓ FM radio
✓ A-GPS / GPS / GLONASS
✓ Acelerómetro
✓ Brújula (Compass)
✓ Giroscopio
✓ Barómetro
✓ Sensor de luz
✓ Sensor de proximidad
✓ Podómetro
```

### Cámaras
```
4 cámaras totales:
  1. Principal: 48 MP, Dual LED flash
  2. Ultra ancho: 8 MP, Dual LED flash
  3. Profundidad: 2 MP, Dual LED flash
  4. Frontal: 32 MP, sin flash
```

### Batería
```
Li-Po 4030 mAh
No removible
```

### Dimensiones
```
153.5 mm (altura)
71.9 mm (ancho)
8.5 mm (espesor)
```

---

## Kernel LineageOS

### Versión en Wiki
```
Kernel: 4.14.x LTS
Código fuente disponible: SÍ
```

### Versión Real (Dispositivo)
```
Kernel: 4.14.356-openela-rc1-perf (Febrero 24, 2026)
Compilador: Clang 20.0.0 con LTO, PGO, BOLT
Base: CAF (Code Aurora Forum) msm-4.14
```

---

## Modelos Soportados
```
M1906F9SH (principal)
M1906F9SI (alternativo)
```

### Bootloader Info
```
Bootloader desbloqueado requerido para LineageOS
A/B partitions: SÍ (para OTA updates seguro)
```

---

## Modos de Boot Especiales

### Recovery Mode
```
Botones: Volume Up + Power
Mantener hasta que aparezca logo "Android One"
Luego soltar
```

### Bootloader/Fastboot Mode
```
Botones: Volume Down + Power
Mantener hasta que aparezca "FASTBOOT"
Luego soltar
```

---

## Versiones LineageOS Soportadas

### Anteriormente Soportadas
```
22.2 (Android 15)
23.0 (Android 16) ← Actualmente en dispositivo
```

### Status Actual
⚠️ **"Device is no longer maintained"**

Esto significa:
- No hay compilaciones nightly oficiales más nuevas
- Pero código fuente sigue disponible
- Los desarrolladores pueden hacer compilaciones privadas
- Perfecto para nuestro puerto a Kupfer

---

## Recursos para Desarrolladores

### Dónde obtener ayuda
- Reddit: Comunidad de LineageOS
- Discord: Servidor oficial
- IRC: #LineageOS en Libera.Chat

### Build Guide
- Disponible para desarrolladores en wiki
- Permite compilaciones privadas
- Posibilidad de reiniciar soporte oficial

---

## Implicaciones para Kupfer

### ✅ Ventajas
1. Código fuente completamente disponible (no será removido)
2. No habrá conflictos con compilaciones oficiales
3. Libertad para realizar cambios significativos
4. Comunidad disponible para debugging

### ⚠️ Consideraciones
1. Actualizaciones de kernelLTS tendrán que ser manuales
2. Posibles security patches que necesitan backport
3. No habrá "upstream" oficial, pero Kupfer será upstream

### ✅ Oportunidad
Este es el momento perfecto para portar a Kupfer - dispositivo "abandonado" por LineageOS.
Kupfer podría ser nueva vida para estos dispositivos.

---

## Documentación Extra de Wiki

### Installation
- Requiere bootloader desbloqueado
- Fastboot mode disponible
- Proceso de flash estándar Qualcomm

### Update Procedures
- A/B slots permiten actualización segura
- Rollback disponible si actualización falla

### Build Instructions
- Disponibles en wiki
- Requiere AOSP + LineageOS repos
- Proceso estándar makefile basado

---

## Resumen para Kupfer

**Dispositivo**: Xiaomi Mi A3 (laurel_sprout)
**Status**: No longer officially maintained (perfecto para nosotros)
**Arquitectura**: arm64 (compatible ARM64 totalmente)
**Kernel**: 4.14 LTS (estable, bien soportado)
**Hardware**: Bien documentado en LineageOS

**Conclusión**: Wiki confirma dispositivo es capaz, código está disponible, 
y no hay barreras para puerto a Kupfer.

