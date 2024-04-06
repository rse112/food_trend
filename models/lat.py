import folium

# 지정된 좌표로 사각형 그리기
min_lat, min_lon = 37.53961654940462, 127.06422361155427

# 최대 위도/경도 (직사각형의 반대편 귀퉁이)
max_lat, max_lon = 37.54628751603561, 127.0868159672261

# 지도의 중심을 사각형의 중심으로 설정
map_center_lat = (min_lat + max_lat) / 2
map_center_lon = (min_lon + max_lon) / 2

# 지도 생성
map_seoul = folium.Map(location=[map_center_lat, map_center_lon], zoom_start=15)

# 사각형의 경계 좌표
rectangle_bounds = [(min_lat, min_lon), (min_lat, max_lon), (max_lat, max_lon), (max_lat, min_lon)]

# 사각형 그리기
folium.Polygon(rectangle_bounds, color="red", fill=True, fill_opacity=0.5).add_to(map_seoul)

# 지도 저장
map_file_path = './data/seoul_rectangle_map.html'
map_seoul.save(map_file_path)

map_file_path


