# Contributing to Kupfer Xiaomi Mi A3 Port

¡Gracias por interesarte en portar Kupfer a Xiaomi Mi A3!

## Visión del Proyecto

**Objetivo**: Lograr que **Kupfer (Arch Linux ARM)** sea un dispositivo oficial soportado en el Xiaomi Mi A3 (laurel_sprout).

**Estado Actual**: Fase 1 - Investigación completada ✅

## Cómo Contribuir

### 1. Reportar Problemas
- Usa GitHub Issues con etiquetas apropiadas
- Describe el problema en detalle
- Incluye logs de compilación si es aplicable
- Etiquetas: `bug`, `hardware`, `driver`, `docs`

### 2. Mejoras a Documentación
- Corrige errores de tipografía/ortografía
- Aclara instrucciones confusas
- Añade diagramas o ejemplos
- Traduce a otros idiomas

### 3. Desarrollo de Kernel/Drivers
- Coordina en GitHub Discussions antes de empezar
- Crea una rama (branch) descriptiva
- Haz commits pequeños y atómicos
- Incluye descripción detallada de cambios

### 4. Experiencias con Hardware
- Documenta problemas específicos de tu dispositivo
- Proporciona logs de kernel (dmesg)
- Reporta funcionamiento parcial de hardware
- Incluye versión exacta del dispositivo (ej. revisión PCB)

## Estructura de Ramas

```
main/master
├── develop (rama principal de desarrollo)
├── feature/kernel-compilation
├── feature/display-support
├── feature/audio-support
├── bugfix/thermal-management
└── docs/spanish-translation
```

## Proceso de Pull Request

1. **Fork el repositorio**
2. **Crea una rama** desde `develop`: `git checkout -b feature/mi-feature`
3. **Haz cambios** con commits descriptivos
4. **Pushea a tu fork**: `git push origin feature/mi-feature`
5. **Crea PR** a `develop` con descripción clara
6. **Responde reviews** y actualiza según feedback

## Convenciones de Código

### Commits
```
type(scope): subject

body (explicación detallada)

Fixes #123
Co-authored-by: Name <email>
```

**Tipos**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Ramas
```
type/short-description
feature/display-mipi-dsi
bugfix/thermal-hang
docs/kernel-building
```

## Fases del Proyecto

### ✅ Fase 1: Investigación (COMPLETADA)
- [x] Extracción de boot.img, dtbo.img, vbmeta.img
- [x] Análisis de kernel y device tree
- [x] Identificación de hardware (SDM439)
- [x] Documentación técnica inicial

### ⏳ Fase 2: Análisis de Kernel & Device Tree (PRÓXIMA)
- [ ] Clonar repositorios LineageOS
- [ ] Comparar con Pixel 3a (SDM670/Kupfer)
- [ ] Identificar drivers SDM439
- [ ] Preparar build configuration

### ⏳ Fase 3: Repositorio GitHub Público
- [ ] Setup de issues y wiki
- [ ] Documentación de colaboración
- [ ] Contacto con comunidad Kupfer

### ⏳ Fase 4: Primera Compilación
- [ ] Kernel minimalista
- [ ] Ramdisk Arch Linux
- [ ] Testing en dispositivo
- [ ] Debug de arranque

### ⏳ Fase 5: Hardware Enablement
- [ ] Display (MDSS/DSI)
- [ ] Input (touchscreen)
- [ ] Audio (WCD938x)
- [ ] Networking (USB/Wifi)

## Recursos Técnicos

### Documentación Local
- `README.md` - Índice general
- `work/TECHNICAL_SPECIFICATION.md` - Especificación hardware
- `work/RESUMEN_EJECUTIVO.md` - Estado del proyecto
- `work/ANALYSIS.md` - Análisis arquitectónico

### Repositorios Relacionados
- **LineageOS Kernel**: https://github.com/MasterAwesome/android_kernel_xiaomi_laurel_sprout
- **Device Tree**: https://github.com/MasterAwesome/android_device_xiaomi_laurel_sprout
- **Kupfer Pixel 3a**: https://kupfer.gitlab.io/devices/dev/sdm670-google-sargo.html
- **PostmarketOS Wiki**: https://wiki.postmarketos.org/wiki/Xiaomi_Mi_A3_%28xiaomi-laurel%29

### Herramientas Necesarias
- adb (Android Debug Bridge)
- fastboot
- arm-linux-gnueabihf-gcc (compilación ARM)
- device-tree-compiler (DTB compilation)

## Contacto

- **GitHub Issues**: Para bugs y features
- **GitHub Discussions**: Para preguntas y brainstorming
- **GitHub Wiki**: Para documentación ampliada
- **Kupfer Matrix/Discord**: Para coordinación con upstream

## Licencia

Este proyecto está bajo licencia GNU General Public License v3.0 (GPLv3).
Ver `LICENSE` para más detalles.

---

**¡Gracias por contribuir a llevar Linux oficial a Xiaomi Mi A3!** 🎉
