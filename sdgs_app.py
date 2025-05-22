# sdgs_app.py

import streamlit as st
from sdgs_data import SDGS
import os

st.set_page_config(page_title="SDGs 소개", layout="wide")

st.title("🌍 지속가능발전목표 (SDGs) 알아보기")
st.markdown("유엔이 채택한 **17가지 지속가능발전목표(SDGs)** 를 시각적으로 탐색해보세요!")

# 두 줄씩 3열로 카드 배치
cols = st.columns(3)

for i, sdg in enumerate(SDGS):
    col = cols[i % 3]

    with col:
        with st.expander(f"🎯 {sdg['id']}. {sdg['title']}"):
            image_path = f"images/sdg{sdg['id']}.png"
            if os.path.exists(image_path):
                st.image(image_path, width=100)
            st.write(f"**간단 설명:** {sdg['short']}")
            st.write(f"**자세한 설명:** {sdg['detail']}")
            st.write(f"**사례:**\n{sdg['example']}")
