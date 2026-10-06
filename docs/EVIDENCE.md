# Evidencias y procedencia

## Material original

- Configuración de los cuatro perfiles y confirmación posterior de contexto 65.536, orden CUDA1,CUDA0 y reparto 70/30.
- Prompts de prefill, generación, código y agentic recuperados del texto de las pruebas. El problema de rutas se transcribe en un archivo legible conservando datos y restricciones.
- Diez tests históricos de `rebuild_sessions`, conservados en `tests/coding/original-tests.py`.
- Proyecto agentic inicial y versiones finales de Qwen y Nemotron, conservados como carpetas completas.
- Capturas finales de los seis vídeos de razonamiento y velocidad, sin modificar, en `assets/evidence/`.

| Captura | Prueba |
|---|---|
| 03-44-55.png | Razonamiento Qwen |
| 03-49-35.png | Razonamiento Nemotron |
| 04-09-10.png | Prefill Qwen |
| 04-11-31.png | Prefill Nemotron |
| 04-15-49.png | Generación Qwen |
| 04-13-53.png | Generación Nemotron |

Los vídeos completos permanecen fuera del repositorio. Sus nombres de sesión se usan para identificar las capturas, sin publicar rutas personales.

## Código histórico y posterior

La función histórica de Nemotron fue transcrita de la grabación; se conserva la lógica de la función y se omite el envoltorio de demostración. Ejecutada con los tests originales reproduce 1/10. La respuesta histórica completa de Qwen no está disponible entre los archivos conservados: su 9/10 y el fallo de orden se mantienen como resultado documentado de la ejecución, sin sustituirla por una función inventada.

`tests/coding/rerun/` contiene soluciones posteriores y su batería. Ambas pasan 10/10. El prompt de esa repetición está en `tests/coding/PROMPT.txt`; no sustituye al prompt original. Las diferencias de procedencia impiden tratar esos archivos como evidencia de la primera respuesta.

## Agentic

El proyecto inicial produce tres fallos en doce tests. Los finales producen doce aprobados y conservan los tests originales. Los cambios funcionales se encuentran en `src/memory.js` y `src/planner.js`. El archivo auxiliar de depuración de Nemotron no está entre los archivos finales y no se reconstruye.

## Límites de reproducción histórica

No se conservaron revisiones o hashes de los pesos del día de la prueba, versiones exactas del entorno, semillas, respuestas completas de todas las pruebas ni configuración íntegra de Hermes. La plantilla permite repetir el protocolo con los ajustes documentados; no garantiza recrear exactamente cada token del histórico.

`results/validation/` registra comprobaciones sobre los archivos incluidos. El manifiesto SHA256 identifica el contenido distribuido, no los modelos originales ni los vídeos.
