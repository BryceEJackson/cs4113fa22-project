import socket
from time import sleep
import server
import client1
import client2

if __name__ == "__main__":
    if(socket.gethostname() == 'server'):
        server.board(10)
    else: 
        sleep(5)
    if(socket.gethostname() == 'trainer1'):
        sleep(1)
        client1.start()
    if(socket.gethostname() == 'trainer2'):
        sleep(1)
        client1.start()
    if(socket.gethostname() == 'trainer3'):
        sleep(1)
        client1.start()
    if(socket.gethostname() == 'trainer4'):
        sleep(1)
        client1.start()
    if(socket.gethostname() == 'trainer5'):
        sleep(1)
        client1.start()
    if(socket.gethostname() == 'trainer6'):
        sleep(15)
        client1.start()
    if(socket.gethostname() == 'trainer7'):
        sleep(15)
        client1.start()
    if(socket.gethostname() == 'trainer8'):
        sleep(15)
        client1.start()
    if(socket.gethostname() == 'pokemon1'):
        sleep(1)
        client2.start()
    if(socket.gethostname() == 'pokemon2'):
        sleep(1)
        client2.start()
    if(socket.gethostname() == 'pokemon3'):
        sleep(1)
        client2.start()
    if(socket.gethostname() == 'pokemon4'):
        sleep(1)
        client2.start()
    if(socket.gethostname() == 'pokemon5'):
        sleep(1)
        client2.start()
    if(socket.gethostname() == 'pokemon6'):
        sleep(15)
        client2.start()
    if(socket.gethostname() == 'pokemon7'):
        sleep(15)
        client2.start()
    if(socket.gethostname() == 'pokemon8'):
        sleep(15)
        client2.start()