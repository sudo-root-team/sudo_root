""" Module to parse pcap files which contain keyboard input reports"""
from scapy.all import rdpcap

KEY_CODES = {
    4: "a",
    5: "b",
    6: "c",
    7: "d",
    8: "e",
    9: "f",
    10: "g",
    11: "h",
    12: "i",
    13: "j",
    14: "k",
    15: "l",
    16: "m",
    17: "n",
    18: "o",
    19: "p",
    20: "q",
    21: "r",
    22: "s",
    23: "t",
    24: "u",
    25: "v",
    26: "w",
    27: "x",
    28: "y",
    29: "z",
    30: "1",
    31: "2",
    32: "3",
    33: "4",
    34: "5",
    35: "6",
    36: "7",
    37: "8",
    38: "9",
    39: "0",
    40: "ENTER",
    41: "ESCAPE",
    42: "DELETE",
    43: "TAB",
    44: "SPACE",
    45: "-",
    46: "=",
    47: "[",
    48: "]",
    49: "\\",
    50: "#",
    51: ";",
    52: "'",
    53: "`",
    54: ",",
    55: ".",
    56: "/",
    57: "CAPS LOCK",
    58: "F1",
    59: "F2",
    60: "F3",
    61: "F4",
    62: "F5",
    63: "F6",
    64: "F7",
    65: "F8",
    66: "F9",
    67: "F10",
    68: "F11",
    69: "F12",
    70: "PRINT SCREEN",
    71: "SCROLL LOCK",
    72: "PAUSE",
    73: "INSERT",
    74: "HOME",
    75: "PAGE UP",
    76: "SUPPR",
    77: "END",
    78: "PAGE DOWN",
    79: "RIGHT",
    80: "LEFT",
    81: "DOWN",
    82: "UP",
    83: "NUM LOCK",
    84: "Keypad /1",
    85: "Keypad *",
    86: "Keypad -",
    87: "Keypad +",
    88: "Keypad Enter",
    89: "Keypad 1",
    90: "Keypad 2",
    91: "Keypad 3",
    92: "Keypad 4",
    93: "Keypad 5",
    94: "Keypad 6",
    95: "Keypad 7",
    96: "Keypad 8",
    97: "Keypad 9",
    98: "Keypad 0",
    99: "Keypad .",
    100: "\\",
    101: "APPLICATION",
    102: "POWER",
    103: "Keypad =",
    104: "F13",
    105: "F14",
    106: "F15",
    107: "F16",
    108: "F17",
    109: "F18",
    110: "F19",
    111: "F20",
    112: "F21",
    113: "F22",
    114: "F23",
    115: "F24",
    116: "EXECUTE",
    117: "HELP",
    118: "MENU",
    119: "SELECT",
    120: "STOP",
    121: "AGAIN",
    122: "UNDO",
    123: "CUT",
    124: "COPY",
    125: "PASTE",
    126: "FIND",
    127: "MUTE",
    128: "VOL UP",
    129: "VOL DOWN",
    130: "LOCKING CAPS LOCK",
    131: "LOCKING NUM LOCK",
    132: "LOCKING SCROLL LOCK",
    133: "Keypad Comma",
    134: "Keypad Equal Sign",
    135: "International1",
    136: "International2",
    137: "International3",
    138: "International4",
    139: "International5",
    140: "International6",
    141: "International7",
    142: "International8",
    143: "International9",
    144: "LANG1",
    145: "LANG2",
    146: "LANG3",
    147: "LANG4",
    148: "LANG5",
    149: "LANG6",
    150: "LANG7",
    151: "LANG8",
    152: "LANG9",
    153: "ALTERNATE ERASE",
    154: "SysReq/Attention",
    155: "Cancel",
    156: "Clear",
    157: "Prior",
    158: "Return",
    159: "Separator",
    160: "Out",
    161: "Oper",
    162: "Clear/Again",
    163: "CrSet/Props",
    164: "ExSel",
    # Reserved 165-175
    176: "Keypad 00",
    177: "Keypad 000",
    178: "Thousands Separator",
    179: "Decimal Separator",
    180: "Currency Unit",
    181: "Currency Sub-unit",
    182: "Keypad (",
    183: "Keypad )",
    184: "Keypad {",
    185: "Keypad }",
    186: "Keypad Tab",
    187: "Keypad BackSpace",
    188: "Keypad A",
    189: "Keypad B",
    190: "Keypad C",
    191: "Keypad D",
    192: "Keypad E",
    193: "Keypad F",
    194: "Keypad XOR",
    195: "Keypad ^",
    196: "Keypad %",
    197: "Keypad <",
    198: "Keypad >",
    199: "Keypad &",
    200: "Keypad &&",
    201: "Keypad |",
    202: "Keypad ||",
    203: "Keypad :",
    204: "Keypad #",
    205: "Keypad Space",
    206: "Keypad @",
    207: "Keypad !",
    208: "Keypad Memory Store",
    209: "Keypad Memory Recall",
    210: "Keypad Memory Clear",
    211: "Keypad Memory Add",
    212: "Keypad Memory Substract",
    213: "Keypad Memory Multiply",
    214: "Keypad Memory Divide",
    215: "Keypad +/-",
    216: "Keypad Clear",
    217: "Keypad Clear Entry",
    218: "Keypad Binary",
    219: "Keypad Octal",
    220: "Keypad Decimal",
    221: "Keypad Hexadecimal",
    # Reserved 222-223
    224: "Left CTRL",
    225: "Left Shift",
    226: "Left ALT",
    227: "Left GUI",
    228: "Right CTRL",
    229: "Right Shift",
    230: "Right ALT",
    231: "Right GUI",
    # Reserved
}

