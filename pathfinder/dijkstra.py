# 다익스트라 알고리즘을 활용하여 안전거점을 경유지로 설정하는 코드

import copy
from haversine import haversine
from crawling import crawling_cctv

INF = int(1e9)  # 인접하지 않은 노드로 설정하는 변수
cctv_info = crawling_cctv.getInfo() # 동구 cctv의 정보를 추출하는 함수 호출 후 cctv_info에 저장 ('num', 'longitude', 'latitude', 'adress', 'manager_name', 'phone_number')
node_info = []  # 안전거점 정보 저장하는 리스트
for list in cctv_info:
    node_info.append(list)

latitude = []; longitude = []
for list in node_info:
    latitude.append(list['latitude']); longitude.append((list['longitude']))

# start_lat = 35.14429517145534; start_lng = 126.93008706784543   # search.html에서 입력받은 출발지의 위경도값
# finish_lat = 35.15134758807111; finish_lng = 126.93696208830134
start_lat = 35.14615224741997; start_lng = 126.92309512644327
finish_lat = 35.146462003524306; finish_lng = 126.92847205021735
# start_lat = 35.18033359239622; start_lng = 126.89034165213242 # 길찾기에 실패하면 경로가 표시되지 않음
# finish_lat = 35.18192617178464; finish_lng = 126.89740977660219

latitude.append(start_lat); latitude.append(finish_lat)
longitude.append(start_lng); longitude.append(finish_lng)

def getDistance():  # 노드간 거리 계산하는 함수


    distance = []
    for i in range(len(latitude)):
        line = []
        for j in range(len(longitude)):
            coord1 = (float(latitude[i]), float(longitude[i]))
            coord2 = (float(latitude[j]), float(longitude[j]))
            line.append(haversine(coord1, coord2, unit='m'))
        distance.append(line)

    return distance

def getEdge(limit): # 거리가 limit미터 이상이면 이웃하지 않은 노드로 설정하는 함수
    distance = getDistance()
    for i in range(0, len(distance)):
        for j in range(0, len(distance[i])):
            edge = distance[i][j]
            if edge > limit:
                distance[i][j] = INF

    return distance

def dijkstra(limit):
    n = len(node_info)+2 # 노드의 개수

    start = n-2    # 시작노드 값을 입력받고 start에 저장
    finish = n-1

    # 노드와 간선의 정보가 담긴 그래프 만들기
    # {0: {0: 0, 1: 1000...}, 1: {0: 1000, 1: 0...}...}  (0번 노드에서 0번 노드까지의 거리는 0, 1번 노드에서 0번 노드까지의 거리는 1000)
    dist = getEdge(limit)
    node = {}
    for i in range(len(dist)):
        node[i] = {}
        for j in range(len(dist)):
            if dist[i][j] != INF:  # 만약 i 노드와 j 노드가 인접하다면
                node[i][j] = dist[i][j]   # {'i노드에서: {j노드까지: 거리}}

    # 시작노드에서 각 노드까지의 최단거리, 경로, 방문여부 저장하는 딕셔너리
    routing = {}
    for place in node.keys():
        routing[place] = {'shortestDist': 0, 'route': [], 'visited': 0}

    # 최단거리, 경로, 방문여부 설정
    def visitPlace(visit):
        routing[visit]['visited'] = 1
        for toGo, betweenDist in node[visit].items():  # visit노드의 인접노드들 확인하면서
            toDist = routing[visit]['shortestDist'] + betweenDist   # 시작노드에서 visit노드까지의 거리 + visit노드에서 인접노드까지의 거리를 toDist에 저장
            if (routing[toGo]['shortestDist'] >= toDist) or not routing[toGo]['route']: # 시작노드에서 visit의 인접노드까지의 거리가 toDist보다 크거나 루트가 없다면
                routing[toGo]['shortestDist'] = toDist  # 시작노드에서 visit의 인접노드까지의 최단거리를 toDist로 설정
                routing[toGo]['route'] = copy.deepcopy(routing[visit]['route']) # 시작노드에서 visit노드까지의 루트를 복사하고 인접노드의 루트에 붙여넣기
                routing[toGo]['route'].append(visit)    # 루트에 visit노드 추가

    # 시작노드의 인접노드부터 설정
    visitPlace(start)


    while 1 :
        minDist = max(routing.values(), key=lambda x:x['shortestDist'])['shortestDist'] # routing 딕셔너리에서 shortestDist값이 가장 큰것을 고르고 minDist에 저장
        toVisit = ''
        for name, search in routing.items():    # routing의 key값을 name에, value값을 search에 저장하고 routing의 끝까지 반복
            if 0 < search['shortestDist'] <= minDist and not search['visited']: # routing의 shotestDist값이 minDist보다 작거나 같고 visited값이 없을때, 즉 방문하지 않았을때
                minDist = search['shortestDist']
                toVisit = name

        if toVisit == '':
            break

        visitPlace(toVisit)

    route = routing[finish]['route']
    distance = routing[finish]['shortestDist']
    return route, distance

n = 100
while 1:
    path = dijkstra(n)
    if path[1] == 0 and n < 500:
        n += 100
    else:
        break

