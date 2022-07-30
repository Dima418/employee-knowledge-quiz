import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect


async def handle_websocket(websocket: WebSocket):
    await websocket.accept()

    pub_queue = asyncio.queues.Queue(2000)

    def force_close():
        async def close_task():
            try:
                await websocket.close()
            except:
                pass

        asyncio.create_task(close_task())

    async def pub_task():
        try:
            while True:
                await websocket.send_text(pub_queue.get_nowait())
        except asyncio.QueueEmpty:
            pass
        except:
            force_close()

    pub_task_handle = asyncio.create_task(pub_task())

    def pub(change_str):
        nonlocal pub_task_handle
        try:
            pub_queue.put_nowait(change_str)
            if pub_task_handle.done():
                pub_task_handle = asyncio.create_task(pub_task())
        except asyncio.QueueFull:
            force_close()

    pub(json.dumps({
        "type": "init",
        "data": {}
    }))

    try:
        # appstate.processor.register_event_listener(pub)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        # appstate.processor.unregister_event_listener(pub)
        pass
