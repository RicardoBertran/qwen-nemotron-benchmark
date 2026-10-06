# Prueba de código

La tarea implementa `rebuild_sessions(events)`: sesiones por usuario, acumulación de bytes, cierres y orden global de apertura. Lee [el prompt histórico](../../prompts/coding-original.txt) antes de probar una solución.

## Batería original

`original-tests.py` contiene los diez casos utilizados en el histórico. Para una nueva respuesta, guarda su función como `solution.py` y copia la batería como `tests.py` a la misma carpeta. Ejecuta `python -B tests.py` y lee el marcador `RESULTADO`. La batería original no devuelve un código de salida distinto cuando hay fallos.

Para revisar la función conservada de Nemotron:

```powershell
Push-Location tests/coding/recovered-nemotron
python -B tests.py
Pop-Location
```

Referencia: **1/10**. La función acumula bytes en el estado activo, pero devuelve otra estructura que mantiene cero. Qwen obtuvo **9/10** en la ejecución histórica: falló el orden global de apertura cuando las sesiones cerraban en orden diferente. Su función histórica completa no se incluye porque no se conserva íntegra.

## Repetición posterior

`rerun/qwen/` y `rerun/nemotron/` incluyen las soluciones y tests de una prueba posterior; `PROMPT.txt` corresponde a esa repetición. Cada una produce 10/10. No son las respuestas originales y no corrigen retrospectivamente las puntuaciones históricas.

```powershell
Push-Location tests/coding/rerun/qwen
python -B tests.py
Pop-Location
Push-Location tests/coding/rerun/nemotron
python -B tests.py
Pop-Location
```
