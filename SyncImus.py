from datetime import datetime, timedelta
from dateutil.parser import parse
import numpy as np

#THIS CODE WORKS FINE WITH METAMOTION R IMUs AND IT'S ADAPTABLE TO OTHERS
#IF THEY HAVE TIMESTAMP 

def sync_imus(imu_1,imu_2):
    #imu_1: Pandas DataFrame from csv file with first imu data
    #imu_2: Pandas DataFrame from csv file with second imu data
    
    fecha_1=[] #Obtain date from TimeStamp
    try:
        for i in imu_1['time (02:00)']:
            fecha_1.append(parse(i)+timedelta(hours=-1))
    except:
        for i in imu_1['time (02:00)']:
            i=i.replace('.',':',2)
            fecha_1.append(parse(i)+timedelta(hours=-1))

    fecha_2=[]
    try:
        for i in imu_2['time (02:00)']:
            fecha_2.append(parse(i)+timedelta(hours=-1))
    except:
        for i in imu_2['time (02:00)']:
            i=i.replace('.',':',2)
            fecha_2.append(parse(i)+timedelta(hours=-1))
            
    fechas_sync=[]
    index_sync=[]
    for i in fecha_1:
        dif_temp=[]
        for j in fecha_2:
            dif_temp.append(np.abs(i-j))

        min_indx=dif_temp.index(np.nanmin(dif_temp))

        index_sync.append([fecha_1.index(i), min_indx])
        fechas_sync.append([i,fecha_2[min_indx]])   
        
    return(index_sync) #returns a list of the indexes of each imu that correspond to each other
    
def ang_imus(imus_index, imu_1, imu_2):
    #imu_1: Pandas DataFrame from csv file with first imu data
    #imu_2: Pandas DataFrame from csv file with second imu data
    #imus_index: list from sync_imus funtion
    
    ang_dif=[]
    for i in imus_index:
        #This formula can be different to others angles
        ang_dif.append(180-(np.abs(imu_1['pitch (deg)'][i[0]])-np.abs(imu_2['pitch (deg)'])[i[1]]))
        
    return(ang_dif)