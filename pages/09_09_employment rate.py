# pages/09_09_employment_rate.py
"""
청년 고용 동향 분석 – SDG 8 (양질의 일자리와 경제 성장)
이 페이지는 employmentrate.csv 파일(2010‑2024)을 활용해 우리나라 청년 고용 지표를 시각화하고,
학생 토론‧교육적 함의‧확장 활동을 제시합니다.
"""

# ───────────────────── 라이브러리 ─────────────────────
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ───────────────────── 페이지 설정 ─────────────────────
st.set_page_config(page_title="🇰🇷 청년 고용 동향 분석", layout="wide")
st.title("👩‍💼 우리나라 청년 고용 동향 분석 (SDG 8)")

# ───────────────────── 데이터 불러오기 ──────────────────
def read_csv(name: str) -> pd.DataFrame:
    path = os.path.join(os.path.dirname(__file__), "..", name)
    if os.path.exists(path):
        return pd.read_csv(path, encoding="utf-8-sig")
    upl = st.file_uploader(f"⬆️ {name} 업로드", type="csv", key=name)
    if upl is not None:
        return pd.read_csv(upl)
    st.stop()

data = read_csv("employmentrate.csv")

# ───────────────────── 데이터 전처리 ─────────────────────
data = data.set_index("Unnamed: 0").T
data.index.name = "연도"
data = data.applymap(lambda x: float(str(x).replace(",", "")))
data["고용률(%)"] = data["취업자"] / data["경제활동인구"] * 100
data["참여율(%)"] = data["경제활동인구"] / data["생산가능인구"] * 100
data = data.reset_index()
data["연도"] = data["연도"].astype(int)

# ───────────────────── 주요 지표 다중 선택 시각화 ─────────────────────
st.markdown("### 📈 고용 지표 추이 분석")
indicators = ["고용률(%)", "실업률", "참여율(%)"]
selected = st.multiselect("분석할 지표를 선택하세요:", indicators, default=["고용률(%)", "실업률"])

if selected:
    fig = px.line(data, x="연도", y=selected, markers=True,
                  title="연도별 주요 고용 지표 변화",
                  labels={"value": "비율 (%)", "variable": "지표"})
    fig.update_layout(title_font_size=18)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("📌 최소 하나 이상의 지표를 선택하세요.")

# ───────────────────── 고용 지표 설명 ─────────────────────
with st.expander("📘 고용률, 실업률, 참여율이란?"):
    st.markdown("""
    **📌 고용률(%)**  
    → 전체 **경제활동인구 중 취업한 사람의 비율**  
    → 높을수록 고용 상태가 양호함을 의미

    **📌 실업률(%)**  
    → **경제활동인구 중 일할 의사는 있지만 취업하지 못한 사람의 비율**  
    → 높을수록 일자리를 찾기 힘든 환경

    **📌 경제활동참가율(%) (참여율)**  
    → 전체 **생산가능인구 중 경제활동에 참여하는 사람의 비율**  
    → 노동시장에 얼마나 많은 인구가 참여하고 있는지를 나타냄  
    → 높다고 항상 긍정적이라고 할 수는 없으며, 청년층의 경우 **학업 중인 인구가 많을수록 낮을 수도 있음**
    """)


# ───────────────────── 데이터 미리보기 ───────────────────
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(data)

# ───────────────────── SDG 연계 및 수업 요소 ───────────────
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
1. **고용률**이나 **실업률** 중 어떤 지표가 사회 변화를 더 잘 보여준다고 생각하나요? 그 이유는 무엇인가요?
2. 고용 지표가 **뚜렷한 변화 없이 유지**되는 것은 긍정적인가요, 부정적인가요?
3. SDGs **목표 8**의 '양질의 일자리'는 단순한 고용률 외에 어떤 요소들이 포함되어야 할까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- **복합 지표 비교 능력**: 다양한 고용 지표의 상관관계 및 추세 비교 학습
- **정태적 데이터의 해석법**: 큰 변화가 없는 데이터에서도 의미를 찾는 능력 함양
- **지속가능발전 목표 연계 사고**: 수치 이상의 사회적 함의를 고려한 해석 훈련
""")

st.markdown("### 🚀 확장 활동")
st.markdown("""
- **다른 나라의 청년 고용 지표와 비교 분석**
- **뉴스나 정책 자료와 연결한 시사점 도출 활동**
- **나의 미래 직업과 관련된 고용환경 탐색 및 발표**
""")

# ───────────────────── 푸터 ──────────────────────────
st.info("데이터 출처: 통계청 청년 고용 동향(2010–2024) | © 2025, 교육용 예시 스크립트")
