import os
import unittest
from sudo_root.stegano import LSBExtractor
from sudo_root.misc import zxing
from sudo_root.crypto import Lcg
from sudo_root.forensic import keycode


def relative_path(path):
    return os.path.join(os.path.dirname(__file__), path)


class TestLSBExtractor(unittest.TestCase):

    def test_all_lsb(self):
        img_path = relative_path("test_assets/stegano/lamiri_sba.png")

        lsb = LSBExtractor(img_path)
        out = lsb.all_lsb(40)

        msg = ""
        for i in range(0, len(out), 8):
            msg += chr(int(out[i:i+8], 2))

        self.assertEqual(msg, "Hello World !!!")

    def test_all_cycle(self):
        img_path = relative_path("test_assets/stegano/esi_sba_lsb_cycle.png")

        lsb = LSBExtractor(img_path)
        out = lsb.cycle_lsb(192)

        msg = ""
        for i in range(0, len(out), 8):
            msg += chr(int(out[i:i+8], 2))

        self.assertEqual(msg, "LSB cycle hidden message")


class TestZxing(unittest.TestCase):

    def test_decode(self):
        img_path = relative_path("test_assets/misc/qrcode_wikipedia.png")

        result = zxing.decode(img_path)
        raw_text = result["Raw text"]
        self.assertEqual(raw_text, "http://en.m.wikipedia.org")


class TestLcg(unittest.TestCase):

    def test_lcg(self):
        lcg = Lcg(0x66e158441b6995, 0xB, 1 << 85, 53)
        state = lcg.get_state(2752470789, 3367609997, 1185935283)
        next_values = [lcg.next() for _ in range(4)]

        expected_next_values = [3367609997, 1185935283, 587646151, 4198508994]

        self.assertEqual(state, 24792052844465667546212387)
        self.assertEqual(next_values, expected_next_values)


class TestKeycode(unittest.TestCase):

    def test_extract_keycode(self):
        keycode_pcap_path = relative_path("test_assets/keycode.pcap")
        extracted_keycode_path = relative_path("test_assets/keycode.extracted")
        keycodes = keycode.get_keystroke_from_pcap(keycode_pcap_path)
        target_keycodes = keycode.get_keystroke_from_data(extracted_keycode_path)
        self.assertEqual(keycodes, target_keycodes)


if __name__ == '__main__':
    unittest.main()
