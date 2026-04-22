# Checkpoint: Fase 5 - Plan basado en postmarketOS

**Fecha**: 22 Abril 2026
**Estado**: plan corregido y consolidado

## Resumen

- postmarketOS será la fuente de estructura para `deviceinfo`, `modules-initfs` y blobs.
- LineageOS seguirá siendo el baseline funcional de arranque.
- El foco ahora es empaquetar para Kupfer, no recompilar el kernel desde cero.

## Decisión técnica

1. No perseguir una recompilación completa del kernel como primer hito.
2. Traducir la base existente a PKGBUILDs Kupfer.
3. Preparar y probar un `boot.img` mínimo.
4. Iterar sobre firmware y hardware enablement después del primer boot.

## Orden correcto de trabajo

1. Mapear `deviceinfo` de postmarketOS a Kupfer.
2. Ajustar `pkgbuilds/repos.yml` y nombres de paquetes.
3. Empaquetar firmware y configs del dispositivo.
4. Crear `boot.img` de prueba.
5. Flashear, validar logs y corregir.

## Siguiente acción inmediata

Crear el paquete `device` equivalente a postmarketOS y dejar listo el boot de prueba.

## Siguiente paso en la fase de desarrollo

La próxima tarea real es convertir la referencia de postmarketOS en un PKGBUILD de `device` para Kupfer, y usarlo para preparar el primer `boot.img` de prueba.

## Bloqueo actual

- El paquete `firmware-xiaomi-laurel` está solo como esqueleto.
- Aún falta identificar y copiar blobs reales desde el dispositivo o la ROM.
- No hay firmware suficiente todavía para declarar el port listo.
