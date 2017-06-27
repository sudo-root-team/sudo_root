from sudo_root.misc import hamming as hamm

def split_15_test():
    f = open("/home/youben/Hacking/Hamming/image_with_flag_defect.jpg.hamming","rb")
    hdata = f.read()
    f.close()
    data_out = hamm.decode_15(hdata)
    f = open("new","wb")
    f.write(data_out)
    f.close()
