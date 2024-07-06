import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split

def def_data_class(age,noise,gender):
    data_class = int(age)-1
    data_class = (int(noise) -1) * 6
    if gender == "F":
        data_class += 36
        print(int(age)-1,(int(noise) -1) * 6,36)
        print(data_class)
    elif gender == "M":
        print(int(age)-1,(int(noise) -1) * 6,0)
        print(data_class)
    return data_class



if __name__ == "__main__":
    train_data_list = []
    val_data_list = []
    test_data_list = []
    data_name_list = []
    data_label_list = []
    data_type_dict = {}
    # make new image folder path and dir
    new_mfcc_image_folder_path = "./data/mfcc_image"
    new_face_image_folder_path = "./data/face_image"
    os.makedirs(new_face_image_folder_path,exist_ok=True)
    os.makedirs(new_mfcc_image_folder_path,exist_ok=True)

    base_path = "/home/data/data_OLKAVS/OLKAVS/data"
    person_list = os.listdir(base_path)
    person_path_list = [os.path.join(base_path,name)for name in person_list]
    for folder_path in person_path_list:
        if os.path.isdir(folder_path):
            folder_name = os.path.basename(folder_path)
            
            _,video_env,audio_noise,gender,age,specificity = folder_name.split("_")
            speakerID = specificity[0:]
            specificity = specificity[0]
            data_name_list.append(folder_name)
            data_class = def_data_class(age,audio_noise,gender)
            data_label_list.append(data_class)
    name_train,name_valid, class_train,class_valid= train_test_split(data_name_list,data_label_list,stratify = data_label_list,test_size=0.2,random_state=42)
    name_valid,name_test, class_valid,class_train= train_test_split(name_valid,class_valid,stratify = class_valid,test_size=0.5,random_state=42)
    for name in name_train:
        data_type_dict[name] = 0
    for name in name_valid:
        data_type_dict[name] = 1
    for name in name_test:
        data_type_dict[name] = 2
    

    #copy image to new folder & make image information
    for folder_path in person_path_list:
        if os.path.isdir(folder_path):
            folder_name = os.path.basename(folder_path)
            image_name = folder_name+".png"
            #copy face image to new face_image_folder
            face_image_path= os.path.join(folder_path , image_name)
            new_face_image_path = os.path.join(new_face_image_folder_path,image_name)
            shutil.copyfile(face_image_path,new_face_image_path)

            folder_mfcc_image_path = os.path.join(folder_path,"mfcc_image")
            # print(folder_name.split("_"))
            
            _,video_env,audio_noise,gender,age,specificity = folder_name.split("_")
            speakerID = specificity[0:]
            specificity = specificity[0]
            
            for mfcc_image_name in os.listdir(folder_mfcc_image_path):
                new_mfcc_image_path = os.path.join(new_mfcc_image_folder_path,folder_name+"_"+mfcc_image_name)
                shutil.copyfile(os.path.join(folder_mfcc_image_path, mfcc_image_name),new_mfcc_image_path)
                if data_type_dict[folder_name] == 0:
                    train_data_list.append([new_mfcc_image_path,new_face_image_path,video_env,audio_noise,gender,age,specificity,speakerID])
                elif data_type_dict[folder_name] == 1:
                    val_data_list.append([new_mfcc_image_path,new_face_image_path,video_env,audio_noise,gender,age,specificity,speakerID])
                elif data_type_dict[folder_name] == 2:
                    test_data_list.append([new_mfcc_image_path,new_face_image_path,video_env,audio_noise,gender,age,specificity,speakerID])

    df = pd.DataFrame(train_data_list, columns=[
    'mfcc_image_path',
    'face_image_path',
    'video_env',
    'audio_noise',
    'gender',
    'age',
    'specificity',
    'speakerID'
    ])
    df.to_csv("./OLKVS_train_dataset.csv",index=False)
    df = pd.DataFrame(val_data_list, columns=[
        'mfcc_image_path',
        'face_image_path',
        'video_env',
        'audio_noise',
        'gender',
        'age',
        'specificity',
        'speakerID'
    ])
    df.to_csv("./OLKVS_valid_dataset.csv",index=False)
    df = pd.DataFrame(test_data_list, columns=[
        'mfcc_image_path',
        'face_image_path',
        'video_env',
        'audio_noise',
        'gender',
        'age',
        'specificity',
        'speakerID'
    ])
    df.to_csv("./OLKVS_test_dataset.csv",index=False)

