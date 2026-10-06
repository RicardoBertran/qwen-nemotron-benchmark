# Comprobaciones de los archivos

Verificación del 6 de octubre de 2026 con Python 3.14.6 y Node.js 24.19.0. Estos registros ejecutan código conservado; no ejecutan los modelos ni vuelven a medir su velocidad.

| Registro | Resultado esperado y comprobado |
|---|---|
| reasoning.txt | Óptimo único 28, 120 permutaciones |
| coding-historical-nemotron.txt | 1/10 con la batería original |
| qwen-rerun.txt | 10/10 en la repetición posterior |
| nemotron-rerun.txt | 10/10 en la repetición posterior |
| nemotron-recovered.txt | 1/10 del código histórico con la batería posterior |
| agentic-original.txt | 9/12; tres fallos intencionados del proyecto inicial |
| agentic-qwen.txt | 12/12 |
| agentic-nemotron.txt | 12/12 |

Los archivos `.diff` muestran las diferencias entre el proyecto inicial y cada versión final. Los tests finales son idénticos a los iniciales. Las duraciones de estos logs pertenecen a esta comprobación local y no al benchmark de los modelos.

También se comprobaron la sintaxis de los scripts de PowerShell, la generación del INI con rutas que contienen espacios, los cuatro perfiles, los JSON y los enlaces internos. Las opciones del lanzador se contrastaron con la ayuda de llama-server b11146; esa comprobación no identifica la versión usada en las grabaciones.

`SHA256.json` identifica los archivos distribuidos, excepto el propio manifiesto y los metadatos de Git.
