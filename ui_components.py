# ui_components.py
import gradio as gr
from analysis_logic import analyze_thumbnail, TERMS_HTML


def create_ui():
    """Gradio Blocks를 사용하여 전체 UI를 생성하고 반환합니다."""

    def run_analysis_wrapper(image, confidence, terms_agreed):
        if not terms_agreed: raise gr.Error("이용약관에 동의해야 분석을 시작할 수 있습니다.")
        if image is None: raise gr.Error("분석할 썸네일 이미지를 업로드해주세요.")

        yield {loading_indicator: gr.update(visible=True), run_button: gr.update(visible=False),
               results_block: gr.update(visible=False)}

        (potential, view_score, trend_score, df_data,
         plot_data, suggestions, analyzed_img) = analyze_thumbnail(image, confidence)

        suggestions_md = "\n".join([f"- {s}" for s in suggestions])

        yield {
            loading_indicator: gr.update(visible=False), run_button: gr.update(visible=True),
            results_block: gr.update(visible=True),
            potential_score_output: gr.update(value=potential), view_model_output: gr.update(value=view_score),
            trend_model_output: gr.update(value=trend_score), dataframe_output: gr.update(value=df_data),
            line_plot_output: gr.update(value=plot_data), bar_plot_output: gr.update(value=plot_data),
            suggestions_output: gr.update(value=suggestions_md), analyzed_image_output: gr.update(value=analyzed_img)
        }

    with gr.Blocks(theme=gr.themes.Soft(), title="YouTube 썸네일 분석기") as demo:
        gr.Markdown("# 🚀 YouTube 썸네일 잠재력 분석기")
        gr.Markdown("AI를 활용하여 YouTube 썸네일의 성공 가능성을 예측하고, 맞춤 개선안을 받아보세요.")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. 썸네일 업로드")
                image_input = gr.Image(type="pil", label="분석할 썸네일 이미지", sources=["upload", "clipboard"])
                confidence_slider = gr.Slider(minimum=0.3, maximum=1.0, value=0.5, step=0.1, label="AI 신뢰도 임계값")
                with gr.Accordion("이용약관 보기", open=False):
                    gr.HTML(TERMS_HTML)
                gr.Markdown(
                    "<p style='font-size:12px; color:gray; margin-top:10px;'>분석 시작 버튼을 클릭하면 위 약관에 모두 동의한 것으로 간주합니다.</p>")
                terms_checkbox = gr.Checkbox(label="위 이용약관에 동의합니다.")
                run_button = gr.Button("분석 시작", variant="primary")

            with gr.Column(scale=2):
                loading_indicator = gr.Markdown("🚀 AI가 썸네일을 분석하고 있습니다...", visible=False)
                with gr.Column(visible=False) as results_block:
                    gr.Markdown("### 2. 종합 분석 대시보드")
                    with gr.Row():
                        with gr.Group(): gr.Markdown("<center>✨ 종합 잠재력</center>"); potential_score_output = gr.Textbox(
                            label="", interactive=False)
                        with gr.Group(): gr.Markdown("<center>📈 조회수 모델</center>"); view_model_output = gr.Textbox(
                            label="", interactive=False)
                        with gr.Group(): gr.Markdown("<center>📊 트렌드 모델</center>"); trend_model_output = gr.Textbox(
                            label="", interactive=False)

                    dataframe_output = gr.DataFrame(headers=["요소", "조회수 모델", "트렌드 모델", "차이(p.p)"],
                                                    datatype=["str", "number", "number", "number"], label="세부 항목 비교")
                    with gr.Tabs():
                        with gr.TabItem("모델별 예측 추세"): line_plot_output = gr.LinePlot(x="요소", y="점수", color="모델",
                                                                                     title="모델별 요소 예측 추세",
                                                                                     overlay_point=True,
                                                                                     x_title="분석 요소", y_title="예측 점수")
                        with gr.TabItem("예측 신뢰도 비교"): bar_plot_output = gr.BarPlot(x="요소", y="점수", color="모델",
                                                                                   title="모델별 요소 신뢰도", x_title="분석 요소",
                                                                                   y_title="신뢰도 점수",
                                                                                   vertical_align="top")
                    gr.Markdown("### 💡 맞춤 개선 제안")
                    suggestions_output = gr.Markdown(label="아래 제안을 확인하고 썸네일을 개선해보세요.")
                    gr.Markdown("### 🖼️ 분석한 이미지")
                    analyzed_image_output = gr.Image(label="분석 완료된 이미지", interactive=False)

                    # [수정] 이미지 하단에 HTML을 이용한 별도의 범례 UI를 추가합니다. [3]
                    with gr.Row():
                        gr.Markdown(
                            "<div style='display:flex; align-items:center; justify-content:center;'>"
                            "<span style='display:inline-block; width:15px; height:15px; background-color:#4285F4; margin-right:8px; border:1px solid #ddd;'></span>"
                            "<span>조회수 모델</span>"
                            "</div>"
                        )
                        gr.Markdown(
                            "<div style='display:flex; align-items:center; justify-content:center;'>"
                            "<span style='display:inline-block; width:15px; height:15px; background-color:#EA4335; margin-right:8px; border:1px solid #ddd;'></span>"
                            "<span>트렌드 모델</span>"
                            "</div>"
                        )

        run_button.click(
            fn=run_analysis_wrapper,
            inputs=[image_input, confidence_slider, terms_checkbox],
            outputs=[
                loading_indicator, results_block, run_button,
                potential_score_output, view_model_output, trend_model_output,
                dataframe_output, line_plot_output, bar_plot_output,
                suggestions_output, analyzed_image_output
            ]
        )
    return demo
