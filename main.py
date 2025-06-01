import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="SDGs 데이터 탐구",
    page_icon="🌍",
    layout="wide"
)

# 제목
st.title("🌱 지속가능한 미래를 위한 탐구: SDGs 데이터로 배우는 세상")

# 간단한 소개 문단
st.markdown("""
---

이 웹페이지는 **고등학생** 여러분이 UN의 지속가능발전목표(SDGs, Sustainable Development Goals)**에 대해  
더 깊이 있게 탐구하고, 실제 데이터를 통해 세상을 이해하는 힘을 기를 수 있도록 설계되었습니다.  

🔍 **무엇을 할 수 있나요?**
- SDGs 17가지 목표 중 관심 있는 주제를 선택할 수 있어요.
- 전 세계 데이터 시각화를 통해 현황을 비교하고 이해할 수 있어요.
- 데이터를 기반으로 나만의 탐구 주제를 설정하고 분석할 수 있어요.

💡 **이 페이지는 데이터와 함께 생각하는 힘을 기르는 곳입니다.**

---

""")



# 간단한 동기 유발
st.markdown("""
🎯 지금부터 데이터를 통해 **지속가능한 세상**을 함께 탐험해볼까요?

👉 왼쪽 메뉴에서 시작할 내용을 선택해보세요!
""")



# ▶ 통계청 SDGs 지표 사이트 안내
st.markdown("""
### 🔗 SDGs 데이터 한눈에 보기  
국내 SDGs 지표를 종합적으로 확인하려면 **통계청 SDGs 지표 대시보드**를 참고하세요.  
[👉 통계청 SDGs 지표 사이트 바로가기](https://kostat-sdg-kor.github.io/sdg-indicators/goals/)
""")

