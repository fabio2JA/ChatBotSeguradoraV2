from cryptography.fernet import Fernet
from PIL import Image
import io
from dotenv import load_dotenv
import os


load_dotenv()


key = os.environ.get('ENCRYPT_IMG_KEY')

def encrypt_image(img_path: str):
    with open(img_path, "rb") as f:
        image_bytes = f.read()

    image = Image.open(io.BytesIO(image_bytes))
    
    with io.BytesIO() as output:
        image.save(output, format="JPEG")
        image_bytes = output.getvalue()

    f = Fernet(key)

    encrypted_bytes = f.encrypt(image_bytes)

    with open(img_path, "wb") as f:
        f.write(encrypted_bytes)


def decrypt_image(encrypted_image_path: str):
    with open(encrypted_image_path, "rb") as f:
        encrypted_bytes = f.read()

    f = Fernet(key)

    decrypted_bytes = f.decrypt(encrypted_bytes)

    decrypted_image = Image.open(io.BytesIO(decrypted_bytes))

    decrypted_image.save(encrypted_image_path)