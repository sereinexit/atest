import argparse
import rdflib
from rdflib import Graph, RDFS
	
def get_attr_set(graph):
	attr_set = set()
	for triple in graph:
		s,p,o = triple	
		if isinstance(o, rdflib.Literal):
			attr_set.add(p)
	return attr_set
def get_txtclass(str):
	num_strings = ["0","1","2","3","4","5","6","7","8","9"]
	for string in num_strings:
		if string in str:
			return False
	return True

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-seed", "--seed", dest = "seed", default = "30", help="Seed ratio")
	parser.add_argument("-dataset", "--dataset", dest = "dataset", default = "DY-NB", help="Dataset name")
	parser.add_argument("-newdataset", "--newdataset", dest = "newdataset", default = "augument/DY-NB-a", help="New dataset name")
	args = parser.parse_args()
	
	### Defined variables ### 
	KB1 = "dbp"
	if args.dataset == "DW-NB":
		KB2 = "wd"
	else:
		KB2 = "yago"
	SEED_RATIO = args.seed
	DATASET = args.dataset
	NEW_DATASET = args.newdataset
	PATH = "/home/wyf/atest"

	### Load data ###
	dbp_filename = PATH+'/DWY-NB/'+DATASET+'/'+KB1+'_'+KB2+'.ttl'
	#new_dbp_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB1+'_'+KB2+'.ttl'
	txt_dbp_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB1+'_'+KB2+'_txt.ttl'
	res_dbp_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB1+'_'+KB2+'_res.ttl'
	kb2_filename = PATH+'/DWY-NB/'+DATASET+'/'+KB2+'.ttl'
	#new_kb2_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB2+'.ttl'
	res_kb2_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB2+'_res.ttl'
	txt_kb2_filename = PATH+'/DWY-NB/'+NEW_DATASET+'/'+KB2+'_txt.ttl'
	#map_filename = PATH+'/DWY-NB/'+DATASET+'/mapping_'+KB2+'.ttl'
	#seed_filename = PATH+'/DWY-NB/'+DATASET+'/seed_'+SEED_RATIO+'.ttl'

	dbp_graph = Graph()
	dbp_graph.parse(location=dbp_filename, format='nt')
	kb2_graph = Graph()
	kb2_graph.parse(location=kb2_filename, format='nt')


    ### Get attribute set ###   
	kb2_attrs = get_attr_set(kb2_graph)
	dbp_attrs = get_attr_set(dbp_graph)
	#new_dbp_graph = Graph()
	res_dbp_graph = Graph()
	txt_dbp_graph = Graph()
	#new_kb2_graph = Graph()
	res_kb2_graph = Graph()
	txt_kb2_graph = Graph()
	
	for triple in dbp_graph:
		s, p, o = triple
		if p in dbp_attrs:
		    if get_txtclass(o):
			    txt_dbp_graph.add(triple)
		    else:	
			    res_dbp_graph.add(triple)
		else:
			res_dbp_graph.add(triple)
		
	
	for triple in kb2_graph:
		s, p, o = triple
		if p in kb2_attrs:
		    if get_txtclass(o):
			    txt_kb2_graph.add(triple)
		    else:	
			    res_kb2_graph.add(triple)
		else:
		   res_kb2_graph.add(triple)
	
	fw1 = open(res_kb2_filename, 'w')
	for s,p,o in res_kb2_graph:
		fw1.write(str(s)+' '+str(p)+' '+str(o)+'\n')
	fw1.close()
	print("res_kb2_graph: ", len(res_kb2_graph))
	
	fw2 = open(txt_kb2_filename, 'w')
	for s,p,o in txt_kb2_graph:
		fw2.write('<'+str(s)+'> <'+str(p)+'> \"'+str(o)+'\" .\n')
	fw2.close()
	print("txt_kb2_graph: ", len(txt_kb2_graph))
	
	fw3 = open(res_dbp_filename, 'w')
	for s,p,o in res_dbp_graph:
		fw3.write(str(s)+' '+str(p)+' '+str(o)+'\n')
	fw3.close()
	print("res_dbp_graph: ", len(res_dbp_graph))

	fw4 = open(txt_dbp_filename, 'w')
	for s,p,o in txt_dbp_graph:
		fw4.write('<'+str(s)+'> <'+str(p)+'> \"'+str(o)+'\" .\n')
	fw4.close()
	print("txt_dbp_graph: ", len(txt_dbp_graph))





	
  