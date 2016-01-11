import gensim
import pickle

st = './data/test_fv/docs.pickle'
d = pickle.load(open(st,'rb'))

st = './data/test_fv/querries.pickle'
q = pickle.load(open(st,'rb'))

def compute_sim(a,b):
    x = {}
    for i in a:
        x[i[0]] = i[1]
    y = {}
    for i in b:
        y[i[0]] = i[1]

    res = 0
    norm_x = 0
    for i in x:
        norm_x += x[i]*x[i]
        if i in y:
            res += x[i]*y[i]
    norm_y = 0
    for i in y:
        norm_y += y[i]*y[i]
    temp = (norm_x*norm_y)**0.5
    res = res/temp
    return res
print 'Starting now'
c = 0
n = 0
k = q.keys()
qu = q['OHSU1']
m = 0
id_ = 0
for i in d:
    doc = d[i]
    val = compute_sim(doc['title'],qu['desc']) 
    if val > m:
        m = val
        id_ = i
    c += val
    n += 1
print k[0]
print c/n
print m
print id_