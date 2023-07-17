import requests
from const import *
from utils import get_id


class WeChatHttpUtil:
    def __init__(self, url='http://127.0.0.1:5555'):
        self.url = url

    def send_request(self, api_url, json_data):
        options = {
            'url': self.url + api_url,
            'json': {
                'para': json_data
            }
        }
        response = requests.post(**options)
        return response.json()

    def generate_json_data(self, type_, wxid='null', roomid='null', content='null', nickname='null', ext='null'):
        return {
            'id': get_id(),
            'type': type_,
            'wxid': wxid,
            'roomid': roomid,
            'content': content,
            'nickname': nickname,
            'ext': ext
        }

    def send_at_msg(self, wx_id, room_id, content, nickname):
        json_data = self.generate_json_data(AT_MSG, roomid=room_id, wxid=wx_id, content=content, nickname=nickname)
        return self.send_request('/api/sendatmsg', json_data)

    def send_pic(self, wx_id, img_path):
        json_data = self.generate_json_data(PIC_MSG, wxid=wx_id, content=img_path)
        return self.send_request('/api/sendpic', json_data)

    def get_member_nick(self, wx_id, room_id):
        json_data = self.generate_json_data(CHATROOM_MEMBER_NICK, wxid=wx_id, roomid=room_id)
        return self.send_request('/api/getmembernick', json_data)

    def get_memberid(self):
        json_data = self.generate_json_data(CHATROOM_MEMBER, content='op:list member')
        return self.send_request('/api/getmemberid', json_data)

    def get_contact_list(self):
        json_data = self.generate_json_data(USER_LIST)
        return self.send_request('/api/getcontactlist', json_data)

    def get_chatroom_member_list(self):
        json_data = self.generate_json_data(CHATROOM_MEMBER)
        return self.send_request('/api/get_charroom_member_list', json_data)

    def send_txt_msg(self, wx_id, content):
        json_data = self.generate_json_data(TXT_MSG, wxid=wx_id, content=content)
        return self.send_request('/api/sendtxtmsg', json_data)

    def send_attach(self, wx_id, file_path):
        json_data = self.generate_json_data(ATTACH_FILE, wxid=wx_id, content=file_path)
        return self.send_request('/api/sendattatch', json_data)

    def main(self):
        j = self.get_contact_list()
        print(j)
        values = next(filter(lambda item: "cc" in item.get("name"), j.get("content")))
        print(values)
        self.send_attach(values.get("wxid"), r"C:\Users\admin\Downloads\123.png")


if __name__ == '__main__':
    wechat_utility = WeChatHttpUtil()
    wechat_utility.main()
