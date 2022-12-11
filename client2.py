from time import sleep
import grpc 
import random
import pokemonou_pb2
import pokemonou_pb2_grpc
import random

response = 0
tdim = 0

def start():
    tx = random.randint(0,9)
    ty = random.randint(1,9)
    count = 0
    dir = 0
    print("client starting...")
    try:
        while(True):
                sleep(2)
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
                response = stub.Setup(dimension)
                tdim = response.dim
               # print(f"dim: {tdim}")

                

                # do some movements
                # print(f"position: {tx}, {ty} ")
                position = pokemonou_pb2.Movepos(x = tx, y = ty, flip = dir)
                try: 
                    response = stub.MoveP(position)
                    if(response.caught == 1):
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

                    # print(f"res.y: {response.y}")
                    # print(f"res.x: {response.x}")

                except grpc.RpcError as e:
                    print(f"error 2: {e}")
                #print(f"count{count}")

                if(count == tdim):
                     dir = 1
                if(count == 0):
                    dir = 0

                

                #print("\nclient running...")
    except KeyboardInterrupt:
        print("Interrupted...")
