# 사용할 dockerhub 이미지
FROM apache/airflow:2.7.3-python3.9

# 관리자 계정 사용
USER root

# airflow 실행에 필요한 패키지 설치
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# apache-airflow와 필수 라이브러리 설치
RUN pip install apache-airflow==2.8.1 \
    beautifulsoup4==4.12.3 \
    pytube==15.0.0 \
    requests==2.31.0 \
    SQLAlchemy==1.4.51 \
    numpy==1.26.4 \
    opencv-python==4.9.0.80 \
    pandas==2.2.0 \
    python-dateutil==2.8.2 \
    pytz==2024.1 \
    six==1.16.0 \
    selenium==4.17.2

# 관리자 권한이 필요한 명령어
## airflow DAG 시간대를 Asia/Seoul로 설정
RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# airflow 계정으로 전환
USER airflow

# 로컬에 저장한 dag 파일 복사
COPY ./dags /opt/airflow/dags

# 해당 dag 파일 실행에 필요한 PYPI 모듈 설치
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# 초기화 스크립트 실행
RUN airflow db init

# 웹 서버 및 스케줄러 시작
CMD ["bash", "-c", "airflow webserver -p 8080 -D && airflow scheduler"]
