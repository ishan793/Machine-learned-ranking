
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

def make_training_data(docs,q_docs,mod,n = 50):
    res = {}
    k = docs.keys()
    print mod

    for q_id in q_docs:
        # print q_id
        res[q_id] = []
        
        q_tuple = mod[q_docs[q_id]['desc']]
        q_vec = make_vector(q_tuple)
        
        add_dk = random.sample(k,n)
        for doc_key in add_dk:
            temp = {'rel':0,'doc_id':0,'vector':[]}
            if doc_key not in q_docs[q_id]['results']:
                try:
                    d_tuple = mod[docs[doc_key]['abstract']]
                except:
                    d_tuple = mod[docs[doc_key]['title']]
                d_vec = make_vector(d_tuple)
                dq_vec = q_vec + d_vec
                temp['doc_id'] = doc_key

                temp['vector'] = dq_vec
                res[q_id].append(temp)

        for doc_key in q_docs[q_id]['results']:
            temp = {'rel':0,'doc_id':0,'vector':[]}
            try:
                d_tuple = mod[docs[doc_key]['abstract']]
            except:
                d_tuple = mod[docs[doc_key]['title']]
            d_vec = make_vector(d_tuple)
            dq_vec = q_vec + d_vec
            temp['doc_id'] = doc_key
            temp['vector'] = dq_vec
            temp['rel'] = q_docs[q_id]['results'][doc_key]
            # if q_id == 'OHSU1':
            #     print temp['doc_id']
            res[q_id].append(temp)
    
    return res

def save_data_svm(typ = 'train',feat = 'lsi',n_topics = 64,n_rand = 50):              
    docs, q_docs, mod = utils.get_data(mode = typ,t_ = feat,n_ = n_topics)
    print 'Making stuff'

    res = make_training_data(docs,q_docs,mod, n = n_rand)

    with open('modified_data_'+typ+'_'+feat,'wb') as f:
        pickle.dump(res,f)

def make_sent(q_id,qd_vec):
    vec = qd_vec['vector']
    doc_id = qd_vec['doc_id']
    rel = qd_vec['rel']
    st = str(rel)+' qid:'+str(q_id)
    vec_st = ' '
    for i in range(len(vec)):
        vec_st += str(i+1)+':'
        vec_st += '{:.4f}'.format(vec[i])
        vec_st += ' '
    st += vec_st + ' #'+str(doc_id)
    return st

def make_file(test_direc, train_direc, frac = 0.25):
    
    with open(test_direc) as f:
        test_docs = pickle.load(f)

    with open(train_direc) as f:
        train_docs = pickle.load(f)

    k = test_docs.keys()
    num_q = len(k)
    test_q = random.sample(k,int(frac*num_q))
    train_q = [i for i in k if i not in test_q]
    test_q = sorted(test_q, key = lambda b:int(b.split('OHSU')[1]))
    train_q = sorted(train_q, key = lambda b:int(b.split('OHSU')[1]))

    count = 0
    f = open('train_file.txt','w')
    for q_id in train_q:
        
        temp = q_id.split('OHSU')
        rel_docs = test_docs[q_id] + train_docs[q_id]
        for i in rel_docs:
            a = make_sent(temp[1],i) + '\n'
            f.write(a)
            count += 1
    print count
    f.close()

    f = open('test_file.txt','w')
    for q_id in test_q:
        
        temp = q_id.split('OHSU')
        rel_docs = test_docs[q_id] + train_docs[q_id]
        
        for i in rel_docs:
            a = make_sent(temp[1],i) + '\n'
            f.write(a)
            count += 1
    print count
    f.close()


save_data_svm(typ = 'test', feat = 'lsi', n_topics = 64, n_rand = 150)
save_data_svm(typ = 'train', feat = 'lsi', n_topics = 64, n_rand = 30)
make_file('modified_data_test_lsi', 'modified_data_train_lsi')


















































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
