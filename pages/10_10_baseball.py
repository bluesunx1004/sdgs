import streamlit as st
import pandas as pd
import pydeck as pdk

# MLB 팀 정보 예시 데이터
teams = [
    {"team": "Arizona Diamondbacks", "city": "Phoenix, AZ", "lat": 33.4455, "lon": -112.0667, "representative_player": "Corbin Carroll", "player_stats": "2023: 25 HR, .285 AVG, 54 SB"},
    {"team": "Atlanta Braves", "city": "Atlanta, GA", "lat": 33.8908, "lon": -84.4677, "representative_player": "Ronald Acuña Jr.", "player_stats": "2023: 41 HR, .337 AVG, 73 SB"},
    {"team": "Baltimore Orioles", "city": "Baltimore, MD", "lat": 39.2839, "lon": -76.6217, "representative_player": "Adley Rutschman", "player_stats": "2023: 20 HR, .277 AVG"},
    {"team": "Boston Red Sox", "city": "Boston, MA", "lat": 42.3467, "lon": -71.0972, "representative_player": "Rafael Devers", "player_stats": "2023: 33 HR, .271 AVG"},
    {"team": "Chicago White Sox", "city": "Chicago, IL", "lat": 41.8300, "lon": -87.6339, "representative_player": "Luis Robert Jr.", "player_stats": "2023: 38 HR, .264 AVG"},
    {"team": "Chicago Cubs", "city": "Chicago, IL", "lat": 41.9484, "lon": -87.6553, "representative_player": "Dansby Swanson", "player_stats": "2023: 22 HR, .244 AVG"},
    {"team": "Cincinnati Reds", "city": "Cincinnati, OH", "lat": 39.0970, "lon": -84.5070, "representative_player": "Elly De La Cruz", "player_stats": "2023: 13 HR, 35 SB"},
    {"team": "Cleveland Guardians", "city": "Cleveland, OH", "lat": 41.4962, "lon": -81.6852, "representative_player": "José Ramírez", "player_stats": "2023: 24 HR, .282 AVG"},
    {"team": "Colorado Rockies", "city": "Denver, CO", "lat": 39.7559, "lon": -104.9942, "representative_player": "Kris Bryant", "player_stats": "2023: 10 HR, .233 AVG"},
    {"team": "Detroit Tigers", "city": "Detroit, MI", "lat": 42.3390, "lon": -83.0485, "representative_player": "Riley Greene", "player_stats": "2023: 11 HR, .288 AVG"},
    {"team": "Houston Astros", "city": "Houston, TX", "lat": 29.7573, "lon": -95.3555, "representative_player": "Yordan Alvarez", "player_stats": "2023: 31 HR, .293 AVG"},
    {"team": "Kansas City Royals", "city": "Kansas City, MO", "lat": 39.0516, "lon": -94.4805, "representative_player": "Bobby Witt Jr.", "player_stats": "2023: 30 HR, 49 SB"},
    {"team": "Los Angeles Angels", "city": "Anaheim, CA", "lat": 33.8003, "lon": -117.8827, "representative_player": "Mike Trout", "player_stats": "2023: 18 HR, .263 AVG"},
    {"team": "Los Angeles Dodgers", "city": "Los Angeles, CA", "lat": 34.0739, "lon": -118.2396, "representative_player": "Mookie Betts", "player_stats": "2023: 39 HR, .307 AVG"},
    {"team": "Miami Marlins", "city": "Miami, FL", "lat": 25.7781, "lon": -80.2197, "representative_player": "Jazz Chisholm Jr.", "player_stats": "2023: 19 HR, 22 SB"},
    {"team": "Milwaukee Brewers", "city": "Milwaukee, WI", "lat": 43.0280, "lon": -87.9712, "representative_player": "Christian Yelich", "player_stats": "2023: 19 HR, 28 SB"},
    {"team": "Minnesota Twins", "city": "Minneapolis, MN", "lat": 44.9817, "lon": -93.2775, "representative_player": "Carlos Correa", "player_stats": "2023: 18 HR, .230 AVG"},
    {"team": "New York Yankees", "city": "New York, NY", "lat": 40.8296, "lon": -73.9262, "representative_player": "Aaron Judge", "player_stats": "2023: 37 HR, .267 AVG"},
    {"team": "New York Mets", "city": "New York, NY", "lat": 40.7571, "lon": -73.8458, "representative_player": "Francisco Lindor", "player_stats": "2023: 31 HR, 31 SB"},
    {"team": "Oakland Athletics", "city": "Oakland, CA", "lat": 37.7516, "lon": -122.2005, "representative_player": "Brent Rooker", "player_stats": "2023: 30 HR, .246 AVG"},
    {"team": "Philadelphia Phillies", "city": "Philadelphia, PA", "lat": 39.9058, "lon": -75.1665, "representative_player": "Bryce Harper", "player_stats": "2023: 21 HR, .293 AVG"},
    {"team": "Pittsburgh Pirates", "city": "Pittsburgh, PA", "lat": 40.4469, "lon": -80.0057, "representative_player": "Oneil Cruz", "player_stats": "2023: Injured"},
    {"team": "San Diego Padres", "city": "San Diego, CA", "lat": 32.7073, "lon": -117.1566, "representative_player": "Fernando Tatis Jr.", "player_stats": "2023: 25 HR, 29 SB"},
    {"team": "San Francisco Giants", "city": "San Francisco, CA", "lat": 37.7786, "lon": -122.3893, "representative_player": "Logan Webb", "player_stats": "2023: 3.25 ERA, 194 K"},
    {"team": "Seattle Mariners", "city": "Seattle, WA", "lat": 47.5914, "lon": -122.3325, "representative_player": "Julio Rodríguez", "player_stats": "2023: 32 HR, 37 SB"},
    {"team": "St. Louis Cardinals", "city": "St. Louis, MO", "lat": 38.6226, "lon": -90.1928, "representative_player": "Nolan Arenado", "player_stats": "2023: 26 HR, .266 AVG"},
    {"team": "Tampa Bay Rays", "city": "St. Petersburg, FL", "lat": 27.7683, "lon": -82.6534, "representative_player": "Randy Arozarena", "player_stats": "2023: 23 HR, 22 SB"},
    {"team": "Texas Rangers", "city": "Arlington, TX", "lat": 32.7513, "lon": -97.0820, "representative_player": "Corey Seager", "player_stats": "2023: 33 HR, .327 AVG"},
    {"team": "Toronto Blue Jays", "city": "Toronto, ON", "lat": 43.6414, "lon": -79.3894, "representative_player": "Bo Bichette", "player_stats": "2023: 20 HR, .306 AVG"},
    {"team": "Washington Nationals", "city": "Washington, DC", "lat": 38.8730, "lon": -77.0074, "representative_player": "CJ Abrams", "player_stats": "2023: 18 HR, 47 SB"}
]


df = pd.DataFrame(teams)

# Streamlit 화면 구성
st.title("🏟️ 미국 메이저리그 팀 지도")
st.markdown("MLB 팀의 위치를 확인하고, 각 팀 대표 선수의 전적을 살펴보세요.")

# pydeck 지도 시각화
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lon, lat]',
    get_radius=50000,
    get_fill_color=[200, 30, 0, 160],
    pickable=True
)

tooltip = {
    "html": """
    <b>{team}</b><br/>
    🏙️ {city}<br/>
    ⭐ 대표 선수: {representative_player}<br/>
    📊 전적: {player_stats}
    """,
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

view_state = pdk.ViewState(
    latitude=39.8283,
    longitude=-98.5795,
    zoom=3.5,
    pitch=0
)

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    )
)
