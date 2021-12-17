import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.pos = self.scope['url_route']['kwargs']['pk']
        self.pos_group_name = f'pos_{self.pos}'


        async_to_sync(self.channel_layer.group_add)(
            self.pos_group_name,
            self.channel_name
            )
        self.accept()


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.pos_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        order_data = json.loads(text_data)
        code = order_data['code']
        date = order_data['date']
        num = order_data['num']

        async_to_sync(self.channel_layer.group_send)(
            self.pos_group_name,
            {
                'type': 'send_order',
                'message': {
                    'code': code,
                    'date': date,
                    'num': num,
                }
            }
        )



    def send_order(self, event):
        data = event['message']
        self.send(text_data=json.dumps({
            'event': 'send',
            'code': data['code'],
            'date': data['date'],
            'num': data['num']
        }))