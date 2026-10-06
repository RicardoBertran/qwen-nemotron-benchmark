# Perfiles

[models.template.ini](models.template.ini) contiene cuatro perfiles completos. Genera una copia con rutas reales mediante `scripts/New-BenchmarkConfig.ps1`; los archivos de `sampling/` permiten consultar los valores de muestreo por separado.

| Parámetro | Qwen tareas | Qwen código/agentic | Nemotron tareas | Nemotron código/agentic |
|---|---:|---:|---:|---:|
| Temperatura | 1,0 | 0,6 | 1,0 | 1,0 |
| Top-p | 0,95 | 0,95 | 0,95 | 0,95 |
| Top-k | 20 | 20 | no fijado | no fijado |
| Min-p | 0 | 0 | no fijado | no fijado |
| Presence penalty | 1,5 | 0 | 0 | 0 |
| Frequency penalty | 0 | 0 | 0 | 0 |
| Repeat penalty | 1,0 | 1,0 | 1,0 | 1,0 |

No fijado significa heredado del motor o de la petición; no significa cero. Registra el valor efectivo en una repetición. La interfaz o el cliente puede sobrescribir los parámetros del servidor.

Todos usan 65.536 tokens, batch 512, ubatch 128, parallel 1, Flash Attention, Jinja, caché de prompt y métricas. `n-predict=-1` no fija un límite corto de salida; el cliente y la capacidad de contexto también pueden limitarla.

Qwen usa KV q4_0 y umbral draft 0,5. Nemotron usa KV f16 y tipos de caché draft q8_0. Los dos solicitan draft-mtp con máximo 2 y mínimo 0. Estas diferencias forman parte de los despliegues comparados. Los perfiles se documentan como configuración del benchmark, no como garantía de rendimiento óptimo en cualquier equipo.
