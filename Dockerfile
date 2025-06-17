# 1. 파이썬 3.9 버전이 설치된 깨끗한 컴퓨터(리눅스)를 준비합니다.
FROM python:3.9-slim

# 2. 컴퓨터 안에 /app 이라는 작업 폴더를 만듭니다.
WORKDIR /app

# 3. requirements.txt 파일을 먼저 복사해서 필요한 프로그램들을 미리 설치합니다.
# (이렇게 하면 나중에 빌드 속도가 빨라집니다.)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 내 컴퓨터에 있는 나머지 모든 소스 코드(.py 등)를 /app 폴더로 복사합니다.
COPY . .

# 5. 외부에서 이 프로그램에 접속할 수 있도록 7860번 포트를 열어둡니다.
# (Gradio 라이브러리의 기본 포트입니다.)
EXPOSE 7860

# 6. 이 컴퓨터가 켜지면 자동으로 실행할 명령어를 알려줍니다.
# (로컬에서 실행하던 python main.py 명령어와 같습니다.)
CMD ["python", "-u", "main.py"]
