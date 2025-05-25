import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="대기오염 시각화 및 예측", layout="wide")
st.title("🌫️ 지역별 월별 대기오염 시각화 및 예측 (PM10 기준)")

# 데이터 로딩
@st.cache_data
def load_data():
    df = pd.read_csv("미세먼지_PM10__월별_도시별_대기오염도.csv", encoding="cp949")
    df = df.rename(columns={df.columns[0]: "지역", df.columns[1]: "세부지역"})
    df = df[df["지역"] != "총계"]  # 총계 제거
    df = df.drop(columns=["세부지역"])  # 세부지역도 생략
    df = df.set_index("지역")
    df = df.transpose()  # 월을 index로 변경
    df.index.name = "월"
    df.reset_index(inplace=True)
    return df

df = load_data()

# 지역 선택
regions = df.columns[1:]
selected = st.selectbox("지역 선택", regions)

# 시계열 그래프
st.subheader(f"📈 {selected} 월별 PM10 농도 추이")
fig = px.line(df, x="월", y=selected, markers=True, title=f"{selected}의 월별 PM10 추이")
st.plotly_chart(fig, use_container_width=True)

# 머신러닝 예측: 선형 회귀 기반으로 2024.11 예측
st.subheader("🔮 2024년 11월 PM10 농도 예측 (선형 회귀)")

# 데이터 준비
y = df[selected].values
X = np.arange(len(y)).reshape(-1, 1)
model = LinearRegression()
model.fit(X, y)
pred = model.predict([[len(y)]])[0]
pred = round(pred, 2)

st.success(f"📌 예측된 2024년 11월 {selected}의 PM10 농도는 **{pred} ㎍/m³** 입니다.")
