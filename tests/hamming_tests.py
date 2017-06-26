from sudo_root.misc import hamming as hamm

def split_15_test():
    f = open("/home/youben/Hacking/Hamming/image_with_flag_defect.jpg.hamming","rb")
    hdata = f.read()
    f.close()
    blocks = hamm.split_15(hdata)
    bin_blocks =[hamm.block2bin(b) for b in blocks]
    data_out = ""
    for b in bin_blocks:
        data_out += hamm.decode_15(b)

    f = open("new","wb")
    f.write(data_out)
    f.close()