MODIFIERS = {
    1: "Left CTRL",
    2: "Left Shift",
    4: "Left ALT",
    8: "Left GUI",
    16: "Right CTRL",
    32: "Right Shift",
    64: "Right ALT",
    128: "Right GUI",
}


def get_key_in(pcap_file):
    """Extract keyboard input reports from a pcap file.
    The extraction depends only on the size of packets.
    """
    pcap = rdpcap(pcap_file)
    in_reports = []

    for p in pcap:
        if len(p) == 35:
            in_reports.append(p.load[-8:])

    return in_reports


def map_key_in(in_reports):
    """Return the keystroke according to the input reports.
    """
    keystroke = []

    for rep in in_reports:
        # skip null report
        if rep == b"\x00" * 8:
            continue

        s_keys = []  # simultaneous key
        modif = map_modifier(rep[0])
        i = 2
        while rep[i]:
            try:
                s_keys.append(KEY_CODES[rep[i]])
            except KeyError:
                s_keys.append("UNKNOWN")

            i += 1

        keystroke.append("(" + ",".join(modif) + ") " + " ".join(s_keys))

    return keystroke


def map_modifier(modifier):
    """Return modifiers from the input report first byte.
    """
    global MODIFIERS
    modif = []

    for m in MODIFIERS.keys():
        if m & modifier:
            modif.append(MODIFIERS[m])

    return modif


def get_keystroke_from_pcap(pcap_file):
    """Extract keystroke from a pcap file.
    """
    input_reports = get_key_in(pcap_file)
    return map_key_in(input_reports)


def get_keystroke_from_data(data_file):
    """Extract keystroke from data file as outputed by tshark
    tshark -r key.pcap -T fields -e usb.capdata.
    """
    with open(data_file) as f:
        data_reports = f.read().split('\n')
        f.close()

    reports = []

    for d in data_reports:
        if len(d) != 23:
            continue
        r = map(lambda x: int(x, 16), d.split(':'))
        reports.append("".join(map(chr, r)).encode())

    return map_key_in(reports)
