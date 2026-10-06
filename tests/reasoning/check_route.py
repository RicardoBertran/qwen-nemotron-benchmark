from itertools import permutations

edges = {'SA':7,'SB':11,'SC':9,'SD':6,'SE':10,'AB':5,'AC':8,'AD':7,'AE':4,'BC':6,'BD':3,'BE':9,'CD':5,'CE':2,'DE':8}
def distance(a,b):
    return edges.get(a+b, edges.get(b+a))
valid=[]
for p in permutations('ABCDE'):
    if p.index('C') > p.index('E') or p.index('D') > p.index('B'):
        continue
    if abs(p.index('A')-p.index('B')) == 1:
        continue
    route=('S',)+p+('S',)
    valid.append((sum(distance(a,b) for a,b in zip(route,route[1:])),route))
best=min(v[0] for v in valid)
winners=[route for total,route in valid if total==best]
assert best==28 and winners==[('S','D','B','C','E','A','S')]
print('120 permutaciones comprobadas. Óptimo único: '+' -> '.join(winners[0])+'; distancia 28.')
