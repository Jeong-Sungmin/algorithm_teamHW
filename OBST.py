import pandas as pd

def bst(p, q):
    """
    최적 이진 탐색 트리(Optimal Binary Search Tree)를 구성하기 위한 함수.
    
    매개변수:
        p (list of float): 각 키(key) 발생 확률 (p[0] ~ p[n-1]), n개의 키
        q (list of float): 각 더미 키(dummy key) 발생 확률 (q[0] ~ q[n]), n+1개의 더미 키
    
    구현 알고리즘:
        동적 계획법(DP)을 사용하여 최적 이진 탐색 트리를 구성하는 최소 비용을 구하고,
        r 테이블을 통해 실제 트리의 루트 구성을 기록한다.
        
    반환값:
        (cost, adjacency_list): 
            cost: 최적 이진 탐색 트리의 최소 비용 값 (float)
            adjacency_list: r 테이블을 이용해 복원한 최적 BST를 인접 리스트 형태로 표현한 딕셔너리
    """
    
    # n은 q의 길이, 실제 키의 개수는 n-1개
    n = len(q)
    
    # w, c, r 테이블 초기화
    # w[i][j]: p와 q의 부분구간 i ~ j에 대한 총 가중치 합
    # c[i][j]: 부분구간 i ~ j를 서브트리로 하는 최적 BST의 최소 비용
    # r[i][j]: 부분구간 i ~ j에서 최적 루트가 되는 키의 인덱스
    w = [[0]*n for _ in range(n)]
    c = [[0]*n for _ in range(n)]
    r = [[0]*n for _ in range(n)]
    
    # 초기 조건:
    # 길이 1짜리 서브트리(즉, 키가 없는 부분: dummy key만 있는 경우)
    # i == j 인 경우, w[i][i] = q[i], c[i][i] = 0
    for i in range(n):
        w[i][i] = q[i]
        c[i][i] = 0
    
    # l은 부분 트리의 길이-1 (즉, 실제 키 개수)
    # l=1부터 시작해서 점차 부분구간을 확장
    for l in range(1, n):
        for i in range(n - l):
            j = i + l
            # w[i][j] = w[i][j-1] + p[j-1] + q[j]
            # p[j-1]: j-1 인덱스의 키가 추가되므로 가중치 증가
            # q[j]: dummy key의 확률도 추가
            w[i][j] = w[i][j-1] + p[j-1] + q[j]
            
            # 최소 비용을 찾기 위해 i < k <= j 범위의 모든 k를 root로 시도
            for k in range(i+1, j+1):
                # c[i][k-1]: 왼쪽 서브트리 비용
                # c[k][j]: 오른쪽 서브트리 비용
                # w[i][j]: 현재 구간 전체 가중치
                # => 전체 비용: c[i][k-1] + c[k][j] + w[i][j]
                temp = c[i][k-1] + c[k][j] + w[i][j]
                
                # 첫 번째 k 또는 더 작은 비용을 찾을 경우 갱신
                if k == i+1:
                    c[i][j] = temp
                    r[i][j] = k
                else:
                    if temp < c[i][j]:
                        c[i][j] = temp
                        r[i][j] = k
                        
    # 테이블 출력(확인용)
    print("w table:")
    print(pd.DataFrame(w))
    print("\nc table:")
    print(pd.DataFrame(c))
    print("\nr table:")
    print(pd.DataFrame(r))
    
    # c[0][n-1]: 전체 구간(0 ~ n-1)에 대한 최적 BST 최소 비용
    # r 테이블을 사용해 트리 구조를 복원할 수 있다.
    
    def construct_tree(r, i, j):
        """
        r 테이블을 통해 (i, j) 구간에서의 최적 서브트리를 재귀적으로 복원하는 함수.
        
        매개변수:
            r (list of list): root 정보 테이블
            i, j (int): 서브트리 범위 인덱스
            
        반환값:
            (root, left_subtree, right_subtree) 형태의 튜플 또는 None
            root: 현재 서브트리의 루트 키 인덱스
            left_subtree: 왼쪽 서브트리에 대한 동일한 구조의 튜플
            right_subtree: 오른쪽 서브트리에 대한 동일한 구조의 튜플
            
            서브트리가 없으면 None을 반환한다.
        """
        if i > j:
            return None
        root = r[i][j]
        if root == 0:
            return None
        # 왼쪽 서브트리는 (i, root-1), 오른쪽 서브트리는 (root, j)
        left_subtree = construct_tree(r, i, root-1)
        right_subtree = construct_tree(r, root, j)
        return (root, left_subtree, right_subtree)
    
    # 전체 트리 복원
    tree = construct_tree(r, 0, n-1)
    
    def tree_to_adjacency(tree):
        """
        복원한 트리 튜플을 인접 리스트로 변환하는 함수.
        
        매개변수:
            tree: (root, left_subtree, right_subtree) 형태의 튜플
            
        반환값:
            adjacency (dict): { 노드인덱스: [왼쪽자식인덱스(있다면), 오른쪽자식인덱스(있다면)] } 형태
        """
        adjacency = {}
        
        def helper(node):
            if node is None:
                return
            root, left, right = node
            adjacency[root] = []
            if left:
                adjacency[root].append(left[0])  # 왼쪽 자식 루트 노드
            if right:
                adjacency[root].append(right[0]) # 오른쪽 자식 루트 노드
            helper(left)
            helper(right)
        
        helper(tree)
        return adjacency
    
    adjacency_list = tree_to_adjacency(tree)

    # 최종 반환:
    # 최소 비용과, 인접 리스트 형태의 트리 구조
    return c[0][n-1], adjacency_list

# 예시 실행
p = [0.04, 0.03, 0.05, 0.03, 0.15, 0.15, 0.05]
q = [0.04, 0.04, 0.03, 0.05, 0.04, 0.1, 0.05, 0.15]

cost, adj = bst(p, q)
print("\nOptimal Cost:", cost)
print("Adjacency List of the BST:", adj)