import json
import websockets
from const import *
from utils import get_id

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]L%(lineno)s: %(message)s')


class WeChatWebSocketUtil:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.message_handlers = {
            RECV_TXT_MSG: self.handle_recv_msg,
            RECV_PIC_MSG: self.handle_recv_msg,
            AT_MSG: self.handle_recv_msg,
            HEART_BEAT: self.heartbeat,
            CONNECT_INIT: self.connect_success,
            # Add more message types and corresponding handler methods here
        }

    async def connect(self):
        self.ws = await websockets.connect(self.url)

    async def listen(self):
        while True:
            message = await self.ws.recv()
            logging.info(message)
            await self.handle_message(message)

    async def handle_message(self, message):
        try:
            data = json.loads(message)
            message_type = data.get('type')
            handler = self.message_handlers.get(message_type)
            if handler:
                await handler(data)
            else:
                logging.info(f'Unhandled message type: {message_type} {data}')
        except json.JSONDecodeError as e:
            logging.info(f'Error decoding message: {message}')
        except Exception as e:
            logging.info(f'Error handling message: {str(e)}')

    async def close(self):
        await self.ws.close()

    @staticmethod
    def generate_json_object(type_, wxid='null', roomid='null', content='null', nickname='null', ext='null'):
        j = {
            'id': get_id(),
            'type': type_,
            'wxid': wxid,
            'roomid': roomid,
            'content': content,
            'nickname': nickname,
            'ext': ext
        }
        return json.dumps(j)

    async def send_attach(self, wx_id, content):
        j = self.generate_json_object(ATTACH_FILE, wxid=wx_id, content=content)
        return j

    async def send_at_msg(self, room_id, wx_id, content, nickname):
        j = self.generate_json_object(AT_MSG, roomid=room_id, wxid=wx_id, content=content, nickname=nickname)
        return j

    async def send_pic_msg(self, wx_id, img_path):
        j = self.generate_json_object(PIC_MSG, wxid=wx_id, content=img_path)
        return j

    async def get_personal_detail(self, wx_id):
        j = self.generate_json_object(PERSONAL_DETAIL, content='op:personal detail', wxid=wx_id)
        return j

    async def get_personal_info(self, wx_id):
        j = self.generate_json_object(PERSONAL_INFO, content='op:personal info', wxid=wx_id)
        return j

    async def send_txt_msg(self, wx_id, content):
        j = self.generate_json_object(TXT_MSG, wxid=wx_id, content=content)
        return j

    async def get_contact_list(self):
        j = self.generate_json_object(USER_LIST)
        return j

    async def connect_success(self, j):
        if j.get("status") == "SUCCSESSED":
            logging.info("连接websocket服务成功")
        else:
            logging.error(j)

    async def handle_recv_msg(self, j):
        logging.info("接收到信息: ")
        logging.info(j)

    async def heartbeat(self, j):
        logging.info("心跳")
