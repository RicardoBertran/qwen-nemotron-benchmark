def rebuild_sessions(events):
    # Sort stably by timestamp; Python's sort is stable, so equal timestamps
    # keep the original relative order.
    sorted_events = sorted(events, key=lambda e: e["timestamp"])

    all_sessions = []
    user_current = {}

    for ev in sorted_events:
        typ = ev["type"]
        user = ev["user"]
        ts = ev["timestamp"]

        if typ == "start":
            if user in user_current:
                # Close the previously open session for this user
                prev = user_current[user]
                all_sessions[prev["index"]]["end"] = ts
                all_sessions[prev["index"]]["reason"] = "restarted"

            # Open a new session
            new_idx = len(all_sessions)
            new_session = {
                "user": user,
                "start": ts,
                "end": None,
                "bytes": 0,
                "reason": None,
            }
            all_sessions.append(new_session)
            user_current[user] = {"start": ts, "bytes": 0, "index": new_idx}

        elif typ == "data":
            # Add bytes only if the user has an open session
            if user in user_current:
                user_current[user]["bytes"] += ev["bytes"]

        elif typ == "end":
            # Close the open session for this user, if any
            if user in user_current:
                curr = user_current[user]
                all_sessions[curr["index"]]["end"] = ts
                all_sessions[curr["index"]]["reason"] = "ended"
                # Session is now closed; remove from current tracking
                del user_current[user]

    # After all events, any session still open gets end = None and reason = "open"
    for user, info in user_current.items():
        idx = info["index"]
        all_sessions[idx]["end"] = None
        all_sessions[idx]["reason"] = "open"

    return all_sessions
