# Metodología e interpretación

Las cuatro secciones separan capacidades distintas: resolver restricciones, procesar y generar texto, escribir código en una respuesta y reparar un proyecto con herramientas.

## Protocolo

1. Carga un solo modelo y verifica el perfil efectivo, contexto y draft.
2. Inicia una conversación nueva y usa el mismo prompt para ambos modelos.
3. En razonamiento y código, evalúa corrección antes de velocidad. No permitas herramientas en la prueba de una respuesta.
4. Para agentic, parte de una copia limpia del mismo proyecto. Mantén tests, herramientas y permisos iguales.
5. Conserva la respuesta completa, métricas y salida de tests; registra intervenciones y errores.

## Qué miden estas ejecuciones

La velocidad procede de la interfaz de llama.cpp; las capturas permiten revisar tasas y cantidades. No se conserva una serie de repeticiones, semillas, calentamiento controlado ni logs completos de cada petición. Los resultados son observaciones individuales, sin intervalos de confianza.

La comparación usa Qwen Q4_K_M con KV q4_0 y Nemotron NVFP4 con KV f16. No aísla arquitectura, cuantización ni efecto de MTP. Tampoco incluye una medición equivalente con MTP apagado. La caché de prompt estaba activada; no hay registro suficiente para cuantificar reutilización de caché entre peticiones.

En prefill el texto es idéntico, pero los tokenizers generan cantidades distintas. En generación extensa las salidas tienen distinta longitud y contenido. Tokens/s no equivale a calidad ni a palabras/s. Los tiempos redondeados de pantalla no deben usarse para reconstruir tasas más precisas que las publicadas.

El contexto de 64K es capacidad configurada, no una prueba de comprensión de 64K. El problema de rutas tiene solo cinco paradas. Diez tests de sesiones y doce tests del proyecto cubren casos concretos, no toda la capacidad de programación.

## Sampling y variación

Las temperaturas utilizadas introducen variación. Repetir el prompt puede cambiar razonamiento, respuesta, tokens, errores e iteraciones. No se puede prometer 9/10 o 12/12 en cada repetición. Para una comparación más robusta, ejecuta varias repeticiones con protocolo y semillas registrados y publica cada resultado, además de la mediana y dispersión de tiempos.

La prueba agentic añade decisiones del cliente, instrucciones del sistema y herramientas. Los tiempos aproximados de grabación incluyen el flujo completo y no son una latencia aislada. Dos modelos pueden alcanzar 12/12 con recorridos diferentes.

## Alcance de la conclusión

Nemotron mostró mayor velocidad; Qwen obtuvo más aciertos en el ejercicio de código de una respuesta y menos iteraciones en el proyecto agentic. Ambas soluciones de ruta fueron correctas. Estas observaciones describen los archivos, perfiles y ejecuciones publicados. No justifican declarar un ganador universal ni atribuir todas las diferencias al modelo base.
