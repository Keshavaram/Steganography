import math
import random
from cv2 import *
import numpy as np


def genE(t):
    possibleEs = []
    for i in range(150, t):
        if math.gcd(i, t) == 1:
            possibleEs.append(i)
    random.seed(100)
    return random.choice(possibleEs)


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = egcd(b % a, a)
        return gcd, y - (b // a) * x, x


def modInv(a, b):
    _, x, _ = egcd(a, b)
    return x


def encryption(n, encrpt, msg):
    cipher = ""
    splChar = [33, 34, 35, 36, 37, 38, 39, 40, 41, 91, 92, 93, 94, 95, 96, 123, 124, 125, 126]
    for i in msg:
        cipher += str(((ord(i) ** encrpt) % n) * 123456789) + chr(random.choice(splChar))
    return cipher


def decryption(n, dycrpt, cipher):
    msg = ""
    parts = []
    temp = ""
    splChar = [33, 34, 35, 36, 37, 38, 39, 40, 41, 91, 92, 93, 94, 95, 96, 123, 124, 125, 126]
    for i in cipher:
        if ord(i) in splChar:
            parts.append(temp)
            temp = ""
        else:
            temp += i

    for i in parts:
        msg += chr(((int(int(i) / 123456789) ** dycrpt) % n))
    return msg

# *********************************************************************************************************************************************************************************************************************************************************************************************
# steganography part
def messageToBinary(message):
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")

def hideData(image, secret_message):
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    if len(secret_message) > n_bytes:
        raise ValueError("Error encountered insufficient bytes,need bigger image or less data.")
    secret_message += "#####"
    data_index = 0
    binary_secret_msg = messageToBinary(secret_message)
    data_len = len(binary_secret_msg)
    for values in image:
        for pixel in values:
            r, g, b = messageToBinary(pixel)
            if data_index < data_len:
                pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len:
                pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index >= data_len:
                break
    return image


def showData(image):
    binary_data = ""
    for values in image:
        for pixel in values:
            r, g, b = messageToBinary(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    all_bytes = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####":
            break
    return decoded_data[:-5]


def encode_text(encrytedData):
    image_name = input("Enter image name with the extension:")
    image = cv2.imread(image_name)

    if len(encrytedData) == 0:
        raise ValueError('Data is empty')
    filename = input("Enter the name of new encoded image with the extension:")
    encoded_image = hideData(image, encrytedData)
    cv2.imwrite(filename, encoded_image)


def decode_text():
    image_name = input("Enter the name of steganographed image with the extension:")
    image = cv2.imread(image_name)
    text = showData(image)
    return text


def steganography():
    a = input("1. ENCODE THE DATA\n2. DECODE THE DATA\nEnter your option : ")
    e = genE(T)
    try:
        userInput = int(a)
        if userInput == 1:
            print("\nEncoding...")
            text = input("Enter the text to be hidden : ")
            rsaRes = encryption(N, e, text)
            print("RSA string = ", rsaRes)
            encode_text(rsaRes)
        elif userInput == 2:
            d = modInv(e, T)
            print("\nDecoding...")
            print("Encoded msg is : ", decryption(N, d, decode_text()))
        else:
            raise ValueError
    except ValueError:
        print("Please choose a valid option...")
        print("#############################################")
        print()
        steganography()


p, q = 61, 67
N = p * q
T = (p - 1) * (q - 1)
steganography()
