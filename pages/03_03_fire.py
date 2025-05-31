import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import plotly.express as px
from pathlib import Path

# ──────────────────────── 페이지 설정 ────────────────────────
st.set_page_config(page_title="산불 피해 시각화", layout="wide")
st.title("🔥 연도별 국내 산불 피해 시각화 대시보드")

# ──────────────────────── 한글 폰트 설정 ─────────────────────
font_path = "NanumGothic.ttf"                       # 프로젝트 폴더에 포함
try:
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = font_prop.get_name()
except FileNotFoundError:
    st.warning("NanumGothic.ttf 폰트를 찾지 못했습니다. 기본 폰트를 사용합니다.")

plt.rcParams["axes.unicode_minus"] = False          # 음수 부호 깨짐 방지

# ──────────────────────── 1. 연도별 데이터 로드 ───────────────
@st.cache_data
def load_yearly():
    df = pd.read_csv("2015_2024 fire.csv")
    df.columns = df.columns.str.strip()
    df["연도"] = df["연도"].astype(str)
    return df

yearly_df = load_yearly()

# ──────────────────────── 2. 월별·지역별 데이터 로드 ─────────
@st.cache_data
def load_monthly():
    return pd.read_csv("2025_monthly_fire.csv")

monthly_df = load_monthly()

# ──────────────────────── 3. 연도별 통합 그래프 ───────────────
st.subheader("📊 국내 연도별 산불 발생 건수 & 피해 면적")

fig, ax1 = plt.subplots(figsize=(12, 5))

# ① 피해 면적 (막대, 왼쪽 y축)
bars = ax1.bar(
    yearly_df["연도"], yearly_df["피해면적(ha)"],
    color="darkgreen", alpha=0.6, label="피해 면적(ha)"
)
ax1.set_xlabel("year")
ax1.set_ylabel("Damaged Area(ha)", color="darkgreen")
ax1.tick_params(axis="y", labelcolor="darkgreen")

# ② 발생 건수 (선, 오른쪽 y축)
ax2 = ax1.twinx()
line = ax2.plot(
    yearly_df["연도"], yearly_df["발생 건 수"],
    color="orangered", marker="o", linewidth=2, label="Number of occurrences"
)
ax2.set_ylabel("number", color="orangered")
ax2.tick_params(axis="y", labelcolor="orangered")

# 범례 결합
lines_labels = [*zip(bars, [bars[0].get_label()]), *zip(line, [line[0].get_label()])]
handles, labels = zip(*lines_labels)
ax1.legend(handles, labels, loc="upper center", ncol=2)

ax1.grid(axis="y", linestyle="--", alpha=0.4)
st.pyplot(fig)

# ──────────────────────── 4. 월별·지역별 시각화 ──────────────
# 4-1) 막대 그래프
st.subheader("📊 2025년 월별 지역별 산불 발생 건수")

melted = monthly_df.melt(id_vars="지역", var_name="월", value_name="산불 발생 건수")
melted["월"] = melted["월"].astype(str)

fig_bar = px.bar(
    melted, x="월", y="산불 발생 건수",
    color="지역", barmode="group",
    labels={"월": "월", "산불 발생 건수": "건수"},
    title="월별 산불 발생 추이 (지역별)"
)
st.plotly_chart(fig_bar, use_container_width=True)

# 4-2) 히트맵(데이터프레임 + 그라디언트)
st.subheader("🗺 지역별 월별 산불 발생 건수 (히트맵)")
heatmap_df = melted.pivot(index="지역", columns="월", values="산불 발생 건수")
st.dataframe(
    heatmap_df.style.background_gradient(cmap="OrRd"),
    height=500
)

# ──────────────────────── 5. 토론·교육적 요소 ────────────────
st.markdown("---")
st.subheader("🗣️ 학생 토론 질문")
st.markdown("""
1. **산불 발생 건수와 피해 면적이 항상 비례할까요?**  
   - 그래프에서 비례하지 않는 연도가 있다면 그 이유는 무엇일지 추론해 보세요.  
2. **기후 요인(강수·기온·풍속)** 과 산불 발생의 상관관계는 어떨까요?  
3. **예방 vs. 진화**: 한정된 예산이 있을 때, 어느 쪽에 더 투자해야 피해를 최소화할 수 있을까요?
""")

st.subheader("🎓 교육적 함의")
st.markdown("""
- **데이터 해석 역량**: 동일 축에 다른 단위를 함께 제시해 복합 지표를 읽는 능력 함양  
- **과학·사회 융합**: 산림 생태·기후 과학, 정책·예산 배분 등 다학제적 시각 강조  
- **SDGs 연결**: 목표 13(기후 변화 대응)·15(육상 생태계 보전) 달성의 필요성 인식
""")

st.subheader("🚀 확장 활동")
st.markdown("""
- **기상 데이터 결합**: AI/머신러닝으로 산불 발생 예측 모델 구축  
- **위성 이미지 분석**: 산불로 인한 산림 훼손 영역을 이미지 세그멘테이션으로 추출  
- **지역 맞춤 캠페인**: 각 지역 특성(지형·기상)을 고려한 산불 예방 교육 자료 제작
""")
