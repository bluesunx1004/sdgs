# pages/09_09_employment_rate.py
"""
청년 고용 동향 분석 – SDG 8 (양질의 일자리와 경제 성장)
이 페이지는 employmentrate.csv 파일(2010‑2024)을 활용해 우리나라 청년 고용 지표를 시각화하고,
학생 토론‧교육적 함의‧확장 활동을 제시합니다.
"""

# ───────────────────── 라이브러리 ─────────────────────
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

raw = read_csv("employmentrate.csv")

# ───────────────────── 데이터 전처리 ─────────────────────
raw = raw.set_index("Unnamed: 0").T
raw.index.name = "연도"
raw = raw.applymap(lambda x: float(str(x).replace(",", "")))
raw["고용률(%)"] = raw["취업자"] / raw["경제활동인구"] * 100
raw["참여율(%)"] = raw["경제활동인구"] / raw["생산가능인구"] * 100
raw = raw.reset_index()
raw["연도"] = raw["연도"].astype(int)

# ───────────────────── 주요 지표 복합 시각화 ───────────────────
st.markdown("### 📊 고용률과 실업률 추이 비교")
fig_combo = go.Figure()
fig_combo.add_trace(go.Bar(x=raw["연도"], y=raw["고용률(%)"], name="고용률(%)",
                           marker_color="skyblue"))
fig_combo.add_trace(go.Scatter(x=raw["연도"], y=raw["실업률"], name="실업률(%)",
                               mode="lines+markers", line=dict(color="crimson", width=3)))
fig_combo.update_layout(title="고용률(%)과 실업률(%)의 연도별 변화",
                        xaxis_title="연도", yaxis_title="비율 (%)",
                        barmode="group", title_font_size=18)
st.plotly_chart(fig_combo, use_container_width=True)

# ───────────────────── 데이터 미리보기 ───────────────────
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(raw)

# ───────────────────── SDG 연계 및 수업 요소 ───────────────
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
1. **실업률이 가장 높았던 해**는 언제이며, 그 해의 사회·경제적 요인은 무엇이었나요?  
2. **고용률과 실업률**이 동시에 상승하거나 하락한 해가 있다면 왜 그런 현상이 나타났을까요?  
3. SDGs **목표 8** 관점에서 _"양질의 일자리"_ 는 어떤 기준으로 판단할 수 있을까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- **복합지표 해석력 향상**: 두 지표의 동시 시각화를 통해 다양한 경제적 의미 도출  
- **정책 분석 사고력 강화**: 고용 및 실업률 추세로부터 사회 구조의 변화 유추  
- **지속가능발전 목표 연결**: 데이터로 보는 경제 성장과 일자리의 질 문제
""")

st.markdown("### 🚀 확장 활동")
st.markdown("""
- **성별 또는 지역별 고용 지표 추가 분석**  
- **코로나19 전후 비교 분석**으로 청년 고용환경 변화 고찰  
- **미래 고용 지표 시나리오 작성 및 발표**
""")

# ───────────────────── 푸터 ──────────────────────────
st.info("데이터 출처: 통계청 청년 고용 동향(2010–2024) | © 2025, 교육용 예시 스크립트")
