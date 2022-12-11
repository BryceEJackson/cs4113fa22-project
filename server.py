# Bryce Jackson, distOS final
#imports
from multiprocessing.pool import TERMINATE
from pickle import FALSE
import time
from urllib import response
import pokemonou_pb2
import pokemonou_pb2_grpc
import grpc
import random
from concurrent.futures import ThreadPoolExecutor

Number = random.randrange(0,50)


#some global variables for trainer/pokemon emojis
t = ['😀', '😈', '🙃', '🤨', '😇', '🤭', '🤑', '😋', '🤡']
p = ['🐒', '🐕', '🙊', '🐗', '🐪', '🐘', '🦬', '🦓','🧸']


#some global variables for trainer/pokemon positions and capture info
tpositions  = [[0 for i in range(100)] for j in range(100)]
ppositions  = [[0 for i in range(100)] for j in range(100)]
capture  = [[0 for i in range(100)] for j in range(100)]


#write the board dimension to a file
def getDim():
    file = open("dim.txt", "r")
    dim = file.read(2)
    file.close()
    dim = int(dim)
    return dim

# print the moves made by the trainers
def Moves():
    file = open("trainer1.txt", "r")
    path = file.read(1024) # read the file to a buffer for output
    print(f"trainer1 Moves: {path}")
    file = open("trainer2.txt", "r")
    path = file.read(1024) # read the file to a buffer for output
    print(f"trainer2 Moves: {path}")
    file = open("trainer3.txt", "r")
    path = file.read(1024) # read the file to a buffer for output
    print(f"trainer3 Moves: {path}")
    file = open("trainer4.txt", "r")
    path = file.read(1024) # read the file to a buffer for output
    print(f"trainer4 Moves: {path}")
    file = open("trainer5.txt", "r")
    path = file.read(1024) # read the file to a buffer for output
    print(f"trainer5 Moves: {path}")




#the feedback servicer code and function definitions
class FeedbackServicer(pokemonou_pb2_grpc.FeedbackServicer):

    def __init__(self, count):
        self.count = count

#setup the board dimension vars
    def Setup(self, request, context): 
        response = pokemonou_pb2.Dim()
        response.dim = getDim()
        return response
#trainer captures a pokemon
    def Capture(self, request, context):
        file = open("np.txt","r")
        txt = file.read(2)
        np = int(txt)
        print(f"NEW NUMBER OF POKEMON: {np}")
        # file.close()
        # file = open("np.txt", "w")
        response = pokemonou_pb2.Dex()
        tx = request.x
        ty = request.y 
        if(ppositions[tx][ty] == 1):
            capture[tx][ty] = 1
            print("pokemon here!")
            print(f"throw ball from: {tx},{ty}")
            ppositions[tx][ty] = 0
            # edit the captured pokemon counter
            file = open("np.txt", "r")
            time.sleep(.2) # sleep to prevent access denial
            np = file.read(2)
            np = int(np)
            np = np - 1
            file.close()
            file = open("np.txt", "w")
            file.write(str(np))
            file.close()    
            # np = np - 1
        # file.write(np)
        # file.close()    
        response.x = tx
        response.y = ty
        response.face = p[np]
        return response
#pokemon senses trainer and must run
    def Flee(self, request, context):
        file = open("dim.txt", "r")
        dim = file.read(2)
        file.close()
        dim = int(dim)
        position = pokemonou_pb2.Position(x=0, y=0)
        px = request.x
        py = request.y
        for i in range(dim):
            for j in range(dim):
                if(tpositions[i][j] == 1 and i + 1 == px and j == py):
                    position.x = i
                    position.y = request.y
                if(tpositions[i][j] == 1 and i - 1 == px and j == py):
                    position.x = i
                    position.y = request.y
                if(tpositions[i][j] == 1 and j + 1 == py) and i == px:
                    position.x = request.x
                    position.y = j
                if(tpositions[i][j] == 1 and j - 1 == py and i == px):
                    position.x = request.x
                    position.y = j
        return position
# trainer and pokekon check the board 
    def CheckBoard(self, request, context):
        file = open("dim.txt", "r")
        dim = file.read(2)
        file.close()
        dim = int(dim)
        position = pokemonou_pb2.Position(x=0,y=0)
        tx = request.x
        ty = request.y
        
        for i in range(dim):
            for j in range(dim):
                if(ppositions[i][j] == 1 and i + 1 == tx and j == ty):
                    position.x = i
                    position.y = request.y
                if(ppositions[i][j] == 1 and i - 1 == tx and j == ty):
                    position.x = i
                    position.y = request.y
                if(ppositions[i][j] == 1 and j + 1 == ty) and i == tx:
                    position.x = request.x
                    position.y = j
                if(ppositions[i][j] == 1 and j - 1 == ty and i == tx):
                    position.x = request.x
                    position.y = j
        return position

    
# the path submission function
    def submit(self, request, context):
        response = pokemonou_pb2.Greeting()
        response.name = "Path submitted.\n"

        file = open(request.name, "w")
        file.write(request.path)
        file.close()
       
        return response

