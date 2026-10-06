# Preparación paso a paso

## Entorno de las ejecuciones

| Componente | Configuración documentada |
|---|---|
| Plataforma | Windows; llama.cpp con backend CUDA |
| CUDA0 | NVIDIA RTX 5070, 12 GB; escritorio y grabación |
| CUDA1 | NVIDIA RTX 5060 Ti, 16 GB |
| Orden de dispositivos | CUDA1,CUDA0; primero la GPU de 16 GB |
| Reparto principal | layer; tensor-split 70,30; todas las capas; fit off |
| Contexto | 65.536 tokens; una secuencia paralela |
| Qwen | Q4_K_M; draft MTP Q4_0; KV q4_0 |
| Nemotron | NVFP4; draft MTP NVFP4; KV f16 |
| MTP | draft-mtp; máximo 2 tokens draft; mínimo 0 |
| Interfaces | Llama UI; Hermes Agent para la prueba con herramientas |

No se conservaron versiones exactas de Windows, driver, CUDA, motor, Hermes, CPU ni RAM en el registro del benchmark. Una instalación actual no identifica retrospectivamente esas versiones. Para una repetición, registra esos datos antes de empezar.

El 70/30 es un reparto solicitado al motor, no una promesa de que la ocupación total de VRAM se divida exactamente así: cachés, buffers y draft también consumen memoria. Los identificadores CUDA pueden cambiar en otra máquina; comprueba su orden.

## 1. Requisitos

- Windows y PowerShell.
- Driver NVIDIA compatible con el paquete CUDA elegido de llama.cpp.
- [llama.cpp, distribución oficial](https://github.com/ggml-org/llama.cpp/releases), con soporte para estos modelos, NVFP4 y draft-mtp. Conserva juntos el ejecutable y sus DLL.
- Python 3 para las pruebas de código y rutas.
- Node.js con `node --test` para el proyecto agentic; no tiene dependencias externas.
- Hermes Agent, con acceso a archivos y terminal, para la prueba agentic.
- Espacio para los pesos principales y sus drafts. La memoria disponible debe permitir los perfiles; bajar contexto o cambiar cuantización produce otro despliegue.

```powershell
python --version
node --version
git --version
& 'PEGA_AQUI_LA_RUTA_DE_LLAMA_SERVER.exe' --version
& 'PEGA_AQUI_LA_RUTA_DE_LLAMA_SERVER.exe' --list-devices
```

## 2. Modelos

| Modelo | Fuente oficial | Archivo utilizado |
|---|---|---|
| Qwen | [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | Qwen3.6-35B-A3B-Q4_K_M.gguf |
| Qwen draft | MTP compatible con la conversión principal | mtp-Qwen3.6-35B-A3B-Q4_0.gguf |
| Nemotron | [NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4), [BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) | Nemotron-3.5-Lightning-30B-A3B-NVFP4.gguf |
| Nemotron draft | MTP compatible con la conversión principal | mtp-Nemotron-3.5-Lightning-30B-A3B-NVFP4.gguf |

Los enlaces identifican los modelos oficiales. No identifican al publicador ni la revisión de las conversiones GGUF concretas utilizadas. Los nombres de archivo no bastan para garantizar pesos idénticos. Elige una distribución compatible, conserva su enlace y revisión y calcula sus hashes:

```powershell
Get-FileHash -Algorithm SHA256 'PEGA_AQUI_LA_RUTA_DE_TU_MODELO.gguf'
```

## 3. Preparar los cuatro perfiles

Desde la raíz del repositorio:

```powershell
./scripts/New-BenchmarkConfig.ps1 `
  -QwenModel 'PEGA_AQUI_LA_RUTA_QWEN.gguf' `
  -QwenDraft 'PEGA_AQUI_LA_RUTA_QWEN_MTP.gguf' `
  -NemotronModel 'PEGA_AQUI_LA_RUTA_NEMOTRON.gguf' `
  -NemotronDraft 'PEGA_AQUI_LA_RUTA_NEMOTRON_MTP.gguf'

./scripts/Start-Server.ps1 `
  -ServerExe 'PEGA_AQUI_LA_RUTA_DE_LLAMA_SERVER.exe' `
  -ConfigPath './results/local/models.ini'
```

Abre `http://127.0.0.1:8080`. El router carga un modelo cada vez. Selecciona `qwen36-35b-a3b` o `nemotron35-lightning-30b-a3b` para razonamiento y velocidad; sus variantes terminadas en `-agentic` para código y Hermes. Comprueba en los logs que se aplica el perfil y que se carga el draft. Activar MTP no demuestra por sí solo una aceleración: para medirla habría que comparar con MTP desactivado.

El INI incorpora los ajustes finales confirmados: 65.536 tokens, CUDA1 primero, 70/30 y fit off. La configuración anterior de Qwen tenía 122.880 tokens y reparto automático; no debe usarse como configuración final del benchmark.

## 4. Conectar Hermes

Configura un proveedor compatible con la API de chat del servidor local y la URL `http://127.0.0.1:8080/v1`. Usa el identificador del perfil `-agentic` correspondiente y confirma que las llamadas a herramientas funcionan. Conserva el system prompt y los ajustes efectivos de tu instalación: los de la ejecución original no se archivaron completos.

Trabaja sobre una copia del proyecto inicial, inicia una sesión nueva para cada modelo y entrega el prompt sin modificaciones. El modelo debe poder ejecutar `npm test` y editar `src/`. La prueba no termina con una afirmación de éxito: termina con la suite completa aprobada.

## 5. Registrar una repetición

Anota las versiones, pesos, hashes y parámetros efectivos; guarda una respuesta completa por prueba y la salida final de tests. No compares una ejecución con herramientas con otra sin ellas. Consulta [la metodología](METHODOLOGY.md) antes de interpretar diferencias.
