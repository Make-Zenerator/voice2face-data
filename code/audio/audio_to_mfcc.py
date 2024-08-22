import os
import numpy as np
import scipy.io.wavfile as wav
from python_speech_features import mfcc
import matplotlib.pyplot as plt
import multiprocessing
import threading

def extract_save_mfcc(audio_path, output_image_path, n_mfcc=13):
    """
    음성 데이터셋을 통해 MFCC를 추출하고, 해당 이미지 저장할 코드

    Args:
        audio_path (str): Mel spectrogram으로 변환할 음성 데이터 경로
        output_image_path (str): 변환된 결과 이미지를 저장할 경로
        n_mfcc (int, optional): 생성할 MFCC 개수. Defaults to 13.

    Raises:
        Exception: 파일을 처리하는 도중 오류가 발생할 경우 예외 발생
    """    

    
    try:
        # 오디오 파일 로드
        rate, signal = wav.read(audio_path)
        
        # MFCC 계산
        mfcc_features = mfcc(signal, rate, numcep=n_mfcc)
        
        # MFCC 이미지 저장
        plt.figure(figsize=(10, 4))
        plt.imshow(mfcc_features.T, aspect='auto', cmap='viridis')
        plt.axis('off')
        plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)
        # print(output_image_path)
        plt.close()
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")

def worker(semaphore, args):
    with semaphore:
        extract_save_mfcc(*args)

if __name__ == "__main__":
    base_path = "/home/data/data_OLKAVS/OLKAVS/data"
    n_mfcc = 13  # MFCC 개수 설정
    max_processes = 16  # 동시에 실행할 최대 프로세스 수

    person_list = os.listdir(base_path)
    person_path_list = [os.path.join(base_path, name) for name in person_list]
    
    tasks = []

    for folder_path in person_path_list[::-1]:
        if os.path.isdir(folder_path):
            folder_audio_path = os.path.join(folder_path, "audio")
            folder_mfcc_image_path = os.path.join(folder_path, "mfcc_image")
            os.makedirs(folder_mfcc_image_path, exist_ok=True)

            folder_audio_list = os.listdir(folder_audio_path)
            folder_audio_path_list = [os.path.join(folder_audio_path, name) for name in folder_audio_list]
            folder_mfcc_image_path_list = [os.path.join(folder_mfcc_image_path, os.path.splitext(name)[0] + ".png") for name in folder_audio_list]

            for mi_path, a_path in zip(folder_mfcc_image_path_list, folder_audio_path_list):
                tasks.append((a_path, mi_path, n_mfcc))

    # 멀티프로세싱 세마포어 설정
    semaphore = threading.Semaphore(max_processes)
    processes = []

    for task in tasks:
        p = multiprocessing.Process(target=worker, args=(semaphore, task))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()