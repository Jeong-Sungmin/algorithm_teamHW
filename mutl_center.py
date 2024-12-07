import math
from itertools import combinations
from collections import defaultdict, deque
import sys

# Union-Find 자료구조
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, u):
        while self.parent[u] != u:
            self.parent[u] = self.parent[self.parent[u]]
            u = self.parent[u]
        return u
    
    def union(self, u, v):
        u_root = self.find(u)
        v_root = self.find(v)
        if u_root == v_root:
            return False
        self.parent[v_root] = u_root
        return True

# MST 구성 (Kruskal's 알고리즘)
def construct_mst(n, points):
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            dist = math.hypot(points[i][0] - points[j][0], points[i][1] - points[j][1])
            edges.append((dist, i, j))
    edges.sort()
    
    uf = UnionFind(n)
    mst = defaultdict(list)
    for edge in edges:
        dist, u, v = edge
        if uf.union(u, v):
            mst[u].append((v, dist))
            mst[v].append((u, dist))
            if len(mst) == n-1:
                break
    return mst

# c-센터 문제 해결 (트리에서의 k-센터)
def find_centers(n, mst, c):
    # Helper function to check if a given maximum distance allows placing c centers
    def can_place_centers(max_dist):
        centers = 0
        visited = [False] * n
        
        def dfs(u, parent):
            nonlocal centers
            for v, w in mst[u]:
                if v != parent:
                    dfs(v, u)
                    if dp[v] + w > max_dist:
                        centers += 1
                        dp[u] = 0
                    else:
                        dp[u] = max(dp[u], dp[v] + w)
        
        dp = [0] * n
        dfs(0, -1)
        if dp[0] > max_dist:
            centers += 1
        return centers <= c

    # Binary search to find the minimal maximum distance
    left, right = 0, 0
    for u in mst:
        for v, w in mst[u]:
            right += w
    right /= 2  # Since it's undirected

    while left < right:
        mid = (left + right) / 2
        if can_place_centers(mid):
            right = mid
        else:
            left = mid + 1e-5  # Precision adjustment

    # Now, place centers with the found minimal maximum distance
    centers = []
    assignments = [None] * n

    def place_centers(u, parent, current_center):
        nonlocal centers
        for v, w in mst[u]:
            if v != parent:
                if dp[v] + w > left:
                    centers.append(u)
                    assignments[u] = len(centers) - 1
                    dp[v] = 0
                else:
                    dp[v] = max(dp[v], dp[u] + w)
                place_centers(v, u, u)
    
    dp = [0] * n
    place_centers(0, -1, None)
    if dp[0] > left:
        centers.append(0)
        assignments[0] = len(centers) - 1

    return centers, assignments

# 각 정점의 가장 가까운 센터 할당
def assign_centers(n, mst, centers):
    assignments = [None] * n
    distances = [math.inf] * n
    for idx, center in enumerate(centers):
        queue = deque()
        queue.append((center, 0))
        visited = [False] * n
        while queue:
            u, dist = queue.popleft()
            if visited[u]:
                continue
            visited[u] = True
            if dist < distances[u]:
                distances[u] = dist
                assignments[u] = idx
            for v, w in mst[u]:
                if not visited[v]:
                    queue.append((v, dist + w))
    return assignments, distances

# 그래픽 시각화 (선택 사항)
import matplotlib.pyplot as plt

def visualize(n, points, mst, centers, assignments):
    plt.figure(figsize=(10,10))
    # Plot all edges
    for u in mst:
        for v, _ in mst[u]:
            if u < v:  # To avoid double plotting
                plt.plot([points[u][0], points[v][0]], [points[u][1], points[v][1]], 'k-', lw=0.5)
    # Plot all points
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    plt.scatter(x, y, c='blue', s=10)
    # Plot centers
    center_x = [points[c][0] for c in centers]
    center_y = [points[c][1] for c in centers]
    plt.scatter(center_x, center_y, c='red', s=50, marker='^')
    # Annotate centers
    for c in centers:
        plt.annotate(f'C{centers.index(c)}', (points[c][0], points[c][1]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.title('Euclidean MST with Centers')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

def main():
    try:
        # 정점 개수 입력
        n = int(input("정점의 개수를 입력하세요: "))
        if n <= 0:
            print("정점의 개수는 양수여야 합니다.")
            return
        
        # 정점 좌표 입력
        print("각 정점의 좌표를 입력하세요 (예: x y):")
        points = []
        for i in range(n):
            while True:
                inp = input(f"정점 {i}의 좌표: ").strip()
                if not inp:
                    print("입력이 비어 있습니다. 다시 입력하세요.")
                    continue
                try:
                    x, y = map(float, inp.split())
                    if not (0 <= x <= 100 and 0 <= y <= 100):
                        print("좌표는 0 이상 100 이하이어야 합니다.")
                        continue
                    points.append((x, y))
                    break
                except ValueError:
                    print("유효한 두 실수 좌표를 입력하세요.")
        
        # MST 구성
        print("\nMST를 구성하는 중...")
        mst = construct_mst(n, points)
        print("MST가 구성되었습니다.")
        
        # 센터 개수 입력
        while True:
            c = int(input("선택할 센터의 개수를 입력하세요: "))
            if 1 <= c <= n:
                break
            else:
                print(f"센터의 개수는 1 이상 {n} 이하이어야 합니다.")
        
        # 센터 선택
        print("\n센터를 선택하는 중...")
        centers, _ = find_centers(n, mst, c)
        print(f"{c}개의 센터가 선택되었습니다: {centers}")
        
        # 각 정점의 센터 할당
        print("\n각 정점의 가장 가까운 센터를 할당하는 중...")
        assignments, distances = assign_centers(n, mst, centers)
        for i in range(n):
            print(f"정점 {i}은 센터 {assignments[i]}에 할당되었습니다. 거리: {distances[i]:.2f}")
        
        # 그래픽 시각화 (선택 사항)
        while True:
            choice = input("\n그래프를 시각화하시겠습니까? (y/n): ").strip().lower()
            if choice == 'y':
                visualize(n, points, mst, centers, assignments)
                break
            elif choice == 'n':
                print("프로그램을 종료합니다.")
                break
            else:
                print("유효한 입력이 아닙니다. 'y' 또는 'n'을 입력하세요.")
        
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()