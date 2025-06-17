# main.py
from dotenv import load_dotenv

# [수정] .env 파일 로드를 다른 모든 모듈 임포트보다 먼저 실행합니다.
# 이렇게 하면 다른 파일에서 os.getenv()를 호출할 때 값을 정상적으로 읽어올 수 있습니다.
load_dotenv()

import gradio as gr
from ui_components import create_ui

def main():
    """
    애플리케이션의 메인 진입점입니다.
    UI를 생성하여 Gradio 앱을 실행합니다.
    """
    # ui_components.py에서 정의한 UI 생성 함수 호출
    demo = create_ui()

    # Gradio 앱 실행
    # server_name="0.0.0.0" 옵션을 추가하여 Docker 컨테이너 외부에서의 접속을 허용합니다.
    demo.launch(server_name="0.0.0.0")

if __name__ == "__main__":
    main()
