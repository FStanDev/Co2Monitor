from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
import time
import subprocess
import uvicorn
from scd30_i2c import SCD30

scd30 = SCD30()
scd30.set_measurement_interval(2)
scd30.start_periodic_measurement()
app = FastAPI()

html="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebSocket Number Display</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <style>
        body {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            background-color: #1D1A05;
        }

        #numberDisplay {
            font-size: 36px;
            font-weight: bold;
            margin-left: 8px;
        }

        .flexer{
          display: flex;
          flex-direction: row;
        }

        .numberText{
           font-size: 36px;
           font-weight: bold;
           color: #004BA8;
        }
    </style>
</head>
<body>
    <div class="flexer">
      <div class="numberText"> Concentración: </div>
<div id="numberDisplay">Loading...</div>
    </div>
<script>
    // Connect to the WebSocket server
    const ws = new WebSocket(`ws://192.168.1.176:8000/ws`);
    ws.onopen = function() {
      ws.send("test"); //Will work here!
    //^^^^^^^^^^^^^^^^^
    }
    ws.onmessage = function(event){
	try {
	     const number = JSON.parse(event.data).number; // Assuming the server sends JSON with a 'number' property
             updateNumberDisplay(number);
             ws.send(event.data)}
	catch(e){
             ws.send("Excepction")
        }        
   }
    // Handle messages from the server

    // Update the displayed number on the webpage
    function updateNumberDisplay(number) {
        const numberDisplay = document.getElementById('numberDisplay');
        numberDisplay.textContent = `${number.toFixed(2)} ppm`;
      if(number < 1000){
        numberDisplay.style.color = "#0B7A75"
      }
      else if(number > 1000 && number < 2000) {
        numberDisplay.style.color = "#F7F052"
      }else{
        numberDisplay.style.color = "#FC440F"
      }
    }
</script>

</body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html)

# WebSocket route
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    number = -5555
    try:
        while True:
            m = scd30.read_measurement()
            if m is not None:
                number = m[0]
                await manager.send_personal_message('{"number": ' + str(number) + "}", websocket)
            time.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client left the chat")
    except KeyboardInterrupt:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Run the app with uvicorn
# uvicorn yourfilename:app --reload
# For example, if your file is named "main.py", run: uvicorn main:app --reload
