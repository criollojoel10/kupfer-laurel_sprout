# Kupfer Port Project: Xiaomi Mi A3 (laurel_sprout)

Objetivo: portar Kupfer al Xiaomi Mi A3 usando postmarketOS como fuente de estructura y LineageOS como baseline funcional de arranque.

## Estado actual

- Dispositivo verificado: `laurel_sprout`
- SoC verificado: `SM6125 / Trinket`
- Kernel verificado: `4.14.356-openela-rc1-perf`
- Bootloader: desbloqueado
- ADB/root: funcional

## Fuente de verdad

- `work/DEVICE_VERIFICATION_REPORT.md`
- `work/CHECKPOINT_22_ABRIL_2026_FASE5.md`
- `pkgbuilds/repos.yml`
- postmarketOS `device-xiaomi-laurel`

## Plan correcto

1. Traducir la información de postmarketOS a PKGBUILDs Kupfer.
2. Mantener el kernel actual de LineageOS como baseline para pruebas.
3. Crear paquetes Kupfer para `device`, `firmware` y, si aplica, `boot`/`linux`.
4. Construir un `boot.img` de prueba.
5. Validar boot y luego habilitar hardware por etapas.

## Siguiente paso

Construir el primer paquete `device` alineado con postmarketOS y preparar el `boot.img` de prueba.
