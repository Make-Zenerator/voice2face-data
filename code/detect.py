import os
import pandas as pd
from moviepy.editor import VideoFileClip
import numpy as np
import face_recognition
import shutil

# 얼굴이 감지된 영상의 오디오를 추출하는 함수
def extract_audio_with_face(video_clip, start_time, end_time):
    audio = video_clip.audio.subclip(start_time, end_time)
    return audio

# 주어진 영상에서 얼굴이 감지된 구간의 오디오를 추출하는 함수
def extract_audio_with_faces(video_clip, face_detections):
    # 얼굴이 감지된 부분의 오디오를 모아서 저장할 리스트
    audio_clips = []

    # 각 얼굴 감지된 구간에서 오디오를 추출하여 리스트에 추가
    for start_time, end_time in face_detections:
        audio_clip = extract_audio_with_face(video_clip, start_time, end_time)
        audio_clips.append(audio_clip)

    # 오디오 클립들을 합쳐서 하나의 오디오 클립으로 반환
    final_audio = np.concatenate([clip.to_soundarray() for clip in audio_clips])
    return final_audio

# 얼굴 감지 함수
def detect_faces(video_clip):
    frames = [frame for frame in video_clip.iter_frames()]
    frame_rate = video_clip.fps
    frame_times = np.arange(len(frames)) / frame_rate

    # 얼굴 감지된 구간의 시작 및 끝 시간을 저장할 리스트
    face_detections = []

    # 각 프레임에 대해 얼굴 감지 수행
    for i, frame in enumerate(frames):
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            start_time = frame_times[max(0, i - 1)]
            end_time = frame_times[min(len(frames) - 1, i + 1)]
            face_detections.append((start_time, end_time))

    return face_detections

# 새로운 영상을 생성하는 함수
def create_new_video(video_clip, face_detections, output_path):
    # 새로운 비디오 클립 초기화
    new_video_clip = None

    # 얼굴이 감지된 구간에서만 비디오를 추출하여 새로운 비디오 클립에 추가
    for start_time, end_time in face_detections:
        subclip = video_clip.subclip(start_time, end_time)
        if new_video_clip is None:
            new_video_clip = subclip
        else:
            new_video_clip = new_video_clip.append(subclip)

    # 새로운 비디오 클립을 파일로 저장
    new_video_clip.write_videofile(output_path)

# CSV 파일에서 데이터 읽어오기
csv_file_path = "/Users/imseohyeon/Documents/crawling/data/Youtube_search_df.csv"
df = pd.read_csv(csv_file_path)

# 다운로드된 영상 파일들이 저장된 폴더 경로
DOWNLOAD_FOLDER = "/Users/imseohyeon/Documents/crawling/download/"
# 새로운 폴더 경로
NEW_FOLDER = "/Users/imseohyeon/Documents/crawling/processed_videos/"

# 새로운 폴더 생성
if not os.path.exists(NEW_FOLDER):
    os.makedirs(NEW_FOLDER)

# 각 영상에 대해 반복하며 얼굴 감지된 구간의 영상과 오디오를 추출하고 새로운 영상 생성
for idx, row in df.iterrows():
    video_filename = f"{idx}_video.mp4"
    video_path = os.path.join(DOWNLOAD_FOLDER, video_filename)

    if os.path.exists(video_path):
        try:
            # 영상 클립 생성
            video_clip = VideoFileClip(video_path)

            # 얼굴 감지 수행
            face_detections = detect_faces(video_clip)

            if face_detections:
                # 얼굴이 감지된 구간의 오디오 추출
                final_audio = extract_audio_with_faces(video_clip, face_detections)

                # 새로운 영상 생성
                output_path = os.path.join(NEW_FOLDER, f"{idx}_new_video.mp4")
                create_new_video(video_clip, face_detections, output_path)

                print(f"{video_filename}에 대한 처리 완료")
            else:
                print(f"{video_filename}에서 얼굴을 감지할 수 없습니다.")
        except Exception as e:
            print(f"{video_filename} 처리 중 오류 발생: {e}")
    else:
        print(f"{video_filename} 파일이 존재하지 않습니다.")

# 다 처리된 영상을 다른 폴더에 옮기기
processed_files = os.listdir(NEW_FOLDER)
for file in processed_files:
    shutil.move(os.path.join(NEW_FOLDER, file), DOWNLOAD_FOLDER)

print("모든 영상 처리 완료")
