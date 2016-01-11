import gensim
import pickle
import random
import math
import time
import math

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
    try:
        res = res/temp
    except ZeroDivisionError:
        return -1
    return res

def get_top(q, docs, mod,m = 150):
    
    res = []
    k = docs.keys()
    mod_k = random.sample(k,m)
    
    test_doc_ids = []
    for d_id in mod_k:
        if d_id not in q['results']:
            test_doc_ids.append(d_id)
    test_doc_ids += q['results'].keys()
    
    
    q_title = mod[q['desc']]
    for i in test_doc_ids:
        doc = docs[i]
        try:
            doc_title = mod[doc['abstract']]
        except:
            doc_title = mod[doc['title']]
        sim_score = compute_sim(q_title,doc_title)
        if i in q['results']:
            res.append(((i,q['results'][i],sim_score)))
        else:
            res.append(((i,0,sim_score)))
    return res

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

def get_data(t_ = 'tfidf',n_ = 64):
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

    # print 'Transforming bow'
    # bow2mod(d,q,mod)

    return d,q,mod

def results(ndcg_val = 10):
    k = q_docs.keys()
    test_queries = k
    n_q = len(test_queries)
    avg = 0
    t = 0
    for j in test_queries:
        b =  q_docs[j]['results']
        # print 'Actual results',str(b)
        start = time.time()
        a = get_top(q_docs[j],docs,mod, m = 500)
        end = time.time()
        val = get_ndcg(a, n = ndcg_val)
        avg += val
        t += end - start
        
    return avg/n_q, t/n_q

def get_results(trials = 20, n = 10):
    res_val = 0
    res_time = 0
    for i in range(trials):
        val,time = results(ndcg_val = n)
        res_val += val
        res_time += time
    st = 'For n = '+str(n)+' ndcg is: '+str(res_val/trials)+' and time is: '+str(res_time/trials)
    print st


docs, q_docs, mod = get_data(t_ = 'lda',n_ = 64)
places = [1,3,5,10]
for p in places:
    print p
    get_results(trials = 1, n = p)