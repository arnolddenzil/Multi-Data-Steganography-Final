from PIL import Image
import crypto
import json
import os
import zipfile
import hashlib
import base64


img_path = str
vault = {}

hash_obj = hashlib.sha3_224()

data_saved = True



def get_encoded_file(file_path):

    # Load the image from a file
    with open(file_path, 'rb') as f:
        data = f.read()

    # Encode the file data as a Base64 string
    encoded_file = base64.b64encode(data).decode('utf-8')

    file_name = os.path.basename(file_path)

    return encoded_file


def get_hashed_text(word):
    encoded_str = word.encode()
    obj_sha3 = hashlib.sha3_256(encoded_str)
    return obj_sha3.hexdigest()


def load_vault_from_img():
    global vault

    try:
        # Extract the hidden file in the image
        os.system(f'tar -xvf {img_path}')

        with open('data.json', 'r') as f:
            vault_str = f.read()

        os.remove("data.json")

        # Lsb retrieval
        # vault_str = lsb.reveal(str(img_path))

        vault = json.loads(vault_str)

    except FileNotFoundError:
        print("No data is hidden in this image")


def open_image():
    global img_path
    img_path = input("Enter image path : ")
    image = Image.open(img_path)
    image.show()

    load_vault_from_img()


def save_image():
    global vault
    global data_saved
    print(img_path)
    print(len(vault))


    # Encode the data as a JSON string
    json_string = json.dumps(vault)

    # print(f"Json_string : {json_string}")

    #Lsb hide method
    # secret = lsb.hide(str(img_path), json_string)
    # secret.save(img_path)

    # Save the JSON string to a file
    with open('data.json', 'w') as f:
        f.write(json_string)

    print("data saved to data.json")

    # # Create a new zip file
    # with zipfile.ZipFile('temporary.zip', 'w') as zip:
    #     # Add a file to the zip file
    #     zip.write('data.json')
    #
    # # Hide zip file in an image and save new image
    # os.system(f"copy /b {img_path}+temporary.zip {img_path}")
    #
    # os.remove("data.json")
    # os.remove("temporary.zip")
    #
    # data_saved = True
    # if os.path.exists("data.json") or os.path.exists("temporary.zip"):
    #     print("file still exit")
    # else:
    #     print("the temporary files are deleted")




def hide_text():
    global vault
    global data_saved
    secret = input("Enter the secret to hide : ")
    k = input("Enter secret key : ")
    encrypted_data = crypto.encrypt_text(key=k, text=secret)

    text_to_hide = "plaintext###" + encrypted_data

    key = get_hashed_text(k)
    vault[key] = text_to_hide

    data_saved = False

    print(vault)
    print(len(vault))



def hide_file():
    global vault
    global data_saved
    file_path = input("Enter the file path : ")
    k = input("Enter key : ")
    print(file_path)
    file_name = os.path.basename(file_path)

    encoded_file = get_encoded_file(file_path)

    # encrypted_data = crypto.encrypt_text(key=k, text=encoded_file)

    # encoded_file = file_name + "###" + encrypted_data
    encoded_file = file_name + "###" + encoded_file
    print(encoded_file)
    # k = input("Enter key : ")
    key = get_hashed_text(k)

    vault[key] = encoded_file

    data_saved = False


def show_data():
    global vault
    global img_path
    global data_saved

    if not data_saved and len(vault)>0:
        print("the vault has some objects...saved automatically")
        save_image()
        data_saved = True

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
            # secret_file_in_base64 = crypto.decrypt_text(key=k, ciphertext=cipher)


            # # Decode the Base64 string into image data
            # file_data = base64.b64decode(secret_file_in_base64)
            file_data = base64.b64decode(cipher)

            print(file_data)
            print(type(file_data))
            print(len(file_data))

            print(file_name)
            # Save the image data to a file
            with open(f'extracted{file_name}', 'wb') as f:
                f.write(file_data)


def show_vault():
    global vault
    global img_path

    print(vault)
    vault_len = len(vault)

    print("################")
    print(vault_len)




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
    # else:
    #     ans = input(f"Do you want to continue? : ")
    #     if ans not in ['yes', 'y', 'ok', 'okay']:
    #         again = False

