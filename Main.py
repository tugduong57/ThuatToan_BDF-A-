
# Hàm heuristic
def heuristic(current, goal, H):
    return H.get((current, goal), float('inf'))

# Thuật toán A* tìm đường đi từ start đến mid_point
def a_star(start, mid_point, G_Cost, Graph, H):
    open_list = [(start, G_Cost[start])]
    g_cost = {start: G_Cost[start]}  
    f_cost = {start: heuristic(start, mid_point, H)} 
    came_from = {}
    
    while open_list:
        open_list.sort(key=lambda x: x[1])
        current = open_list.pop(0)
        current_node = current[0]; current_g = current[1]
        
        if current_node == mid_point:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            return path[::-1]  

        if current_node in Graph:
            for neighbor in Graph[current_node]:
                # Tổng chi phí từ nốt hiện tại tới nốt neighbor
                tong_g = current_g + G_Cost.get(neighbor, float('inf'))
                
                if neighbor not in g_cost or tong_g < g_cost[neighbor]:
                    g_cost[neighbor] = tong_g
                    f_cost[neighbor] = tong_g + heuristic(neighbor, mid_point, H)
                    open_list.append((neighbor, tong_g))
                    came_from[neighbor] = current_node
    return None

def bfs(start, goal, Graph):
    visited = set()
    queue = [start] 
    visited.add(start)
    came_from = {}
    while queue:
        current = queue.pop(0)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for neighbor in Graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor) 
                queue.append(neighbor) 
                came_from[neighbor] = current
    
    return None 


# Đọc đồ thị từ tệp
with open("dothi2.txt") as inp:
    n, start, end = inp.readline().split()  # Số lượng đỉnh, bắt đầu và kết thúc
    n = int(n)
    Nodes = {}
    for i in range(n):
        node, gn = inp.readline().split()
        Nodes[node] = int(gn)  # Tập đỉnh lưu chi phí G(n)
    
    T = {}  # Lưu đồ thị
    H = {}  # Lưu giá trị đánh giá h của mỗi cạnh
    x = inp.readline()
    while x != "-1":
        s, e, h = x.split()
        if s not in T:
            T[s] = []  # Khởi tạo danh sách các đỉnh kề
        T[s].append(e)
        H[(s, e)] = int(h)  # Lưu giá trị heuristic giữa s và e
        x = inp.readline()

# Chạy A* từ start đến điểm trung gian
mid_point = list(Nodes.keys())[n-3]  
path1 = a_star(start, mid_point, Nodes, T, H)
print("Đường đi từ {} đến {} theo A_star:".format(start, mid_point))
print(path1)

# Dùng BFS từ mid_point đến goal
path2 = bfs(mid_point, end, T)
print("Đường đi từ {} đến {} theo BFS:".format(mid_point, end))
print(path2)

# Kết hợp hai đường đi
if path1 and path2:
    full_path = path1[:-1] + path2
    print("Tổng đường đi từ {} đến {}:".format(start, end))
    print(full_path)
else:
    print("Không tìm thấy đường đi.")
