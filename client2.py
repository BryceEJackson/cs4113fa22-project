from time import sleep
import grpc 
import random
import pokemonou_pb2
import pokemonou_pb2_grpc
import random

# TODO: 
# implement tainer() functionality
trainer = ""
response = 0
tdim = 0
stepsArray = [None] * 300
stepCounter = 0

def Path(sc):
    string = "Path: "
    for i in range(sc):
        string += f"{stepsArray[i]}, "
    print(string)

def start():
    tx = random.randint(0,9)
    ty = random.randint(1,9)
    count = 0
    dir = 0
    sc = 0
    path = ""
    print("pokemon client starting...")
    try:
        while(True):
                #print(f"pokemon @: {tx},{ty}")
                sleep(4)
                # set up the channel and dummy dim for setup request
                channel = grpc.insecure_channel('server:50051')
                stub = pokemonou_pb2_grpc.FeedbackStub(channel)
                
                # get the board dimensions
                try:
                    # move = pokemonou_pb2.Position(x = 1, y = 1) 
                    dimension = pokemonou_pb2.Dim(dim = 0)
                except grpc.RpcError as e: 
                    if grpc.StatusCode.UNKNOWN == e.code():
                        print("error 1")


                try:
                    response = stub.Setup(dimension)
                    tdim = response.dim
                except grpc.RpcError as e:
                    #print("pokemon client shutting down!")
                    break

                stepsArray[sc] = f"({tx},{ty})"
                sc = sc + 1

                # flee from trainers if they are around
                position = pokemonou_pb2.Position(x = tx, y = ty)
                response1 = stub.Flee(position)
                if(response1.x != 0 and response1.y != 0):
                    dir = -1
                    if(response1.x + 1 < tdim):
                        tx = response1.x + 1
                    elif(response1.x - 1 >= 0):
                        tx = response1.x - 1
                    ty = response1.y

                # do some movements
                position = pokemonou_pb2.Movepos(x = tx, y = ty, flip = dir)
                try: 
                    response = stub.MoveP(position)
                    if(response.caught == 1):
                        stub.remove(position)
                        print("caught!")
                        break

                    if dir == 0:
                        count = count + 1
                        #print("count incremented")
                    if dir == 1:
                        count = count - 1
                        #print("count decremented")
                    sleep(1)
                    tx = response.x
                    ty = response.y
                    stepCounter = sc

                except grpc.RpcError as e:
                    print(f"error 2: {e}")
                    
# prevent pokemon from walking off the borad (just makes sure they dont use pos out of bounds)
                if(count == tdim):
                    dir = 1
                if(count == 0):
                    dir = 0
        Path(sc)           

    except KeyboardInterrupt:
        print("Interrupted...")
