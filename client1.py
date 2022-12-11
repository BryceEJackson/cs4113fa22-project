import socket
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
    ty = random.randint(0,9)
    if(socket.gethostname() == 'trainer1'):
        tx = 8
        ty = 8

    count = 0
    dir = 0
    print("client starting...")
    try:
        while(True):
                sleep(.85)
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

                # check the board
                position = pokemonou_pb2.Position(x = tx, y = ty)
                response = stub.CheckBoard(position)
                # print(f"@: {response.x},{response.y}")

                # do some movements
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
                    if(response.x != 0 and response.y != 0):
                        cpos = pokemonou_pb2.Position(x = response.x, y = response.y)
                        response3 = stub.Capture(cpos)
                        
                    dir = random.randint(0,3)

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
