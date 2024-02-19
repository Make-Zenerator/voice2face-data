import os
import pandas as pd
from pytube import YouTube
import time

# CSV 파일에서 링크 읽어오기
csv_file_path = "/Users/imseohyeon/Documents/crawling/data/Youtube_search_df.csv"
df = pd.read_csv(csv_file_path)

# 다운로드할 폴더 경로 정의
DOWNLOAD_FOLDER = "/Users/imseohyeon/Documents/crawling/download/"

# 폴더가 없다면 생성
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# 각 영상에 대해 반복하며 다운로드
for idx, row in df.iterrows():
    video_url = row['url_link']
    try:
        # Pytube를 사용하여 영상 정보 가져오기
        yt = YouTube(video_url)
        length_seconds = yt.length

        # 파일 이름 설정
        filename = f"{idx}_video.mp4"

        # 영상 길이가 5분 이상이면 처음 5분까지만 다운로드
        if length_seconds > 5 * 60:
            print(f"{yt.title} 영상이 5분을 초과합니다. 처음 5분만 다운로드합니다.")
            stream = yt.streams.filter(adaptive=True, file_extension='mp4').first()
            if stream:
                print(f"다운로드 중: {yt.title}")
                stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
                print(f"{yt.title} 다운로드 완료")
            else:
                print(f"{yt.title}에 대한 최고 품질 스트림이 없습니다.")
        else:
            # 5분 이하의 영상은 전체를 다운로드
            stream = yt.streams.get_highest_resolution()
            if stream:
                print(f"다운로드 중: {yt.title}")
                stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
                print(f"{yt.title} 다운로드 완료")
            else:
                print(f"{yt.title}에 대한 최고 품질 스트림이 없습니다.")
    except Exception as e:
        print(f"{yt.title} 다운로드 실패: {e}")
