from solution import rebuild_sessions


def check(name, events, expected):
    result = rebuild_sessions(events)
    if result != expected:
        print(f"\n❌ {name}")
        print("EXPECTED:")
        print(expected)
        print("GOT:")
        print(result)
        return False

    print(f"✅ {name}")
    return True


tests = []


# 1. Sesión normal
tests.append((
    "basic",
    [
        {"user": "a", "timestamp": 1, "type": "start"},
        {"user": "a", "timestamp": 2, "type": "data", "bytes": 100},
        {"user": "a", "timestamp": 3, "type": "end"},
    ],
    [
        {"user": "a", "start": 1, "end": 3, "bytes": 100, "reason": "ended"}
    ]
))


# 2. Eventos desordenados
tests.append((
    "unordered",
    [
        {"user": "a", "timestamp": 3, "type": "end"},
        {"user": "a", "timestamp": 1, "type": "start"},
        {"user": "a", "timestamp": 2, "type": "data", "bytes": 25},
    ],
    [
        {"user": "a", "start": 1, "end": 3, "bytes": 25, "reason": "ended"}
    ]
))


# 3. Data y end huérfanos
tests.append((
    "orphan_events",
    [
        {"user": "a", "timestamp": 1, "type": "data", "bytes": 99},
        {"user": "a", "timestamp": 2, "type": "end"},
        {"user": "a", "timestamp": 3, "type": "start"},
        {"user": "a", "timestamp": 4, "type": "data", "bytes": 5},
    ],
    [
        {"user": "a", "start": 3, "end": None, "bytes": 5, "reason": "open"}
    ]
))


# 4. Restart
tests.append((
    "restart",
    [
        {"user": "a", "timestamp": 1, "type": "start"},
        {"user": "a", "timestamp": 2, "type": "data", "bytes": 10},
        {"user": "a", "timestamp": 5, "type": "start"},
        {"user": "a", "timestamp": 6, "type": "data", "bytes": 20},
        {"user": "a", "timestamp": 7, "type": "end"},
    ],
    [
        {"user": "a", "start": 1, "end": 5, "bytes": 10, "reason": "restarted"},
        {"user": "a", "start": 5, "end": 7, "bytes": 20, "reason": "ended"},
    ]
))


# 5. Usuarios independientes
tests.append((
    "multiple_users",
    [
        {"user": "a", "timestamp": 1, "type": "start"},
        {"user": "b", "timestamp": 2, "type": "start"},
        {"user": "a", "timestamp": 3, "type": "data", "bytes": 10},
        {"user": "b", "timestamp": 4, "type": "data", "bytes": 50},
        {"user": "a", "timestamp": 5, "type": "end"},
        {"user": "b", "timestamp": 6, "type": "end"},
    ],
    [
        {"user": "a", "start": 1, "end": 5, "bytes": 10, "reason": "ended"},
        {"user": "b", "start": 2, "end": 6, "bytes": 50, "reason": "ended"},
    ]
))


# 6. Mismo timestamp: el orden original importa
tests.append((
    "stable_same_timestamp",
    [
        {"user": "a", "timestamp": 10, "type": "start"},
        {"user": "a", "timestamp": 10, "type": "data", "bytes": 7},
        {"user": "a", "timestamp": 10, "type": "end"},
    ],
    [
        {"user": "a", "start": 10, "end": 10, "bytes": 7, "reason": "ended"}
    ]
))


# 7. Sesión que queda abierta
tests.append((
    "open_session",
    [
        {"user": "a", "timestamp": 1, "type": "start"},
        {"user": "a", "timestamp": 5, "type": "data", "bytes": 42},
    ],
    [
        {"user": "a", "start": 1, "end": None, "bytes": 42, "reason": "open"}
    ]
))


# 8. Bytes de start/end deben ignorarse
tests.append((
    "ignore_non_data_bytes",
    [
        {"user": "a", "timestamp": 1, "type": "start", "bytes": 999},
        {"user": "a", "timestamp": 2, "type": "data", "bytes": 3},
        {"user": "a", "timestamp": 3, "type": "end", "bytes": 999},
    ],
    [
        {"user": "a", "start": 1, "end": 3, "bytes": 3, "reason": "ended"}
    ]
))


# 9. Varios reinicios
tests.append((
    "multiple_restarts",
    [
        {"user": "a", "timestamp": 1, "type": "start"},
        {"user": "a", "timestamp": 2, "type": "data", "bytes": 1},
        {"user": "a", "timestamp": 3, "type": "start"},
        {"user": "a", "timestamp": 4, "type": "data", "bytes": 2},
        {"user": "a", "timestamp": 5, "type": "start"},
        {"user": "a", "timestamp": 6, "type": "end"},
    ],
    [
        {"user": "a", "start": 1, "end": 3, "bytes": 1, "reason": "restarted"},
        {"user": "a", "start": 3, "end": 5, "bytes": 2, "reason": "restarted"},
        {"user": "a", "start": 5, "end": 6, "bytes": 0, "reason": "ended"},
    ]
))


# 10. Orden global de apertura con varios usuarios
tests.append((
    "global_open_order",
    [
        {"user": "b", "timestamp": 5, "type": "end"},
        {"user": "b", "timestamp": 1, "type": "start"},
        {"user": "a", "timestamp": 4, "type": "end"},
        {"user": "a", "timestamp": 2, "type": "start"},
        {"user": "c", "timestamp": 3, "type": "start"},
    ],
    [
        {"user": "b", "start": 1, "end": 5, "bytes": 0, "reason": "ended"},
        {"user": "a", "start": 2, "end": 4, "bytes": 0, "reason": "ended"},
        {"user": "c", "start": 3, "end": None, "bytes": 0, "reason": "open"},
    ]
))


passed = 0

for name, events, expected in tests:
    if check(name, events, expected):
        passed += 1

print(f"\nRESULTADO: {passed}/{len(tests)} tests superados")
