# app.py
# 청년 고용 동향 분석 – SDGs(목표 8) 수업용 스트림릿 앱
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="청년 고용 동향 분석", layout="wide")

# 1) 데이터 불러오기 & 전처리 --------------------------------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.set_index("Unnamed: 0").T           # 행·열 전치
    df.index.name = "연도"
    df = df.applymap(lambda x: float(str(x).replace(",", "")))  # 숫자형 변환
    # 추가 지표 계산
    df["고용률(%)"] = df["취업자"] / df["경제활동인구"] * 100
    df["참여율(%)"] = df["경제활동인구"] / df["생산가능인구"] * 100
    return df.reset_index()

data = load_data("employmentrate.csv")
years = data["연도"].astype(int)

st.title("📈 대한민국 청년 고용 동향 (2010 – 2024)")

st.markdown(
"""
**SDGs 목표 8**: _“모두를 위한 지속적·포용적·지속가능한 경제성장, 완전하고 생산적인 고용, 양질의 일자리 제공”_  
고등학생 눈높이에서 청년 고용 데이터를 해석하며, 사회·경제적 맥락과 지속가능발전 목표를 함께 탐구합니다.
"""
)

# 2) 사이드바 – 인터랙티브 설정 ---------------------------------------------
st.sidebar.header("🔧 그래프 옵션")
year_range = st.sidebar.slider("연도 범위 선택", int(years.min()), int(years.max()),
                               (2010, 2024), step=1)

metric_options = ["생산가능인구", "경제활동인구", "취업자", "실업자",
                  "실업률", "고용률(%)", "참여율(%)"]
metrics_to_show = st.sidebar.multiselect("표시할 지표", metric_options,
                                         default=["경제활동인구", "취업자", "실업률"])

filtered = data[(data["연도"] >= year_range[0]) & (data["연도"] <= year_range[1])]

# 3) 시각화 -------------------------------------------------------------------
st.subheader("① 연도별 주요 지표 추이")

base = alt.Chart(filtered).encode(
    x=alt.X("연도:O", axis=alt.Axis(title=None))
)

line = base.transform_fold(
    metrics_to_show, as_=["지표", "값"]
).mark_line(point=True).encode(
    y=alt.Y("값:Q", title="값"),
    color="지표:N"
)

st.altair_chart(line, use_container_width=True)

st.divider()

st.subheader("② 경제활동참가율·고용률 비교")

rate_chart = base.transform_fold(
    ["참여율(%)", "고용률(%)"], as_=["지표", "값"]
).mark_bar().encode(
    y=alt.Y("값:Q", title="비율(%)"),
    color="지표:N"
)

st.altair_chart(rate_chart, use_container_width=True)

st.divider()

# 4) 수업용 콘텐츠 ------------------------------------------------------------
with st.expander("💬 학생 토론 질문"):
    st.markdown("""
- **실업률이 가장 높았던 해**는 언제이며, 그 당시 사회·경제적 상황은 어땠을까?  
- **고용률과 실업률**은 항상 반비례할까? 예외가 있다면 이유는?  
- **코로나19**(2020 년경)가 청년 고용에 미친 구체적 영향은 무엇일까?  
- SDGs 목표 8 관점에서 **‘양질의 일자리’**란 무엇이며, 청년층에게 왜 중요할까?
""")

with st.expander("🎓 교육적 함의"):
    st.markdown("""
1. **자료 해석력 강화** – 실제 국가 통계 읽기·그래프 해석을 통해 수리적 사고 향상  
2. **사회 구조 이해** – 청년 실업·고용 변화를 경제·정책과 연결  
3. **지속가능성 관점** – 데이터 기반으로 ‘포용적‧지속가능한 성장’의 필요성 모색  
4. **비판적 사고** – 지표 간 인과(혹은 상관) 관계를 비판적으로 분석
""")

with st.expander("🚀 확장 활동"):
    st.markdown("""
- **지역별·성별 데이터 추가** → 지역 격차·젠더 관점 분석  
- 과거 추세로 **미래 고용률 예측** → 선형 회귀 등 간단한 ML 모델 실습  
- **청년 인터뷰 프로젝트** → 통계 수치와 실제 경험 비교  
- 관련 **정책 제안서 작성** → 데이터를 근거로 청년 고용 개선 방안 제시
""")

st.info("데이터 출처: 통계청 청년 고용 동향 (2010–2024)  |  © 2025, 교육용 예시 스크립트")
