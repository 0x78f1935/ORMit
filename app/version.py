from app.settings import VAPI
import binascii, urllib.request

class VersionCheck(object):
    def __init__(self):
        self.x, self.y = [binascii.unhexlify(i) for i in VAPI.decode().split('l')]

    def check(self):
        try:
            with urllib.request.urlopen('https://'+ self.x.decode()) as f:
                state = [i.decode() for i in f.readlines() if 'ORMit' in i.decode()][0].split('=')[1]
            if state != self.y.decode(): return True
            else: return False
        except Exception as e:
            print('Could not connect update server: {}'.format(e.args))
