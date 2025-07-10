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

    # 描画 or 編集モードの切り替え
    mode = st.radio("操作モードを選択", ("ラインを描く", "ラインを移動・編集"))
    drawing_mode = "line" if mode == "ラインを描く" else "transform"

    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 255, 0.5)",
        stroke_color="rgba(0, 0, 255, 0.7)",
        stroke_width=3,
        background_image=image,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode=drawing_mode,
        key="canvas"
    )

    if canvas_result.json_data is not None:
    objs = canvas_result.json_data["objects"]
    lines = [obj for obj in objs if obj["type"] == "line"]

    results = []

    # 必ず偶数本（0ライン → 終点ラインの順でペア）であることを想定
    for i in range(0, len(lines) - 1, 2):
        line0 = lines[i]       # 0ライン
        line1 = lines[i + 1]   # 終点ライン

        # 中心Y座標を取得
        y0_center = (line0["y1"] + line0["y2"]) / 2
        y1_center = (line1["y1"] + line1["y2"]) / 2

        dy = abs(y1_center - y0_center)
        estimated_balls = int(dy * bullets_per_pixel)

        results.append({
            "ペア": f"{i+1} & {i+2}",
            "差(px)": round(dy, 1),
            "推定打ち込み玉数": estimated_balls
        })

    if results:
        df = pd.DataFrame(results)
        st.dataframe(df)
        st.text_area("📤 LINEに貼り付ける用メッセージ", value=df.to_string(index=False), height=200)
