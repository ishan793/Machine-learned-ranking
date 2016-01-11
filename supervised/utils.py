import gensim
import pickle
import random
import math
import time

import math

def compute_dcg(ranking):
    res = ranking[0]
    temp = []
    temp.append(ranking[0])
    n = len(ranking)
    for i in range(1,n):
        num = (ranking[i])
        den = math.log(1+i,2)
        temp.append(num/den)
        res += num/den
    return res

def get_ndcg(a,q_res,n = None,p_based = False): # (q, docs, n_ = 10):
    
    sorted_a = sorted(a.items(), key = lambda b:b[1])
    temp = []
    if n == None:
        n = len(sorted_a)
    for i in range(n):
        temp.append(sorted_a[n-i-1])
    sys_ranking = []
    for i in temp:
        key = i[0]
        if key in q_res:
            sys_ranking.append(q_res[key])
        else:
            sys_ranking.append(0)
    sys_score = compute_dcg(sys_ranking)
    if sys_score == 0:
        return 0
    
    if not p_based:
        ideal_ranking = sorted(q_res.items(), key = lambda b:b[1], reverse = True)
        temp = []
        for i in range(n):
            try:
                temp.append(ideal_ranking[i][1])
            except IndexError:
                print 'error ocurred, ',str(len(ideal_ranking)),'set length',str(n)
                temp.append(sys_ranking[i])
        ideal_score = compute_dcg(temp)
    else:
        sys_ranking = sorted(sys_ranking, reverse = True)
        ideal_score = compute_dcg(sys_ranking)
    
    res = sys_score/ideal_score
    return res

def transform_bow(docs,q_docs,dct): # add docs
##    # create a duplicate var, because of pythons var passing antics
    print 'Converting docs to bow'
    for d in docs:
        try:
            abst = docs[d]['abstract']
            docs[d]['abstract'] = dct.doc2bow(abst.lower().split())
        except:
            # we do nothing here, what you see below is absolutely the whim of a whimsical mind
            tuiy = 2
        tit = docs[d]['title']
        docs[d]['title'] = dct.doc2bow(tit.lower().split())

    print 'Converting Querries to bow'

    for d in q_docs:
        try:
            title = q_docs[d]['title']
            desc = q_docs[d]['desc']
        except:
            print str(q_docs[d]),'Error ocurred'
        q_docs[d]['title'] = dct.doc2bow(title.lower().split())
        q_docs[d]['desc'] = dct.doc2bow(desc.lower().split())


def load_model(n = 128,t = 'tfidf',id = 5):
    mod_name = 'data/models/'
    if t == 'tfidf':
        mod_name += str(t)+'_'+str(id)
        mod = gensim.models.TfidfModel.load(mod_name)
    elif t == 'hdp':
        mod_name += str(t)+'_'+str(id)
        mod = gensim.models.HdpModel.load(mod_name)
    elif t == 'lda':
        mod_name += str(t)+'_'+str(n)+'_'+str(id)
        mod = gensim.models.LdaModel.load(mod_name)
    elif t == 'lsi':
        mod_name += str(t)+'_'+str(n)+'_'+str(id)
        mod = gensim.models.LsiModel.load(mod_name)
    return mod

def bow2mod(docs, q_docs, mod):
    for d in docs:
        temp = {}
        try:
            abst = docs[d]['abstract']
            docs[d]['abstract'] = mod[abst]
        except:
            poi = 2
        tit = docs[d]['title']
        docs[d]['title'] = mod[tit]
      
    for d in q_docs:
        tit = q_docs[d]['title']
        desc = q_docs[d]['desc']
        q_docs[d]['title'] = mod[tit]
        q_docs[d]['desc'] = mod[desc]

def get_data(mode = 'train',t_ = 'tfidf',n_ = 64):
    if mode == 'train':
        docs_direc = 'data/bow/train_docs_bow_5'
        q_direc = 'data/bow/q_bow_5'
        dct_direc = 'data/dcts/dict5'
        
        print 'Loading Dictionary'
        dct = gensim.corpora.Dictionary.load(dct_direc)
        
        print 'Loading Model',str(t_),str(n_)
        mod = load_model(t = t_,n = n_)
        
        print 'Loading Data from',str(docs_direc)
        with open(docs_direc,'rb') as f:
            d = pickle.load(f)

        print 'Loading querries from',str(q_direc)
        with open(q_direc,'rb') as f:
            q = pickle.load(f)

    else:
        docs_direc = 'data/raw/test_docs_stemmed.pickle'
        q_direc = 'data/raw/test_querry_results_stemmed.pickle'
        dct_direc = 'data/dcts/dict5'
    
        print 'Loading Dictionary'
        dct = gensim.corpora.Dictionary.load(dct_direc)
    
        print 'Loading Model',str(t_),str(n_)
        mod = load_model(t = t_,n = n_)
        
        print 'Loading Data from',str(docs_direc)
        with open(docs_direc,'rb') as f:
            d = pickle.load(f)

        print 'Loading querries from',str(q_direc)
        with open(q_direc,'rb') as f:
            q = pickle.load(f)

        print 'Creating bow'
        transform_bow(d,q,dct)
        
    return d,q,mod

def get_top(q, docs, mod, n = 10,m = 160):
    
    k = docs.keys()
    mod_k = random.sample(k,m)
    print str(len(q['results']))
    test_doc_ids = []
    for d_id in mod_k:
        if d_id not in q['results']:
            test_doc_ids.append(d_id)
    test_doc_ids += q['results'].keys()
    print len(test_doc_ids)
    
    res = k_top(n)
    q_title = mod[q['desc']]
    for i in test_doc_ids:
        doc = docs[i]
        try:
            doc_title = mod[doc['abstract']]
        except:
            doc_title = mod[doc['title']]
        temp = compute_sim(q_title,doc_title)
        if temp != -1:
            res.add(i,temp)
    return res.items
