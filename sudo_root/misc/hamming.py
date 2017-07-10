"""Module that help to deal with hamming data"""
def split_15(hdata):
    "Split hdata to blocks of 15 bytes."
    dataout = [hdata[i : i+15] for i in range(0,len(hdata),15)]
    return dataout

def split_7(hdata):
    "Split hdata to blocks of 7 bytes."
    dataout = [hdata[i : i+7] for i in range(0,len(hdata),7)]
    return dataout

def block2bin(block):
    "Codify each byte of block in binary form (8 bits)."
    bbin =[]
    for b in block:
        bbin.append([int(c) for c in bin(ord(b))[2:].zfill(8)])
                
    return bbin

def decode_block_15(bin_block):
    "Decode and correct a block of 15 bytes, represented in a binary form."
    b = bin_block
    i = 0 #bit position
    while i < 8:

        h1 = b[0][i] ^ b[2][i] ^ b[4][i] ^ b[6][i] ^ b[8][i] ^ b[10][i] ^ b[12][i] ^ b[14][i]
        h2 = b[1][i] ^ b[2][i] ^ b[5][i] ^ b[6][i] ^ b[9][i] ^ b[10][i] ^ b[13][i] ^ b[14][i]
        h4 = b[3][i] ^ b[4][i] ^ b[5][i] ^ b[6][i] ^ b[11][i] ^ b[12][i] ^ b[13][i] ^ b[14][i]
        h8 = b[7][i] ^ b[8][i] ^ b[9][i] ^ b[10][i] ^ b[11][i] ^ b[12][i] ^ b[13][i] ^ b[14][i]
        
        key = int("".join(map(str,[h8, h4, h2, h1])), 2)

        if key != 0:
            b[key - 1][i] ^= 1
        else:
            i += 1

    bin_decoded = [int("".join(map(str,bit)), 2) for bit in b]
    
    data_corrected = [bin_decoded[j] for j in [2,4,5,6,8,9,10,11,12,13,14]]
    return "".join(map(chr,data_corrected))

def decode_15(data):
    """Decode and correct data using hamming_15_11
    Exemple:
    
    from sudo_root.misc import hamming as hamm
    
    f = open("file.hamm","rb")
    hdata = f.read()
    f.close()
    data_out = hamm.decode_15(hdata)
    f = open("decoded","wb")
    f.write(data_out)
    f.close()
    """
    blocks = split_15(data)
    bin_blocks = [block2bin(b) for b in blocks]
    data_out = ""

    for b in bin_blocks:
        data_out += decode_block_15(b)
    
    return data_out
