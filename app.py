import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import io
import base64

st.set_page_config(page_title="グラフ差玉測定ツール", layout="wide")
st.title("🎯 サイトセブンのグラフ画像から差玉を推定")

# CSSでプライマリボタンを白背景に
st.markdown("""
<style>
button[kind="primary"] {
    background-color: white !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

uploaded_image = st.file_uploader("📷 グラフ画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")
    width, height = image.size

    # base64エンコード（canvasの背景画像用）
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    background_url = f"data:image/png;base64,{img_str}"

    # 測定設定
    st.sidebar.header("📏 測定設定")
    pixel_distance = st.sidebar.number_input("📐 -10,000〜-20,000の目盛間隔（mm）", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    pixel_length = st.sidebar.slider("📏 画面上での-10,000〜-20,000の距離（px）", min_value=10, max_value=300, value=100)

    mm_per_pixel = pixel_distance / pixel_length
    bullets_per_mm = 1000
    bullets_per_pixel = bullets_per_mm * mm_per_pixel

    # 描画モード
    drawing_option = st.radio("操作モードを選択", ("0ライン", "終点ライン", "移動（パン）"))
    drawing_mode_map = {
        "0ライン": "line",
        "終点ライン": "line",
        "移動（パン）": "pan"
    }
    line_colors = {
        "0ライン": "rgba(0, 0, 255, 0.7)",    # 青
        "終点ライン": "rgba(255, 0, 0, 0.7)"  # 赤
    }

    current_mode = drawing_option
    stroke_width = 3 if current_mode != "移動（パン）" else 0
    fill_color = line_colors.get(current_mode, "rgba(0,0,0,0)") if current_mode != "移動（パン）" else "rgba(0,0,0,0)"

    canvas_result = st_canvas(
        fill_color=fill_color,
        stroke_width=stroke_width,
        background_image=None,
        background_image_url=background_url,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode=drawing_mode_map[current_mode],
        key="canvas"
    )

    if canvas_result.json_data is not None:
        objs = canvas_result.json_data["objects"]
        lines = [obj for obj in objs if obj["type"] == "line"]

        results = []
        for i, line in enumerate(lines):
            y0 = line["y1"]
            y1 = line["y2"]
            dy = abs(y1 - y0)
            estimated_balls = int(dy * bullets_per_pixel)

            results.append({
                "ペア": i + 1,
                "差(px)": round(dy, 1),
                "推定差玉": estimated_balls
            })

        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
            st.text_area("📤 LINEに貼り付ける用メッセージ", value=df.to_string(index=False), height=200)
