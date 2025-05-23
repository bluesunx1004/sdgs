# sea_level_streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("sealevel.csv")
    df = df[['Year', 'SmoothedGSML_GIA']]
    df = df.groupby("Year").mean().reset_index()  # 연도별 평균 해수면 레벨
    return df

df = load_data()

# Streamlit 페이지 설정
st.set_page_config(page_title="NASA 해수면 상승 시각화", layout="wide")
st.title("🌊 NASA 기반 해수면 상승 시각화")
st.markdown("1993년 이후 지구 평균 해수면(GMSL) 변화를 시각화하고, 특정 도시의 침수 가능 지역을 지도로 확인합니다.")

# 1. 해수면 상승 그래프
st.subheader("📈 연도별 전 지구 평균 해수면 상승")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df['Year'], df['SmoothedGSML_GIA'], marker='o', color='blue')
ax.set_xlabel("연도")
ax.set_ylabel("GMSL (mm)")
ax.set_title("전 세계 평균 해수면 상승 (Smoothed GIA 보정)")
ax.grid(True)
st.pyplot(fig)

# 2. 침수 영향 지도
st.subheader("🗺 도시별 해수면 상승 시 침수 영향 예상 지도")

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
folium.Marker([lat, lon], popup=f"{city} 중심지").add_to(map_)

# 해수면 상승에 따른 단순 침수 영역 가정 (3m 이하 저지대 원형 표현)
folium.Circle(
    location=[lat, lon],
    radius=3000,  # 약 3km 반경 단순 표현
    color="blue",
    fill=True,
    fill_opacity=0.3,
    popup="예상 침수 범위 (단순 반경 기준)"
).add_to(map_)

st_folium(map_, width=700, height=500)
