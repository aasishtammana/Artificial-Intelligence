import random
from os.path import exists
import os
def Generatelayout(x,y):
    wall='%'
    food='.'
    foodcount=0
    ghost='G'
    ghostlimit=3
    ghostcount=0
    powerup='o'
    pacman='P'
    emptyspace=' '
    layout=[]
    
    for i in range(0,x):
        row=[]
        for j in range(0,y):
            if i==0 or i==x-1:
                row.append(wall)
            elif j==0 or j==y-1:
                row.append(wall)
            else:
                rnum=random.randint(0, 99)
                if rnum<70:
                    row.append(emptyspace)
                elif rnum<75:
                    row.append(powerup)
                elif rnum<80:
                    row.append(food)
                    foodcount+=1
                elif rnum<83:
                    if ghostcount<ghostlimit:
                        row.append(ghost)
                        ghostcount+=1
                    else:
                        row.append(emptyspace)
                elif rnum<=90:
                    row.append(wall)
                elif rnum<=99:
                    row.append(food)
                    foodcount+=1
        layout.append(row) 
    whereghostgoesx=-1
    whereghostgoesx=-1
    wherefoodgoesx=-1
    wherefoodgoesy=-1
    if ghostcount==0:
        whereghostgoesx=random.randint(1, x-2)
        whereghostgoesy=random.randint(1, y-2)
        layout[whereghostgoesx][whereghostgoesy]=ghost

    if foodcount==0:
        wherefoodgoesx=random.randint(1, x-2)
        wherefoodgoesy=random.randint(1, y-2)
        while whereghostgoesx==wherefoodgoesx and wherefoodgoesy==whereghostgoesy :
            wherefoodgoesx=random.randint(1, x-2)
            wherefoodgoesy=random.randint(1, y-2)
        layout[wherefoodgoesx][wherefoodgoesy]=food
    wherepacmangoesx=random.randint(1, x-2)
    wherepacmangoesy=random.randint(1, y-2)
    while whereghostgoesx==wherepacmangoesx and wherepacmangoesy==whereghostgoesy or wherefoodgoesx==wherepacmangoesx and wherepacmangoesy==wherefoodgoesy :
        wherepacmangoesx=random.randint(1, x-2)
        wherepacmangoesy=random.randint(1, y-2)
    layout[wherepacmangoesx][wherepacmangoesy]=pacman
    
    return layout

def printlayout(layout, name):
    fileName = "layouts/generatedlayout" + name + ".lay"
    if exists(fileName):
        os.remove(fileName)
    with open(fileName,'a') as f:
        for i in layout:
            for j in i:
                print(j, end='', file=f)
            print("", file=f)

for i in range(0,20):
    x=random.randint(7, 15)
    y=random.randint(7, 15)
    printlayout(Generatelayout(x,y),str(i))