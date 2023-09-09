import argparse
import rdflib
from rdflib import Graph, RDFS,Literal
import ask
import pandas as pd


#def get_row(answer_filename,i):
#	data_file = open(answer_filename, "a")
#	data_file.close()
#	data_file = pd.read_csv(answer_filename, delimiter=',', header=None)
#	keywordss = data_file.iloc[:, :]
#	keywords = keywordss.iloc[i]
#	while len(str(keywords))!=0:
#	    i+=1
#	    keywords = keywordss.iloc[i]
#	return i

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-dataset", "--dataset", dest = "dataset", default = "DY-NB", help="Dataset name")
	parser.add_argument("-newdataset", "--newdataset", dest = "newdataset", default = "augument/DY-NB-a", help="New dataset name")
	args = parser.parse_args()
	
	### Defined variables ### 
	KB1 = "dbp"
	if args.dataset == "DW-NB":
		KB2 = "wd"
	else:
		KB2 = "yago"
	#SEED_RATIO = args.seed
	DATASET = args.dataset
	NEW_DATASET = args.newdataset
	PATH = "/home/wyf/atest"

	### Load data ###
	#dbp_filename = PATH+'/DWY-NB/'+DATASET+'/'+KB1+'_'+KB2+'.ttl'
	new_dbp_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB1+'_'+KB2+'.ttl'
	txt_dbp_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB1+'_'+KB2+'_txt_t.ttl'
	un_dbp_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB1+'_'+KB2+'_un.ttl'
	#res_dbp_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB1+'_'+KB2+'_res.ttl'
	#kb2_filename = PATH+'/DWY-NB/'+DATASET+'/'+KB2+'.ttl'
	new_kb2_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB2+'.ttl'
	#res_kb2_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB2+'_res.ttl'
	txt_kb2_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB2+'_txt_t.ttl'
	un_kb2_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB2+'_un.ttl'
	#map_filename = PATH+'/DWY-NB/'+DATASET+'/mapping_'+KB2+'.ttl'
	#seed_filename = PATH+'/DWY-NB/'+DATASET+'/seed_'+SEED_RATIO+'.ttl'
	log_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/conversation_log.txt'
	answer_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/answer.txt'

	txt_dbp_graph = Graph()
	txt_dbp_graph.parse(location=txt_dbp_filename, format='nt')
	#res_dbp_graph = Graph()
	#res_dbp_graph.parse(location=res_dbp_filename, format='nt')
	txt_kb2_graph = Graph()
	txt_kb2_graph.parse(location=txt_kb2_filename, format='nt')
	#res_kb2_graph = Graph()
	#res_kb2_graph.parse(location=res_kb2_filename, format='nt')


    ### Get attribute set ###   
	new_dbp_graph = Graph()
	new_kb2_graph = Graph()
	un_dbp_graph = Graph()
	un_kb2_graph = Graph()
	
	
	for triple in txt_dbp_graph:
		s, p, o = triple
		#i=get_row(answer_filename,i)
		answers = ask.get_xinghuo_answers(o,log_filename,answer_filename)
		#print(answers)
		if(len(answers)!=10):
			print(o+' 未获得十个关键词，跳过该三元组')
			un_dbp_graph.add((s,p,o))
			continue
		else:
		    for answer in answers:
			    answer_literal=Literal(answer)
			    new_dbp_graph.add((s,p,answer_literal))
	
	for triple in txt_kb2_graph:
		s, p, o = triple
		#i=get_row(answer_filename,i)
		answers = ask.get_xinghuo_answers(o,log_filename,answer_filename)
		#print(answers)
		if(len(answers)!=10):
			print(o+' 未获得十个关键词，跳过该三元组')
			un_kb2_graph.add((s,p,o))
			continue
		else:
		    for answer in answers:
			    answer_literal=Literal(answer)
			    new_kb2_graph.add((s,p,answer_literal))
	    
	fw1 = open(new_kb2_filename, 'w')
	for s,p,o in new_kb2_graph:
		fw1.write('<'+str(s)+'> <'+str(p)+'> '+str(o)+' .\n')
	fw1.close()
	print("new_kb2_graph: ", len(new_kb2_graph))
	
	fw2 = open(new_dbp_filename, 'w')
	for s,p,o in new_dbp_graph:
		fw2.write('<'+str(s)+'> <'+str(p)+'> '+str(o)+' .\n')
	fw2.close()
	print("new_dbp_graph: ", len(new_dbp_graph))

	fw3 = open(un_kb2_filename, 'w')
	for s,p,o in un_kb2_graph:
		fw3.write('<'+str(s)+'> <'+str(p)+'> '+str(o)+' .\n')
	fw3.close()
	print("un_kb2_graph: ", len(un_kb2_graph))

	fw4 = open(un_dbp_filename, 'w')
	for s,p,o in un_dbp_graph:
		fw4.write('<'+str(s)+'> <'+str(p)+'> '+str(o)+' .\n')
	fw4.close()
	print("un_dbp_graph: ", len(un_dbp_graph))
