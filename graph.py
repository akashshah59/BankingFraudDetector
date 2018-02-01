from __future__ import print_function
from neo4j.v1 import GraphDatabase


uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))


def get_paths(name,all,temp,target,source_count,all_source,leaf):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for record in tx.run("MATCH (n) where n.name={leaf} return n",leaf=leaf):
                if(list(record[0].labels)!= []):
                    leaff=list(record[0].labels)[0]
            q="MATCH p=(Customer {name:'"+name+"'})-[*]->(:"+leaff+") WITH EXTRACT(x IN RELATIONSHIPS(p)|x) AS result return result"
            for record in tx.run(q):
                rec=[str(record[0][i].type) for i in range(0,len(record[0]))]
                if(rec not in all_source):
                    all_source=all_source+[rec]
                Query="MATCH p=(Customer)-"
                for i in range(0,len(rec)):
                    if(i==len(rec)-1):
                        Query+="[:"+rec[i]+"]-"
                    else:
                        Query+="[:"+rec[i]+"]-()-"
                Query = Query + "(:"+leaff+")   WHERE Customer.name={id1} RETURN DISTINCT Customer.name"
                for result in tx.run(Query,id1=target):
                    rec_string=""
                    for i in range(0,len(rec)):
                        if(i==len(rec)-1):
                            rec_string+=rec[i]
                        else:
                            rec_string+=rec[i]+"->"
                    if(rec_string not in temp):
                        all=all+[str(str(result[0]) + "|Follows Path " + rec_string + "|1")]
                        temp+=[rec_string]
                        #print(rec_string)
                Final=[]
                for elem in all:
                    Final+=[elem.split('|')]
                l=[filter(lambda x: target in x[0], Final),len(all_source)]
    return l

def getCustomers(all):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for record in tx.run("MATCH (n:Customer) return DISTINCT n.name"):
                if(record[0] != None):
                    all=all+[record[0]]
            for record in tx.run("MATCH (m:Organization) return DISTINCT m.name"):
                if(record[0] != None):
                    all=all+[record[0]]
    return all

def getTargets(all,option,source):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            if(option == 'country'):
                country=""
                for record in tx.run("MATCH (n:Customer {name:{name}}) return n.citizenship",name=source):
                    country=record[0]
                for record in tx.run("MATCH (n:Customer {citizenship:{country}}) return DISTINCT n.name",country=country):
                    if(record[0] != None):
                        all=all+[record[0]]
                    for record in tx.run("MATCH (m:Organization{location:{country}}) return DISTINCT m.name",country=country):
                        if(record[0] != None and record[0] not in all):
                            all=all+[record[0]]
            elif(option == 'occupation'):
                occupation=""
                for record in tx.run("MATCH (n:Customer {name:{name}}) return n.occupation",name=source):
                    occupation=record[0]
                for record in tx.run("MATCH (n:Customer {occupation:{occupation}}) return DISTINCT n.name",occupation=occupation):
                    if(record[0] != None and record[0] not in all):
                        all=all+[record[0]]
            else:
                asset=[]
                for record in tx.run("MATCH (n:Customer {name:{name}})--(m:ASSET) return m.name",name=source):
                #MATCH (n:Customer {name:'Lionel Messi'})--(m:ASSET) return m.name
                    if(str(record[0]) not in asset):
                        asset+=[str(record[0])]
                for elem in asset:
                    for record in tx.run("MATCH (n:Customer)--(ASSET {name:{ast}}) where n.name IS NOT NULL return DISTINCT n.name",ast=str(elem)):
                        if(record[0] != None and record[0] not in all):
                            all=all+[record[0]]
    return all

def getAll(all):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for record in tx.run("MATCH (n) return DISTINCT n.name"):
                if(str(record[0]) != None and str(record[0])!="null" and str(record[0])!="None" and str(record[0]) not in all):
                    all=all+[str(record[0])]
    print(all)
    return all
