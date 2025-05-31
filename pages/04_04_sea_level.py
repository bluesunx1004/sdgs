import streamlit as st

# ✅ 페이지 설정은 가장 먼저
st.set_page_config(page_title="NASA 해수면 상승 시각화", layout="wide")

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import folium
from streamlit_folium import st_folium

import matplotlib.font_manager as fm

# 프로젝트에 포함된 NanumGothic.ttf 사용
font_path = "NanumGothic.ttf"
font_prop = fm.FontProperties(fname=font_path)

# 한글 깨짐 방지 적용
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# ✅ 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')


# ✅ 데이터 로딩
@st.cache_data
def load_data():
    df = pd.read_csv("sealevel.csv")
    df = df[['Year', 'SmoothedGSML_GIA']]
    df = df.groupby("Year").mean().reset_index()
    return df

df = load_data()

# ✅ 제목 및 설명
st.title("🌊 NASA 기반 해수면 상승 시각화")
st.markdown("1993년 이후 **전 지구 평균 해수면(GMSL)** 변화를 시각화하고, "
            "특정 도시의 해수면 상승 시 침수 영향을 지도에서 확인합니다.")

# ✅ 1. 해수면 상승 그래프
st.subheader("📈 연도별 해수면 상승 추이")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df['Year'], df['SmoothedGSML_GIA'], marker='o', color='blue')
ax.set_xlabel("Year")
ax.set_ylabel("Global Mean Sea Level rise (mm)")
ax.set_title("Global Mean Sea Level Rise (Smoothed GIA-Corrected)")
ax.grid(True)
st.pyplot(fig)

# ✅ 2. 도시별 침수 영향 지도
st.subheader("🗺 침수 영향 도시 지도")

city_coords = {
    "인천": (37.4563, 126.7052),
    "부산": (35.1796, 129.0756),
    "제주": (33.4996, 126.5312),
    "방콕": (13.7563, 100.5018),
    "뉴욕": (40.7128, -74.0060)
}

city = st.selectbox("도시를 선택하세요", list(city_coords.keys()))
lat, lon = city_coords[city]

map_ = folium.Map(location=[lat, lon], zoom_start=10)
folium.Marker([lat, lon], popup=f"{city} 중심").add_to(map_)

# 단순 침수 영향 가정 (반경 3km 원형)
folium.Circle(
    location=[lat, lon],
    radius=3000,  # 3km 반경
    color="blue",
    fill=True,
    fill_opacity=0.3,
    popup="예상 침수 영향 반경"
).add_to(map_)

st_folium(map_, width=700, height=500)
