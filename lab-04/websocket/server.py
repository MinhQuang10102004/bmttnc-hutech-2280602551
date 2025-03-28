import random
import tornado.ioloop
import tornado.web
import tornado.websocket

class WebsocketServer(tornado.websocket.WebSocketHandler):
    clients = set()
    def open(self):
        WebsocketServer.clients.add(self)
    def on_close(self):
        WebsocketServer.clients.remove(self)
    @classmethod
    def send_message(cls, message):
        print(f"Sending message {message} to {len(cls.clients)} client(s).")
        for client in cls.clients:
            client.write_message(message)
class RandomWordSelector:
    def __init__(self, word_list):
        self.word_list = word_list
    def sample(self):
        return random.choice(self.word_list)
def main():
    app = tornado.web.Application([
        (r"/websocket/", WebsocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=60)
    app.listen(8080)
    io_loop = tornado.ioloop.IOLoop.current()
    word_selector = RandomWordSelector(['apple','banana','orange','grape','melon'])
    periodic_callback = tornado.ioloop.PeriodicCallback(lambda:WebsocketServer.send_message(word_selector.sample()), 3000)
    periodic_callback.start()
    io_loop.start()
if __name__ == "__main__":
    main()                 