# Resultados de referencia

Ejecuciones originales: 5 de octubre de 2026. Comprobación de archivos conservados: 6 de octubre de 2026. Una comprobación local de código guardado no es una nueva generación del modelo.

## Razonamiento

| Métrica | Qwen | Nemotron |
|---|---:|---:|
| Ruta | S-D-B-C-E-A-S | S-D-B-C-E-A-S |
| Distancia | 28 | 28 |
| Tokens generados en la interfaz | 27.665 | 7.225 |
| Tiempo mostrado | 3 min 41 s | 48 s |
| Generación mostrada, tokens/s | 125,04 | 148,25 |

Ambas rutas cumplen las restricciones y alcanzan el óptimo único. El mayor número de tokens de Qwen no mejoró el resultado final en este caso. Capturas: [Qwen](../assets/evidence/03-44-55.png), [Nemotron](../assets/evidence/03-49-35.png).

## Velocidad

| Prefill, mismo texto de entrada | Qwen | Nemotron |
|---|---:|---:|
| Tokens de entrada | 9.625 | 10.554 |
| Tiempo mostrado | 8,3 s | 6,7 s |
| Tokens/s | 1.157,69 | 1.570,92 |
| Tokens generados | 89 | 236 |
| Respuesta visible | LISTO | LISTO |

El texto fue el mismo, mostrado como 42,3 KB en la interfaz. Cada tokenizer produjo una cantidad distinta de tokens. Capturas: [Qwen](../assets/evidence/04-09-10.png), [Nemotron](../assets/evidence/04-11-31.png).

| Generación extensa | Qwen | Nemotron |
|---|---:|---:|
| Tokens generados | 5.275 | 5.652 |
| Tiempo mostrado | 1 min 16 s | 41 s |
| Tokens/s | 69,17 | 136,54 |

Nemotron mostró aproximadamente un 97,4 % más tokens/s en esta salida extensa. No se midieron salidas iguales de 2.048 tokens: ese límite se había planteado, pero no se aplicó a estas ejecuciones. Capturas: [Qwen](../assets/evidence/04-15-49.png), [Nemotron](../assets/evidence/04-13-53.png).

Los tiempos mostrados están redondeados. Se conservan las tasas de la interfaz; dividir por el tiempo redondeado puede dar una tasa distinta.

## Código

| Primera respuesta, batería histórica | Qwen | Nemotron |
|---|---:|---:|
| Tests | 9/10 | 1/10 |
| Tokens generados | 1.295 | 5.178 |
| Tiempo mostrado | 10 s | 32 s |
| Tokens/s aproximados registrados | 123,3 | 158,6 |

Qwen falló el orden global de apertura: devolvió las sesiones cerradas según el orden de cierre. Nemotron acumuló bytes en la sesión activa, pero no los trasladó a las sesiones devueltas, cuyos contadores quedaron a cero. Su único test aprobado fue el de orden global.

El código histórico de Nemotron conservado reproduce 1/10 con los tests originales. El 9/10 de Qwen está documentado en la ejecución y su análisis; no se conserva aquí la función histórica completa. Las soluciones de una prueba posterior pasan 10/10 ambas y no sustituyen las puntuaciones originales.

## Agentic

| Métrica de la ejecución original | Qwen | Nemotron |
|---|---:|---:|
| Estado inicial | 9/12 | 9/12 |
| Estado final | 12/12 | 12/12 |
| Ejecuciones de la suite | 2 | 3 |
| Archivos funcionales corregidos | memory.js, planner.js | memory.js, planner.js |
| Intervención del usuario | ninguna | ninguna |
| Duración aproximada de la grabación | 1 min 48 s | 2 min 45 s |

Había dos errores funcionales: conversión de bytes con divisor decimal en vez de binario, y desempate que prefería mayor huella de memoria. Qwen corrigió ambos directamente. Nemotron hizo una modificación intermedia equivocada en la conversión, volvió a probar y la corrigió. También utilizó un archivo auxiliar de depuración que no se conserva.

Las duraciones son de las grabaciones, no una medición aislada de latencia del modelo. Los proyectos inicial y finales sí se incluyen; los tests se conservan sin cambios. Consulta [la procedencia](../docs/EVIDENCE.md).

## Nuevas ejecuciones

Guarda modelo y hash, versión del motor, hardware, perfil efectivo, plantilla, prompt, respuesta, semilla, tokens, tiempos, herramientas, intervenciones y salida de tests. `results/local/` está excluido de Git para tus registros y rutas locales.
