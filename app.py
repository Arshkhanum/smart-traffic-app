import streamlit as st
import heapq
from collections import deque
import random

# Graph data (Bengaluru)
graph = {
    'Majestic': {'Rajajinagar': 4, 'Jayanagar': 6},
    'Rajajinagar': {'Yeshwanthpur': 5, 'Majestic': 4},
    'Yeshwanthpur': {'Rajajinagar': 5, 'BTM': 10},
    'Jayanagar': {'Majestic': 6, 'BTM': 3},
    'BTM': {'Jayanagar': 3, 'Silk Board': 2, 'Yeshwanthpur': 10},
    'Silk Board': {'BTM': 2}
}

heuristic = {
    'Majestic': 7, 'Rajajinagar': 6, 'Yeshwanthpur': 10,
    'Jayanagar': 4, 'BTM': 3, 'Silk Board': 0
}

def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

def astar(start, goal):
    pq = [(0, start, [start], 0)]
    visited = set()
    while pq:
        f, current, path, g = heapq.heappop(pq)
        if current == goal:
            return path, g
        visited.add(current)
        for neighbor, cost in graph[current].items():
            if neighbor not in visited:
                g_new = g + cost
                f_new = g_new + heuristic[neighbor]
                heapq.heappush(pq, (f_new, neighbor, path + [neighbor], g_new))

# --- Streamlit App UI ---
st.title("🚦 Smart Traffic Route Finder")
st.write("Uses BFS & A* Search Algorithms (Real-World Simulation)")

cities = list(graph.keys())

start = st.selectbox("Select Start Location", cities)
goal = st.selectbox("Select Destination", cities)

traffic = st.checkbox("Simulate Traffic Conditions")
roadblock = st.checkbox("Block a Road")

if traffic:
    for city in graph:
        for dest in graph[city]:
            graph[city][dest] += random.randint(0, 3)
    st.warning("🚦 Traffic Applied: Route weights increased")

if roadblock:
    block_from = st.selectbox("Block From:", cities)
    block_to = st.selectbox("Block To:", cities)
    if st.button("Block Now"):
        if block_to in graph[block_from]:
            graph[block_from].pop(block_to)
            # st.error(f"🚧 Road blocked: {block_from} -> {block_to}")
    if block_from in graph[block_to]:
        graph[block_to].pop(block_from)

st.error(f"🚧 Road blocked: {block_from} ✖ {block_to} (Both Directions Closed)")

if st.button("Find Best Route"):
    bfs_path = bfs(start, goal)
    a_path, cost = astar(start, goal)

    st.subheader("🔍 Results")
    st.write("➡ BFS Route (Not optimal):", bfs_path)
    st.write("➡ A* Optimal Route:", a_path)
    st.write("🛣 Travel Cost:", cost)

    st.success("A* is better because it uses heuristic intelligence like GPS systems.")
