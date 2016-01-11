import gensim
import string
import pickle

##algo:
##    1 transform test data to bow
##    2 generate hdp fv and store them
##    3 pick a querry and compare it's compnents to querry vec'
##    4 pick out top 10 results
def make_fv(docs,q_docs,dct,model):
    '''
    docs - dict file of abstracts and titles of the form:
        docs[id]['abstract']-['titles']
    q_docs - dict file of querries of the form:
        q_docs[id]['desc']-['title']-['results'][doc_id][score]
    dct - dictionary used to make bow model
    model - model used
    '''
    print 'Featurizing documents'
    for d in docs:
        try:
            abst = docs[d]['abstract'].translate(string.maketrans("",""),string.punctuation).lower()
            abst = dct.doc2bow(abst.lower().split())
            docs[d]['abstract'] = mod[abst]
        except:
            tyui = 2
        tit = docs[d]['title'].translate(string.maketrans("",""),string.punctuation).lower()
        tit = dct.doc2bow(tit.lower().split())
        docs[d]['title'] = mod[tit]
    print 'Featurizing querries'
    for q in q_docs:
        desc = q_docs[q]['desc'].translate(string.maketrans("",""),string.punctuation).lower()
        title = q_docs[q]['title'].translate(string.maketrans("",""),string.punctuation).lower()

        q_docs[q]['desc'] = mod[dct.doc2bow(desc.lower().split())]
        q_docs[q]['title'] = mod[dct.doc2bow(title.lower().split())]
        q_docs[q]['results'] = {}
        
    print 'Saving data'
    with open('data/test_fv/docs.pickle','wb') as f:
        pickle.dump(docs,f)

    print 'Saving querries'
    with open('data/test_fv/querries.pickle','wb') as f:
        pickle.dump(q_docs,f)

    return docs,q_docs

mod = gensim.models.LdaModel.load('data/models/lda_5128')

print 'Loading data'
q = pickle.load(open('data/raw/querry_content.pickle','rb'))
d = pickle.load(open('data/raw/test_data.pickle','rb'))

dct_direc = 'data/dcts/filtered_dict_5'
dct = gensim.corpora.Dictionary.load(dct_direc)

d_fv,q_fv = make_fv(d,q,dct,mod)

    
