import json
path="PageObjectLocator/AssistedBookingJT.json"
class Test():
    def __init__(self, path):
        self.fileobj=json.load(path)
        for key in self.fileobj:
            print(key)



