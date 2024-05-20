"""
Encrypts .bnp images and outputs image as .jpeg 
with encrypted image bytes being the body
"""

# initilization vector
__iv__ = get_random_bytes(16)
# 128byte key
__hexkey__ = b"770A8A65DA156D24EE2A093277530142"


from Crypto.Cipher import AES
from Crypto.Util import Padding
from PIL import Image
from Crypto.Random import get_random_bytes
from io import BytesIO


def ECB_Encrypt(image_bytes):
    """
    AES -ECB Encryption Mode

    @param image_bytes Bytes to encrypt

    @return Return image bytes as ciphertext
    """

    # set cipher mode
    ECB_cypher = AES.new(__hexkey__, AES.MODE_ECB)
    # pad bytes
    padded = Padding.pad(image_bytes, 16)
    # encrypt
    ciphertext = ECB_cypher.encrypt(padded)
    return ciphertext


def CBC_Encrypt(image_bytes):
    """
    AES -CBC Encryption Mode

    @param image_bytes Bytes to encrypt

    @return Return image bytes as ciphertext
    """

    # set cipher mode
    CFB_cypher = AES.new(__iv__, AES.MODE_CBC)
    # pad bytes
    ct_bytes = Padding.pad(image_bytes, 16)
    cyphertext = CFB_cypher.encrypt(ct_bytes)

    return cyphertext


def CFB_Encrypt(image_bytes):
    """
    AES -CFB Encryption Mode

    @param image_bytes Bytes to encrypt

    @return Return image bytes as ciphertext
    """

    # set cipher mode
    CFB_cypher = AES.new(__hexkey__, AES.MODE_CFB, segment_size=8, iv=__iv__)
    # encrypt bytes
    ciphertext = CFB_cypher.encrypt(image_bytes)
    return ciphertext


# Ask user for input
print("Enter Path to bmp image")
image_name = input()

try:
    # Check file extention
    img_name_split = image_name.split(".")
    if img_name_split[1] != "bmp":
        raise Exception
# catch error
except Exception:
    print("File must be BMP")
    exit()

# get image bytes
try:
    image = Image.open(image_name)
    image_bytes = image.tobytes()
except FileNotFoundError:
    print(image_name + " File not found")
    exit()

# Encrypt image using ECB encryption
cipher_text = ECB_Encrypt(image_bytes)
# Create and save
new_image = Image.frombytes(mode="RGB", size=image.size, data=cipher_text)
new_image.save(fp="ECB.jpg", format="JPEG")

# Encrypt image using CFB encryption
cipher_text = CFB_Encrypt(image_bytes)
# Create and save
new_image = Image.frombytes(mode="RGB", size=image.size, data=cipher_text)
new_image.save(fp="CFB.jpg", format="JPEG")

# Encrypt image using CBC encryption
cipher_text = CBC_Encrypt(image_bytes)
# Create and save
new_image = Image.frombytes(mode="RGB", size=image.size, data=cipher_text)
new_image.save(fp="CBC.jpg", format="JPEG")
