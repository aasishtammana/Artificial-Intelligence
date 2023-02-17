import os
layouts = os.listdir('./layouts')
print(layouts)
rates=[0.3]
for i in layouts:
    inst=0
    print('Starting for AprroxQ')
    os.system('python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor,inst='+str(inst)+' -x 2000 -n 2000 -l '+i)
    for j in rates:
        print('training layout:',i,', tdrate:',j, 'instace:' ,inst)
        
        print('Starting for TOS')
        os.system('python pacman.py -p TOSarsaAgent -a extractor=SimpleExtractor,tDRate='+str(j)+',inst='+str(inst)+' -x 2000 -n 2000 -l '+i)
        inst+=1