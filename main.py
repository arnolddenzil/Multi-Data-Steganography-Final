from PIL import Image
import crypto
import json
import os
import zipfile
import hashlib
import base64
from stegano import lsb


img_path = str
vault = {}

hash_obj = hashlib.sha3_224()



def get_encoded_file(file_path):

    # Load the image from a file
    with open(file_path, 'rb') as f:
        data = f.read()

    # Encode the file data as a Base64 string
    encoded_file = base64.b64encode(data).decode('utf-8')

    # file_type = file_path.split(".")[-1]
    # print(file_type)

    file_name = os.path.basename(file_path)

    # if file_type in ['jpeg', 'jpg', 'png']:
    #     print("the file is a image type")
    #     encoded_file = "img" + encoded_file
    #
    # elif file_type in ['mp4', 'mkv']:
    #     print("the file is a video type")

    # add the file type to the start of the encoded file to save it in the correct format during retrieval
    encoded_file = file_name + "###" + encoded_file

    return encoded_file

    # # print(f"Encoded image : {encoded_image}")
    #
    # # Create a dictionary to hold the JSON data
    # data = {
    #     'image': encoded_image
    # }
    #
    # # Encode the data as a JSON string
    # json_string = json.dumps(data)
    #
    # print(f"Json_string : {json_string}")
    #
    #
    # # Save the JSON string to a file
    # with open('data.json', 'w') as f:
    #     f.write(json_string)


def get_hashed_text(word):
    encoded_str = word.encode()
    obj_sha3 = hashlib.sha3_256(encoded_str)
    return obj_sha3.hexdigest()


def open_image():
    global img_path
    img_path = input("Enter image path : ")
    image = Image.open(img_path)
    image.show()


def save_image():
    # img_type = img_path.split(".")[-1]        # Will get the image type/format
    # print(img_type)
    # print(img_path)

    # Encode the data as a JSON string
    json_string = json.dumps(vault)

    print(f"Json_string : {json_string}")

    secret = lsb.hide(str(img_path), json_string)
    # os.remove("./bmw.png")
    secret.save(img_path)

    # # Save the JSON string to a file
    # with open('data.json', 'w') as f:
    #     f.write(json_string)
    #
    # # Create a new zip file
    # with zipfile.ZipFile('temporary.zip', 'w') as zip:
    #     # Add a file to the zip file
    #     zip.write('data.json')
    #
    # # Hide zip file in an image and save new image
    # os.system(f"copy /b {img_path}+temporary.zip hidden_img.png")
    #
    # os.remove("data.json")
    # os.remove("temporary.zip")
    # if os.path.exists("data.json") or os.path.exists("temporary.zip"):
    #     print("file still exit")
    # else:
    #     print("the temporary files are deleted")



def hide_text():
    global vault
    secret = input("Enter the secret to hide : ")
    k = input("Enter secret key : ")
    encrypted_data = crypto.encrypt_text(key=k, text=secret)

    text_to_hide = "plaintext###" + encrypted_data

    key = get_hashed_text(k)
    vault[key] = text_to_hide





    # secret = lsb.hide(r"C:\Users\Arnold\Pictures\test\field.png", "Okat nadfljl")
    # print(secret)
    # secret.save(r"C:\Users\Arnold\Pictures\test\new\sneekyfield.png")
    # print(lsb.reveal(r"C:\Users\Arnold\Pictures\test\new\sneekyfield.png"))


def hide_file():
    global vault
    file_path = input("Enter the file path : ")
    print(file_path)

    encoded_file = get_encoded_file(file_path)
    print(encoded_file)
    #
    k = input("Enter key : ")
    #
    key = get_hashed_text(k)

    vault[key] = encoded_file


def show_data():
    # print("inside show data")
    # print(lsb.reveal("hidden.jpg"))
    # print(4)
    global vault

    if len(vault) > 0:
        print("the vault has some objects...saved automatically")
        save_image()



    # # Extract the hidden file in the image
    # os.system('tar -xvf hidden_img.png')
    #
    # with open('data.json', 'r') as f:
    #     vault_str = f.read()


    vault_str = lsb.reveal(str(img_path))


    vault = json.loads(vault_str)
    print(vault, type(vault))

    k = input("Enter key : ")

    key = get_hashed_text(k)

    if key not in vault:
        print(key)
        print("There is no data stored for that key")
    else:
        print(key)
        # a = str(hash(k))

        key_val = vault[key]

        y = key_val.split("###")
        file_name = y[0]
        cipher = y[1]

        if file_name == "plaintext":
            secret = crypto.decrypt_text(key=k, ciphertext=cipher)
            print(secret)

        else:
            # Decode the Base64 string into image data
            file_data = base64.b64decode(cipher)

            # Save the image data to a file
            with open(f'extracted{file_name}', 'wb') as f:
                f.write(file_data)


def show_vault():
    global vault
    global img_path
    vault_str = lsb.reveal(img_path)

    vault = json.loads(vault_str)
    print(vault, type(vault))



operations = {
    "1": open_image,
    "2": save_image,
    "3": hide_text,
    "4": hide_file,
    "5": show_data,
    "6": show_vault,
}



again = True

while again:
    print("""
    ----------------------------
        Menu
        ````
    1. Open image
    2. Save image
    3. Hide text
    4. Hide file
    5. Show data
    6. Show vault
    """)
    try:
        choice = input("Enter your choice : ")
        operations[choice]()
        print('\n')
    except KeyError:
        ask_again = True
        while ask_again:
            choice = input("Please enter one of the provided choices : ")
            try:
                operations[choice]()
            except KeyError:
                pass
            else:
                ask_again = False
    else:
        ans = input(f"Do you want to continue? : ")
        if ans not in ['yes', 'y', 'ok', 'okay']:
            again = False

