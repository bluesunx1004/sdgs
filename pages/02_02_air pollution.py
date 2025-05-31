# 2_📊_PM10_시각화.py
import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

st.set_page_config(page_title="PM10 시각화", page_icon="📊", layout="wide")

st.title("📊 월별‧도시별 미세먼지(PM10) 데이터 탐구")

# --------------------------------------------------------------------------------
# 1) 데이터 로드 & 전처리 ----------------------------------------------------------
# --------------------------------------------------------------------------------
@st.cache_data
def load_data():
    # CSV는 /data 폴더 등에 두어도 되고, 경로만 맞추면 됩니다
    df = pd.read_csv("data/미세먼지_PM10__월별_도시별_대기오염도.csv", encoding="cp949")

    # 긴 형태(long)로 변환 → 선 그래프 편리
    df_long = df.melt(id_vars=["지역"], var_name="월", value_name="PM10")
    df_long["date"] = pd.to_datetime(df_long["월"], format="%Y년%m월")  # datetime 변환

    return df, df_long

df_wide, df_long = load_data()

# --------------------------------------------------------------------------------
# 2) 도시 선택 → 선 그래프 --------------------------------------------------------
# --------------------------------------------------------------------------------
st.subheader("① 도시별 월간 추세(선 그래프)")

city_options = df_wide["지역"].unique().tolist()
sel_cities = st.multiselect("도시(복수 선택 가능)", city_options, default=["서울특별시"])

if sel_cities:
    chart_data = df_long[df_long["지역"].isin(sel_cities)]
    line_chart = (
        alt.Chart(chart_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("date:T", title="연‧월"),
            y=alt.Y("PM10:Q", title="PM10 농도(㎍/㎥)"),
            color="지역:N",
            tooltip=["지역", "월", "PM10"]
        )
        .properties(height=400)
    )
    st.altair_chart(line_chart, use_container_width=True)
else:
    st.info("좌측 체크박스에서 한 개 이상 도시를 선택하세요.")

# --------------------------------------------------------------------------------
# 3) 월 선택 → 지도 시각화 --------------------------------------------------------
# --------------------------------------------------------------------------------
st.subheader("② 선택 월 지도 시각화")

# 월 컬럼만 추출해 셀렉트박스 옵션으로
month_cols = [c for c in df_wide.columns if c != "지역"]
sel_month = st.selectbox("보고 싶은 월", month_cols, index=len(month_cols)-1)

# 한국 주요 행정구역 중심 좌표(대략) ------------------------------------------------
city_coords = {
    "서울특별시": (37.5665, 126.9780), "부산광역시": (35.1796, 129.0756),
    "대구광역시": (35.8714, 128.6014), "인천광역시": (37.4563, 126.7052),
    "광주광역시": (35.1595, 126.8526), "대전광역시": (36.3504, 127.3845),
    "울산광역시": (35.5384, 129.3114), "세종특별자치시": (36.4800, 127.2890),
    "경기도": (37.4133, 127.5183),   "강원특별자치도": (37.8228, 128.1555),
    "충청북도": (36.6358, 127.4914), "전북특별자치도": (35.8200, 127.1088),
    "전라남도": (34.8160, 126.4630), "경상북도": (36.4919, 128.8889),
    "경상남도": (35.4606, 128.2132), "제주특별자치도": (33.4996, 126.5312),
}

map_df = (
    df_wide[["지역", sel_month]]
    .assign(lat=lambda d: d["지역"].map(lambda x: city_coords[x][0]),
            lon=lambda d: d["지역"].map(lambda x: city_coords[x][1]),
            radius=lambda d: d[sel_month] * 500,           # 농도에 비례한 원 크기
            pm=lambda d: d[sel_month])                     # 툴팁용 별도 컬럼
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position="[lon, lat]",
    get_radius="radius",
    get_fill_color="[255, 100, 50, 160]",  # 불투명도 α=160
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=36.5, longitude=127.8, zoom=5.5)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state,
                         tooltip={"text": "{지역}\nPM10: {pm} ㎍/㎥"}))

# --------------------------------------------------------------------------------
# 4) 학생 토론 질문 · 교육적 함의 · 확장 활동 --------------------------------------
# --------------------------------------------------------------------------------
st.markdown("---")
st.subheader("🗣️ 학생 토론 질문")
st.markdown("""
1. **도시별·계절별로 PM10 농도가 달라지는 가장 큰 요인은 무엇일까요?**  
2. **SDGs 목표 11 ‘지속가능한 도시와 공동체’ 달성을 위해** 각 도시가 취할 수 있는 대기질 개선 정책은 무엇이 있을까요?  
3. **여러분이 사는 지역**의 실제 체감 공기 질과 데이터가 다른 부분이 있다면, 왜 그럴지 가설을 세워보세요.
""")

st.subheader("🎓 교육적 함의")
st.markdown("""
- **데이터 해석 역량**: 시계열‧공간 데이터를 함께 분석하며 패턴·상관관계를 파악  
- **과학·사회 융합**: 기상·산업·교통 등 요인과 연계해 과학적 근거 기반 정책 제안  
- **SDGs 연결**: 대기오염이 건강(Goal 3), 기후(Goal 13)와도 긴밀히 연결돼 있음을 이해
""")

st.subheader("🚀 확장 활동")
st.markdown("""
- **기상 데이터(기온·풍속 등)**를 추가해 다중 회귀 분석 → PM10 농도 예측 모델 만들기  
- **다른 대기오염물질(PM2.5·NO₂ 등)**로 지표 확장, SDGs Goal 3∙13 탐구 심화  
- **현장 중심 프로젝트**: 지역 의회·시청에 대기 개선 정책 제안서 또는 인포그래픽 제작·발표
""")
