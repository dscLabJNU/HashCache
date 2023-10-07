
#-*- coding=utf-8 -*-  
  

###较小规模的最大团问题  
import copy
  
def isConnected(u,v):
    if u==-1 or v==-1:###虚拟节点-1与所有的节点都相连  
        return 1  
    edge_points=E[u]  
    if v in edge_points:  
        return 1  
    else:  
        edge_points = E[v]  
        if u in edge_points:  
            return 1  
        else:  
            return 0  
  
def isConnectedAll(clique,v):#判断v是否和clique中所有节点相连  
    flag = 1  
    for i in clique:  
        if not isConnected(i,v):  
            flag =0  
            break  
    return flag  
  
class Step:  
    def __init__(self):  
        self.maxClique = [] #计算完毕时的解集（每个阶段的实际结果）  
        self.cliqueList = []#计算时用的解集  
        self.maxnC = 0  
    def maxCliqn(self):#计算当前阶段最大值  
        max = 0  
        for clique in self.cliqueList:  
            if max < len(clique):  
                max = len(clique)  
        return max  
    def isNew(self,clique): #判断一个解组合是否已经存在于该阶段的实际解集中  
        for cl in self.maxClique:#针对每个已存入的解集进行判断  
            diff = list(set(clique).difference(set(cl)))  # 取解的差集  
            if (len(diff)):  
                continue      #差集不为空，说明不同，继续循环  
            else:  
                return False  # 差集为空,说明有个解完全一样，返回False 
  
        return True  
  
    def updateMaxClique(self):#更新当前阶段的最大团数目  
        self.maxnC= self.maxCliqn()  
        for clique in self.cliqueList:  
            if(len(clique)==self.maxnC):  
                if self.isNew(clique):  
                    self.maxClique.append(clique)  
  
  
def main(args):
    global V, E
    V = args.get("V",[0, 1, 2, 3, 4]) 
    E = args.get("combination", [[1,3,4],[2,3,4],[4],[4],[]])
    if "No subset with given sum" in E:
        return {'body':{"result":"No solution, please try another sequence"}}
    n = len(V)  
    solutions = {}  
    for i in range(0,n):  
        solutions[i]= Step()    #初始化n个阶段  
    for v in V:  
       a = []  
       a.append(v)  
       solutions[0].cliqueList.append(a)  
    solutions[0].updateMaxClique()#设置初始值  
  
    for i in range(1,n):  
        #cliqList= solutions[i-1].maxClique  
        preData = solutions[i-1]  
        cliqList = preData.maxClique  
        preMax = preData.maxnC  
        for clique in cliqList:#针对前一阶段的每个clique求解  
            for v in V:#针对所有的点  
                tempclique = copy.deepcopy(clique)##必须使用深拷贝  
                if not v in tempclique:#如果该clique没有包含v  
                    if isConnectedAll(tempclique,v):#如果v与clique的所有点相连  
                        tempclique.append(v)#加入该点  
                        solutions[i].cliqueList.append(tempclique)#加入这个解  
        solutions[i].updateMaxClique()  
        if not len(solutions[i].maxClique):#如果已经找不到更多的点加入团，那么后面的也不用计算了（比如找不到4个的团，那么5个的团也没必要再尝试计算）  
            break  
  
    # for i in range(0,n):  
        # print("step"+str(i)+": "+str(solutions[i].maxClique))  
  
    for i in range(n-1,-1,-1):  
        solution = solutions[i]  
        if len(solution.maxClique):
            max_clique = solution.maxClique
            maxn = solution.maxnC  
            break 

    return {"body":{"result":{"num_clique":maxn, "clique":max_clique}}}

# print(main({}))