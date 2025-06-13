# 🚀 YouTube 썸네일 분석기 (YouTube Thumbnail Analyzer)

<br>

### 🎬 프로젝트 개요

**YouTube 썸네일 분석기**는 Azure AI 맞춤 비전(Custom Vision)을 활용하여 YouTube 썸네일 이미지의 성공 가능성을 예측하고, 데이터 기반의 맞춤 개선안을 제공하는 웹 애플리케이션입니다.

이 도구는 두 개의 특화된 AI 모델('조회수 최적화 모델'과 '트렌드 적합성 모델')을 통해 썸네일을 다각도로 분석합니다. 사용자는 간단한 이미지 업로드만으로 썸네일의 종합적인 잠재력 점수, 세부 요소별 비교, 그리고 실질적인 개선 팁까지 한눈에 확인할 수 있습니다.

특히, 사용자의 직관적인 경험을 최우선으로 고려하여 여러 차례 UI/UX를 개선하며 발전시켜 온 프로젝트입니다[^2].

<br>

### ✨ 주요 기능

* **듀얼 모델 AI 분석**: '조회수'와 '트렌드'라는 두 가지 관점에서 썸네일을 동시에 분석하고 예측 결과를 제공합니다.
* **종합 분석 대시보드**: 두 모델의 예측치를 종합한 '종합 잠재력' 점수와 각 모델의 점수를 나란히 비교하여 보여줍니다.
* **상세 비교 데이터**: '인물', '텍스트' 등 핵심 요소별로 두 모델의 예측 점수와 그 차이를 데이터 표로 명확하게 제시합니다.
* **동적 시각화**: 분석된 객체의 위치를 이미지 위에 경계 상자(Bounding Box)로 표시하며, 사용자가 AI 신뢰도 임계값을 조절함에 따라 시각화 결과가 실시간으로 변경됩니다.
* **맞춤 개선 제안**: 분석 점수를 기반으로 썸네일을 개선할 수 있는 구체적이고 실용적인 팁을 생성합니다.

<br>

### 🛠️ 기술 스택 (Tech Stack)

* **Backend**: Python
* **ML/AI**: Azure Custom Vision API [^1][^3]
* **Web Framework**: Gradio
* **Data Handling**: Pandas
* **Image Processing**: Pillow (PIL)

<br>

### ⚙️ 설치 및 실행 방법

1. **저장소 복제(Clone)**

```bash
git clone https://github.com/your-username/youtube_thumbnail_analyzer.git
cd youtube_thumbnail_analyzer
```

2. **필요 패키지 설치**

```bash
pip install -r requirements.txt
```

3. **환경 변수 설정**
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고, Azure AI Studio에서 발급받은 키와 모델 정보를 아래와 같이 입력합니다.

```env
# .env
AZURE_PREDICTION_KEY="<Your Azure Prediction Key>"
AZURE_ENDPOINT="<Your Azure Endpoint URL>"
AZURE_PROJECT_ID="<Your Project ID>"
VIEWCOUNT_PUBLISHED_NAME="<Your View-Model Published Name>"
TRENDING_PUBLISHED_NAME="<Your Trend-Model Published Name>"
```

4. **애플리케이션 실행**

```bash
python main.py
```

5. 터미널에 출력된 로컬 URL(예: `http://127.0.0.1:7860`)을 웹 브라우저에서 열어 서비스를 확인합니다.
<br>

### 💡 사용법

1. '분석할 썸네일 이미지' 영역에 파일을 드래그 앤 드롭하거나, 클립보드에 복사된 이미지를 붙여넣습니다.
2. 'AI 신뢰도 임계값' 슬라이더를 조절하여 이미지에 표시될 분석 결과의 민감도를 설정합니다.
3. '이용약관'을 확인하고 동의란에 체크합니다.
4. '분석 시작' 버튼을 클릭하여 결과를 확인합니다.
5. 오른쪽에 나타나는 대시보드에서 점수, 차트, 개선 제안, 그리고 시각화된 이미지를 확인하며 썸네일을 개선합니다.
<br>

### 🤝 기여(Contributing)

이 프로젝트에 기여하고 싶으신 분은 언제나 환영합니다! 버그 리포트, 기능 제안, 코드 개선을 위한 Pull Request 등 어떤 형태의 기여도 감사히 받겠습니다. 자세한 내용은 이슈 트래커를 확인해주세요.

<br>

### 📄 라이선스 (License)

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.

<div style="text-align: center">⁂</div>
