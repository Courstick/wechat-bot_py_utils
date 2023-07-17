import asyncio

from wechat_websocket import WeChatWebSocketUtil


async def main():
    ws = WeChatWebSocketUtil("ws://127.0.0.1:5555")
    await ws.connect()
    await ws.listen()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
