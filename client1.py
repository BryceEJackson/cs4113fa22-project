import socket
from time import sleep
import grpc 
import random
import pokemonou_pb2
import pokemonou_pb2_grpc
import random
response = 0
tdim = 0

class Step(): 
    def __init__(self, x, y): 
        self.x = x
        self.y = y

class dexEntry():
    def __init__(self, x, y, face):
        self.x = x
        self.y = y 
        self.face = face
        
#  testing pokedex array 
# TestArray = [dexEntry(0,1, 'face1'),
#              dexEntry(3,4, 'face2')]
# TestArray[1] = dexEntry(0,0,'xxx')
# 
# print(f"pokemon: {TestArray[1].x},{TestArray[1].y}: {TestArray[1].face}")

# define some global variables for pokedex and path 
stepsArray = [None] * 100
dexArray = [None] * 100
stepsCounter=0
dexCounter = 0

#pokedex
def pokeDex(dc):
    print("\nPokedex Entries: ")
    string = ""
    for i in range(dc):
        string += f"({dexArray[i].x},{dexArray[i].y}): {dexArray[i].face}\n"
    print(string)

def printPath(sc):
    string = "Path: "
    for i in range(sc):
        string += f"({stepsArray[i].x},{stepsArray[i].y}), "
    print(string)

def start():
    tx = random.randint(0,9)
    ty = random.randint(0,9)

    sc = 0
    dc = 0
    count = 0
    dir = 0 

    print("trainer client starting...")
    sleep(5) # wait for pokemon to spawn in ...


    try:
        while(True):
                sleep(.85)
                # set up the channel and dummy dim for setup request
                channel = grpc.insecure_channel('server:50051')
                stub = pokemonou_pb2_grpc.FeedbackStub(channel)

                # get the board dimensions
                try:
                    dimension = pokemonou_pb2.Dim(dim = 0)
                except grpc.RpcError as e: 
                    if grpc.StatusCode.UNKNOWN == e.code():
                        print("error 1")

                try: 
                    response = stub.Setup(dimension)
                    tdim = response.dim
                except grpc.RpcError as e: # Game Over. ( or server unavailable... )

                    # print game over message. 
                    print("Game Over... shutting down!!")

                    # implement functions for printing the path 
                    printPath(sc)
                    # print("Steps Taken: ")
                    # string = "Path: "
                    # for i in range(sc):
                    #     string += f"({stepsArray[i].x},{stepsArray[i].y}), "
                    # print(string)

                    #implement the function for printing the pokedex
                    pokeDex(dc)

                    break
                    # end of game over output


                # submit the path to the server 
                string = ""
                for i in range(sc):
                        string += f"({stepsArray[i].x},{stepsArray[i].y}), "
                path = pokemonou_pb2.Path()
                path.path = string
                path.name = socket.gethostname() + ".txt"
                message = stub.submit(path)
                # print(message.name)

                # check the board
                position = pokemonou_pb2.Position(x = tx, y = ty)
                stepsArray[sc] = Step(tx,ty)
                sc = sc + 1
                response = stub.CheckBoard(position)

                if(response.x != 0 and response.y != 0):
                    dir = -1
                    tx = response.x
                    ty = response.y
                # print(f"@: {response.x},{response.y}")

                # do some movements
                # case for if the trainer is chasing a pokemon
                # case for if the trainer is moving regularly
                position = pokemonou_pb2.Movepos(x = tx, y = ty, flip = dir)

                try: 
                    response1 = stub.MoveT(position)

                    if dir == 0:
                        count = count + 1
                        #print("count incremented")
                    if dir == 1:
                        count = count - 1
                        #print("count decremented")

                    if(response.x == 0 and response.y == 0):
                        tx = response1.x
                        ty = response1.y
                    #implement else case for capture
                    if(response.x == tx and response.y == ty):
                        cpos = pokemonou_pb2.Position(x = response.x, y = response.y)
                        response3 = stub.Capture(cpos)
                        dexArray[dc] = dexEntry(response3.x,response3.y, response3.face)
                        dc = dc+1 # finish implementing dex
                   

                        
                    # update global variable
                    dexCounter = dc
                    stepsCounter = sc

                    #choose a random direction to step
                    dir = random.randint(0,3)


                    # print(f"res.y: {response.y}")
                    # print(f"res.x: {response.x}")

                except grpc.RpcError as e:
                    print(f"error 2: {e}")
                    

                if(count == tdim):
                    dir = 1
                if(count == 0):
                    dir = 0

                

                #print("\ntrainer client running...")
    except KeyboardInterrupt:
        print("Interrupted...")
