import math, random

"""
Random Map Algorythm Generator
 
"""

# map = [[1,1,1,1,0],
#        [1,0,0,0,0],
#        [1,0,1,1,1],
#        [1,0,0,0,1],
#        [1,1,1,0,1]]

# helper function to make a two dimentional array that takes a number and the dimentions of the array
def createArray(num, dimensions):
    array = []
    for i in range(0, dimensions):
        array.append([])
        for j in range(0, dimensions):
            array[i].append(num)
    return array 

  #lets create a randomly generated map for our dungeon crawler
def createMap():
    dimensions = 5 # width and height of the map
    maxTunnels = 3 # max number of tunnels possible
    maxLength = 3 # max length each tunnel can have
    map = createArray(1, dimensions) # create a 2d array full of 1's
    currentRow = math.floor(random.randint(0,9) * dimensions) # our current row - start at a random spot
    currentColumn = math.floor(random.randint(0,9) * dimensions) # our current column - start at a random spot
    directions = [ [-1, 0], [1, 0], [0, -1], [0, 1] ] # array to get a random direction from (left,right,up,down)
    lastDirection = [] # save the last direction we went
    randomDirection = [] # next turn/direction - holds a value from directions

    # lets create some tunnels - while maxTunnels, dimentions, and maxLength  is greater than 0.
    while (maxTunnels and dimensions and maxLength) :
        # lets get a random direction - until it is a perpendicular to our lastDirection
        # if the last direction = left or right,
        # then our new direction has to be up or down,
        # and vice versa
        print('hola')
        randomDirection = directions[random.randint(0,3)]
        while ( (randomDirection[0] == -lastDirection[0] and randomDirection[1] == -lastDirection[1]) or (randomDirection[0] == lastDirection[0] and randomDirection[1] == lastDirection[1])):
            randomDirection = directions[random.randint(0,3)]


        randomLength = math.ceil(random.randint(0,9) * maxLength), #length the next tunnel will be (max of maxLength)
        tunnelLength = 0 #current length of tunnel being created

		# lets loop until our tunnel is long enough or until we hit an edge
        while (tunnelLength < randomLength):
            #break the loop if it is going out of the map
            if (((currentRow == 0) and (randomDirection[0] == -1)) or
                ((currentColumn == 0) and (randomDirection[1] == -1)) or
                ((currentRow == dimensions - 1) and (randomDirection[0] == 1)) or
                ((currentColumn == dimensions - 1) and (randomDirection[1] == 1))) :
                break
            else:
                map[currentRow][currentColumn] = 0 #set the value of the index in map to 0 (a tunnel, making it one longer)
                currentRow += randomDirection[0] #add the value from randomDirection to row and col (-1, 0, or 1) to update our location
                currentColumn += randomDirection[1]
                tunnelLength += 1 #the tunnel is now one longer, so lets increment that variable
            

        if tunnelLength: # update our variables unless our last loop broke before we made any part of a tunnel
            lastDirection = randomDirection #set lastDirection, so we can remember what way we went
            maxTunnels-= 1 # we created a whole tunnel so lets decrement how many we have left to create
    return map # all our tunnels have been created and our map is complete, so lets return it to our render()

print(createMap())
# print( random.randint(0,9) )