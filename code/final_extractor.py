from pytube import YouTube
import os
import ffmpeg
from getpass import getuser
import subprocess
import librosa
import soundfile as sf
from pydub import AudioSegment
import cv2
from facenet_pytorch import MTCNN
from moviepy.editor import VideoFileClip

class Download:
    '''
    파일을 변환하기 위해선 ffmpeg란 프로그램을 별도로 설치해 컴퓨터 환경변수 설정을 마쳐야 함.
    '''
    def __init__(self, link):
        # link 인자는 GUI에서 입력된 값을 받을 때 사용
        # 컴퓨터 이용자명을 받아서 다운로드 폴더를 기본 폴더로 지정
        self.parent_dir = f"/voice2face-data/code/file"
        self.yt = YouTube(link)

    def getVideoName(self):
        '''(GUI 버전) 비디오 이름을 내보내는 함수'''
        name = self.yt.title
        return name

    def downloadVideo(self):
        '''mp4 파일로 다운로드하는 함수'''
        # mp4 형태로 비디오 다운로드
        stream = self.yt.streams.filter(file_extension='mp4').first()
        stream.download(output_path=self.parent_dir, filename_prefix="video")
        return stream.default_filename   # 저장한 파일명 리턴

    def downloadAudio(self):
        '''mp3 파일로 다운로드하는 함수'''
        # mp3 형태로 오디오 다운로드
        stream = self.yt.streams.filter(only_audio=True).first()
        stream.download(output_path=self.parent_dir, filename_prefix="audio")
        return stream.default_filename   # 저장한 파일명 리턴

# Define paths
output_folder = "/Users/imseohyeon/Documents/voice2face-data/code/file/images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Download video
link = "https://youtu.be/2DnGKEeRB4g?si=93Cf_Mg2n53kSpGQ"
downloader = Download(link)
downloaded_video_file = downloader.downloadVideo()
downloaded_audio_file = downloader.downloadAudio()

# Extract audio from downloaded video
audio_file_path = os.path.join(downloader.parent_dir, f"audio_{os.path.splitext(downloaded_video_file)[0]}.mp3")
command = f"ffmpeg -i {os.path.join(downloader.parent_dir, downloaded_video_file)} -vn -acodec pcm_s16le -ar 44100 -ac 2 {audio_file_path}"
subprocess.call(command, shell=True)

# Initialize MTCNN for face detection
mtcnn = MTCNN()

# 2. 사람 음성부분 추출 
def detect_human_voice(audio_file): 
    # 오디오 파일에서 사람 음성부분을 감지하여 해당 인덱스 반환
    y, sr = librosa.load(audio_file, sr=None)
    voice_segments = librosa.effects.split(y, top_db=18)
    voice_indices = []
    for start, end in voice_segments:
        if end - start >= sr * 1:  # 1초 이상인 경우에만 추가
            voice_indices.extend(range(start, end))
    return voice_indices 

# 3. 음성부분만 모아 다시 저장. + 비디오도 이 간격 맞춰 다시 저장 
def save_detected_voice(audio_file, video_file, save_audio_file, save_video_file):
    # 감지된 사람 음성부분을 추출하여 저장
    y, sr = librosa.load(audio_file, sr=None)
    voice_indices = detect_human_voice(audio_file)
    combined_audio = y[voice_indices]
    sf.write(save_audio_file, combined_audio, sr)

    # 비디오도 해당 음성에 맞게 잘라서 저장
    audio_clip = AudioSegment.from_file(save_audio_file)
    video_clip = VideoFileClip(video_file)
    video_duration = int(video_clip.duration * 1000)  # 비디오의 길이를 정수로 변환
    if len(audio_clip) > video_duration:
        audio_clip = audio_clip[:video_duration]
    else:
        audio_clip += audio_clip[-1] * (video_duration - len(audio_clip))

    audio_clip.export(save_audio_file, format="mp3")
    video_clip.write_videofile(save_video_file, codec='libx264', audio_codec='aac')

# 4. 새로운 비디오에서 얼굴인식되는 부분중에 frame 추출 + frame에서도 256x256으로 얼굴 부분 bbox 맞춰 잘라 이미지 저장. 
def extract_frames_with_faces(video_file, output_folder):
    # 비디오 파일에서 프레임 추출하여 얼굴을 인식하고 이미지 저장
    cap = cv2.VideoCapture(video_file)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    success, frame = cap.read()
    while success:
        success, frame = cap.read()
        frame_count += 1
        if frame_count % (10 * frame_rate) == 0:  # 10초마다 프레임 추출
            try:
                boxes, _ = mtcnn.detect(frame)
                if boxes is not None:
                    for i, box in enumerate(boxes):
                        x, y, w, h = [int(coord) for coord in box]
                        face_image = frame[y:y+h, x:x+w]
                        cv2.imwrite(os.path.join(output_folder, f"{frame_count}_{i}.png"), face_image)
            except Exception as e:
                print(f"Failed to detect face in frame {frame_count}: {e}")
    cap.release()

# Convert audio file to MP3 format
converted_audio_file_path = os.path.splitext(audio_file_path)[0] + ".mp3"
AudioSegment.from_file(audio_file_path).export(converted_audio_file_path, format="mp3")

# Create necessary folders
for folder in [output_folder, os.path.dirname(converted_audio_file_path)]:
    os.makedirs(folder, exist_ok=True)

# Step 2: Save the detected human voice segment and corresponding video
save_detected_voice(converted_audio_file_path, os.path.join(downloader.parent_dir, downloaded_video_file), converted_audio_file_path, trimmed_video_file_path)

# If no human voice segments are detected, delete the corresponding video file
if not os.path.exists(converted_audio_file_path):
    os.remove(trimmed_video_file_path)
else:
    # Step 3: Extract frames with detected faces every 10 seconds
    extract_frames_with_faces(trimmed_video_file_path, output_folder)

print("작업이 완료되었습니다.")
