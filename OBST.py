"""OBST"""
import pandas as pd

def bst(p, q):
    # Initialize tables
    n = len(q) if len(p) < len(q) else len(p)
    w = [[0]*n for _ in range(n)]
    c = [[0]*n for _ in range(n)]
    r = [[0]*n for _ in range(n)]
    
    # Fill in the tables
    for i in range(n):
        w[i][i] = q[i]
        c[i][i] = 0
        
    for l in range(1, n):
        for i in range(n-l):
            j = i + l
            w[i][j] = w[i][j-1] + p[j-1] + q[j]
            for k in range(i+1, j+1):
                temp = c[i][k-1] + c[k][j] + w[i][j]
                if k == i + 1:
                    c[i][j] = temp
                    r[i][j] = k
                else:
                    if temp < c[i][j]:
                        c[i][j] = temp
                        r[i][j] = k
                        
    # Create dataframes for w, c, and r
    df_w = pd.DataFrame(w)
    df_c = pd.DataFrame(c)
    df_r = pd.DataFrame(r)

    # Display the dataframes
    print("w table:")
    print(df_w)

    print("c table:")
    print(df_c)

    print("r table:")
    print(df_r)
    return c[0][len(q)-1]

# p = [0.14, 0.1, 0.05, 0.25]
# q = [0.09, 0.05, 0.04, 0.08, 0.2]
p = [0.04, 0.03, 0.05, 0.03, 0.15, 0.15, 0.05]
q = [0.04, 0.04, 0.03, 0.05, 0.04, 0.1, 0.05, 0.15]
print(bst(p, q))  # 2