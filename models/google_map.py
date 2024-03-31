import requests
import pandas as pd

# API 키 및 URL 설정
api_key = "AIzaSyDGo7v_t8bl1GZKU0MuX6UMsVJVSAeHgMk"  # 여기에 실제 API 키 입력
query = "restaurants in Gwangjin-gu Seoul"
url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"

# API 요청
response = requests.get(url)
restaurants = response.json()

# 음식점 이름 추출
restaurant_names = [restaurant["name"] for restaurant in restaurants["results"]]

# DataFrame 생성
df = pd.DataFrame(restaurant_names, columns=["Restaurant Name"])

# CSV 파일로 저장
df.to_csv("restaurants_in_seoul.csv", index=False)
print("CSV 파일이 저장되었습니다.")
