from particule import Particule
import random
import numpy as np
from modifNEH import modif_NEH
import time





def read_data(filename):
    file = open(filename, "r")

    tasks_val, machines_val = file.readline().split()
    #print("tasks = ", tasks_val , "machines = ", machines_val)
    tasks_val = int(tasks_val)
    machines_val = int(machines_val)

    tasks = np.zeros((tasks_val,machines_val))
    for i in range(tasks_val):
        tmp = file.readline().split()
        for j in range(machines_val):
            tasks[i][j] = int(tmp[j])
    file.close()
    return tasks_val, machines_val, tasks

def compute_makespan(schedule, p):
    _, m = p.shape
    n = len(schedule)
    c = [[0]*m for i in range(n)]
    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                c[i][j] = p[schedule[i]][j]
            elif i == 0:
                c[i][j] = c[i][j-1] + p[schedule[i]][j]
            elif j == 0:
                c[i][j] = c[i-1][j] + p[schedule[i]][j]
            else:
                c[i][j] = max(c[i][j-1], c[i-1][j]) + p[schedule[i]][j]
    return c[n-1][m-1]

def initialise(num_particules, num_jobs):
    # initialiser X,Y,V
    particules = []
    X=[]
    for i in range (1,num_jobs+1):
        X.append(i)

    for j in range(num_particules-1):
        random.shuffle(X)
        l = X.copy()
        part = Particule(l)
        part.BestPersonal = l.copy()
        part.V=[0 for _ in range(20)]
        part.lambda_=[0 for _ in range(20)]
        part.ps=[0 for _ in range(20)]
        particules.append(part)
    return particules
if __name__ == "__main__": 
    upper = [1278, 1359,1088,1293,1236,1195,1239,1206,1230,1108]
    for p in [1]:

        n, m, data = read_data(f'data/instance_alea.txt')

        num_particules = 50
        n = 10 # jobs
        m=5 # machines
        c1= 0.8 # [0.1 , 0.2 , 0.3 ...] 1
        c2= 0.2 # [0.1 , 0.2 , 0.3 ...] 0.75
        # Best r1 = 0.14 , r2 = 0.09, num_particule =50
        r1=0.3
        r2= 0.9
        w = 0.75 # [0.5,0.55, 0.6, 0.65] 0.93
        alpha=0.4 # [0.1 , 0.2 , 0.3 ...]
                
        G_best = Particule()
        particules = initialise(num_particules,n)

        seq, _ = modif_NEH(data.T, m,n)
        part = Particule(seq)
        part.BestPersonal = seq.copy()
        part.V=[0 for _ in range(20)]
        part.lambda_=[0 for _ in range(20)]
        part.ps=[0 for _ in range(20)]
        particules.append(part)
        G_best.X = particules[-1].X.copy()


        start = time.time()

        for it in range(1000):
            for i in range (num_particules):
                # update the personal best position
                if(compute_makespan([p-1 for p in particules[i].X],data.T) < compute_makespan( [p-1 for p in particules[i].BestPersonal],data.T)):
                    #print('Best Personal got updated !')
                    particules[i].BestPersonal = particules[i].X.copy()
            
            # update the global best position
            for i in range(0,num_particules):
                if(compute_makespan([p-1 for p in particules[i].BestPersonal] ,data.T) < compute_makespan([p-1 for p in G_best.X] ,data.T)):
                    #print('seq BP = ',particules[i].BestPersonal , 'Cmax = ',_get_makespan(particules[i].BestPersonal,data,m) )
                    #print('seq GLOBAL = ',G_best.X , 'Cmax = ',_get_makespan(G_best.X,data,m) )
                    #print('Global got updated !')
                    end = time.time()
                    G_best.X= particules[i].BestPersonal.copy()
                    cc = compute_makespan([p-1 for p in G_best.X] ,data.T)
                    print('Instance = ',p+1 ,'| Cmax = ',cc, f"| deviation =  {(cc - upper[p])*100/upper[p]:.2f} %", 'time = ', (end-start) * 10**3)
            
            # update Yij
            for i in range(num_particules):
                # n est le nombre des jobs
                for j in range(n):
                    if (particules[i].X[j] == G_best.X[j]):
                        if(it==0):
                            particules[i].Y.append(1)
                        else:
                            particules[i].Y[j] = 1
                    elif (particules[i].X[j] == particules[i].BestPersonal[j]):
                        if(it==0):
                            particules[i].Y.append(-1)
                        else:
                            particules[i].Y[j] = -1
                    elif(particules[i].X[j] == particules[i].BestPersonal[j] ==G_best.X[j]):
                        if(it==0):
                            particules[i].Y.append(random.choice([-1, 1]))
                        else:
                            particules[i].Y[j] = random.choice([-1, 1])
                    else:
                        if(it==0):
                            particules[i].Y.append(0)
                        else:
                            particules[i].Y[j] = 0

            
            # update Vij
            for i in range(num_particules):
                # n est le nombre des jobs
                for j in range(n):
                    particules[i].V[j] = w*particules[i].V[j] + c1*r1*(-1-particules[i].Y[j]) + c2*r2*(1-particules[i].Y[j]) 
            

            # update Xij
            for i in range(num_particules):
                # n est le nombre des jobs
                for j in range(n):
                    particules[i].lambda_[j] = particules[i].V[j] + particules[i].Y[j] 
                    if(particules[i].lambda_[j]>alpha):
                        particules[i].Y[j] = 1
                    elif(particules[i].lambda_[j]<-alpha):
                        particules[i].Y[j] = -1  
                    else:
                        particules[i].Y[j] =0     
                    
            #initialisation de ps
            for i in range(num_particules):
                # n est le nombre des jobs
                for j in range(n):
                    #ps = pos te3 job j dans Xi (pos a partir de 1 ) 
                    #print(particules[i].X.index(j+1))
                    particules[i].ps[j] = particules[i].X.index(j+1)+1
                        
            for i in range(num_particules):
                # n est le nombre des jobs
                for j in range(n):
                    r=-1
                    if(particules[i].Y[j]==1):
                        r = particules[i].ps[G_best.X[j]-1]
                    elif(particules[i].Y[j]==-1):
                        r = particules[i].ps[particules[i].BestPersonal[j]-1]
                    else:
                        find = False
                        k = j
                        while (not find and k<n):
                            if(particules[i].X[k]!=particules[i].BestPersonal[j] and particules[i].X[k]!=G_best.X[j] ):
                                r = k+1
                                find=True
                            k = k+1

                    rand = random.uniform(0, 1)
                    if ((r>=j) or (rand >0.5) and (r!=-1)):
                            particules[i].X[j], particules[i].X[r-1] = particules[i].X[r-1] , particules[i].X[j]
                            particules[i].ps[particules[i].X[j]-1], particules[i].ps[particules[i].X[r-1]-1] = particules[i].ps[particules[i].X[r-1]-1] , particules[i].ps[particules[i].X[j]-1]
        
        
        end = time.time()
        #print('seq = ',G_best.X ,'Cmax = ',compute_makespan([p-1 for p in G_best.X] ,data.T))
        res = compute_makespan([p-1 for p in G_best.X] ,data.T)
        print('Instance = ',p+1 ,'| Cmax = ',res, f"| deviation =  {(res - upper[p])*100/upper[p]:.2f} %")

