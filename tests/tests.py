import unittest
from sudo_root.stegano import LSBExtractor


class TestLSBExtractor(unittest.TestCase):

    def test_all_lsb(self):
        img_path = "./test_assets/stegano/lamiri_sba.png"

        lsb = LSBExtractor(img_path)
        out = lsb.all_lsb(40)

        msg = ""
        for i in range(0, len(out), 8):
            msg += chr(int(out[i:i+8], 2))

        self.assertEqual(msg, "Hello World !!!")

    def test_all_cycle(self):
        img_path = "./test_assets/stegano/esi_sba_lsb_cycle.png"

        lsb = LSBExtractor(img_path)
        out = lsb.cycle_lsb(192)

        msg = ""
        for i in range(0, len(out), 8):
            msg += chr(int(out[i:i+8], 2))

        self.assertEqual(msg, "LSB cycle hidden message")


if __name__ == '__main__':
    unittest.main()
