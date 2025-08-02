import requests

def get_weather(city, api_key):
    """
    從 OpenWeatherMap API 獲取指定城市的天氣資訊。

    Args:
        city (str): 城市名稱
        api_key (str): OpenWeatherMap 的 API 金鑰

    Returns:
        dict: 天氣資訊字典（成功時）或 None（失敗時）
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric',  # 改為攝氏溫度
            'lang': 'zh_tw'     # 顯示繁體中文描述
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        weather = {
            '城市': data['name'],
            '天氣': data['weather'][0]['description'],
            '氣溫': f"{data['main']['temp']}°C",
            '體感溫度': f"{data['main']['feels_like']}°C",
            '濕度': f"{data['main']['humidity']}%",
            '風速': f"{data['wind']['speed']} m/s"
        }

        return weather

    except requests.exceptions.RequestException as e:
        print(f"連線錯誤：{e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"資料解析錯誤：{e}")
        return None


if __name__ == "__main__":
    api_key = "4e80d551541e0bcc4d781a4067594fed"

    while True:
        city = input("\n請輸入城市名稱（英文，例如 Taipei）：或輸入N結束程式")
        
        if city == 'N':
            print("👋 已結束查詢。")
            break
          
        weather = get_weather(city, api_key)

        if weather:
            print("\n🌤 天氣資訊：")
            for key, value in weather.items():
                print(f"{key}: {value}")
        else:
            print("⚠️ 無法取得天氣資訊，請確認城市名稱或 API 金鑰。")

        
