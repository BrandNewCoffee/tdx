import requests
from pprint import pprint
import json

access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJER2lKNFE5bFg4WldFajlNNEE2amFVNm9JOGJVQ3RYWGV6OFdZVzh3ZkhrIn0.eyJleHAiOjE3Njk4MzYxMDksImlhdCI6MTc2OTc0OTcwOSwianRpIjoiMjEwYTJiYWYtYjA3MS00ZTUxLWJhYzctM2VmNDYyMmQ5ODg5IiwiaXNzIjoiaHR0cHM6Ly90ZHgudHJhbnNwb3J0ZGF0YS50dy9hdXRoL3JlYWxtcy9URFhDb25uZWN0Iiwic3ViIjoiNDQzOTdjOWEtZGFkNC00MjNkLTk0YzAtNWI5ODllN2FkZDZkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiMzEwNzU4LWYwYjJlMTA2LWEyNzUtNGU2NiIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic3RhdGlzdGljIiwicHJlbWl1bSIsInBhcmtpbmdGZWUiLCJtYWFzIiwiYWR2YW5jZWQiLCJnZW9pbmZvIiwidmFsaWRhdG9yIiwidG91cmlzbSIsImhpc3RvcmljYWwiLCJjd2EiLCJiYXNpYyJdfSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwidXNlciI6ImY1ZWUzNjE5In0.Qg-ehG9cwdCwlTi_EuyN76uBBGk2-NYu-tonV1qqQNZyKKY0_V54lmynvXAoYl1VjXsBBWKdc5-d2wzA4C3UqsmYlwrGliaDAwlBcflDMqd2Isty4aEojvqc1M0mqXKmDHe1FZ2xvp2AhseNmOmA1x_PAc7pWfk9QUaKjjzQWnu6whZujv9r41c0LyXH12ZPyyVReSLcOzenXzzwE71mXAJP8TTkVGd0PFMID7fozlad1P3mvLzWqthsm5tyf2eUD542Faa-wTqowKlWT4-kVWS2lTd1Qs_D2ohb3lCrZuE1vIG2KQmjdA9fAw4aaa0h43WWscgW-JhZbDhr6LLttQ"
url = "https://tdx.transportdata.tw/api/basic/v2/Bus/Route/City/Taipei/612?%24top=30&%24format=JSON"
headers = {
    "authorization": f"Bearer {access_token}"
}

response = requests.get(url, headers=headers)
print(response.status_code)   # 通常是 200 表示成功

data = response.json()[0]  # ← 直接轉成 Python dict / list
print(data['DepartureStopNameZh'],data['DestinationStopNameZh'])
with open("testt.json", "w", encoding="utf-8") as f:
    json.dump((data['DepartureStopNameZh'],data['DestinationStopNameZh']), f, ensure_ascii=False, indent=2)