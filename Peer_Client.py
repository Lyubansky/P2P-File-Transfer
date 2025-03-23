
import asyncio
import json
import random
import uuid

# each client registers with a unique username - need to implement this
# using a known to client other username be able to chat with him

class Peer_Client:
    #TODO: look for a way to find the server without using local host
    # discover server function
    def __init__(self, user_name, rendezvous_host='127.0.0.1', rendezvous_port=8888):
        self.user_name = user_name
        self.rendezvous_addr = (rendezvous_host, rendezvous_port)
        self.listen_port = random.randint(1000, 5000)  # Random port for listening
        self.peers = {}

    async def register(self):
        # Connect to rendezvous server and register
        reader, writer = await asyncio.open_connection(*self.rendezvous_addr)
        message = f"REGISTER {self.user_name} {self.listen_port}" # No need to send ip because server will know it
        writer.write(message.encode())
        await writer.drain()

        # Get peer list
        #TODO: delete later
        data = await reader.read(1024)
        self.peers = json.loads(data.decode())
        print(f"{self.user_name} registered. Peers: {self.peers}")
        writer.close()
        await writer.wait_closed()
    #TODO: Create a full sequence of events for the client - register, choose a peer to connect to, start a chat between 2 peers
    async def start(self):
        # Register with server
        await self.register()

if __name__ == "__main__":
    #TODO: Creation of a client - at first just choosing a username
    # allow creation of multiple clients (with threads)
    client1 = Peer_Client("Alice")
    asyncio.run(client1.start())
