def rebuild_sessions(events):
    sorted_events = sorted(enumerate(events), key=lambda x: x[1]['timestamp'])
    
    open_sessions = {}
    all_sessions = []
    order_counter = 0
    
    for _, event in sorted_events:
        user = event['user']
        timestamp = event['timestamp']
        event_type = event['type']
        
        if event_type == 'start':
            if user in open_sessions:
                order, session = open_sessions.pop(user)
                session['end'] = timestamp
                session['reason'] = 'restarted'
                all_sessions.append((order, session))
            new_session = {
                'user': user,
                'start': timestamp,
                'end': None,
                'bytes': 0,
                'reason': 'open'
            }
            open_sessions[user] = (order_counter, new_session)
            order_counter += 1
        
        elif event_type == 'data':
            if user in open_sessions:
                open_sessions[user][1]['bytes'] += event['bytes']
        
        elif event_type == 'end':
            if user in open_sessions:
                order, session = open_sessions.pop(user)
                session['end'] = timestamp
                session['reason'] = 'ended'
                all_sessions.append((order, session))
    
    for user, (order, session) in open_sessions.items():
        session['end'] = None
        session['reason'] = 'open'
        all_sessions.append((order, session))
    
    all_sessions.sort(key=lambda x: x[0])
    return [session for _, session in all_sessions]

