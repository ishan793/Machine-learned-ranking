from sklearn.cluster import KMeans
import gensim
import utils
import matplotlib.pyplot as plt
import pickle, random
import numpy as np
import math

def make_vector(tuple_vec):
    res = [0]*64
    for i in tuple_vec:
        res[i[0]] = i[1]
    return res

def assign_cluster(docs, km_mod, mod):
	res = {}
	count = 0
	for d_id in docs:
		try:
			abst = mod[docs[d_id]['abstract']]
		except:
			abst = mod[docs[d_id]['title']]

		doc_vec = np.asarray(make_vector(abst))
		doc_vec = doc_vec.reshape(1,-1)
		cluster = km_mod.predict(doc_vec)[0]
		if count ==0:
			print cluster
			count += 1
		if cluster not in res:
			res[cluster] = []
		res[cluster].append(d_id)
	return res
# cl_as = cluster_assignment
def get_top(q, docs, mod, km_mod,cl_as):
    
    res = []
    q_title = mod[q['desc']]
    
    q_vec = np.asarray(make_vector(q_title)).reshape(1,-1)
    q_cluster = km_mod.predict(q_vec)
    test_doc_ids = cl_as[q_cluster[0]]
    for d_id in q['results']:
    	if d_id not in test_doc_ids:
    		test_doc_ids.append(d_id)
    for i in test_doc_ids:
        doc = docs[i]
        try:
            doc_title = mod[doc['abstract']]
        except:
            doc_title = mod[doc['title']]
        sim_score = utils.compute_sim(q_title,doc_title)
        if i in q['results']:
            res.append(((i,q['results'][i],sim_score)))
        else:
            res.append(((i,0,sim_score)))

    for i in q['results']:
        doc = docs[i]
        try:
            doc_title = mod[doc['abstract']]
        except:
            doc_title = mod[doc['title']]
        sim_score = utils.compute_sim(q_title,doc_title)
        if i not in test_doc_ids:
            res.append(((i,q['results'][i],0)))
        
    return res

def compute_dcg(ranking):
    res = 0
    n = len(ranking)
    for i in range(n):
        num = 2**(ranking[i]) - 1
        den = math.log(2+i,2)
        res += num/den
    return res

def get_ndcg(res_q, n=10): # (q, docs, n_ = 10):
    ideal_rank = sorted(res_q, key = lambda b:b[1], reverse = True)
    i_rank = [i[1] for i in ideal_rank]
    n_i = i_rank[:n]
    ideal_score = compute_dcg(n_i)

    pred_rank = sorted(res_q, key = lambda b:b[2], reverse = True)
    p_rank = [i[1] for i in pred_rank]
    n_p = p_rank[:n]
    sys_score = compute_dcg(n_p)
    res = sys_score/ideal_score
    return res

def save_ass(a):	
	with open('cluster_assignment','wb') as f:
		pickle.dump(a,f)

def load_ass(f_name):
	with open(f_name,'rb') as f:
		model = pickle.load(f)
	return model

docs, q_docs, mod = utils.get_data(mode = 'test',t_ = 'lda',n_ = 64)
print 'Loading cluster'
with open('km_80','rb') as f:
	model = pickle.load(f)
# a = assign_cluster(docs,model,mod)
# print 'Saving assignments'
# save_ass(a)
a = load_ass('cluster_assignment')
avg = 0
n = len(q_docs)
print n
for q_id in q_docs:
	q = q_docs[q_id]
	rankings = get_top(q,docs,mod, model, a)
	val = get_ndcg(rankings,10)
	print str(q_id),str(val)
	avg += val
print val/n
