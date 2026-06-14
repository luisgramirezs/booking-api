# NOTAS - Transparencia y Proceso de Desarrollo con IA

De acuerdo con las directrices específicas de la guía de postulación, se detalla de forma transparente cómo se integraron las herramientas de Inteligencia Artificial (IA) en el ciclo de desarrollo de este proyecto:

#Metodología de Trabajo: Programación en Pareja (Pair Programming)
La Inteligencia Artificial no se utilizó como un generador automático de código a ciegas, sino como un **consultor técnico de soporte y validación de sintaxis en tiempo real**. El flujo de trabajo se basó en el diseño manual de las reglas de negocio basadas en los requerimientos, seguido de un proceso de debate y optimización con la IA para asegurar las mejores prácticas del lenguaje.

#Partes Desarrolladas y Ajustadas en Consenso

1. **Diseño y Estructura de Entidades**:
   - Se plantearon manualmente los atributos necesarios para el negocio (`id_cliente`, `total_pagado`, `monto_reembolso`).
   - Se consultó con la IA la implementación correcta en **Pydantic V2** para forzar el tipado estático nativo de Python (`date`, `time`, `EmailStr`), asegurando que el motor de FastAPI realizara el parseo sintáctico de forma automática en la puerta de entrada.

2. **Auditoría del Generador de Semillas (`seed.json`)**:
   - Durante la construcción del script de automatización de datos, se debatió activamente la ubicación de la regla de validación de las 3 reservas máximas. 
   - El diseño original presentaba problemas de alcance (*scope*) y ciclos infinitos. A través de la consultoría con la IA, se reestructuró la jerarquía de los bucles `while True` e `if not solapamiento`, logrando un algoritmo de generación 100% consistente y relacional.

3. **Manejo de Tiempos y Lógica de Negocio (Horarios y Anticipación)**:
   - Se diseñó la lógica para calcular la `hora_fin` de manera automática a partir de la duración del servicio del catálogo comercial.
   - Al intentar restar horas directamente sobre objetos `time` estáticos, Python arrojaba errores de tipo (`TypeError`). Se utilizó la IA para confirmar la sintaxis de conversión obligatoria mediante la combinación con `datetime.combine` y el uso de bloques `timedelta`, logrando que las tres validaciones horarias compilaran sin redundancias de memoria en la CPU.

4. **Optimización y Eliminación de Grasa**:
   - Tras proponer soluciones iniciales con variables intermedias para los cálculos de tiempos y porcentajes de reembolsos, se evaluó junto con la IA la manera de simplificar las funciones siguiendo el principio *KISS (Keep It Simple, Stupid)*. 
   - Se eliminaron asignaciones redundantes inyectando los métodos del sistema directo en los argumentos de los esquemas, optimizando la legibilidad general del código fuente para su posterior mantenimiento.

#Conclusión del Proceso
Esta interacción permitió auditar cada línea de código de forma defensiva antes de su integración final en la capa de Routers de FastAPI. El entregable final refleja un consenso técnico donde las reglas de negocio de la empresa se cumplen de forma estricta, predecible y bajo una arquitectura limpia de software.


#Luis Guillermo Ramirez 