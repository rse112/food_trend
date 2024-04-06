import folium
import pandas as pd

file_path = './data/restaurants_in_gwangjin_gu_seoul_extended.csv'

# 파일 로드
df = pd.read_csv(file_path)
# 서울 광진구의 대략적 중심 좌표
center_lat, center_lon = df['latitude'].mean(), df['longitude'].mean()

# 지도 생성
map_gwangjin = folium.Map(location=[center_lat, center_lon], zoom_start=14)

# 레스토랑 위치에 마커 추가
for idx, row in df.iterrows():
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=row['name'],
        tooltip=row['name']
    ).add_to(map_gwangjin)

# 지도 저장
map_file_path = './data/gwangjin_gu_restaurants_map.html'
map_gwangjin.save(map_file_path)

map_file_path