import pickle
import gensim

def make_vec(sparse_vec,n):
	res = [0]*n
	for i in sparse_vec:
		res[i[0]] = i[1]
	return res

print make_vec([(1,3),(5,10)],15)

doc_file = './data/bow/train_docs_bow_5'
dct_file = './data/dcts/filtered_dict_5'

dct = gensim.corpora.Dictionary.load(dct_file)
f_length = len(dct)

with open(doc_file,'rb') as f:
	docs = pickle.load(f)
print 'Documents loaded'
res = []
count = 0
m = 1
n = len(docs)
for i in docs:
	try:
		sparse_vec_abst = docs[i]['abstract']
	#sparse_vec_tit = docs[i]['title']
	except:
		pass
	temp = make_vec(sparse_vec_abst,f_length)
	res.append(temp)
	# temp = make_vec(sparse_vec_tit,f_length)
	# res.append(temp)
	count += 1.0
	if count/n == m*0.1:
		print str(m),'% done'
		m += 1


print len(res)
print len(res[0])

with open('fmat.pickle','wb') as f:
	pickle.dump(res,f)



