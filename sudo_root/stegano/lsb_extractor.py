"""Module Description: TODO"""

from PIL import Image


class LSBExtractor(object):
    """docstring for lsb_extractor."""

    def __init__(self, img_path):
        self.img = Image.open(img_path)
        self.data = list(self.img.getdata())

    def all_lsb(self, length):
        out = ""
        for i in range(min(len(self.data), length)):
            out += "".join(map(lambda x: str(x & 1), self.data[i]))
        return out

    def cycle_lsb(self, length):
        out = ""
        for i in range(min(len(self.data), length)):
            out += str(self.data[i][i % 3] & 1)
        return out

    @staticmethod
    def bits2bytes(bits):
        out = ""
        for i in range(0, len(bits)/8, 8):
            out += chr(int(bits[i:i+8], 2))
        return out
