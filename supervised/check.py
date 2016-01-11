
import random
import time
import utils
import math
import numpy as np
import pickle

def make_vector(tuple_vec):
    res = [0]*64
    for i in tuple_vec:
        res[i[0]] = i[1]
    return res

def make_training_data(docs,q_docs,mod):
    x = []
    y = []
    k = docs.keys()
    print mod
    for q_id in q_docs:
        temp = []
        q_tuple = mod[q_docs[q_id]['desc']]
        q_vec = make_vector(q_tuple)
        mod_k = random.sample(k,50)
        for doc_key in mod_k:
            if doc_key not in q_docs[q_id]['results']:
                try:
                    d_tuple = mod[docs[doc_key]['abstract']]
                    d_vec = make_vector(d_tuple)
                except:
                    d_tuple = mod[docs[doc_key]['title']]
                    d_vec = make_vector(d_tuple)
                res = q_vec + d_vec
                x.append(np.asarray(res))
                y.append(0)

        for doc_key in q_docs[q_id]['results']:
            try:
                d_tuple = mod[docs[doc_key]['abstract']]
                d_vec = make_vector(d_tuple)
            except:
                d_tuple = mod[docs[doc_key]['title']]
                d_vec = make_vector(d_tuple)
            res = q_vec + d_vec
            x.append(np.asarray(res))
            y.append(q_docs[q_id]['results'][doc_key])
    return x,y
                
docs, q_docs, mod = utils.get_data(mode = 'test',t_ = 'lsi',n_ = 64)
print 'Making stuff'
x,y = make_training_data(docs,q_docs,mod)

with open('modified_data_x','wb') as f:
    pickle.dump(x,f)
with open('modified_data_y','wb') as f:
    pickle.dump(y,f)

x = np.asarray(x)
print x.shape
# print x[0]
# k = q_docs.keys()



















































# avg = 0
# res = []
# print 'Begining Quering '
# for j in range(63):
#     st = ''
#     print str(k[j])
#     b =  q_docs[k[j]]['results']
#     # print 'Actual results',str(b)
#     start = time.time()
#     a = get_top(q_docs[k[j]],docs,mod,n = 10, m = 10000)
#     #print 'retrieved results',str(a)
#     end = time.time()
#     val = get_ndcg(a,b,n = 10)
#     avg += val
#     st += 'Time taken: ' +str(end-start)
#     st += ' and NDCG score: '+str(val)
#     print st
#     count = 0
#     for i in a:
#         if i in b:
#             count += 1
#             if j not in res:
#                 res.append(j)
#     print 'Out of 10',str(count),'results are present'
#     print '-'*30
    
# print len(res)/63.0
# print avg/63.0
