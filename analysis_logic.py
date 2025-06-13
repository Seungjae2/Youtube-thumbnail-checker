# analysis_logic.py
import time
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
import io

from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction.models import CustomVisionErrorException

# --- Azure 설정 및 클라이언트 초기화 ---
ENDPOINT = os.getenv("AZURE_ENDPOINT")
PREDICTION_KEY = os.getenv("AZURE_PREDICTION_KEY")
PROJECT_ID = os.getenv("AZURE_PROJECT_ID")
VIEWCOUNT_PUBLISHED_NAME = os.getenv("VIEWCOUNT_PUBLISHED_NAME")
TRENDING_PUBLISHED_NAME = os.getenv("TRENDING_PUBLISHED_NAME")

try:
    credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})
    predictor = CustomVisionPredictionClient(ENDPOINT, credentials)
except Exception as e:
    print(f"오류: Azure 클라이언트 초기화 실패. .env 파일의 설정을 확인하세요. ({e})")
    predictor = None


def _load_terms():
    try:
        with open("terms.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<p>이용약관 파일을 찾을 수 없습니다.</p>"


TERMS_HTML = _load_terms()


def _run_real_prediction(image_data, published_name):
    if not predictor:
        raise ConnectionError("Azure 예측 클라이언트가 초기화되지 않았습니다. .env 설정을 확인하세요.")
    try:
        results = predictor.detect_image(PROJECT_ID, published_name, image_data)
        predictions = [{"tagName": p.tag_name, "probability": p.probability,
                        "boundingBox": {"left": p.bounding_box.left, "top": p.bounding_box.top,
                                        "width": p.bounding_box.width, "height": p.bounding_box.height}} for p in
                       results.predictions]
        return {"predictions": predictions}
    except CustomVisionErrorException as e:
        error_message = (
            f"Azure API 호출 오류 발생: '{e.message}'\n'{published_name}'이라는 이름으로 게시된 모델을 찾을 수 없습니다. Azure AI Studio에서 모델이 정상적으로 게시되었는지, 그리고 .env 파일의 PUBLISHED_NAME이 올바른지 확인해주세요.")
        raise ValueError(error_message) from e
    except Exception as e:
        raise ConnectionError(f"Azure 서버와 통신 중 알 수 없는 오류가 발생했습니다: {e}") from e


def _calculate_score(predictions):
    if not predictions["predictions"]: return 0
    weights = {"인물": 1.2, "텍스트": 1.1, "브랜드/로고": 1.0, "캐릭터": 0.9}
    weighted_score, total_weight = 0, 0
    for pred in predictions["predictions"]:
        weight = weights.get(pred["tagName"], 1.0)
        weighted_score += pred["probability"] * weight
        total_weight += weight
    final_score = (weighted_score / total_weight) * 100 if total_weight > 0 else 0
    return min(final_score, 100)


def _generate_recommendations(view_score, trend_score):
    recs = []
    if view_score < 75: recs.append("📈 조회수 향상 팁: 인물의 표정이나 포즈를 더 역동적으로 만들고, 텍스트 가독성을 높여보세요.")
    if trend_score < 75: recs.append("🔥 트렌드 팁: 현재 유행하는 밝은 색상 팔레트를 사용하거나, 인기 캐릭터/이모지를 추가해보세요.")
    if not recs: recs.append("🎉 완벽해요! 현재 썸네일은 조회수와 트렌드 모두에 최적화되어 있습니다.")
    return recs


# [수정] 이미지에서 범례(Legend)를 그리는 코드를 완전히 제거합니다. [3]
def _draw_on_image(image, view_preds, trend_preds, confidence_threshold):
    editable_image = image.copy().convert("RGBA")
    draw = ImageDraw.Draw(editable_image)
    img_width, img_height = editable_image.size
    try:
        font = ImageFont.truetype("malgun.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    model_colors = {"view": (66, 133, 244, 255), "trend": (234, 67, 53, 255)}

    # 객체 감지 경계 상자 그리기 (이 부분은 유지)
    for pred in view_preds['predictions']:
        if pred['probability'] >= confidence_threshold:
            box = pred['boundingBox'];
            abs_box = [box['left'] * img_width, box['top'] * img_height, (box['left'] + box['width']) * img_width,
                       (box['top'] + box['height']) * img_height]
            draw.rectangle(abs_box, outline=model_colors['view'], width=4)
            label = f"{pred['tagName']}: {pred['probability']:.1%}";
            draw.text((abs_box[0] + 5, abs_box[1] + 5), label, fill=model_colors['view'], font=font)
    for pred in trend_preds['predictions']:
        if pred['probability'] >= confidence_threshold:
            box = pred['boundingBox'];
            abs_box = [box['left'] * img_width, box['top'] * img_height, (box['left'] + box['width']) * img_width,
                       (box['top'] + box['height']) * img_height]
            draw.rectangle(abs_box, outline=model_colors['trend'], width=4)
            label = f"{pred['tagName']}: {pred['probability']:.1%}";
            draw.text((abs_box[0] + 5, abs_box[3] - 25), label, fill=model_colors['trend'], font=font)

    # 범례 그리기 로직은 여기서 완전히 삭제되었습니다.
    return editable_image


def analyze_thumbnail(image, confidence_threshold):
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image_data = output.getvalue()
    viewcount_predictions = _run_real_prediction(image_data, VIEWCOUNT_PUBLISHED_NAME)
    trending_predictions = _run_real_prediction(image_data, TRENDING_PUBLISHED_NAME)
    view_model_score_val = _calculate_score(viewcount_predictions)
    trend_model_score_val = _calculate_score(trending_predictions)
    potential_score = (view_model_score_val + trend_model_score_val) / 2
    all_tags = ["인물", "텍스트", "브랜드/로고", "캐릭터"]
    data = []
    for tag in all_tags:
        vc_prob = next((p['probability'] for p in viewcount_predictions['predictions'] if p['tagName'] == tag), 0)
        tr_prob = next((p['probability'] for p in trending_predictions['predictions'] if p['tagName'] == tag), 0)
        data.append({'요소': tag, '조회수 모델': round(vc_prob * 100, 1), '트렌드 모델': round(tr_prob * 100, 1),
                     '차이(p.p)': round((tr_prob - vc_prob) * 100, 1)})
    df = pd.DataFrame(data)
    plot_df = df.drop(columns=['차이(p.p)']).melt(id_vars='요소', var_name='모델', value_name='점수')
    suggestions = _generate_recommendations(view_model_score_val, trend_model_score_val)
    analyzed_image = _draw_on_image(image, viewcount_predictions, trending_predictions, confidence_threshold)

    # 퍼센트 및 소수점 형식 선호도 반영 [4]
    return (
        f"{potential_score:.1f}%", f"{view_model_score_val:.1f}%", f"{trend_model_score_val:.1f}%",
        df, plot_df, suggestions, analyzed_image
    )
