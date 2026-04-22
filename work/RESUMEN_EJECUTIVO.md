# Resumen Ejecutivo: Puerto de Kupfer para Xiaomi Mi A3

## Estado

- Hardware verificado: `laurel_sprout`, `SM6125 / Trinket`
- Kernel verificado: `4.14.356-openela-rc1-perf`
- Bootloader y root: disponibles

## Plan correcto

1. Usar postmarketOS como fuente de la capa device.
2. Mantener LineageOS como baseline de boot.
3. Crear PKGBUILDs para `device` y `firmware`.
4. Construir y probar un `boot.img` mínimo.

## Siguiente paso

Empaquetar el primer `device` Kupfer a partir de la referencia postmarketOS.
