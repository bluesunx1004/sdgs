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
import plotly.graph_objects as go


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

st.markdown("### 📊 고용률과 실업률 비교 시각화")

fig_dual = go.Figure()

# 막대그래프: 고용률
fig_dual.add_trace(go.Bar(
    x=data["연도"], y=data["고용률(%)"],
    name="고용률(%)", marker_color="deepskyblue", yaxis="y"
))

# 선그래프: 실업률
fig_dual.add_trace(go.Scatter(
    x=data["연도"], y=data["실업률"],
    name="실업률", mode="lines+markers", line=dict(color="orange"), yaxis="y2"
))

# 레이아웃 설정
fig_dual.update_layout(
    title="청년 고용동향 (고용률 및 실업률)",
    xaxis=dict(title="연도"),
    yaxis=dict(title="고용률(%)", range=[30, 50], side="left"),
    yaxis2=dict(title="실업률(%)", overlaying="y", side="right", range=[0, 14]),
    legend=dict(x=0.01, y=0.99),
    bargap=0.2,
    width=900,
    height=500
)

st.plotly_chart(fig_dual, use_container_width=True)

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
