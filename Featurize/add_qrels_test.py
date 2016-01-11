import pickle

doc = './data/raw/test_querry_content_stemmed.pickle'
qres = './data/raw/qrels.ohsu.88-91'

with open(doc) as f:
	t_q = pickle.load(f)

count = 0
with open(qres) as f:
	f = f.readlines()
	for line in f:
		w = line.strip().split()
		t_q[w[0]]['results'][int(w[1])] = int(w[2])
k = t_q.keys()
for i in range(1):
	print t_q[k[i+5]]

doc = './data/raw/test_querry_results_stemmed.pickle'

print 'Saving data'
with open(doc,'wb') as f:
	pickle.dump(t_q,f)
