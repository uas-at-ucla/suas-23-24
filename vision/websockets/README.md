# WebSockets Server

This server is connected to a drone flight control software and has four microservices connected to it:

- **Camera**: This microservice is responsible for taking photos and collecting telemetry data.
- **ODLC (Object Detection, Localization, and Classification)**: This microservice is used for detecting, localizing, and classifying objects.
- **Flight Software**: This microservice receives detected targets and decides when to drop the payload.
- **Airdrop**: This microservice is triggered to drop the payload.


The WebSocket server is responsible for handling all the WebSocket connections. It is also responsible for handling all the messages that are sent over WS. It would be created in Python using the [WebSockets](https://pypi.org/project/websockets/) library. It is initialized like the following

```python
import asyncio
import websockets

async def handler(websocket, path):
    async for message in websocket:
        print(message)

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
```

The server would be able to handle multiple connections at the same time. It would also be able to handle multiple messages at the same time. Any service that wants to send a message over WS by first connecting to the WS server and then sending the message. The following code snippet shows how to send a message over WS

```python
import asyncio
import websockets

async def send_message(message):
    async with websockets.connect("ws://localhost:8765") as websocket:
        await websocket.send(message)

asyncio.get_event_loop().run_until_complete(send_message("Hello World!"))
```

Although the flight software code would be handling both the drop mechanism and retaining/parsing the detection location information, it would just connect to the WS server once. All communication between the flight and the airdrop microservice would happen over WS, making the code more modular and easier to maintain and visible at the GCS.

Essentially, the WS server would act as a constant stream of messages from all modules of the system. 

# Implementation

During a mission, the following events would take place and the following messages would be sent:

**1. The camera takes a photo and requests telemetry data from the flight control software via POST.**

This is the first step in the mission where the camera microservice captures an image and requests the necessary telemetry data from the flight control software using a POST request.

Flight software would trigger the camera to start taking photos at set intervals in WS with the following payload

```json
{
    "client": "camera",
    "action": "start",
    "interval": 5
}
```
As the camera takes photos, it requests telemetry data from the flight software via POST with the following payload
and receives the following response

```json
{
    "data": {
        "latitude": 37.335480,
        "longitude": -121.893028,
        "altitude": 100,
        "heading": 0,
        "pitch": 0,
        "roll": 0
    }
}
```

The image is saved on disk and the following payload is sent over WS

```json
{
    "client": "odlc",
    "image": "/path/to/time/series/image.jpg",
    "latitude": 37.335480,
    "longitude": -121.893028,
    "altitude": 100,
    "heading": 0,
    "pitch": 0,
    "roll": 0
}
```

**2. ODLC receives the photo and telemetry data and analyzes the photo.**

The image analysis process involves detecting where the objects are, classifying them, and finding their exact location. 

**3. ODLC sends the analyzed photo to the flight software via WS.** 

The ODLC microservice then sends the analyzed image to the flight software using WS with the following payload

```json
{
    "client": "flight",
    "action": "update",
    "targets": [
        {
            "type": "alphanumeric",
            "latitude": 37.335480,
            "longitude": -121.893028,
            "shape": "circle",
            "background_color": "red",
            "alphanumeric": "A",
            "alphanumeric_color": "white",
        },
        {
            "type": "emergent",
            "latitude": 37.335480,
            "longitude": -121.893028,
        }
    ]
}
```

**4. The flight software receives the analyzed photo and decides if the targets match the mission criteria.** 

The flight software microservice receives the analyzed image and makes a decision based on whether the detected targets match the mission criteria.

**5. If the targets match the mission criteria, the detection location information is retained.** 

If the detected targets meet the mission criteria, the flight software retains the detection location information for future use.

The following table outlines the information that is retained by the flight software:

Sr No|Target Type| Status |Target Parameters|Current Detection Location|Confidence|
---|---|---|---|---|---|
1|Alphanumeric| Detected |Shape: Circle, BG Color: Red, Alphanumeric: A, Alphanumeric Color: White |`34.18294, -112.494393`|0.98|
2|Emergent| Detected ||`34.46920, -112.472949`|0.7|
3|Alphanumeric|  |Shape: Square, BG Color: Blue, Alphanumeric: B, Alphanumeric Color: Black||NA|

**6. ODLC keeps analyzing photos and sending them to the flight software via WS.**

**7. If the new information sent by ODLC has a better confidence score than the previous information, or if it carries information about a new target, the flight software updates the detection location information.**

Every time a new target is detected, the flight software checks if the target is already present in the table. If it is, it checks if the new detection has a higher confidence score than the previous detection. If it does, the flight software updates the detection location information. If it doesn't, the flight software retains the previous detection location information.

**8. Once the scanning area is covered, the flight software navigates the drone to the closest detection location.** 

It would send the following payload over WS to the flight software

```json
{
    "client": "flight",
    "action": "navigate",
    "latitude": 37.335480,
    "longitude": -121.893028,
    "altitude": 100
}
```

This code is only present for debugging since the flight software would be responsible for navigating the drone to the closest detection location.

**9. Once the drone reaches the best detection location, the flight software triggers the airdrop microservice via WS.** 

The flight software triggers the airdrop microservice via WS with the following payload

```json
{
    "client": "airdrop",
    "action": "drop"
}
```

**10. The airdrop microservice drops the payload.** The airdrop microservice is responsible for dropping the payload once it receives the trigger from the flight software.

**11. Flight software navigates to the next location.** After the payload is dropped, the flight software navigates the drone to the next location.

**12. Repeat steps 9-11 until all the payloads are dropped.** Steps 9 to 11 are repeated until all the payloads are dropped.

**13. The flight software navigates the drone back to the home location.** After all the payloads are dropped, the flight software navigates the drone back to its home location.

# GCS Components

The Ground Control Station would also be connected to the WebSockets channel. It would receive all the aforementioned messages and display them on the UI. The GCS would also be able to send messages to the flight software via WS. The following table outlines the messages that the GCS would be able to send to the flight software:

Sr No|Message|Description|Payload|
---|---|---|---|
1|Start Mission|Starts the mission|`{"client": "flight", "action": "start"}`|
2|Pause Mission|Pauses the mission|`{"client": "flight", "action": "pause"}`|
3|Resume Mission|Resumes the mission|`{"client": "flight", "action": "resume"}`|
4|Stop Mission|Stops the mission|`{"client": "flight", "action": "stop"}`|
5|Set Mission Parameters|Sets the mission parameters|`{"client": "flight", "action": "set", "parameters": {"altitude": 100, "interval": 5}}`|
6|Set Home Location|Sets the home location|`{"client": "flight", "action": "set", "parameters": {"latitude": 37.335480, "longitude": -121.893028}}`|
7|Set Detection Parameters|Sets the detection parameters|`{"client": "flight", "action": "set", "parameters": {"confidence": 0.8}}`|
8|Set Target Parameters|Sets the target parameters|`{"client": "flight", "action": "set", "parameters": {"type": "alphanumeric", "shape": "circle", "background_color": "red", "alphanumeric": "A", "alphanumeric_color": "white"}}`|
9|Set Target Parameters|Sets the target parameters|`{"client": "flight", "action": "set", "parameters": {"type": "emergent"}}`|
