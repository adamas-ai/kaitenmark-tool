import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import pandas as pd
<<<<<<< HEAD
=======
import io
import base64
>>>>>>> 090c55f (初回コミット: app.pyとrequirements.txtを追加)

st.set_page_config(page_title="グラフ差玉測定ツール", layout="wide")
st.title("🎯 サイトセブンのグラフ画像から差玉を推定")

uploaded_image = st.file_uploader("📷 グラフ画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
<<<<<<< HEAD
    # PIL.Imageで読み込み
    image = Image.open(uploaded_image).convert("RGB")
    width, height = image.size

=======
    image = Image.open(uploaded_image).convert("RGB")
    width, height = image.size

    # PIL.Image → base64に変換（streamlit_drawable_canvas対応のため）
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    background_url = f"data:image/png;base64,{img_str}"

>>>>>>> 090c55f (初回コミット: app.pyとrequirements.txtを追加)
    st.sidebar.header("📏 測定設定")
    pixel_distance = st.sidebar.number_input("📐 -10,000〜-20,000の目盛間隔（mm）", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    pixel_length = st.sidebar.slider("📏 画面上での-10,000〜-20,000の距離（px）", min_value=10, max_value=300, value=100)

<<<<<<< HEAD
    # mm→発 換算
    mm_per_pixel = pixel_distance / pixel_length  # mm / px
=======
    mm_per_pixel = pixel_distance / pixel_length
>>>>>>> 090c55f (初回コミット: app.pyとrequirements.txtを追加)
    bullets_per_mm = 1000
    bullets_per_pixel = bullets_per_mm * mm_per_pixel

    st.subheader("🖱️ 画像上で 0ライン → 終点 を線で描画（複数可）")

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",
        stroke_width=3,
<<<<<<< HEAD
        background_image=image,  # ✅ PIL.Imageオブジェクトで渡す
=======
        background_image=None,
        background_image_url=background_url,  # ✅ PILじゃなくbase64を直接指定
>>>>>>> 090c55f (初回コミット: app.pyとrequirements.txtを追加)
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="line",
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
