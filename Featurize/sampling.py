import random
import pickle

docs_direc = 'data/raw/test_docs_stemmed.pickle'
q_direc = 'data/raw/test_querry_results_stemmed.pickle'

print 'Loading Data from',str(docs_direc)
with open(docs_direc,'rb') as f:
    d = pickle.load(f)

print 'Loading querries from',str(q_direc)
with open(q_direc,'rb') as f:
    q = pickle.load(f)

k = d.keys()
for q_id in q:
    mod_k = random.sample(k,160)
    print str(len(q[q_id]['results'])),str(q_id)
    for d_id in mod_k:
        if d_id not in q[q_id]['results']:
            q[q_id]['results'][d_id] = 0
    print len(q[q_id]['results'])
    print '-'*20
q_direc = 'data/raw/test_querry_results_sampled.pickle'
print 'Saving querries to',str(q_direc)
with open(q_direc,'wb') as f:
    q = pickle.dump(q,f)

# for q_id in q:
#     print len(q[q_id]['results'].keys())
#     print '-'*10
