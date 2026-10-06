"""Nueva bateria compartida: 10 casos, sin dependencias externas."""
import copy
import importlib.util
from pathlib import Path
import sys


def event(user, timestamp, kind, size=None):
    value = {"user": user, "timestamp": timestamp, "type": kind}
    if size is not None:
        value["bytes"] = size
    return value


def session(user, start, end, size, reason):
    return dict(user=user, start=start, end=end, bytes=size, reason=reason)


CASES = [
    ("Entrada vacia", [], []),
    ("Sesion normal y suma de bytes",
     [event("a", 1, "start"), event("a", 2, "data", 7),
      event("a", 3, "data", 5), event("a", 4, "end")],
     [session("a", 1, 4, 12, "ended")]),
    ("Eventos desordenados",
     [event("a", 9, "end"), event("a", 4, "data", 13), event("a", 1, "start")],
     [session("a", 1, 9, 13, "ended")]),
    ("Eventos huerfanos y posteriores al cierre",
     [event("a", 0, "data", 100), event("a", 1, "end"),
      event("a", 2, "start"), event("a", 3, "data", 6),
      event("a", 4, "end"), event("a", 5, "data", 90), event("a", 6, "end")],
     [session("a", 2, 4, 6, "ended")]),
    ("Reinicio conserva bytes y separa sesiones",
     [event("a", 1, "start"), event("a", 2, "data", 8),
      event("a", 3, "start"), event("a", 4, "data", 3), event("a", 5, "end")],
     [session("a", 1, 3, 8, "restarted"), session("a", 3, 5, 3, "ended")]),
    ("Sesion abierta al finalizar",
     [event("a", 1, "start"), event("a", 2, "data", 4), event("a", 3, "data", 0)],
     [session("a", 1, None, 4, "open")]),
    ("Usuarios independientes y orden global de apertura",
     [event("a", 1, "start"), event("b", 2, "start"),
      event("b", 3, "data", 11), event("b", 4, "end"),
      event("a", 5, "data", 2), event("a", 6, "end")],
     [session("a", 1, 6, 2, "ended"), session("b", 2, 4, 11, "ended")]),
    ("Empates mantienen el orden original",
     [event("a", 5, "data", 99), event("a", 5, "start"),
      event("a", 5, "data", 7), event("a", 5, "end"),
      event("a", 5, "data", 88), event("a", 5, "start"),
      event("a", 5, "data", 3)],
     [session("a", 5, 5, 7, "ended"), session("a", 5, None, 3, "open")]),
    ("Cerradas y abiertas conservan orden global",
     [event("b", 2, "start"), event("a", 1, "start"),
      event("a", 3, "data", 5), event("b", 4, "data", 9),
      event("b", 5, "end"), event("b", 6, "start"), event("b", 7, "data", 2)],
     [session("a", 1, None, 5, "open"), session("b", 2, 5, 9, "ended"),
      session("b", 6, None, 2, "open")]),
    ("Reinicios empatados y reapertura tras end",
     [event("a", 1, "start"), event("a", 1, "data", 4),
      event("a", 1, "start"), event("a", 1, "data", 6),
      event("a", 2, "end"), event("a", 2, "start"),
      event("a", 2, "data", 10), event("a", 3, "end")],
     [session("a", 1, 1, 4, "restarted"), session("a", 1, 2, 6, "ended"),
      session("a", 2, 3, 10, "ended")]),
]


def main():
    folder = Path(__file__).resolve().parent
    label = {"qwen": "Qwen", "nemotron": "Nemotron"}.get(folder.name.lower(), folder.name)
    spec = importlib.util.spec_from_file_location("benchmark_solution", folder / "solution.py")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        if getattr(module, "BENCHMARK_PENDING", False):
            print(f"{label}: pendiente. Guarda la respuesta del modelo en solution.py.")
            return 2
        function = module.rebuild_sessions
        if not callable(function):
            raise TypeError("rebuild_sessions no es una funcion")
    except Exception as exc:
        print(f"{label}: no se pudo cargar solution.py: {type(exc).__name__}: {exc}")
        print("Prueba no ejecutada; revisa que hayas pegado el codigo completo sin Markdown.")
        return 2

    passed = 0
    print(f"Benchmark de codigo - {label}\n")
    for index, (name, source, expected) in enumerate(CASES, 1):
        data = copy.deepcopy(source)
        try:
            actual = function(data)
            if data != source:
                raise AssertionError("La funcion modifico la entrada")
            if actual != expected:
                raise AssertionError(f"Esperado: {expected!r}\n     Obtenido: {actual!r}")
        except Exception as exc:
            print(f"[{index:02d}] FAIL - {name}\n     {type(exc).__name__}: {exc}")
        else:
            passed += 1
            print(f"[{index:02d}] PASS - {name}")
    print(f"\n{label}: {passed}/10 tests superados")
    return 0 if passed == 10 else 1


if __name__ == "__main__":
    sys.exit(main())
