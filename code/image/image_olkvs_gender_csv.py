import os 
import pandas as pd

base_path = "/home/data/data_OLKAVS/OLKAVS/data"
person_list = os.listdir(base_path)
person_path_list = [os.path.join(base_path,name)for name in person_list]
data_list=[]

for folder_path in person_path_list:
    if os.path.isdir(folder_path):
        print(os.path.basename(folder_path))
        image_sex = os.path.basename(folder_path).split("_")[3]
        data_list.append([os.path.join(folder_path,os.path.basename(folder_path)+".png"),image_sex])

df = pd.DataFrame(data_list, columns=['이미지주소', '이미지성별'])
df.to_csv("./OLKVS_gender.csv",index=False)
