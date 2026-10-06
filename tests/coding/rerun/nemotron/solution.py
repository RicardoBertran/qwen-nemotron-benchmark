def rebuild_sessions(events):
    sorted_events = sorted(events, key=lambda e: e['timestamp'])
    sessions = []
    user_open = {}

    for ev in sorted_events:
        typ = ev['type']
        user = ev['user']
        ts = ev['timestamp']

        if typ == 'start':
            if user in user_open:
                prev_idx = user_open[user]
                prev = sessions[prev_idx]
                prev['end'] = ts
                prev['reason'] = 'restarted'

            new_session = {
                'user': user,
                'start': ts,
                'end': None,
                'bytes': 0,
                'reason': 'open'
            }
            sessions.append(new_session)
            user_open[user] = len(sessions) - 1

        elif typ == 'data':
            if user in user_open:
                idx = user_open[user]
                sessions[idx]['bytes'] += ev['bytes']

        elif typ == 'end':
            if user in user_open:
                idx = user_open[user]
                sessions[idx]['end'] = ts
                sessions[idx]['reason'] = 'ended'
                del user_open[user]

    return sessions

