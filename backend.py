from PIL import Image
import crypto
import json
import os
import zipfile
import hashlib
import base64
from stego_lsb import LSBSteg as lsb

LSB_BITS = 3

img_path = str
vault = {}

hash_obj = hashlib.sha3_224()

data_saved = True

max_size_able_to_hide_in_bytes = 0

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
    global max_size_able_to_hide_in_bytes
    global vault
    vault.clear()

    try:
        # Extract the hidden file in the image
        lsb.recover_data(steg_image_path=str(img_path), output_file_path="data.json", num_lsb=LSB_BITS)
    except ValueError:
        print("No data is hidden in this image")
    else:
        with open('data.json', 'r') as f:
            vault_str = f.read()
        vault = json.loads(vault_str)
    finally:
        max_size_able_to_hide_in_bytes, data_size_in_bytes, maximum_size_to_hide, input_file_size, x_resolution, y_resolution = lsb.analysis(image_file_path=str(img_path), input_file_path="data.json", num_lsb=LSB_BITS)
        os.remove("data.json")
        return max_size_able_to_hide_in_bytes, data_size_in_bytes, maximum_size_to_hide, input_file_size, x_resolution, y_resolution


def save_image():
    global vault
    global data_saved



    # Encode the data as a JSON string
    json_string = json.dumps(vault)

    # print(f"Json_string : {json_string}")

    #Lsb hide method
    # secret = lsb.hide(str(img_path), json_string)
    # secret.save(img_path)

    # Save the JSON string to a file
    with open('data.json', 'w') as f:
        f.write(json_string)
    try:
        filename, file_ext = os.path.splitext(str(img_path))
        # lsb.hide_data(input_image_path=str(img_path), input_file_path="data.json", steg_image_path=f"{filename}_lsb{file_ext}", num_lsb=LSB_BITS, compression_level=9)
        lsb.hide_data(input_image_path=str(img_path), input_file_path="data.json",
                      steg_image_path=str(img_path), num_lsb=LSB_BITS, compression_level=9)
    except OverflowError:
        print("message is too big")
    except ValueError as e:
        print("size of input file demands more space than the capacity able to store")
        print(e)

    os.remove("data.json")

    data_saved = True
    if os.path.exists("data.json"):
        print("file still exit")
    else:
        print("the temporary files are deleted")


def hide_text(secret, key, action):
    global vault
    global data_saved
    try:
        if action == "hide":
            encrypted_data = crypto.encrypt_text(key=key, text=secret)

            text_to_hide = "plaintext###" + encrypted_data
            key = get_hashed_text(key)
            # print("hashed key :", key)
            # print("hashed key length :", len(key))
            # print("Value length :", len(text_to_hide))
            temp_vault = vault.copy()
            temp_vault[key] = text_to_hide

            # Convert the dictionary to JSON
            json_data = json.dumps(temp_vault)

            # Calculate the size of 'vault' in bytes
            size_of_vault = len(json_data.encode('utf-8'))
            if size_of_vault > max_size_able_to_hide_in_bytes:
                rem_cap = max_size_able_to_hide_in_bytes - len(json.dumps(vault).encode('utf-8'))
                if rem_cap < 1024:
                    rem_cap = str(round(rem_cap, 2)) + " B"
                elif rem_cap / 1024 < 1024:
                    rem_cap = str(round(rem_cap / 1024, 2)) + " KB"
                else:
                    rem_cap = str(round(rem_cap / 1024 / 1024, 2)) + " MB"

                size_needed = len(key)+len(text_to_hide)+8
                if size_needed < 1024:
                    size_needed = str(round(size_needed, 2)) + " B"
                elif size_needed / 1024 < 1024:
                    size_needed = str(round(size_needed / 1024, 2)) + " KB"
                else:
                    size_needed = str(round(size_needed / 1024 / 1024, 2)) + " MB"
                return {"Status": False,
                        "Remaining_Capacity": rem_cap,
                        "Size_to_store_msg": size_needed}


            vault[key] = text_to_hide

            data_saved = False
        else:
            key = get_hashed_text(key)
            vault.pop(key)
        return {"Status": True}
    except Exception:
        return {"Status": False}




def hide_file(secret, key):
    global vault
    global data_saved
    file_path = secret
    k = key
    # print("inside bnd hide_file fun")
    # print(file_path)
    try:
        file_name = os.path.basename(file_path)

        encoded_file = get_encoded_file(file_path)

        # encrypted_data = crypto.encrypt_text(key=k, text=encoded_file)

        # encoded_file = file_name + "###" + encrypted_data
        encoded_file = file_name + "###" + encoded_file
        # print(encoded_file)
        # k = input("Enter key : ")
        key = get_hashed_text(k)


        temp_vault = vault.copy()
        temp_vault[key] = encoded_file



        # Convert the dictionary to JSON
        json_data = json.dumps(temp_vault)

        # Calculate the size of 'vault' in bytes
        size_of_vault = len(json_data.encode('utf-8'))
        if size_of_vault > max_size_able_to_hide_in_bytes:

            rem_cap = max_size_able_to_hide_in_bytes - len(json.dumps(vault).encode('utf-8'))
            if rem_cap < 1024:
                rem_cap = str(round(rem_cap, 2)) + " B"
            elif rem_cap / 1024 < 1024:
                rem_cap = str(round(rem_cap / 1024, 2)) + " KB"
            else:
                rem_cap = str(round(rem_cap / 1024 / 1024, 2)) + " MB"
            print("remaining Capacity : ", rem_cap)

            size_needed = len(key) + len(encoded_file) + 8
            if size_needed < 1024:
                size_needed = str(round(size_needed, 2)) + " B"
            elif size_needed / 1024 < 1024:
                size_needed = str(round(size_needed / 1024, 2)) + " KB"
            else:
                size_needed = str(round(size_needed / 1024 / 1024, 2)) + " MB"
            return {"Status": False,
                    "Remaining_Capacity": rem_cap,
                    "Size_to_store_msg": size_needed}


        vault[key] = encoded_file

        data_saved = False
        return {"Status": True}
    except Exception:
        return {"Status": False}


def show_data(k):
    global vault
    global img_path
    global data_saved

    if not data_saved and len(vault)>0:
        print("the vault has some objects...saved automatically")
        save_image()
        data_saved = True

    # k = input("Enter key : ")

    key = get_hashed_text(k)

    if key not in vault:
        print(key)
        return {"type": "no_data",
                "result": "There is no data stored for that key"}
    else:
        print(key)
        # a = str(hash(k))

        key_val = vault[key]

        y = key_val.split("###")
        file_name = y[0]
        cipher = y[1]

        if file_name == "plaintext":
            secret = crypto.decrypt_text(key=k, ciphertext=cipher)
            return {"type": "plaintext",

                    "result": secret}

        else:
            # secret_file_in_base64 = crypto.decrypt_text(key=k, ciphertext=cipher)
            #
            # # Decode the Base64 string into image data
            # file_data = base64.b64decode(secret_file_in_base64)
            # print(type(file_data))
            # print(len(file_data))

            file_data = base64.b64decode(cipher)

            file_size = len(file_data)/1048576

            return {"type": "file",
                    "filename": file_name,
                    "filedata": file_data,
                    "filesize": file_size}

            # # Save the image data to a file
            # with open(f'extracted{file_name}', 'wb') as f:
            #     f.write(file_data)


def show_vault():
    global vault
    global img_path

    print(vault)
    vault_len = len(vault)

    print("################")
    print(vault_len)