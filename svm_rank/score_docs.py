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

def get_ndcg(res_q): # (q, docs, n_ = 10):
    
    ideal_rank = sorted(res_q, key = lambda b:b[1], reverse = True)
    i_rank = [i[1] for i in ideal_rank]
    ideal_score = compute_dcg(i_rank)
    
    pred_rank = sorted(res_q, key = lambda b:b[0], reverse = True)
    p_rank = [i[1] for i in pred_rank]
    sys_score = compute_dcg(p_rank)
    
    res = sys_score/ideal_score
    return res

def get_score(pred_name,file_name):
	with open(file_name) as f:
		file_lines = f.readlines()

	with open(pred_name) as f:
		pred_lines = f.readlines()
	print str(len(file_lines)),str(len(pred_lines))

	res = {}
	for i in range(len(file_lines)):
		file_line_items = file_lines[i].strip().split()
		
		doc_id = file_line_items[-1]
		q_id = file_line_items[1]
		ideal_score = int(file_line_items[0])
		pred_score = float(pred_lines[i].strip())
		temp = (doc_id,ideal_score,pred_score)
		# temp[doc_id] = {'pred_score':pred_score,'ideal':ideal_score}
		if q_id not in res:
			res[q_id] = []
		res[q_id].append(temp)
	return res


a = get_score('pred','test_file.txt')
n = len(a)
acc = 0
for i in a:
	acc += get_ndcg(a[i])
print acc/n


