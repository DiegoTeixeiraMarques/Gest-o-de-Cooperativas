import serial

def pegarPeso():

    __message = str(chr(5))
    _serial = serial.Serial(
        'com1',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,
        writeTimeout=2
    )

    print(_serial)

    # if True:
    if _serial.isOpen():
        print("aberto")
        _serial.write(__message.encode('ascii'))
        _serial.flushInput()
        weight = _serial.read(14)
        str_weight = str(weight.decode())
        # new_weight = ["0","3",".","1","2"]
        new_weight = []
        for x in range(len(str_weight)):
            if 0 < x < 7:
                new_weight.append(str_weight[x])

        _serial.close()

        new_weight = "".join(new_weight)
    else:
        print("fechado")

    print(new_weight)

pegarPeso()
