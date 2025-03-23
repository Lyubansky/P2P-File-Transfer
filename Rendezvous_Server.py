import asyncio
import json


class Rendezvous_Server:
    def __init__(self):
        #TODO: Store peers in a db
        #key = user name ; value = (ip, port)
        self.peers = {}

    """
    Handle incoming connections from clients
    """
    async def handle_client(self, reader, writer):
        # Get message from client
        data = await reader.read(1024)  # reads up to 1024 bytes of data sent by the client
        message = data.decode()
        addr = writer.get_extra_info('peername')  # (Client IP, Client port)

        # Register peer
        # TODO: check if user_name already exists - make a separate function for this
        if message.startswith("REGISTER"):
            # Format: "REGISTER peer_id port"
            _, user_name, port = message.split()
            self.peers[user_name] = (addr[0], int(port))  # Store IP and chosen port
            print(f"Registered {user_name} at {addr[0]}:{port}")


        # TODO: Later replace with a separate function that lets the user search for a peer he wants to connect to
        # Send peer list to client
        response = json.dumps(self.peers)
        writer.write(response.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def start(self, host='127.0.0.1', port=8888):
        # Create TCP server
        server = await asyncio.start_server(self.handle_client, host, port)
        print(f"Rendezvous server running on {host}:{port}")
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    server = Rendezvous_Server()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("Server stopped")
