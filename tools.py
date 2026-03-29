from utils import haversine

def get_distance_matrix(locations):
    n = len(locations)
    matrix = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = haversine(locations[i], locations[j])

    return matrix


def optimize_route(locations):
    n = len(locations)
    visited = [False]*n
    route = [0]
    visited[0] = True

    for _ in range(n-1):
        last = route[-1]
        next_city = min(
            [(i, haversine(locations[last], locations[i]))
             for i in range(n) if not visited[i]],
            key=lambda x: x[1]
        )[0]

        route.append(next_city)
        visited[next_city] = True

    return route


def predict_delay(weather="clear", traffic="low"):
    score = 0

    if weather == "rain":
        score += 2
    if traffic == "high":
        score += 3

    if score >= 4:
        return "High Delay Risk"
    elif score >= 2:
        return "Moderate Delay"
    else:
        return "Low Delay"