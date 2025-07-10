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
    # 画像読み込み
    image = Image.open(uploaded_image).convert("RGB")
    width, height = image.size

    # base64変換（未使用）
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # 測定設定
    st.sidebar.header("📏 測定設定")
    pixel_distance = st.sidebar.number_input("📐 -10,000〜-20,000の目盛間隔（mm）", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    pixel_length = st.sidebar.slider("📏 画面上での-10,000〜-20,000の距離（px）", min_value=10, max_value=300, value=100)

    mm_per_pixel = pixel_distance / pixel_length
    bullets_per_pixel = 1000 * mm_per_pixel

    # 操作モード
    drawing_option = st.radio("操作モードを選択", ("0ライン", "終点ライン", "移動（パン）"))

    drawing_mode_map = {
        "0ライン": "line",
        "終点ライン": "line",
        "移動（パン）": "pan"
    }

    line_colors = {
        "0ライン": "rgba(0, 0, 255, 1)",    # 青
        "終点ライン": "rgba(255, 0, 0, 1)"   # 赤
    }

    current_mode = drawing_option
    stroke_width = 3 if current_mode != "移動（パン）" else 0
    stroke_color = line_colors.get(current_mode, "rgba(0,0,0,1)") if current_mode != "移動（パン）" else "rgba(0,0,0,0)"
    fill_color = "rgba(0,0,0,0)"  # 塗りつぶしなし

    # Canvas
    canvas_result = st_canvas(
        fill_color=fill_color,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        background_image=image,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode=drawing_mode_map[current_mode],
        key="canvas"
    )

    # 結果処理
    if canvas_result.json_data is not None:
        objs = canvas_result.json_data["objects"]
        lines = [obj for obj in objs if obj["type"] == "line"]

        # 偶数本の線をペアにする
        results = []
        for i in range(0, len(lines) - 1, 2):
            y0 = lines[i]["y1"]
            y1 = lines[i + 1]["y1"]
            dy = abs(y1 - y0)
            estimated_balls = int(dy * bullets_per_pixel)
            results.append({
                "ペア": f"{i + 1}-{i + 2}",
                "差(px)": round(dy, 1),
                "推定差玉": estimated_balls
            })

        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
            st.text_area("📤 LINEに貼り付ける用メッセージ", value=df.to_string(index=False), height=200)
