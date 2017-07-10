from sudo_root.crypto import lcg

def break_lcg_test():
    l = lcg.Lcg(0x66e158441b6995, 0xB, 1<<85, 53)
    state = l.get_state(2752470789, 3367609997,1185935283)
    l.next()
