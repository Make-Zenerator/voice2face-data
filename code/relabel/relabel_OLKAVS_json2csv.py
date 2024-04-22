import json
import os
import csv

def write_csv(json_file: str, save_folder: str):

    count = 1

    f = open('data.csv','a', newline='')
    wr = csv.writer(f)

     # json 파일 열기
    with open(json_file, 'r') as f:
        data = json.load(f)
        data= data[0]

    folder_name = "_".join(data['Video_info']['video_Name'].split('.')[0].split('_')[:-2])
    file_name = data['Video_info']['video_Name'].split('_')[-1].split('.')[0]
    gender = data['Video_info']["video_Name"].split("_")[3]
    age = data['Video_info']["video_Name"].split("_")[2]
    noise = data['Audio_env']['Noise']
    
    for sentence_info in data['Sentence_info']:
        start_time = round(int(sentence_info['start_time']), 3)
        end_time = round(int(sentence_info['end_time']), 3)
        time = end_time - start_time
        if time <3 or time  > 10 :
            continue
        topic = sentence_info['topic']
        sentence = sentence_info['sentence_text']

        wr.writerow([folder_name,f"{file_name}-{count:03d}", gender,age,noise,topic,sentence])
        
        count += 1
    print(folder_name)


def find_json(json_folder:str, save_folder: str):

    for root,_,files in os.walk(json_folder):
        for file in files:
            if file.endswith('.json'):
                json_file = os.path.join(root, file)
                write_csv(json_file, save_folder)
                
def main(json_folder, save_folder):
    find_json(json_folder, save_folder)
    print("End of processing")


if __name__ == '__main__':  
    # JSON 파일이 들어있는 폴더 경로 
    json_folder = '/home/carbox/Desktop/data/009.립리딩(입모양) 음성인식 데이터/01.데이터/2.Validation/라벨링데이터'  
    # 원천데이터를 저장할 폴더 경로
    save_folder = '/home/carbox' 

    main(json_folder, save_folder)
