# pages/2_📊_PM10_시각화.py
import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk
from pathlib import Path

# ────────────────────────────────────────────────────────────
# 0. 페이지 설정
# ────────────────────────────────────────────────────────────
st.set_page_config(page_title="PM10 시각화", page_icon="🌫️", layout="wide")
st.title("📊 월별‧도시별 미세먼지(PM10) 데이터 탐구")

# ────────────────────────────────────────────────────────────
# 1. CSV 로드 함수 (다중 인코딩 시도)
# ────────────────────────────────────────────────────────────
@st.cache_data
def try_read_csv(path_or_file):
    encodings = ["utf-8", "utf-8-sig", "cp949", "euc-kr"]
    for enc in encodings:
        try:
            df = pd.read_csv(path_or_file, encoding=enc)
            st.success(f"✅ CSV 파일을 불러왔습니다 (encoding='{enc}')")
            return df
        except UnicodeDecodeError:
            continue
    st.error("❌ 파일 인코딩을 감지하지 못했습니다.")
    return None

# ────────────────────────────────────────────────────────────
# 2. CSV 확보 (로컬 파일 또는 업로드)
# ────────────────────────────────────────────────────────────
DATA_PATH = Path(__file__).parent / "미세먼지_PM10__월별_도시별_대기오염도.csv"

if DATA_PATH.exists():
    df_wide = try_read_csv(DATA_PATH)
else:
    uploaded = st.file_uploader("📤 CSV 파일 업로드", type=["csv"])
    if uploaded:
        df_wide = try_read_csv(uploaded)
    else:
        st.stop()          # 파일 없으면 이후 코드 중단

if df_wide is None:
    st.stop()

# ────────────────────────────────────────────────────────────
# 3. 데이터 전처리 (wide → long)
# ────────────────────────────────────────────────────────────
try:
    df_long = df_wide.melt(
        id_vars=[df_wide.columns[0]],           # 첫 열 → 지역
        var_name="월",
        value_name="PM10"
    ).rename(columns={df_wide.columns[0]: "지역"})

    # 월을 날짜형으로 변환해 정렬용 컬럼 추가
    df_long["순서"] = pd.to_datetime(df_long["월"], format="%Y년%m월", errors="coerce")
except Exception as e:
    st.error("📛 데이터 변환 오류: " + str(e))
    st.stop()

# ────────────────────────────────────────────────────────────
# 4. 데이터 미리보기
# ────────────────────────────────────────────────────────────
with st.expander("🔍 원본 데이터 미리보기", expanded=False):
    st.dataframe(df_wide.head())

# ────────────────────────────────────────────────────────────
# 5. Altair 선 그래프 (도시별 월간 추세)
# ────────────────────────────────────────────────────────────
st.subheader("① 도시별 월간 추세 (선 그래프)")

city_options = df_long["지역"].unique().tolist()
sel_cities = st.multiselect(
    "도시(복수 선택 가능)",
    city_options,
    default=["서울특별시"]
)

if sel_cities:
    chart_data = df_long[df_long["지역"].isin(sel_cities)]
    
    # 정렬 기준 리스트 (문자열 순서)
    month_order = (
        chart_data.sort_values("순서")["월"]
        .dropna()
        .unique()
        .tolist()
    )

    line_chart = (
        alt.Chart(chart_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("월:N", sort=month_order, title="연‧월"),
            y=alt.Y("PM10:Q", title="PM10 농도(㎍/㎥)"),
            color="지역:N",
            tooltip=["지역", "월", "PM10"]
        )
        .properties(height=400)
    )
    st.altair_chart(line_chart, use_container_width=True)
else:
    st.info("좌측 체크박스에서 한 개 이상 도시를 선택하세요.")

# ────────────────────────────────────────────────────────────
# 6. 월 선택 → pydeck 지도 (PM10 색상 매핑)
# ────────────────────────────────────────────────────────────
st.subheader("② 선택 월 지도 시각화")
def pm10_level(value):
    if value <= 30:
        return "좋음"
    elif value <= 80:
        return "보통"
    elif value <= 150:
        return "나쁨"
    else:
        return "매우나쁨"
        
month_cols = [c for c in df_wide.columns if c != "지역"]
sel_month = st.selectbox("보고 싶은 월", month_cols, index=len(month_cols) - 1)

# (1) 좌표 사전
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

# (2) 색상 변환 함수  ▸ 낮음=녹색, 보통=노랑, 높음=빨강
def pm_to_color(pm):
    if pd.isna(pm):
        return [200, 200, 200, 160]        # 회색
    if pm <= 30:
        return [0, 200, 0, 160]            # 녹색
    elif pm <= 80:
        return [255, 215, 0, 160]          # 노랑
    else:
        return [255, 0, 0, 160]            # 빨강

# (3) 지도 데이터 프레임
map_df = (
    df_wide[["지역", sel_month]]
    .assign(
        lat=lambda d: d["지역"].map(lambda x: city_coords[x][0]),
        lon=lambda d: d["지역"].map(lambda x: city_coords[x][1]),
        radius=lambda d: d[sel_month] * 500,
        pm=lambda d: d[sel_month],
        등급=lambda d: d[sel_month].apply(pm10_level)
    )
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position="[lon, lat]",
    get_radius="radius",
    get_fill_color="[255, 100, 50, 160]",
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=36.5, longitude=127.8, zoom=5.5)

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{지역}\nPM10: {pm} ㎍/㎥\n등급: {등급}"}
    )
)


# ────────────────────────────────────────────────────────────
# 7. 토론 질문 · 교육적 함의 · 확장 활동
# ────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🗣️ 학생 토론 질문")
st.markdown("""
1. **도시별·계절별로 PM10 농도가 달라지는 주된 요인은 무엇일까요?**  
2. **SDGs 목표 11 ‘지속가능한 도시와 공동체’** 달성을 위해, 각 도시가 시행할 수 있는 대기질 개선 정책은 무엇이 있을까요?  
3. **여러분 지역**의 체감 공기 질과 데이터가 다른 부분이 있다면, 왜 그런지 가설을 세워보세요.
""")

st.subheader("🎓 교육적 함의")
st.markdown("""
- **데이터 해석 역량**: 시계열·공간 데이터를 함께 분석하여 패턴과 상관관계 파악  
- **과학·사회 융합**: 기상·산업·교통 요인과 연계해 과학적 근거 기반 정책 제안  
- **SDGs 연결**: 대기오염이 건강(Goal 3), 기후(Goal 13)와 밀접히 관련됨을 이해
""")

st.subheader("🚀 확장 활동")
st.markdown("""
- **기상 데이터(기온·풍속 등)** 추가 후 다중 회귀 분석으로 PM10 예측 모델 만들기  
- **다른 대기오염물질(PM2.5·NO₂ 등)**로 지표 확장 → SDGs Goal 3·13 심화 탐구  
- **현장 중심 프로젝트**: 시청·의회에 대기 개선 정책 인포그래픽 또는 제안서 제출
""")
