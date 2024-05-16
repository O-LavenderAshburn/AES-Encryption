from Crypto.Cipher import AES
from Crypto.Util import Padding
from PIL import Image
from Crypto.Random import get_random_bytes
from io import BytesIO

#initilization vector
iv = get_random_bytes(16)

#128byte key
hexkey = b"770A8A65DA156D24EE2A093277530142"

#ECB Encryption
def ECB_Encrypt(image_bytes):
    ECB_cypher =  AES.new(hexkey, AES.MODE_ECB)
    padded = Padding.pad(image_bytes,16)
    ciphertext = ECB_cypher.encrypt(padded)
    return ciphertext

#CBC Encryption
def CBC_Encrypt(image_bytes):
    CFB_cypher =  AES.new(iv, AES.MODE_CBC)
    ct_bytes = Padding.pad(image_bytes,16)
    cyphertext = CFB_cypher.encrypt(ct_bytes)

    return cyphertext

#CFB Encryption
def CFB_Encrypt(image_bytes):
    CFB_cypher =  AES.new(hexkey, AES.MODE_CFB,segment_size=8,iv=iv)
    ciphertext = CFB_cypher.encrypt(image_bytes)

    return ciphertext

#Ask user for input
print("Enter Path to bmp image")
image_name = input()

try:
    #Check file extention
    img_name_split = image_name.split(".")
    if img_name_split[1] != "bmp":
        raise Exception
#catch error
except Exception:
    print("File must be BMP")
    exit()
    
#get image bytes 
try:
    image = Image.open(image_name)
    image_bytes = image.tobytes()
except FileNotFoundError:
    print(image_name + " File not found")
    exit()

#Encrypt image using ECB encryption
cipher_text = ECB_Encrypt(image_bytes)
new_image = Image.frombytes(mode='RGB',size =image.size,data=cipher_text)
new_image.save(fp="ECB.jpg",format="JPEG")

#Encrypt image using CFB encryption
cipher_text = CFB_Encrypt(image_bytes)
new_image = Image.frombytes(mode='RGB',size =image.size,data=cipher_text)
new_image.save(fp="CFB.jpg",format="JPEG")

#Encrypt image using CBC encryption
cipher_text = CBC_Encrypt(image_bytes)
new_image = Image.frombytes(mode='RGB',size =image.size,data=cipher_text)
new_image.save(fp="CBC.jpg",format="JPEG")





