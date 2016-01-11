from sklearn.cluster import KMeans
import gensim
import utils
import matplotlib.pyplot as plt
import pickle

def make_vector(tuple_vec):
    res = [0]*64
    for i in tuple_vec:
        res[i[0]] = i[1]
    return res

def get_docs(d):
	res = []
	for d_id in docs:
		abst = ''
		try:
			abst = docs[d_id]['abstract']
		except:
			abst = docs[d_id]['title']
	
		res.append(make_vector(abst))
	return res

docs, q_docs, mod = utils.get_data(mode = 'train',t_ = 'lda',n_ = 64)
utils.bow2mod(docs,q_docs,mod)
print 'Getting Docs'
a = get_docs(docs)
print str(len(a)),'docs retrieved'

k_ = []
inertia = []
print 'Clustering Started'
k_opt = 80
est = KMeans(n_clusters = k_opt)
est.fit(a)
res = est.predict(a)
cent = est.cluster_centers_

pickle.dump(cent, open('centers','wb'))
pickle.dump(res, open('predictions','wb'))
pickle.dump(est,open('km_80','wb'))