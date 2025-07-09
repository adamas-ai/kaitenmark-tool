import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
<<<<<<< HEAD
import pandas as pd
=======
>>>>>>> d870011 (初回コミット：app.pyとrequirements.txtを追加)
import io
import base64

st.set_page_config(page_title="グラフ差玉測定ツール", layout="wide")
st.title("🎯 サイトセブンのグラフ画像から差玉を推定")

<<<<<<< HEAD
uploaded_image = st.file_uploader("📷 グラフ画像をアップロード", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # PIL.Imageで読み込み
    image = Image.open(uploaded_image).convert("RGB")
    width, height = image.size

    # base64エンコード（streamlit_drawable_canvas用）
=======
# CSSでプライマリボタンを白背景に（全体のプライマリボタンに影響します）
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

    # base64変換（canvasの背景画像用）
>>>>>>> d870011 (初回コミット：app.pyとrequirements.txtを追加)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    background_url = f"data:image/png;base64,{img_str}"

<<<<<<< HEAD
=======
    # 設定
>>>>>>> d870011 (初回コミット：app.pyとrequirements.txtを追加)
    st.sidebar.header("📏 測定設定")
    pixel_distance = st.sidebar.number_input("📐 -10,000〜-20,000の目盛間隔（mm）", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
    pixel_length = st.sidebar.slider("📏 画面上での-10,000〜-20,000の距離（px）", min_value=10, max_value=300, value=100)

<<<<<<< HEAD
    # mm→発 換算
    mm_per_pixel = pixel_distance / pixel_length
    bullets_per_mm = 1000
    bullets_per_pixel = bullets_per_mm * mm_per_pixel

    st.subheader("🖱️ 画像上で 0ライン → 終点 を線で描画（複数可）")

    canvas_result = st_canvas(
    fill_color="rgba(255, 0, 0, 0.3)",
    stroke_width=3,
    background_image=image,  # PIL.Imageで読み込んだもの
    update_streamlit=True,
    height=height,
    width=width,
    drawing_mode="line",
    key="canvas"
)
=======
    mm_per_pixel = pixel_distance / pixel_length  # mm / px
    bullets_per_mm = 1000
    bullets_per_pixel = bullets_per_mm * mm_per_pixel

    # 描画モードと色の切替
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

    canvas_result = st_canvas(
        fill_color=line_colors.get(drawing_option, "rgba(0,0,0,0)"),
        stroke_width=3,
        background_image=None,
        background_image_url=background_url,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode=drawing_mode_map[drawing_option],
        key="canvas",
        # 移動モード時はペン非表示にしたい場合はstroke_color透明などに設定可
    )
>>>>>>> d870011 (初回コミット：app.pyとrequirements.txtを追加)

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
<<<<<<< HEAD
            df = pd.DataFrame(results)
            st.dataframe(df)

            st.text_area("📤 LINEに貼り付ける用メッセージ", value=df.to_string(index=False), height=200)
=======
            import pandas as pd
            df = pd.DataFrame(results)
            st.dataframe(df)
            st.text_area("📤 LINEに貼り付ける用メッセージ", value=df.to_string(index=False), height=200)
>>>>>>> d870011 (初回コミット：app.pyとrequirements.txtを追加)
