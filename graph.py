import math

from itertools import permutations

def euclid(p,q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)

# Helper function for to get the coordinates in test files
# It returns the first number in a line and returns the stripped line without that number
def stripLine(x, line):
    idx = 0
    strippedLine = ''
    while line[idx] != ' ':
        x = x + line[idx]
        idx += 1
        strippedLine = line[idx:]
    strippedLine = strippedLine.strip()
    return x,strippedLine

class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self,n,filename):

        with open(filename,'r') as fileHandler:

            lines = fileHandler.readlines()

            # For the -1 case (Euclidean TSP)
            if n == -1:
                noOfLines = len(lines)
                self.dists = [[0 for i in range(noOfLines)] for j in range(noOfLines)]
                self.n = noOfLines

                # Initialise local variables
                listOfXs = []
                listOfYs = []
                x = ''
                y = ''

                for line in lines:
                    line = line.strip()
                    x,line = stripLine(x,line)
                    y = y + line
                    listOfXs.append(x)
                    listOfYs.append(y)
                    x = ''
                    y = ''
                #print("The list of X coordinates are", listOfXs)
                #print("The list of Y coordinates are", listOfYs)

                for i in range(noOfLines):
                    for j in range(noOfLines):
                        if i != j:
                            currX1 = int(listOfXs[i])
                            currY1 = int(listOfYs[i])
                            currX2 = int(listOfXs[j])
                            currY2 = int(listOfYs[j])
                            self.dists[i][j] = euclid([currX1,currY1],[currX2,currY2])

                # for i in range(noOfLines):
                #     for j in range(noOfLines):
                #         print("self.dists["+str(i)+"]["+str(j)+"] is:"+str(self.dists[i][j]))

            # For the n.0 case (More general TSP inputs)
            else:
                self.n = n
                self.dists = [[0 for i in range(n)] for j in range(n)]

                i = '' # first endpoint i
                j = '' # second endpoint j
                distance = '' # given weight/distance for the edge between i and j

                for line in lines:
                    line = line.strip() # Strip the \n character
                    i,line = stripLine(i,line) # Get endpoint i
                    j,line = stripLine(j,line) # Get endpoint j
                    distance = distance + line # Get weight/distance for the edge between i and j
                    self.dists[int(i)][int(j)] = int(distance)
                    self.dists[int(j)][int(i)] = int(distance)
                    i = ''
                    j = ''
                    distance = ''

                # for i in range(n):
                #     for j in range(n):
                #         print("self.dists[",i,"][",j,"] is:",self.dists[i][j])

            self.perm = []
            for i in range(self.n):
                self.perm.append(i)

    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        val = 0
        firstNode = 0
        secondNode = 0
        for i in range(len(self.perm)-1):
            firstNode = self.perm[i]
            secondNode = self.perm[i+1]
            val = val + self.dists[firstNode][secondNode]
        firstNode = self.perm[-1]
        secondNode = self.perm[0]
        val = val + self.dists[firstNode][secondNode]
        return val

    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self,i):
        prevTourValue = self.tourValue()
        self.perm[i], self.perm[(i+1)%self.n] = self.perm[(i+1)%self.n], self.perm[i]
        currTourValue = self.tourValue()
        flag = False

        if currTourValue < prevTourValue:
            flag = True
        else:
            if i == len(self.perm)-1:
                self.perm[i], self.perm[0] = self.perm[0], self.perm[i]
            else:
                self.perm[i], self.perm[i+1] = self.perm[i+1], self.perm[i]
            flag = False
        return flag


    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.
    def tryReverse(self,i,j):
    # ------------------------ 2720 SOLUTION ------------------------
        # flag = False
        # prevTourValue = self.tourValue()
        # reversedList, restOfList, frontList, backList, fullList = [], [], [], [], []
        # if i == 0:
        #     reversedList = self.perm[j::-1]
        #     restOfList = self.perm[(j+1):]
        #     fullList = reversedList + restOfList
        # else:
        #     reversedList = self.perm[j:(i-1):-1]
        #     frontList = self.perm[:i]
        #     backList = self.perm[(j+1):]
        #     fullList = frontList + reversedList + backList
        # self.perm = fullList
        # currTourValue = self.tourValue()
        #
        # if currTourValue < prevTourValue:
        #     flag = True
        # else:
        #     reversedList.reverse()
        #     if i == 0:
        #         fullList = reversedList + restOfList
        #     else:
        #         fullList = frontList + reversedList + backList
        #     self.perm = fullList
        # return flag

    # ------------------------ 2628 SOLUTION ------------------------
        flag = False
        reversedList, restOfList, frontList, backList, fullList = [], [], [], [], []

        iFirstNode = self.perm[i-1]
        iSecondNode = self.perm[i]
        jFirstNode = self.perm[j]
        jSecondNode = self.perm[j+1]

        # The only thing that changes the tourValue in original and reversed perm is the difference in:
        # the paths i-1 -> i and path j -> j+1 (for original perm) and paths i-1 -> j and i -> j+1 (for reversed perm)
        prevDifference = self.dists[iFirstNode][iSecondNode] + self.dists[jFirstNode][jSecondNode]
        reversedDifference = self.dists[iFirstNode][jFirstNode] + self.dists[iSecondNode][jSecondNode]

        if reversedDifference < prevDifference:
            if i == 0:
                reversedList = self.perm[j::-1]
                restOfList = self.perm[(j+1):]
                fullList = reversedList + restOfList
            else:
                reversedList = self.perm[j:(i-1):-1]
                frontList = self.perm[:i]
                backList = self.perm[(j+1):]
                fullList = frontList + reversedList + backList
            self.perm = fullList
            flag = True

        return flag

    def swapHeuristic(self):
        better = True
        while better:
            better = False
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self):
        better = True
        while better:
            better = False
            for j in range(self.n-1):
                for i in range(j):
                    if self.tryReverse(i,j):
                        better = True

    # Helper function for methods Greedy and myPartC.
    # It returns the closest node to the node perm[i].
    def findClosestNode(self,perm,i):
        idx = perm[i]
        destinations = self.dists[idx]
        closest = min(j for j in destinations if j>0)
        nextDest = destinations.index(closest)
        return nextDest

    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
        myPerm = [0]
        while len(myPerm) < self.n:
            nextDest = self.findClosestNode(myPerm,-1)
            destinations = self.dists[myPerm[-1]]
            while nextDest in myPerm:
                destinations[nextDest] = 0
                closest = min(i for i in destinations if i>0)
                nextDest = destinations.index(closest)
            myPerm.append(nextDest)
        self.perm = myPerm

    def tryReversePartC(self, i, j, k):
        flag = False
        # self.perm given is [...a-b...c-d...e-f...]
        a,b,c,d,e,f = self.perm[i-1], self.perm[i], self.perm[j-1], self.perm[j], self.perm[k-1], self.perm[k % self.n]
        originalDist = self.dists[a][b] + self.dists[c][d] + self.dists[e][f]
        swappedDist1 = self.dists[a][c] + self.dists[b][d] + self.dists[e][f]
        swappedDist2 = self.dists[a][b] + self.dists[c][e] + self.dists[d][f]
        swappedDist3 = self.dists[a][d] + self.dists[e][b] + self.dists[c][f]
        swappedDist4 = self.dists[f][b] + self.dists[c][d] + self.dists[e][a]

        if originalDist > swappedDist1:
            flag = True
            self.perm[i:j] = reversed(self.perm[i:j])
        elif originalDist > swappedDist2:
            flag = True
            self.perm[j:k] = reversed(self.perm[j:k])
        elif originalDist > swappedDist4:
            flag = True
            self.perm[i:k] = reversed(self.perm[i:k])
        elif originalDist > swappedDist3:
            flag = True
            temp = self.perm[j:k] + self.perm[i:j]
            self.perm[i:k] = temp
        return flag

    def ThreeOptHeuristic(self):
        better = True
        while better:
            better = False
            for i in range(self.n):
                for j in range(i+2, self.n):
                    for k in range(j+2, self.n+(i>0)):
                        if self.tryReversePartC(i,j,k):
                            better = True

    def optimal(self):
        tours = permutations(self.perm)
        bestCost = 100000
        for tour in list(tours):
            temp = self.perm
            self.perm = list(tour)
            currCost = self.tourValue()
            if currCost < bestCost:
                bestCost = currCost
            else:
                self.perm = temp

    def restartTour(self):
        self.perm = []
        for i in range(self.n):
            self.perm.append(i)
