from channels.generic.websocket import AsyncJsonWebsocketConsumer


class SaleConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('client connected')
        await self.accept()
        await self.channel_layer.group_add('sale', self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard('sale', self.channel_name)

    async def receive_json(self, content, **kwargs):
        pass

    async def group_message(self, event):
        pass
