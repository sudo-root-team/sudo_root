"""This module use the zxing.org website to decode 1D and 2D barcode"""

import requests as req
import lxml.html


def parse_zxing_respone(response):
    """Parse the zxing response to get barcode decoded value.
    """
    val_xpath = {
        'Raw text': 'tr[1]/td[2]/pre',
        'Raw bytes': 'tr[2]/td[2]/pre',
        'Barcode format': 'tr[3]/td[2]',
        'Parsed Result Type': 'tr[4]/td[2]',
        'Parsed Result': 'tr[5]/td[2]/pre'
        }
    parsed = dict()
    html = lxml.html.fromstring(response.text)
    base_xpath = '/html/body/div/table/'
    for value_name, v_xpath in val_xpath.items():
        try:
            value = html.xpath(base_xpath + v_xpath)[0].text
            parsed[value_name] = value
        except IndexError:
            print(value_name)
            parsed[value_name] = ''

    return parsed


def decode(filename):
    """Decode the barcode image (filename)

    Exemple:

    >>> from sudo_root.misc import zxing
    >>> print zxing.decode("qr.png")
    """

    files = dict(f=open(filename, "rb").read())
    r = req.post("https://zxing.org/w/decode", files=files, timeout=5)
    return parse_zxing_respone(r.text)