# move the trainer around
    def MoveT(self, request, context):
        response = pokemonou_pb2.Position()

        #set response to request values
        response.x = request.x
        response.y = request.y

        # read the dimension to an integer veriable
        file = open("dim.txt", "r")
        dim = file.read(2)
        file.close()
        dim = int(dim)
        dir = request.flip
        #print(f"dir: {dir}")

        # # handle collisions
        # if(tpositions[request.x+1][request.y] == 1 and dir == 2):
        #     return response

        if(dir  == -1):
            response.x = request.x
            response.y = request.y
        if(dir == 0):
            if(request.x + 1 < dim):
                response.x = request.x + 1
            else:
                response.x = request.x
                dir = 1
            response.y = request.y
        if(dir == 1):
            if(request.x -1 >= 0):
                response.x = request.x -1
                response.y = request.y
        if(dir == 2):
            if(request.y + 1 < dim):
                response.y = request.y + 1
            else:
                response.y = request.y 
            response.x = response.x 
        if(dir == 3):
            if(request.y - 1 > 0):
                response.y = request.y -1
            else: 
                response.y = response.y
            response.x = request.x

        # deal with collisions
        if(tpositions[response.x][response.y] == 0): # the player can move here
            # zero out the current position, so the trainer moves
            tpositions[request.x][request.y] = 0
            # set new position 
            tpositions[response.x][response.y] = 1
        else: # the player cant move here (another player is here)
            # change nothing 
            response.x = request.x
            response.y = request.y 
                    
        return response

# move the pokemon around
    def MoveP(self, request, context):
    
    	#check for having been caught, if so return caught = 1 (pokemon exit) 
        response1 = pokemonou_pb2.Catch()
        if(ppositions[request.x][request.y] == 0 and capture[request.x][request.y] == 1):
            response1.caught = 1
            response1.x = request.x
            response1.y = request.y
            if(response1.caught == 1):
                print(f"caught at {response1.x}, {response1.y}!!!!!!\n")

                ppositions[response1.x][response1.y] = 0
                ppositions[request.x][request.y] = 0
                capture[request.x][request.y] = 0
                return response1
        
    
        response = pokemonou_pb2.Catch()
        response.caught = 0

        #set response to request values
        response.x = request.x
        response.y = request.y

        # zero out the current position, so the trainer moves
        ppositions[request.x][request.y] = 0

        #print(f"request: {request.x},{request.y}")

        # read the dimension to an integer veriable
        file = open("dim.txt", "r")
        dim = file.read(2)
        file.close()
        dim = int(dim)
        dir = request.flip
        #print(f"dir: {dir}")

        # move up and down
        if(dir == 0):
            ppositions[request.x][request.y] = 1
            ppositions[request.x-1][request.y] = 0
            response.y = response.y 
            if(response.x +1 < dim):
                response.x = response.x + 1

        if(dir == 1):
            ppositions[request.x+1][request.y] = 0
            if(response.y == 0):
                tpositions[1][0] = 0
            ppositions[request.x][request.y] = 1
            response.y = response.y 
            if(response.x-1 > 0):
                response.x = response.x - 1

        # Run away!
        if(dir == -1):
            response.x = request.x
            response.y = request.y
        
        # if request.x == 0 and request.y == 0:
        #     ppositions[1][0] = 0

        #print(f"response: {response.x},{response.y}")
        return response



# setup the server ...    
count = 0
server = grpc.server(ThreadPoolExecutor(max_workers=10))
fbs = FeedbackServicer(count = 0)
pokemonou_pb2_grpc.add_FeedbackServicer_to_server(fbs, server)

print("starting server...")
server.add_insecure_port('[::]:50051')
server.start()

# set the number of pokemon variable and store it to a file. 
np = 5
file = open("np.txt","w")
file.write(str(np))
file.close()
file = open("np.txt", "r")
txt = file.read()
nptest= int(txt)
#print the value and close the file
print(f"NUMBER OF POKEMON: {nptest}")
file.close()

# empty space character
empty = " "

# the board printing function (and the main loop)
def board(size):
    file = open("dim.txt", "w")
    file.write(str(size))
    file.close()

#run the server and print the board
    try:
        while True:
            tc = 5
            pc = 5

            # shut down on no pokemon left
            file = open("np.txt", "r")
            np = file.read(2)
            np = int(np)
            if(np == 0):
                Moves()
                print("no more pokemon! GAME OVER!\n")
                break

            #clear players, (basically prevents trails)
            for i in range(0,size):
                for j in range(0,size):
                    tpositions[i][j] = 0

            time.sleep(1) # wait .75 sec between board print updates
            for i in range(0,size):
                print(f"___", end='')
            print()


            for i in range(0,size):
                
                for j in range(0,size):
                    
                    #pokemon here
                    if(ppositions[i][j] == 1):
                        print(f"|{p[pc]}", end='')
                        pc = pc - 1

                    try: 
                        #trainer here
                        if(tpositions[i][j] == 1):
                            print(f"|{t[tc]}", end='')
                            tc = tc  - 1
                    except IndexError:
                        print(IndexError)

                    #trainer not here ( also pokemon not here )
                    if(tpositions[i][j] == 0 and ppositions[i][j] == 0):
                        print(f"| {empty}", end='')

                print()

            for i in range(0,size):
                    print(f"___", end='')
            print()

                #print(f"({setx},{sety})")
            
    except KeyboardInterrupt:
        print("Interrupted")
        server.stop(0)
