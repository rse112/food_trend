import numpy as np

# 영역 정의 (서울 광진구 지역)
min_lat, max_lat = 37.540, 37.545  # 최소/최대 위도
min_lon, max_lon = 127.060, 127.070  # 최소/최대 경도

# 위도와 경도에 따라 변화하는 거리가 다르기 때문에, 위도에 따른 경도의 변화량을 조정합니다.
# 서울 지역에서 위도 1도는 약 111km, 경도 1도는 약 88.8km에 해당합니다.

# 50미터에 해당하는 위도 변화량
lat_step_size = 50 / 111000  # 위도 1도에 해당하는 거리(미터)

# 50미터에 해당하는 경도 변화량 (위도를 고려하여 조정)
lon_step_size = 50 / (88800 * np.cos(np.radians((min_lat + max_lat) / 2)))  # 경도 1도에 해당하는 거리(미터)

# 그리드 생성
lats = np.arange(min_lat, max_lat, lat_step_size)
lons = np.arange(min_lon, max_lon, lon_step_size)

# 생성된 위도와 경도의 그리드 포인트 수를 확인합니다.
print("Latitude grid points:", len(lats))
print("Longitude grid points:", len(lons))
print(lats, lons)
