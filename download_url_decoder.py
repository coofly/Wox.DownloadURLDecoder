#encoding=utf8
__author__ = 'coofly'

from wox import Wox,WoxAPI
import base64
import pyperclip

class Decoder():

    def __init__(self):
        pass

    def type_header(self):
        pass

    def type_name(self):
        pass

    def decode(self, url_body):
        pass

class ThunderDecoder(Decoder):

    def type_header(self):
        return 'thunder'

    def type_name(self):
        return "迅雷下载链接"

    def decode(self, url_body):
        try:
            decode_str = base64.decodestring(url_body)
        except Exception:
            return None
        if len(decode_str) <= 4:
            return None
        return decode_str[2:-2]

class QQDLDecoder(Decoder):

    def type_header(self):
        return 'qqdl'

    def type_name(self):
        return "QQ旋风下载链接"

    def decode(self, url_body):
        try:
            decode_str = base64.decodestring(url_body)
        except Exception:
            return None
        return decode_str

class FlashGetDecoder(Decoder):

    def type_header(self):
        return 'flashget'

    def type_name(self):
        return "快车下载链接"

    def decode(self, url_body):
        try:
            decode_str = base64.decodestring(url_body)
        except Exception:
            return None
        if len(decode_str) <= 20:
            return None
        return decode_str[10:-10]


class Main(Wox):

    def __init__(self):
        self._decoder_list = [ThunderDecoder(), QQDLDecoder(), FlashGetDecoder()]
        super(Main, self).__init__()

    def query(self,key):
        results = []
        parts = key.strip().split('://', 2)
        if len(parts) != 2:
            return results

        header = parts[0].lower()
        body = parts[1]
        for decoder in self._decoder_list:
            if decoder.type_header() == header:
                real_url = decoder.decode(body)
                if None == real_url:
                    continue
                else:
                    results.append({
                        "Title":decoder.type_name(),
                        "SubTitle":real_url,
                        "IcoPath":"ico.png",
                        "JsonRPCAction":{
                            "method":"copy_url",
                            "parameters":[real_url],
                            "dontHideAfterAction":False
                        }
                    })
                    break
        return results

    def copy_url(self, url):
        pyperclip.copy(url)

if __name__ == '__main__':
    Main()