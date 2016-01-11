import nltk.stem as ns
import string
import pickle

def stem_sent(st):
	'''
	Function to return the stemmed version of a sentence
	'''
	stemmer = ns.PorterStemmer()
	sent = st.translate(string.maketrans("",""), string.punctuation).lower().split()
	res = ''
	for word in sent:
		res += stemmer.stem(word)+' '
	return res[:-1]

def stem_docs(docs,q_docs):
    stemmed_docs = {}
    stemmed_qdocs = {}
    
    for d in docs:
        temp = {}
        try:
            abst = docs[d]['abstract']
            temp['abstract'] = stem_sent(abst)
        except:
            poi = 2
        tit = docs[d]['title']
        temp['title'] = stem_sent(tit)
        stemmed_docs[d] = temp
      
    for d in q_docs:
    	temp = {}
        try:
            tit = q_docs[d]['title']
            desc = q_docs[d]['desc']
            temp['title'] = stem_sent(tit)
            temp['desc'] = stem_sent(desc)
        except:
            print d
        temp['results'] = {}
        stemmed_qdocs[d] = temp
    return stemmed_docs,stemmed_qdocs


docs_direc = 'data/raw/test_data.pickle'
q_direc = 'data/raw/querry_content.pickle'

print 'Loading Data'
with open(docs_direc,'rb') as f:
    d = pickle.load(f)

print 'Loading querries'
with open(q_direc,'rb') as f:
    q = pickle.load(f)

k = d.keys()
print d[k[0]]

a,b = stem_docs(d,q)

print a[k[0]]

docs_direc = 'data/raw/test_docs_stemmed.pickle'
q_direc = 'data/raw/test_querry_content_stemmed.pickle'

print 'saving Data'
with open(docs_direc,'wb') as f:
    pickle.dump(a,f)

print 'saving querries'
with open(q_direc,'wb') as f:
    pickle.dump(b,f)



