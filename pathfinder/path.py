from pathfinder import dijkstra
import requests
import json

def getPath(startX, startY, endX, endY, passList):
    url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1"
    payload = {
        "angle": 0,
        "speed": 0,
        "reqCoordType": "WGS84GEO",
        "searchOption": "0",
        "resCoordType": "WGS84GEO",
        "sort": "index",
        "startX": startX,
        "startY": startY,
        "endX": endX,
        "endY": endY,
        "passList": passList,
        "startName": "start",
        "endName": "goal"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "appKey": "l7xxfdc75c1509a74ecdba02bf5e024ee9d5"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response

def main():
    latitude = dijkstra.latitude    # dijkstra.py에서 안전거점들의 위경도 가져오기
    longitude = dijkstra.longitude

    path = dijkstra.path[0] # 경유지로 설정할 안전거점의 번호
    waypoints_lat = []; waypoints_lng = []
    for i in path:
        waypoints_lat.append(latitude[i])
        waypoints_lng.append(longitude[i])

    pathCoord = []  # 전체 경로 좌표 저장할 리스트
    waypoints = ''  # 요청 url의 경유지 파라미터에 추가할 경유지 텍스트

    for i in range(len(waypoints_lat)):
        if i != len(waypoints_lat)-1:
            if i%7 == 0:
                startX = waypoints_lng[i]; startY = waypoints_lat[i]
            elif i%7 == 6:
                endX = waypoints_lng[i]; endY = waypoints_lat[i]
                passList = waypoints[:-1]
                pathInfo = getPath(startX, startY, endX, endY, passList)    # 출발지, 목적지, 5개 이하의 경유지를 getpath의 파라미터로 제공
                pathInfo_json = json.loads((pathInfo.text)) # 응답받은 데이터를 json형식으로 변환
                for j in range(len(pathInfo_json['features'])): # 경로의 좌표 추출 후 pathCoord에 저장
                    pathCoord.append(pathInfo_json['features'][j]['geometry']['coordinates'])
                print(pathCoord)
                waypoints = ''  # 경유지 텍스트 초기화
            else:
                waypoints = waypoints + str(waypoints_lng[i]) + ',' + str(waypoints_lat[i]) + '_'
        else:
            endX = waypoints_lng[i]; endY = waypoints_lat[i]
            passList = waypoints[:-1]
            pathInfo = getPath(startX, startY, endX, endY, passList)
            pathInfo_json = json.loads((pathInfo.text))
            for j in range(len(pathInfo_json['features'])):
                pathCoord.append(pathInfo_json['features'][j]['geometry']['coordinates'])
            print(pathCoord)

    return pathCoord

# asdf = getPath(startX, startY, endX, endY, passList)
# print(asdf.text)
# [0]['geomatry']['coordinates']
#
# if __name__ == '__main__':
#     main()