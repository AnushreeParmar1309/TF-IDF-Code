
# coding: utf-8

# In[35]:


import sys
#Read the file
filepath = sys.argv[1]
postingLists={}
with open(filepath) as filepath:
    l= filepath.readline()
    count=0
    countofDocument=0
    docCount={}
    while l:
        words=l.split()
        docid=words[0]
        docCount[docid]=len(words)-1
        countofDocument+=1
        for i in range(1, len(words)):
            if(words[i] in postingLists.keys()):
                postingLists[words[i]].append(docid)
            else:
                postingLists[words[i]]=[]
                postingLists[words[i]].append(docid)
        l=filepath.readline()
        count+=1
tf={}

for key in postingLists:
    newlist=list(set(postingLists[key]))
    tf[key]={}
    for i in (newlist):
        tf[key][i]=postingLists[key].count(i)/docCount[i]

for key in postingLists:
    postingLists[key]=list(sorted(set(postingLists[key])))

#Calculate IDF
idf={}
for key in postingLists:
    idf[key]=countofDocument/len(postingLists[key])
    


# In[36]:


def GetPostings(query):
    querywords=query.split()
    finalstr=""
    for word in querywords:
        finalstr+="GetPostings" + "\n"
        finalstr += word + "\n"
        s= " "
        s=s.join(postingLists[word])
        finalstr+= "Postings list: " + s + "\n"
    return finalstr


# In[37]:


def datAnd(query):
    querywords=query.split()
    
    if(len(querywords)==1):
        
        return postingLists[querywords[0]]
    result=postingLists[querywords[0]][:]
    comparison=0
    for i in range(1,len(querywords)):
        resultiterator=0
        pliterator=0
        plterm=postingLists[querywords[i]]
        while(resultiterator<len(result) and pliterator<len(plterm)):
            comparison+=1
            if(result[resultiterator]<plterm[pliterator]):
                result.remove(result[resultiterator])
            elif(result[resultiterator]==plterm[pliterator]):
                resultiterator+=1
                pliterator+=1
            else:
                pliterator+=1
                
            if(pliterator==len(plterm)):
                
                result=result[:resultiterator]
    
    res={}
    res["docs"]=result
    res["comparison"]=comparison
    return res

def datOr(query):
    comparison=0
    querywords=query.split()
    
    if(len(querywords)==1):
        return postingLists[querywords[0]]
    result=postingLists[querywords[0]][:]
    for i in range(1,len(querywords)):
        resultiterator=0
        pliterator=0
        plterm=postingLists[querywords[i]]
        tempresult=[]
        while(resultiterator<len(result) and pliterator<len(plterm)):
            comparison+=1
            if(result[resultiterator]<plterm[pliterator]):
                tempresult.append(result[resultiterator])
                resultiterator+=1
            elif(result[resultiterator]==plterm[pliterator]):
                tempresult.append(result[resultiterator])
                resultiterator+=1
                pliterator+=1
            else:
                tempresult.append(plterm[pliterator])
                pliterator+=1
                
            
        if(pliterator==len(plterm)):
            for j in range(resultiterator,len(result)):
                tempresult.append(result[j])   
        if(resultiterator==len(result)):
            for j in range(pliterator,len(plterm)):
                tempresult.append(plterm[j])       
                
        result=tempresult
    
    res={}
    res["docs"]=result
    res["comparison"]=comparison
    return res


def calculateScore(result, query):
    querywords=query.split()
    score={}
    for doc in result:
        score[doc]=0
    for words in querywords:
        for doc in result:
            if(doc in postingLists[words]):
                score[doc]+=(tf[words][doc]*idf[words])
    
    a=list(sorted(score,key=score.get,reverse=True))
    return a
        




# In[73]:


def writeDetails(query):
    finalString = GetPostings(query)
    #Add queries
    andData=datAnd(query)
    finalAnd="DaatAnd" + "\n"
    finalAnd+=query + "\n"
    st=" "
    if(len(andData["docs"])!=0):
        st=st.join(andData["docs"])
    else:
        st="empty"
    finalAnd+="Results: " + st +"\n"
    finalAnd+="Number of documents in results: " + str(len(andData["docs"])) + "\n"
    finalAnd+="Number of comparisons: " + str(andData["comparison"]) + "\n"
    finalAnd+="TF-IDF" + "\n"
    tfidf=calculateScore(andData["docs"],query)
    if(len(tfidf)==0):
        stif="empty"
    else:
        stif=" ".join(tfidf)
    finalAnd+="Results: " + stif + "\n"
    finalString += finalAnd
    orData=datOr(query)
    finalOr="DaatOr" + "\n"
    finalOr+=query + "\n"
    st=" "
    if(len(orData["docs"])!=0):
        st=st.join(orData["docs"])
    else:
        st="empty"
    finalOr+="Results: " + st +"\n"
    finalOr+="Number of documents in results: " + str(len(orData["docs"])) + "\n"
    finalOr+="Number of comparisons: " + str(orData["comparison"]) + "\n"
    finalOr+="TF-IDF" + "\n"
    tfidf=calculateScore(orData["docs"],query)
    if(len(tfidf)==0):
        stif="empty"
    else:
        stif=" ".join(tfidf)
    finalOr+="Results: " + stif + "\n"
    finalString+= finalOr +"\n"
    return finalString


# In[74]:


#Fetch Queries
foutput=sys.argv[2]
fpinput=sys.argv[3]

with open(fpinput) as fpinput:
    l= fpinput.readline()
    count=0
    countofDocument=0
    docCount={}
    while l:
        l=l.strip()
        fs=writeDetails(l)
        with open(foutput,"a") as f:
            
            f.write(fs)
        l=fpinput.readline()
        
        


# In[69]:


