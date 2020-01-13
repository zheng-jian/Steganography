# -*- coding: UTF-8 -*-
import os


def get2bits(hex):
    list_bit = ["00", "01", "10", "11"]
    temp = hex[1]
    if temp == 'a':
        temp = 10
    elif temp == 'b':
        temp = 11
    elif temp == 'c':
        temp = 12
    elif temp == 'd':
        temp = 13
    elif temp == 'e':
        temp = 14
    elif temp == 'f':
        temp = 15
    temp = int(temp)
    bit = list_bit[temp % 4]
    return bit


def decoder(ori_name):
    with open (ori_name,'rb') as a:
        buff = a.read()
        #print(buff)
        hex_list = ["{:2x}".format(c) for c in buff]
    print(hex_list[23:31])
    list_bit = ["00", "01", "10", "11"]
    taille = ""
    for c in hex_list[23:31]:
        bit = get2bits(c)
        taille = taille + str(bit)
    print(int(taille,2))

    name = ""
    for i in range(31,87,4):
        temp = ""
        for j in range(0,4):
            bit = get2bits(hex_list[i+j])
            temp += str(bit)
        temp = int(temp,2)
        temp = chr(temp)

        name += str(temp)

    print(name)


    image = []
    for i in range(159,159+int(taille,2)*4,4):
        temp = ""
        for j in range(0,4):
            bit = get2bits(hex_list[i+j])
            temp += str(bit)
        temp = int(temp,2)
        temp = str(hex(temp))
        x = temp[2:]
        if len(x) == 1:
            x = "0" + x
        image.append(x)
    print(len(image))
    print(image[0:20])

    # pour verifier
    with open('tatoumina1.jpg','rb') as f:
        a = f.read()
        list_a = ["{:2x}".format(c) for c in a]
        print(len(list_a))
        print(image[0:20])

    with open('test.jpg','wb') as f:
         f.write(bytes.fromhex(''.join(image)))

#decoder('Tatou.pgm')


# i : index of list_ori to change
def cacher(i,list_ori,binary_to_hide):
    j = 0
    while j < len(binary_to_hide):
        # get hex ori
        byte_ori = list_ori[i].replace(' ', '0')

        # get last 4 bits
        bits_to_change = byte_ori[1]
        # print(bits_to_change)

        # change to binary : 0000
        bit_binary = bin(int(bits_to_change, 16))
        # print(bit_binary)

        # change last two bits
        bit_binary = bit_binary[2:][:-2] + binary_to_hide[j:j + 2]
        # print (bit_binary)

        # change to hex
        bits_final = hex(int(bit_binary, 2))
        # print(bits_final)

        # only use last element
        byte_ori = byte_ori[0] + bits_final[-1]
        list_ori[i] = byte_ori
        j += 2
        i += 1


def encoder(origin, hide):
    name = hide
    with open(hide,'rb') as f:
        a = f.read()
        list_hide = ["{:2x}".format(c) for c in a]
    size = len(list_hide)
    print(size)
    print(name)

    with open(origin,'rb') as f:
        ori = f.read()
        list_ori = ["{:2x}".format(c) for c in ori]


    #taille cacher
    bin_size = bin(size)[2:]
    #print(bin_size)

    i = 23
    cacher(i,list_ori,bin_size)
    #print(list_ori[23:31])

    #name cacher
    i = 31
    for s in name:
        s = bin(ord(s)).replace('0b', '')
        for num0 in range(8-len(s)):
            s = '0' + s
        #print(s)
        cacher(i,list_ori,s)
        i += 4
    #print(list_ori[31:87])

    #image cacher
    i = 159
    for item in list_hide:
        s = bin(int(item.replace(' ','0'),16))[2:]
        for num0 in range(8-len(s)):
            s = '0' + s
        # print(s)
        cacher(i,list_ori,s)
        i += 4

    for i in range(len(list_ori)):
        list_ori[i] = list_ori[i].replace(' ','0')
    print(list_ori[0:22])

    with open('lsb_output.jpg','wb') as f:
         f.write(bytes.fromhex(''.join(list_ori)))




encoder('Lena.pgm','tatoumina1.jpg')
decoder('lsb_output.jpg')

