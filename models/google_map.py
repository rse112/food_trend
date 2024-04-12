import requests
import pandas as pd
import time
from models.utils import get_secret
import numpy as np
import os

# API 키 및 URL 설정
api_key = get_secret("google_api_key")  # 여기에 실제 API 키 입력

# 영역 정의
min_lat, min_lon = 37.53961654940462, 127.06422361155427

# 최대 위도/경도 (직사각형의 반대편 귀퉁이)
max_lat, max_lon = 37.54628751603561, 127.0868159672261

# 50미터 간격으로 그리드 생성
lat_step = 50 / 110574  # 위도 1도에 대략 111km
lon_step = 50 / (
    111320 * np.cos(np.radians(min_lat))
)  # 경도 1도에 대략 111km * cos(latitude)

# 그리드 포인트 생성
lat_points = np.arange(min_lat, max_lat, lat_step)
lon_points = np.arange(min_lon, max_lon, lon_step)

# 수집된 데이터를 저장할 리스트
restaurants = []

# 각 그리드 포인트에 대해 요청 실행
for lat in lat_points:
    for lon in lon_points:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=50&type=restaurant&key={api_key}"

        while True:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch data: Status code {response.status_code}")
                break

            data = response.json()
            if data["status"] != "OK":
                print(
                    f"API request failed: {data.get('error_message', 'Unknown error')}"
                )
                break

            # 현재 페이지의 결과 추가
            restaurants.extend(data["results"])

            # 다음 페이지 토큰 확인
            page_token = data.get("next_page_token")
            if page_token:
                url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={page_token}&key={api_key}"
                time.sleep(2)  # 대기 시간 준수
            else:
                break  # 다음 페이지가 없으면 중단

# 결과를 DataFrame으로 변환
if restaurants:
    df_restaurants = pd.DataFrame(restaurants)
    # 중복 데이터 제거
    df_restaurants = df_restaurants.drop_duplicates(subset="place_id")

    # 필요한 컬럼 선택
    df_restaurants = df_restaurants[["name", "vicinity", "geometry", "types"]]

    # 위도, 경도 컬럼 추가
    df_restaurants["latitude"] = df_restaurants.apply(
        lambda row: row["geometry"]["location"]["lat"], axis=1
    )
    df_restaurants["longitude"] = df_restaurants.apply(
        lambda row: row["geometry"]["location"]["lng"], axis=1
    )

    # 필요 없는 컬럼 삭제
    df_restaurants = df_restaurants.drop(columns="geometry")

    # CSV 파일로 저장
    df_restaurants.to_csv("./datarestaurants_in_gwangjin_gu_seoul.csv", index=False)
    print("Data collection complete. CSV file saved.")
else:
    print("No data collected.")
