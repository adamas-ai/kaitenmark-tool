from PIL import Image
from streamlit_drawable_canvas import st_canvas
import streamlit as st

st.set_page_config(page_title="グラフ測定ツール", layout="wide")

st.title("🎯 グラフ画像から差玉を推定")

uploaded_image = st.file_uploader("📷 グラフ画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # PILで画像を開く
    image = Image.open(uploaded_image)
    width, height = image.size

    st.sidebar.header("📏 測定設定")
    pixel_distance = st.sidebar.number_input("📐 -10,000〜-20,000の間隔（mm）", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    pixel_length = st.sidebar.slider("📏 -10,000〜-20,000の画面距離（ピクセル）", min_value=10, max_value=300, value=100)

    # 1px あたりの玉数
    mm_per_pixel = pixel_distance / pixel_length
    bullets_per_mm = 1000
    bullets_per_pixel = bullets_per_mm * mm_per_pixel

    st.subheader("🖱️ 画像上で 0ラインと終点 を1ペアずつクリック")

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=3,
        background_image=image,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="line",
        key="canvas",
    )

    # 描画された線のデータを処理
    if canvas_result.json_data is not None:
        import pandas as pd
        import numpy as np

        objs = canvas_result.json_data["objects"]
        lines = [obj for obj in objs if obj["type"] == "line"]

        st.write(f"🧮 測定ペア数：{len(lines)}")

        results = []

        for i, line in enumerate(lines):
            y0 = line["y1"]
            y1 = line["y2"]
            diff = abs(y1 - y0)
            estimated_balls = int(diff * bullets_per_pixel)

            results.append({
                "ペア": i + 1,
                "線の高さ差(px)": round(diff, 1),
                "推定差玉(発)": estimated_balls
            })

        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)

            st.text_area("📤 LINEに貼り付ける用", value=df.to_string(index=False), height=200)
