import os
import pandas as pd

# CSV 파일에서 링크 읽어오기
csv_file_path = "/Users/imseohyeon/Documents/crawling/data/Youtube_search_df.csv"
df = pd.read_csv(csv_file_path)

# 다운로드한 영상들이 저장된 폴더 경로
DOWNLOAD_FOLDER = "/Users/imseohyeon/Documents/crawling/download/"

# 폴더 내의 모든 파일을 확인하여 이름 변경
for filename in os.listdir(DOWNLOAD_FOLDER):
    # 파일의 전체 경로
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    # 파일이 .mp4인지 확인
    if filename.endswith(".mp4"):
        # 파일 이름에서 index 값을 추출 (영상의 title이 index로 저장된 것으로 가정)
        idx = filename.split("_")[0]  # 예시: "0_video.mp4" -> "0"
        # 새로운 파일 이름 생성
        new_filename = f"{idx}_video.mp4"
        # 새로운 파일 경로 생성
        new_file_path = os.path.join(DOWNLOAD_FOLDER, new_filename)
        # 파일 이름 변경
        os.rename(file_path, new_file_path)
        print(f"파일 이름 변경: {filename} -> {new_filename}")
