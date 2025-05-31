import streamlit as st
from datetime import date

st.set_page_config(page_title="플라스틱 사용량 추적기", layout="wide")
st.title("🧃 나의 일회용 플라스틱 사용량 추적기")

st.markdown("""
이 앱은 **당신의 일회용 플라스틱 사용 습관**을 추적하고,  
전 세계 플라스틱 소비 추세와 지구의 쓰레기 문제에 대해 인식할 수 있도록 도와줍니다.  
""")

# 🎯 사용자 입력: 오늘 사용한 일회용 플라스틱
today = date.today().strftime("%Y-%m-%d")
st.subheader("📥 오늘 사용한 일회용 플라스틱 수량을 입력하세요")
cups = st.slider("텀블러 없이 사용한 일회용 컵", 0, 10, 1)
bags = st.slider("비닐봉지", 0, 10, 1)
straws = st.slider("플라스틱 빨대", 0, 10, 1)

total_today = cups + bags + straws

st.metric(label="오늘의 총 사용량", value=f"{total_today} 개")

# 🌿 피드백
if total_today == 0:
    st.success("🌱 멋져요! 오늘은 플라스틱을 사용하지 않았어요.")
elif total_today <= 3:
    st.info("😊 좋은 출발이에요. 내일은 조금 더 줄여볼까요?")
else:
    st.warning("😢 오늘 플라스틱 사용이 많았어요. 대신할 수 있는 대안을 생각해봐요!")


# 🔁 지속 실천 독려
st.markdown("""
> 💡 오늘부터 작은 실천이 모여 큰 변화를 만들어냅니다.  
> 내일은 텀블러 하나, 에코백 하나 챙겨보는 건 어떨까요?
""")
