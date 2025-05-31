# pages/04_04_sea_level.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ───────────────────── 페이지 설정 ─────────────────────
st.set_page_config(page_title="해수면 상승 분석", layout="wide")
st.title("🌊 해수면 상승과 기후 변화 (SDG 13·14) 대시보드")

# ───────────────────── 데이터 불러오기 ──────────────────
def load_csv():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "sealevel_data_download.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    uploaded = st.file_uploader("CSV 파일을 업로드하세요", type="csv")
    if uploaded:
        return pd.read_csv(uploaded)
    st.stop()  # 파일이 없으면 앱 중단

df_wide = load_csv()

# ───────────────────── 전처리: long 형태 변환 ────────────
year_cols = [c for c in df_wide.columns if c.isdigit()]
id_vars   = ["location", "country", "continent", "latitude", "longitude"]

df_long = (
    df_wide.melt(id_vars=id_vars,
                 value_vars=year_cols,
                 var_name="Year",
                 value_name="Sea_Level_mm")
    .dropna(subset=["Sea_Level_mm"])
)
df_long["Year"] = df_long["Year"].astype(int)

# ───────────────────── 데이터 미리보기 ───────────────────
with st.expander("🔍 데이터 표 보기"):
    st.dataframe(df_long.head())

# ───────────────────── 전지구 평균 추이 ──────────────────
st.markdown("### 📈 전지구 평균 해수면 상승 추이")
global_mean = df_long.groupby("Year")["Sea_Level_mm"].mean().reset_index()
fig_global  = px.line(global_mean, x="Year", y="Sea_Level_mm",
                      labels={"Sea_Level_mm": "해수면(mm)"},
                      title="전지구 평균 해수면(GMSL) 변화")
st.plotly_chart(fig_global, use_container_width=True)

# ───────────────────── 연도 범위 슬라이더 ────────────────
st.markdown("### 🔍 기간별 상세 분석")
yr_min, yr_max = st.slider("분석할 연도 범위 선택",
                           int(df_long["Year"].min()),
                           int(df_long["Year"].max()),
                           (1993, 2018))
mask_period = df_long[(df_long["Year"] >= yr_min) & (df_long["Year"] <= yr_max)]
st.write(f"선택 범위 평균 해수면(mm): **{mask_period['Sea_Level_mm'].mean():.2f}**")

# ───────────────────── 대륙별 평균 비교 ──────────────────
st.markdown("### 🌍 대륙별 평균 해수면 변화")
cont_mean = (mask_period
             .groupby(["continent", "Year"])["Sea_Level_mm"]
             .mean()
             .reset_index())
fig_cont  = px.line(cont_mean, x="Year", y="Sea_Level_mm",
                    color="continent",
                    labels={"Sea_Level_mm": "해수면(mm)"},
                    title="대륙별 평균 해수면 추이")
st.plotly_chart(fig_cont, use_container_width=True)

# ───────────────────── 국가별 분석기 ─────────────────────
st.markdown("### 🏳️ 국가별 해수면 변화")
sel_country = st.selectbox("국가 선택", sorted(df_long["country"].unique()))
country_df  = df_long[df_long["country"] == sel_country]
fig_country = px.line(country_df, x="Year", y="Sea_Level_mm",
                      color="location",
                      labels={"Sea_Level_mm": "해수면(mm)"},
                      title=f"{sel_country} 관측소별 해수면 변화")
fig_country.update_layout(legend_title_text="관측소")
st.plotly_chart(fig_country, use_container_width=True)

# ───────────────────── 특정 연도 지도 시각화 ─────────────
st.markdown("### 🗺️ 선택 연도 관측소 지도")
sel_year = st.slider("지도로 볼 연도 선택", yr_min, yr_max, yr_max)
map_df   = df_long[df_long["Year"] == sel_year]

fig_map = px.scatter_geo(
    map_df, lat="latitude", lon="longitude",
    hover_name="location",
    size="Sea_Level_mm",
    color="Sea_Level_mm",
    color_continuous_scale="Blues",
    projection="natural earth",
    title=f"{sel_year}년 관측소별 해수면(mm)"
)
fig_map.update_layout(coloraxis_colorbar_title="해수면(mm)")
st.plotly_chart(fig_map, use_container_width=True)

# ───────────────────── SDGs 연결 & 교육 요소 ─────────────
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
1. 해수면 상승은 어떤 지역·국가에 가장 큰 위협이 될까요?  
2. 해수면 변화와 **SDG 13·14** 달성은 어떻게 연결될까요?  
3. 기후 행동을 위해 개인·지역사회·국가·국제사회가 할 수 있는 일은 무엇일까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- **데이터 해석 역량**: 시계열·공간 데이터를 분석하여 기후 변화의 증거를 탐구  
- **융합적 사고**: 과학·사회·경제 요소를 조합해 지속가능 전략 도출  
- **SDGs 통합 학습**: 목표 13(기후 행동), 목표 14(해양 생태계 보호)의 상호작용 이해
""")

st.markdown("### 🚀 확장 활동")
st.markdown("""
- **지역 조사**: 우리나라 해안선 변화 사진·위성영상 비교 분석  
- **정책 제안서 작성**: 탄소 저감·연안 보호 정책을 데이터 근거로 제안  
- **국제 협력 시뮬레이션**: 모의 UN 회의 형식으로 해수면 상승 대응 협상
""")
