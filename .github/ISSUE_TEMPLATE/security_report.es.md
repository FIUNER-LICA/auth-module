---
name: "[ES] Reporte de Seguridad"
about: Reportar una vulnerabilidad o aspecto de seguridad en la biblioteca
title: "[SECURITY]: "
labels: ["security"]
assignees: ""
---

## Aviso de Divulgación Responsable
Si la vulnerabilidad descubierta es crítica y puede comprometer sistemas en producción de forma activa, evalúe informar a los mantenedores por un canal privado antes de hacer pública una prueba de concepto explotable.

## Descripción de la Vulnerabilidad
Descripción clara y concisa de la debilidad de seguridad detectada (ej. vectores de ataque, derivación de autorización, exposición indebida de datos, etc.).

## Componente Afectado
- Módulo / Clase / Ruta: [ej. core/security, flask_ext/routes.py, MailDispatcher]
- Versiones Afectadas: [ej. todas las versiones <= 1.2.0]

## Nivel de Severidad Estimado
- [ ] Crítica (RCE, bypass completo de autenticación)
- [ ] Alta (Escalación de privilegios, exposición masiva de credenciales)
- [ ] Media (Enumeración de usuarios, ausencia de protección CSRF en acciones secundarias)
- [ ] Baja (Inconsistencia menor sin impacto directo de explotación)

## Prueba de Concepto (PoC) / Pasos para Reproducir
Describa los pasos técnicos para evidenciar la vulnerabilidad en un entorno controlado:
1. Configuración de prueba...
2. Petición o ejecución específica...
3. Resultado o impacto observado...

## Impacto Potencial
¿Qué podría lograr un atacante si explota esta vulnerabilidad?

## Mitigación o Corrección Propuesta
Sugerencias técnicas para solucionar o mitigar el problema (parches de código, cabeceras HTTP, validaciones adicionales, etc.).
