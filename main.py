import random
from numpy import *
from utils import *

# The Romania road map taken from the book and translated into a dictionary
routes = {
    "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
    "Zerind": [("Arad", 75), ("Oradea", 71)],
    "Timisoara": [("Arad", 118), ("Lugoj", 111)],
    "Sibiu": [("Arad", 140), ("Fagaras", 99), ("Rimnicu Valcea", 80)],
    "Oradea": [("Zerind", 71), ("Sibiu", 151)],
    "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
    "Rimnicu Valcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
    "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
    "Fagaras": [("Sibiu", 90), ("Bucharest", 211)],
    "Drobeta": [("Mehadia", 75), ("Craiova", 120)],
    "Pitesti": [("Rimnicu Valcea", 97), ("Bucharest", 101), ("Craiova", 138)],
    "Craiova": [("Pitesti", 138), ("Rimnicu Valcea", 146), ("Drobeta", 120)],
    "Bucharest": [("Girgiu", 90), ("Urziceni", 85), ("Pitesti", 101), ("Fagaras", 211)],
    "Girgiu": [("Bucharest", 90)],
    "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
    "Hirsova": [("Urziceni", 98), ("Eforie", 86)],
    "Eforie": [("Hirsova", 86)],
    "Vaslui": [("Urziceni", 142), ("Iasi", 92)],
    "Iasi": [("Neamt", 87), ("Vaslui", 92)],
    "Neamt": [("Iasi", 87)]
}

# Check if start has a direct route to end
def hasRouteToCity(start, end):
    startRoutes = routes[start]

    for i in range(0, startRoutes.__len__()):
        if startRoutes[i][0] == end:
            return True

    return False

# Generates a random solution, that prevents repeats and handles cases where the route leads
# to a dead-end
def randomSolution(start, end):
    romania_map = deepcopyDict(routes)
    solution = []
    solution.append(start)

    while hasRouteToCity(solution[solution.__len__() - 1], end) == False:
        directions = romania_map[solution[solution.__len__() - 1]].copy()
        randCity = directions[random.randint(0, directions.__len__() - 1)][0]
        
        while randCity in solution:
            for item in directions:
                if item[0] == randCity:
                    directions.remove(item)
                    break
            if len(directions) == 0:
                randCity = False
                break
            randCity = directions[random.randint(0, directions.__len__() - 1)][0]

        if randCity != False:
            solution.append(randCity)
        else:
            romania_map = removeCityFromMap(solution[len(solution) - 1], romania_map)
            solution.pop(len(solution) - 1)

    
    solution.append(end)
    return solution

# Remove a city from the map, as well as all routes leading to it
def removeCityFromMap(city, map_):
    map_copy = deepcopyDict(map_)
    map_copy.pop(city)

    for key in map_copy:
        arr = map_copy[key]
        for route in arr:
            if route[0] == city:
                arr.remove(route)

    return map_copy

# Creates a deep copy of an object, whose addresses are completely different
def deepcopyDict(dict):
    dictCopy = {}

    for key in dict:
        dictCopy[key] = dict[key].copy()
    return dictCopy


# Prints the total distance of a route from 'start' to 'end'
def solutionDistance(solution):
    distance = 0

    for i in range(1, solution.__len__()):
        cityFrom = solution[i - 1]
        cityTo = solution[i]
        cityFromRoutes = routes[cityFrom]
        for j in range(0, cityFromRoutes.__len__()):
            if cityFromRoutes[j][0] == cityTo:
                distance += cityFromRoutes[j][1]

    return distance

# Build neighboring solutions
def buildNeighbors(solution):
    neighbors = []
    start = solution[0]
    end = solution[len(solution) - 1]
    # The function has 4 attempts to find a new solution to the problem. Each time a copy is found, the count goes down
    count = 10

    while(True):
        # If a new solution can't be found after 4 tries, return the neighboring solutions
        if count == 0:
            return neighbors
        rand = randomSolution(start,end)
        l1 = solution.copy()
        l2 = rand.copy()
        while l1 == l2:
            count -= 1
            if count == 0:
                return neighbors
            rand = randomSolution(start, end)
            l2 = rand.copy()
        
        for sol in neighbors:
            l1 = sol.copy()

            if l1 == l2:
                l1 = False
                break
        if l1 != False:
            neighbors.append(rand)
            # A new solution was found so the count goes back up
            count = 4
        else:
            count -= 1

def hill_climbing(start, end):
    print(start, end)

    #Generate a random solution
    randSolution = randomSolution(start, end)

    #Calculate its distance
    randSolutionDistance = solutionDistance(randSolution)
    print(randSolution)
    print(randSolutionDistance)

    #Get neighboring solutions
    neighbors = buildNeighbors(randSolution)
    
    for neighbor in neighbors:
        print(neighbor)

    # Initiate the optimum solution and distance with the randomly generated one
    optimumSolution = randSolution.copy()
    optimumDistance = randSolutionDistance

    # Go through each neighbor and see if its solution is more optimal
    for neighbor in neighbors:
        d = solutionDistance(neighbor)
        if d < optimumDistance:
            optimumSolution = neighbor.copy()
            optimumDistance = solutionDistance(optimumSolution)

    print("The optimum route from " + start + " to " + end + " is: ")
    print(optimumSolution)
    print("With a distance of", optimumDistance)

hill_climbing("Oradea", "Neamt")



