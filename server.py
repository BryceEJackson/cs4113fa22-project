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


t = ['😀', '😈', '🙃', '🤨', '😇', '🤭', '🤑', '😋', '🤡']
p = ['🐒', '🐕', '🙊', '🐗', '🐪', '🐘', '🦬', '🦓','🧸']
tpositions  = [[0 for i in range(100)] for j in range(100)]
ppositions  = [[0 for i in range(100)] for j in range(100)]
capture  = [[0 for i in range(100)] for j in range(100)]


def getDim():
    file = open("dim.txt", "r")
    dim = file.read(2)
    file.close()
    dim = int(dim)
    return dim


class FeedbackServicer(pokemonou_pb2_grpc.FeedbackServicer):

    def __init__(self, count):
        self.count = count

    def Setup(self, request, context): 
        response = pokemonou_pb2.Dim()
        response.dim = getDim()
        return response

    def Capture(self, request, context):
        file = open("np.txt","r")
        txt = file.read(2)
        np = int(txt)
        print(f"NEW NUMBER OF POKEMON: {np}")
        # file.close()
        # file = open("np.txt", "w")
        response = pokemonou_pb2.Position()
        tx = request.x
        ty = request.y 
        if(ppositions[tx][ty] == 1):
            capture[tx][ty] = 1
            print("pokemon here!")
            print(f"throw ball from: {tx},{ty}")
            ppositions[tx][ty] = 0
            # np = np - 1
        # file.write(np)
        # file.close()    
        response.x = tx
        response.y = ty
        return response

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
                file = open("np.txt", "r")
                np = file.read(2)
                np = int(np)
                np = np - 1
                file.close()
                file = open("np.txt", "w")
                file.write(str(np))
                file.close()    

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
        
        if request.x == 0 and request.y == 0:
            ppositions[1][0] = 0

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

np = 5
file = open("np.txt","w")
file.write(str(np))
file.close()
file = open("np.txt", "r")
txt = file.read()
nptest= int(txt)
print(f"NUMBER OF POKEMON: {nptest}")
file.close()


empty = " "
def board(size):
    file = open("dim.txt", "w")
    file.write(str(size))
    file.close()

    try:
        while True:
            # # shut down on no pokemon left
            # file = open("np.txt", "r")
            # np = file.read(2)
            # np = int(np)
            # if(np == 0):
            #     print("no more pokemon! GAME OVER!\n")
            #     break

            #clear players, (basically prevents trails)
            for i in range(0,size):
                for j in range(0,size):
                    tpositions[i][j] = 0

            # print("\nserver running...\n")
            time.sleep(1) # wait .75 sec between board print updates
            # print("y: 0  1  2  3  4") # debug x axis
            for i in range(0,size):
                print(f"___", end='')
            print()
            for i in range(0,size):
                
               # print(f"{i}: ") # print the row number

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
