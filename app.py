import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd
import io
import base64

st.set_page_config(page_title="グラフ差玉測定ツール", layout="wide")
st.title("🎯 サイトセブンのグラフ画像から差玉を推定")

uploaded_image = st.file_uploader("📷 グラフ画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    image = Image.open(uploaded_image).convert("RGB")
    width, height = image.size

    # 差玉計算設定
    st.sidebar.header("📏 測定設定")
    pixel_distance = st.sidebar.number_input("📐 -10,000〜-20,000の目盛間隔（mm）", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    pixel_length = st.sidebar.slider("📏 画面上での-10,000〜-20,000の距離（px）", min_value=10, max_value=300, value=100)
    mm_per_pixel = pixel_distance / pixel_length
    bullets_per_pixel = 1000 * mm_per_pixel

    # 描画モード切替
    mode = st.radio("モード", ["ラインを描く", "ラインを編集する"])

    drawing_mode = "line" if mode == "ラインを描く" else "transform"

    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_color="rgba(0, 0, 255, 1)",
        stroke_width=3,
        background_image=image,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode=drawing_mode,
        key="canvas"
    )

    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        lines = [obj for obj in objects if obj["type"] == "line"]

        results = []
        for i in range(0, len(lines), 2):
            try:
                line0 = lines[i]
                line1 = lines[i + 1]
                y_start = line0["y1"]
                y_end = line1["y1"]
                dy = abs(y_end - y_start)
                estimated_balls = int(dy * bullets_per_pixel)

                results.append({
                    "ペア": f"{i+1}-{i+2}",
                    "差(px)": round(dy, 1),
                    "推定打ち込み玉数": estimated_balls
                })
            except IndexError:
                # 奇数本だけ描かれてる場合は無視
                continue

        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
            st.text_area("📤 LINEに貼り付ける用", value=df.to_string(index=False), height=200)
