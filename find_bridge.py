from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
        self.time = 0  # 전역 시간 변수

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def bridge_util(self, u, visited, parent, low, disc, bridges):
        visited[u] = True
        disc[u] = self.time
        low[u] = self.time
        self.time += 1

        for v in self.graph[u]:
            if not visited[v]:
                parent[v] = u
                self.bridge_util(v, visited, parent, low, disc, bridges)

                # 현재 노드의 low 값을 자식 노드의 low 값과 비교
                low[u] = min(low[u], low[v])

                # 브리지 조건: low[v] > disc[u]
                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent[u]:
                # 역방향 간선인 경우 low[u]를 갱신
                low[u] = min(low[u], disc[v])

    def find_bridges(self):
        visited = [False] * self.V
        disc = [float('inf')] * self.V
        low = [float('inf')] * self.V
        parent = [-1] * self.V
        bridges = []

        for i in range(self.V):
            if not visited[i]:
                self.bridge_util(i, visited, parent, low, disc, bridges)

        return bridges

    def is_bridge(self, edge):
        u, v = edge
        all_bridges = self.find_bridges()
        # 간선이 양방향으로 저장되므로 양쪽을 확인
        return (u, v) in all_bridges or (v, u) in all_bridges

def main():
    try:
        V = int(input("정점개수를 입력:> "))
        g = Graph(V)
        print("간선의 양 끝점을 입력하고 엔터를 누르시오 (종료: -1 -1):")
        while True:
            inp = input().strip()
            if not inp:
                continue
            u, v = map(int, inp.split())
            if u == -1 and v == -1:
                break
            if u < 0 or u >= V or v < 0 or v >= V:
                print("유효하지 않은 정점 번호입니다. 다시 입력하세요.")
                continue
            g.add_edge(u, v)

        bridges = g.find_bridges()
        if bridges:
            print("\n브리지(Bridge) 목록:")
            for bridge in bridges:
                print(f"{bridge[0]} - {bridge[1]}")
        else:
            print("\n브리지가 없습니다.")

        while True:
            choice = input("\n특정 간선이 브리지인지 확인하시겠습니까? (y/n): ").strip().lower()
            if choice == 'y':
                print("간선 목록")
                for u in range(V):
                    for v in g.graph[u]:
                        if u < v:
                            print(f"{u} - {v}")
                edge_input = input("간선의 양 끝점을 입력하세요 (예: 0 3): ").strip()
                if not edge_input:
                    print("입력이 비어 있습니다. 다시 시도하세요.")
                    continue
                try:
                    u, v = map(int, edge_input.split())
                    if g.is_bridge((u, v)):
                        print(f"간선 {u} - {v} 는 브리지입니다.")
                    else:
                        print(f"간선 {u} - {v} 는 브리지가 아닙니다.")
                except ValueError:
                    print("유효한 두 정점 번호를 입력하세요.")
            elif choice == 'n':
                print("프로그램을 종료합니다.")
                break
            else:
                print("유효한 입력이 아닙니다. 'y' 또는 'n'을 입력하세요.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()