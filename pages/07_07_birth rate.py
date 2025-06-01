import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="출산율과 SDGs", layout="centered")

st.title("👶 대한민국 출생아 수 변화와 지속가능한 미래")

# CSV 불러오기
df = pd.read_csv("born baby.csv")

# 컬럼명 자동 출력
st.write("📂 현재 DataFrame의 컬럼:")
st.write(df.columns)
st.write("🔢 컬럼 수:", len(df.columns))
st.dataframe(df.head())

# 'Unnamed: 0'가 있는 경우 제거
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# 열 개수 확인 후 열 이름 지정
if len(df.columns) == 2:
    df.columns = ["연도", "출생아수(천 명)"]

# 숫자형 변환
df["연도"] = pd.to_numeric(df["연도"], errors="coerce")
df["출생아수(천 명)"] = pd.to_numeric(df["출생아수(천 명)"], errors="coerce")
df = df.dropna()

# 시각화
st.subheader("📈 출생아 수 변화 추이")
fig = px.line(df, x="연도", y="출생아수(천 명)", markers=True,
              title="대한민국 출생아 수 추이 (1970~2023)",
              labels={"출생아수(천 명)": "출생아 수 (천 명)", "연도": "연도"})
st.plotly_chart(fig)

# 🔍 최근 10년 평균
st.subheader("📉 최근 10년 평균 출생아 수")
recent_mean = df[df["연도"] >= 2014]["출생아수(천 명)"].mean()
st.write(f"최근 10년 평균 출생아 수는 **{recent_mean:.1f}천 명**입니다.")

# 🌍 SDGs와의 연결
st.subheader("🌍 지속가능발전목표(SDGs)와의 연결")
st.markdown("""
출산율 감소는 다음과 같은 SDGs 목표와 깊은 관련이 있습니다:

- **SDG 3: 건강과 웰빙** – 출산 의료, 산모 건강 관리  
- **SDG 5: 성평등** – 경력단절, 육아 부담의 성별 불균형  
- **SDG 8: 양질의 일자리와 경제성장** – 고용 불안정과 육아 환경  
- **SDG 11: 지속 가능한 도시와 공동체** – 보육시설, 주거환경 등

""")

# 🗣️ 토론 질문
st.subheader("🗣️ 학생 토론 질문")
st.markdown("""
1. 출생아 수가 감소하면 우리 사회에 어떤 영향이 있을까요?  
2. 청소년의 입장에서 아이를 낳고 기르기 쉬운 사회란 어떤 모습일까요?  
3. 저출산 문제를 해결하기 위한 정책은 어떤 방향이어야 할까요?  
4. 성평등과 출산율은 어떤 관계가 있을까요?
""")

# 📚 교육적 함의
st.subheader("📚 교육적 함의")
st.markdown("""
- **데이터를 통한 사회 변화 해석** 능력 향상  
- **SDGs를 실제 사회 문제에 연결**하는 비판적 사고력 강화  
- **정책적 상상력**과 **청소년의 시민 참여 의식** 고취
""")

# 🚀 확장 활동 제안
st.subheader("🚀 확장 활동 제안")
st.markdown("""
- **국가별 출산율 비교 분석** (OECD 등과 비교)  
- **출산율 예측 모델 만들기**: 간단한 회귀모델로 미래 예측  
- **세대 간 인식 비교 조사**: 부모/조부모 인터뷰 과제  
- **정책 제안 프로젝트**: 청소년이 생각하는 '아이 낳고 싶은 사회' 만들기
""")
