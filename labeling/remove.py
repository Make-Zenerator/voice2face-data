import os
import re
import tarfile

def extract_tar_if_needed(root_folder):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.tar'):
                tar_path = os.path.join(root, file)
                folder_name = os.path.splitext(tar_path)[0]
                if not os.path.exists(folder_name):
                    with tarfile.open(tar_path) as tar:
                        tar.extractall(path=root)
                    dirs.append(os.path.basename(folder_name))

def delete_files_except_patterns(root_folder, pattern):
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            # 파일명에서 패턴을 찾기 위해 정규표현식 사용
            if re.search(pattern, file):
                continue  # 해당 패턴이 있는 경우 건너뜁니다.
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"Deleted {file}")

def main(root_folder, pattern):
    extract_tar_if_needed(root_folder)
    delete_files_except_patterns(root_folder, pattern)
    print("End of processing")

if __name__ == '__main__':
    root_folder = '/home/carbox/Desktop/data/009.립리딩(입모양) 음성인식 데이터/01.데이터/2.Validation/라벨링데이터'
    pattern = r'.*_A_.*\.json'
    main(root_folder, pattern)
