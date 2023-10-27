from websockets.sync.client import connect
import asyncio

async def main():
    async with connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello world!")
        await websocket.recv()


asyncio.run(main())