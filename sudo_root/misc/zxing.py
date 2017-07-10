"""This module use the zxing.org website to decode 1D and 2D barcode"""

import requests as req
from HTMLParser import HTMLParser

class RespParser(HTMLParser):
    """Create a parser that will parse the response
    from the zxing.org website.
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.decoded = dict()
        self.decoded['Raw text'] = ""
        self.decoded['Raw bytes'] = ""
        self.decoded['Barcode format'] = ""
        self.decoded['Parsed Result Type'] = ""
        self.decoded['Parsed Result'] = ""
        
        self.found = dict()
        self.found['Raw text'] = False
        self.found['Raw bytes'] = False
        self.found['Barcode format'] = False
        self.found['Parsed Result Type'] = False
        self.found['Parsed Result'] = False                        
        
    def handle_data(self, data):
        
        for key in self.found.iterkeys():
            if self.found[key]:
                self.decoded[key] = data
                self.found[key] = False
        
        for key in self.found.iterkeys():
            if data ==  key:
                self.found[key] = True
        

def decode(filename):
    """Decode the barcode image (filename)
    
    Exemple:
    
    from sudo_root.misc import zxing
    
    print zxing.decode("qr.png")
    """
    
    files = dict(f=open(filename,"rb").read())
    r = req.post("https://zxing.org/w/decode",files=files,timeout=5)
    
    parser = RespParser()
    parser.feed(r.text)
    return parser.decoded
