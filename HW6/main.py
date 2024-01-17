import random
import os

os.chdir('/Users/kristianivanov/Desktop/IS Homeworks/HW7/')

import matplotlib.pyplot as plt

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.centroidIndex = -1

points = []
centroids = []
indexesOfPointsCentroids = set()
pointDistances = []

magicNum = 1000
scaledMaxX, scaledMaxY, scaledMinX, scaledMinY = 0, 0, 0, 0
maxx, maxy, minx, miny = 0, 0, 0, 0

width, height = 1820, 980

def initX():
    global scaledMaxX, scaledMinX, maxx, minx
    maxPoint = max(points, key=lambda p: p.x)
    minPoint = min(points, key=lambda p: p.x)

    maxx = maxPoint.x
    scaledMaxX = maxPoint.x * magicNum
    minx = minPoint.x
    scaledMinX = minPoint.x * magicNum

def initY():
    global scaledMaxY, scaledMinY, maxy, miny
    maxPoint = max(points, key=lambda p: p.y)
    minPoint = min(points, key=lambda p: p.y)

    maxy = maxPoint.y
    scaledMaxY = maxPoint.y * magicNum
    miny = minPoint.y
    scaledMinY = minPoint.y * magicNum

def initMinMax():
    initX()
    initY()

def computeSquaredDistance(a, b):
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2

def initRandomCentroids(K):
    global centroids
    for _ in range(K):
        x = random.uniform(scaledMinX, scaledMaxX) / magicNum
        y = random.uniform(scaledMinY, scaledMaxY) / magicNum
        centroid = Point(x, y)
        centroids.append(centroid)

def findMinimalDistanceFromPointToCentroid(pointIndex):
    minDistance = computeSquaredDistance(points[pointIndex], points[0])

    for centroidIndex in indexesOfPointsCentroids:
        curDistance = computeSquaredDistance(points[pointIndex], points[centroidIndex])
        if curDistance < minDistance:
            minDistance = curDistance

    return minDistance

def chooseNewCentroid():
    sumAllPointDistances = sum(pointDistances)
    val = random.random()
    curSum = 0

    for i, dist in enumerate(pointDistances):
        curSum += dist
        if val < curSum / sumAllPointDistances:
            return i

def initCentroidsPlusPlus(K):
    pointIndex = random.randint(0, len(points) - 1)
    indexesOfPointsCentroids.add(pointIndex)
    pointDistances.extend([0.0] * len(points))

    counter = 0
    while counter < K - 1:
        for i in range(len(points)):
            if i not in indexesOfPointsCentroids:
                pointDistances[i] = findMinimalDistanceFromPointToCentroid(i)

        newCentroidIndex = chooseNewCentroid()
        while newCentroidIndex in indexesOfPointsCentroids:
            newCentroidIndex = chooseNewCentroid()

        indexesOfPointsCentroids.add(newCentroidIndex)
        counter += 1

    for pointIndex in indexesOfPointsCentroids:
        centroid = Point(points[pointIndex].x, points[pointIndex].y)
        centroids.append(centroid)

def findNearestCentroid(p):
    minDistance = computeSquaredDistance(p, centroids[0])
    nearestCentroidIndex = 0

    for i, centroid in enumerate(centroids):
        curDistance = computeSquaredDistance(p, centroid)
        if curDistance < minDistance:
            minDistance = curDistance
            nearestCentroidIndex = i

    return nearestCentroidIndex

def changeCentroid(centroidIndex):
    sumx, sumy = 0, 0
    counter = 0

    for p in points:
        if p.centroidIndex == centroidIndex:
            sumx += p.x
            sumy += p.y
            counter += 1

    if counter == 0:
        return False

    newCentroid = Point(sumx / counter, sumy / counter)
    oldCentroid = centroids[centroidIndex]

    if oldCentroid.x == newCentroid.x and oldCentroid.y == newCentroid.y:
        return False

    centroids[centroidIndex] = newCentroid
    return True

def clusterize():
    toContinue = True

    while toContinue:
        toContinue = False

        for i, p in enumerate(points):
            p.centroidIndex = findNearestCentroid(p)

        for j in range(len(centroids)):
            isChanged = changeCentroid(j)
            toContinue = isChanged or toContinue

def fromCartesianToComp(coord, isX):
    if isX:
        return (coord - minx) * width / (maxx - minx)
    else:
        return (maxy - coord) * height / (maxy - miny)

def getColor(index):
    colors = [
        'red', 'blue', 'green', 'magenta', 'yellow',
        'black', 'cyan', 'orange', 'pink', 'purple'
    ]
    return colors[index % len(colors)]

def drawKMeans(title):
    plt.figure(figsize=(8, 6))

    for p in points:
        x = fromCartesianToComp(p.x, True)
        y = fromCartesianToComp(p.y, False)
        color = getColor(p.centroidIndex)
        plt.scatter(x, y, color=color)

    for i, centroid in enumerate(centroids):
        x = fromCartesianToComp(centroid.x, True)
        y = fromCartesianToComp(centroid.y, False)
        plt.scatter(x, y, marker='^', s=100, color=getColor(i))

    plt.title(title)
    plt.show()

def kMeans(K):
    initRandomCentroids(K)
    clusterize()
    drawKMeans("kMeans")

def kMeansPlusPlus(K):
    initCentroidsPlusPlus(K)
    clusterize()
    drawKMeans("kMeans++")

def main():
    K = int(input("Enter K: "))
    fname = input("\nEnter file name: ")

    with open(fname, 'r') as file:
        for line in file:
            x, y = map(float, line.split())
            p = Point(x, y)
            points.append(p)

    initMinMax()

    kMeans(K)
    centroids.clear()
    kMeansPlusPlus(K)

if __name__ == "__main__":
    main()
