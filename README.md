# Qwen 3.6 vs Nemotron 3.5 Lightning · benchmark local

**Menos humo. Más IA real.** Cuatro pruebas, dos modelos y resultados de ejecuciones locales del 5 de octubre de 2026.

Qwen 3.6 35B-A3B **Q4_K_M** frente a NVIDIA Nemotron 3.5 Lightning 30B-A3B **NVFP4**, con MTP, contexto de **65.536 tokens** y dos GPU en reparto **70/30**. Es una comparación de estos despliegues completos: pesos, cuantización, caché y perfiles diferentes.

## Resultados de referencia

| Prueba | Qwen | Nemotron |
|---|---:|---:|
| Razonamiento: ruta óptima | 28; correcta | 28; correcta |
| Razonamiento: tiempo mostrado | 3 min 41 s | 48 s |
| Prefill: tokens/s | 1.157,69 | 1.570,92 |
| Generación extensa: tokens/s | 69,17 | 136,54 |
| Código: batería histórica | 9/10 | 1/10 |
| Agentic: suite final | 12/12 | 12/12 |
| Agentic: ejecuciones de tests | 2 | 3 |

Nemotron fue más rápido en las pruebas de velocidad. Qwen resolvió mejor la prueba de código de una sola respuesta. Ambos repararon el proyecto agentic; Qwen necesitó menos iteraciones. Son resultados de estas ejecuciones, no un ranking universal.

Consulta [los resultados completos](results/README.md), [la metodología](docs/METHODOLOGY.md) y [el alcance de las evidencias](docs/EVIDENCE.md). Los tokens generados incluyen el contenido que contabiliza la interfaz, también cuando hay pensamiento oculto.

## Empieza aquí

1. Prepara Windows, llama.cpp CUDA, los cuatro GGUF y las herramientas de pruebas: [instalación y configuración](docs/SETUP.md).
2. Genera tu configuración y arranca el servidor siguiendo los comandos de esa guía.
3. Usa el perfil de tareas para razonamiento y velocidad; cambia al perfil agentic para código y herramientas.
4. Ejecuta las cuatro pruebas siguientes y guarda tus resultados por separado.

Si ya conoces el entorno: [INI](configs/models.template.ini) · [sampling](configs/README.md) · [prompts](prompts/README.md) · [tests](tests/coding/README.md) · [proyecto agentic](tests/agentic/project).

## 1. Razonamiento

Pega [el problema de rutas](prompts/reasoning.txt) en una conversación nueva. No permitas herramientas. Comprueba restricciones, recorrido y suma, además del tiempo y los tokens.

Referencia de ambos modelos: **S → D → B → C → E → A → S**, distancia **28**. El [verificador exhaustivo](tests/reasoning/check_route.py) comprueba las 120 permutaciones posibles:

```powershell
python -B tests/reasoning/check_route.py
```

## 2. Velocidad

**Prefill:** pega [el texto completo](prompts/speed-prefill.txt), que pide responder `LISTO`. Anota tokens de entrada, tiempo de procesamiento y tokens/s de la interfaz. Usa exactamente el mismo archivo en ambos modelos.

**Generación:** pega [el prompt de salida extensa](prompts/speed-generation.txt). Anota tokens generados, duración y tokens/s. Las salidas originales no tuvieron la misma longitud; no fueron una prueba fija de 2.048 tokens.

Las capturas de referencia están en [assets/evidence](assets/evidence). No sumes las métricas globales del servidor si un monitor las repite junto a cada GPU.

## 3. Código

Pega [el prompt histórico](prompts/coding-original.txt), sin herramientas ni correcciones posteriores. Guarda la función como `solution.py` junto a una copia de [los diez tests originales](tests/coding/original-tests.py) llamada `tests.py` y ejecuta:

```powershell
python -B tests.py
```

La batería imprime `RESULTADO`; su salida, y no solo el código de salida del proceso, determina la puntuación. [La guía de código](tests/coding/README.md) explica el fallo de orden de Qwen y el fallo de acumulación de Nemotron. Las soluciones posteriores están separadas del histórico.

## 4. Agentic

Copia el proyecto inicial a una carpeta de trabajo nueva para cada modelo:

```powershell
New-Item -ItemType Directory -Force results/local | Out-Null
Copy-Item -Recurse tests/agentic/project results/local/qwen-agentic
Set-Location results/local/qwen-agentic
npm test
```

El estado inicial debe dar **9 aprobados y 3 fallos**. Abre Hermes Agent en esa carpeta, conecta el perfil agentic al servidor y entrega [el prompt original](prompts/agentic.txt). Deja que inspeccione, pruebe, corrija y vuelva a probar. No modifiques los tests.

Repite desde otra copia limpia para Nemotron. Las [versiones finales conservadas](results/agentic) dan **12/12**; sirven para revisar las reparaciones después de la prueba. El proyecto utiliza el ejecutor de tests integrado de Node.js y no necesita instalar dependencias.

## Estructura

| Carpeta | Contenido |
|---|---|
| `configs/` | Cuatro perfiles, plantilla portable y sampling |
| `prompts/` | Entradas de las cuatro pruebas |
| `tests/` | Baterías de código, verificador de rutas y proyecto inicial |
| `results/` | Resultados, soluciones conservadas y comprobaciones locales |
| `assets/evidence/` | Capturas de las mediciones originales |
| `docs/` | Entorno, metodología, fuentes y procedencia |
| `scripts/` | Preparación y arranque de llama-server |

Los pesos y los vídeos completos no se distribuyen en este repositorio. Descarga los modelos desde sus fuentes y respeta sus licencias. Los requisitos y los comandos son reproducibles; los resultados de un modelo con sampling pueden variar.
