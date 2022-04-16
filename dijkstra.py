import sys
input = sys.stdin.readline
INF = int(1e9)

n, m = map(int, input().split())    # 각각 한개의 변수를 입력받은 n, m을 map에 저장. n은 노드의 개수
start = int(input())    # 시작노드 값을 입력받고 start에 저장

# 주어지는 그래프 정보 담는 N개 길이의 리스트
graph = [[] for _ in range(n+1)]
visited = [False] * (n+1)   # 방문처리 기록용. 노드가 이 리스트에 방문했으면 False가 1이 돼서 n+1번 노드는 방문했다 라고 리스트에 기록됨
distance = [INF] * (n+1)    # 거리 테이블용

for _ in range(m):
    a, b, c = map(int, input().split())
    graph[a].append((b,c))

# 방문하지 않은 노드이면서 시작노드와 최단거리인 노드 반환
def get_smallest_node():
    min_value = INF # 최단거리
    index = 0   # 최단거리인 노드
    for i in range(1, n+1):
        if not visited[i] and distance[i] < min_value:  # visited 리스트에 현재 노드가 없고 거리가 최단거리보다 작으면
            min_valu = distance[i]  # 현재 노드의 거리를 최단거리로 기록
            index = i   # 현재 노드를 최단거리 노드로 설정
        return index    # 현재 노드 반환

# 다익스트라 알고리즘
def dijkstra(start):
    # 시작노드 -> 시작노드 거리 계산 및 방문처리
    distance[start] = 0 # 시작노드 -> 시작노드 거리는 0
    visited[start] = True   # 시작노드는 방문했으니 true로

    # 시작노드 제외한 n-1개의 다른 노드들 처리
    for _ in range(n-1):
        now = get_smallest_node()   # 방문하지 않은 노드이면서 시작노드와 최단거리인 노드 반환
        visited[now] = True # 해당 노드 방문처리
        # 해당 노드의 인접한 노드들 간의 거리 계산
        for next in graph[now]: # 방문하지 않은 노드이면서 시작노드와 최단거리인 노드를 더이상 찾지 못할때 까지
            cost = distance[now] + next[1]  # (시작노드에서 now노드까지 거리) + (now노드에서 now의 인접노드까지 거리)
            if cost < distance[now] + next[0]:  # (위의 cost) < (시작 -> now의 인접노드까지의 직선 거리) 이면, 즉 최단거리면
                distance[next[0]] = cost    # next[0]의 거리를 cost(최단거리)로 설정


dijkstra(start)

for i in range(1, n+1):
    if distance[i] == INF:
        print('도달 할 수 없음')
    else:
        print(distance[i])