# pages/07_07_birth_rate_korea.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ───────────────────────── 페이지 설정 ─────────────────────────
st.set_page_config(page_title="🇰🇷 출생아 수 분석", layout="wide")
st.title("👶 대한민국 출생아 수 시각화 (SDG 3, 11)")

# ───────────────────────── 데이터 로드 ─────────────────────────
def read_csv(name):
    path = os.path.join(os.path.dirname(__file__), "..", name)
    if os.path.exists(path):
        return pd.read_csv(path)
    upl = st.file_uploader(f"⬆️ {name} 업로드", type="csv", key=name)
    if upl is not None:
        return pd.read_csv(upl)
    st.stop()

df = read_csv("born baby2.csv")   # 파일명은 정확히 동일하게

# ───────────────────────── 전처리 ──────────────────────────────
# 불필요한 열 제거
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# 컬럼명 정리
if len(df.columns) == 2:
    df.columns = ["연도", "출생아수(천 명)"]

# 숫자형 변환
df["연도"] = pd.to_numeric(df["연도"], errors="coerce")
df["출생아수(천 명)"] = pd.to_numeric(df["출생아수(천 명)"], errors="coerce")
df = df.dropna()

# ───────────────────────── 출생아 수 추세 ─────────────────────
st.markdown("### 📈 출생아 수 변화 추이")

fig_birth = px.line(df, x="연도", y="출생아수(천 명)",
                    markers=True,
                    title="연도별 출생아 수 추이 (천 명 단위)",
                    labels={"출생아수(천 명)": "출생아 수 (천 명)", "연도": "연도"})
fig_birth.update_layout(title_font_size=18)
st.plotly_chart(fig_birth, use_container_width=True)

# ───────────────────────── 최근 연도 강조 ──────────────────────
st.markdown("### 📊 특정 연도의 출생아 수")

sel_year = st.slider("연도 선택", int(df["연도"].min()), int(df["연도"].max()), int(df["연도"].max()))
selected = df[df["연도"] == sel_year]

if not selected.empty:
    count = selected["출생아수(천 명)"].values[0]
    st.metric(label=f"{sel_year}년 출생아 수", value=f"{count:,.0f}천 명")

# ───────────────────────── 데이터 미리보기 ──────────────────────
with st.expander("🔍 원본 데이터 보기"):
    st.dataframe(df)

# ───────────────────────── SDG 연계 & 교육 요소 ────────────────
st.markdown("### 💬 학생 토론 질문")
st.markdown("""
1. 출생아 수가 지속적으로 감소하는 원인은 무엇이라고 생각하나요?  
2. 출생률 감소가 사회에 미치는 영향은 어떤 것이 있을까요?  
3. **SDG 3 '건강과 웰빙'**, **SDG 11 '지속가능한 도시와 공동체'** 관점에서 어떤 정책이 필요할까요?
""")

st.markdown("### 📚 교육적 함의")
st.markdown("""
- **인구통계 데이터 해석**: 출생률 변화를 수치로 이해하고 사회적 의미를 파악  
- **지속가능성 이해**: 출산율과 복지·교육·주거 등 다양한 분야의 연결성 분석  
- **미래 예측**: 데이터 기반 인구 구조 변화 예측 및 대응 방향 논의
""")

st.markdown("### 🚀 확장 활동")
st.markdown("""
- **지역별 출생률 조사**: 우리 지역과 다른 지역의 출생률 차이 비교  
- **청소년 인식 조사**: 결혼·출산에 대한 또래 인식 설문 후 분석  
- **국제 비교 분석**: 저출산 국가 vs 고출산 국가 정책 비교 및 시사점 도출
""")
