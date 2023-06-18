import json

import customtkinter as ctk
import tkinter
from PIL import Image, ImageTk
import backend as bnd
from tkinter import messagebox
import os

# Get the username of the current user
username = os.getlogin()

# Replace "Arnold" with the obtained username
INITIAL_DIRECTORY = f"C:/Users/{username}/Pictures"



root = ctk.CTk()
ctk.set_appearance_mode("dark")
# root.title("ENIGMA")
root.title("HushHider")
root.resizable(False, False)
root.after(201, lambda :root.iconbitmap("invisible-man.ico"))


received_secret_data = {"status": False}

is_image_open = False

max_size_able_to_hide_in_bytes = 0
data_size_in_bytes = 0

x_res: int
y_res: int

max_size_able_to_hide: str
data_size: str



def show_image_data_on_textbox():
    image_file_size = os.stat(str(bnd.img_path)).st_size
    if image_file_size < 1024:
        image_file_size = str(round(image_file_size, 2)) + " B"

    elif image_file_size / 1024 < 1024:
        image_file_size = str(round(image_file_size / 1024, 2)) + " KB"

    else:
        image_file_size = str(round(image_file_size / 1024 / 1024, 2)) + " MB"

    vault_size = len(json.dumps(bnd.vault).encode('utf-8')) - 2
    if vault_size < 1024:
        vault_size = str(round(vault_size, 2)) + " B"
    elif vault_size / 1024 < 1024:
        vault_size = str(round(vault_size / 1024, 2)) + " KB"
    else:
        vault_size = str(round(vault_size / 1024 / 1024, 2)) + " MB"

    hidden_data_textbox_showtab.configure(state="normal")
    hidden_data_textbox_showtab.delete("0.0", "end")
    hidden_data_textbox_showtab.insert("0.0", f'''
Image Detail :
--------------------------------
Image resolution: {x_res} x {y_res}

Path : {bnd.img_path}

Image size : {image_file_size}

Maximum storage size of the image : {max_size_able_to_hide}

Size of data stored in the image  : {vault_size}
''')
    hidden_data_textbox_showtab.configure(state="disabled")


def openImage():
    global x_res, y_res
    global is_image_open
    global max_size_able_to_hide_in_bytes
    global data_size_in_bytes
    global max_size_able_to_hide
    global data_size
    filepath = tkinter.filedialog.askopenfilename(initialdir=INITIAL_DIRECTORY, title="Select a File", filetypes=[('*.png', '*.png')])

    if filepath:
        # filename, file_ext = os.path.splitext(filepath)
        # Replace forward slash of filepath with backward slash for proper image saving
        filepath = filepath.replace("/", "\\")
        image = Image.open(filepath)
        # # Convert non png image file to png
        # if file_ext != '.png':
        #     image.save(fr'{filename}.png')
        #     bnd.img_path = fr'{filename}.png'
        # else:
        #     bnd.img_path = filepath
        bnd.img_path = filepath
        print(bnd.img_path)

        image = image.resize((800, 600))

        # Load an image in the script
        one = ImageTk.PhotoImage(image=image)
        root.one = one

        # Add image to the Canvas Items
        canvas.create_image(0, 0, anchor="nw", image=one)

        max_size_able_to_hide_in_bytes, data_size_in_bytes, max_size_able_to_hide, data_size, x_res, y_res = bnd.load_vault_from_img()
        show_image_data_on_textbox()

        is_image_open = True


def on_click_save_image():
    bnd.save_image()
    show_image_data_on_textbox()
    messagebox.showinfo(title="Success", message="You have successfully saved the data to a file")


def on_click_show_data():
    global received_secret_data
    global is_image_open
    if not is_image_open:
        messagebox.showerror(title="Oh oh.. ☹ ", message="You need to first open the image file")
        return
    key = key_entry.get()
    result = bnd.show_data(k=key)

    hidden_data_textbox_showtab.configure(state="normal")
    hidden_data_textbox_showtab.delete("0.0", "end")
    if result["type"] == "plaintext":
        received_secret_data["status"] = True
        received_secret_data["type"] = "plaintext"
        received_secret_data["content"] = result["result"]
        hidden_data_textbox_showtab.insert("0.0", result["result"])
    elif result["type"] == "file":
        received_secret_data["status"] = True
        received_secret_data["type"] = "file"
        received_secret_data["filename"] = result["filename"]
        received_secret_data["content"] = result["filedata"]
        hidden_data_textbox_showtab.insert("0.0",
f'''
Stored File Detail :
--------------------------------
filename : {result["filename"]}
''')
        # hidden_data_textbox_showtab.insert("0.0",
        #                                    f'''
        # Stored File Detail :
        # -------------------
        # filename : {result["filename"]}
        # filesize : {result["filesize"]} MB''')


    else:
        hidden_data_textbox_showtab.insert("0.0", result["result"])
    hidden_data_textbox_showtab.configure(state="disabled")


def on_click_show_data_tab_clear():
    received_secret_data["status"] = False
    key_entry.delete(0, "end")
    hidden_data_textbox_showtab.configure(state="normal")
    hidden_data_textbox_showtab.delete("0.0", "end")
    hidden_data_textbox_showtab.insert("0.0", "Hidden data will be displayed here")
    hidden_data_textbox_showtab.configure(state="disabled")

    # msg = hidden_data_textbox_showtab.get("0.0", "end")
    # if msg[:len(msg)-1] == "Hidden data will be displayed here":
    #     pass
    # else:
    #     hidden_data_textbox_showtab.configure(state="normal")
    #     hidden_data_textbox_showtab.delete("0.0", "end")
    #     hidden_data_textbox_showtab.configure(state="disabled")


def on_click_save_as_file():
    global received_secret_data
    if received_secret_data["status"] == False:
        messagebox.showerror(title="Oh oh.. ☹️", message="You need to first get some data to able to store it")

    else:
        print("here")
        if received_secret_data["type"] == "file":
            print("received file type")
            file_name = received_secret_data["filename"]
            file_type = received_secret_data["filename"].split(".")[-1]
            print(file_type)
            filepath = tkinter.filedialog.asksaveasfilename(initialdir=INITIAL_DIRECTORY,
                                                            title="Select File Storage Path",
                                                            initialfile=file_name,
                                                            filetypes=[(file_type, file_type)],
                                                            defaultextension=file_type)
            # filepath = tkinter.filedialog.asksaveasfilename(initialdir=INITIAL_DIRECTORY, title="Select File Storage Path", initialfile=file_name, defaultextension=".txt")
            # print(filepath, type(filepath))
            if filepath:
                # Save the image data to a file
                with open(filepath, 'wb') as f:
                    f.write(received_secret_data["content"])
                messagebox.showinfo(title="Success", message="You have successfully saved the data to a file")
        else:
            filepath = tkinter.filedialog.asksaveasfilename(initialdir=INITIAL_DIRECTORY,
                                                            title="Select File Storage Path",
                                                            initialfile="secret",
                                                            filetypes=[(".txt", ".txt")],
                                                            defaultextension=".txt")
            if filepath:
                # Save the image data to a file
                with open(filepath, 'w') as f:
                    f.write(received_secret_data["content"])
                messagebox.showinfo(title="Success", message="You have successfully saved the data to a file")


# Left Section
left_frame = ctk.CTkFrame(root)
left_frame.pack(side="left", padx=10, pady=10, fill="both")

canvas = tkinter.Canvas(left_frame, width=800, height=600,)
canvas.grid(row=0, column=0, columnspan=2, pady=5)

open_image_btn = ctk.CTkButton(left_frame, text="Open Image", command=openImage)
open_image_btn.grid(row=1, column=0, padx=10, pady=10)

save_image_btn = ctk.CTkButton(left_frame, text="Save Image", command=on_click_save_image)
save_image_btn.grid(row=1, column=1, padx=10, pady=10)


# Right Side

# Creating tab section
tabsection = ctk.CTkTabview(root)
tabsection.pack(side="left", padx=10, pady=10, expand=True, fill="both")


show_data_tab = tabsection.add("🔓  Show Data")
hide_data_tab = tabsection.add("🔒  Hide Data")
tabsection.set("🔓  Show Data")

# Show data section
key_entry = ctk.CTkEntry(show_data_tab, placeholder_text="Enter Key", width=250, show="*")
key_entry.grid(row=0, column=0, padx=10, pady=20)
key_submit_button = ctk.CTkButton(show_data_tab, text="Show Data", width=30, command=on_click_show_data)
key_submit_button.grid(row=0, column=1, padx=10, pady=20)


hidden_data_textbox_showtab = ctk.CTkTextbox(show_data_tab, border_width=3, border_color="lightblue", border_spacing=10,
                                     fg_color="transparent", height=360, width=350)
hidden_data_textbox_showtab.grid(row=1, column=0, columnspan=2, sticky="we", padx=10, pady=10)
hidden_data_textbox_showtab.insert("0.0", "Hidden data will be displayed here")
hidden_data_textbox_showtab.configure(state="disabled")


show_data_bottom_frame = ctk.CTkFrame(show_data_tab, fg_color="transparent")
show_data_bottom_frame.grid(row=2, column=0, columnspan=2)

save_as_file_btn = ctk.CTkButton(show_data_bottom_frame, text="Save As File", width=100, command=on_click_save_as_file)
save_as_file_btn.grid(row=2, column=0, padx=20, pady=5)
clear_btn_showtab = ctk.CTkButton(show_data_bottom_frame, text="Clear", width=100, command=on_click_show_data_tab_clear)
clear_btn_showtab.grid(row=2, column=1, padx=20, pady=5)

FILE_TYPE = "Plaintext"

secret_filepath = ""


# ---------------------------------------------------------------------------------------------------------------------
# Hide Section Operations

def get_remaining_img_capacity():
    # Convert the dictionary to JSON
    json_data = json.dumps(bnd.vault)

    # Calculate the size of 'vault' in bytes
    size_of_vault = len(json_data.encode('utf-8'))
    capacity_in_bytes = max_size_able_to_hide_in_bytes - size_of_vault
    if capacity_in_bytes < 1024:
        return f"{round(capacity_in_bytes,2)} B"
    elif capacity_in_bytes / 1024 < 1024:
        return f"{round(capacity_in_bytes / 1024, 2)} KB"
    else:
        return f"{round(capacity_in_bytes / 1024 / 1024, 2)} MB"

def check_if_data_will_fit(data):
    # Convert the dictionary to JSON
    json_data = json.dumps(bnd.vault)

    # Calculate the size of 'vault' in bytes
    size_of_vault = len(json_data.encode('utf-8'))
    print("Checking if data can fit in the vault")
    print(len(data) + size_of_vault)
    if len(data) + size_of_vault > max_size_able_to_hide_in_bytes:
        return False
    else:
        return True

def onclick_hide_data_btn():
    global is_image_open
    global secret_filepath
    key1 = enter_key_entry_hidetab.get()
    key2 = confirm_key_entry_hidetab.get()
    if not is_image_open:
        messagebox.showerror(title="Oh oh.. ☹ ", message="You need to first open the image file")
        return

    if len(key1) == 0 and len(key2) == 0:
        messagebox.showerror(title="Oh oh.. ☹ ", message="You need to enter the key to hide")
        return
    if key1 != key2:
        messagebox.showerror(title="Oh oh.. ☹️", message="The keys you have entered is not matching")
    else:
        if FILE_TYPE == "Plaintext":
            secret_txt = hide_data_textbox_hidetab.get("0.0", "end")
            if len(secret_txt) == 1:
                sure_to_proceed = messagebox.askokcancel(title="Are you sure ?", message="There is no data given to hide in the textbox. This could  erase any previous data stored for this key")
                if sure_to_proceed:
                    confirm_hide = bnd.hide_text(secret_txt, key1, "pop")
                    if confirm_hide["Status"]:
                        capacity = get_remaining_img_capacity()
                        messagebox.showinfo(title="Successful", message=f"Operation Successful\n "
                                                                        f"Remaining capacity to store data : {capacity}")
                    else:
                        messagebox.showerror(title="Oh oh.. ☹️", message=f"The size required to store this data : {confirm_hide['Size_to_store_msg']}\n"
                                                                         f"But the capacity that is remaining is : {confirm_hide['Remaining_Capacity']}")
            else:
                existing_data = bnd.show_data(k=key1)
                if existing_data["type"] in ["plaintext", "file"]:
                    sure_to_proceed = messagebox.askokcancel(title="Are you sure ?",
                                                             message="There is already some data present for this key. This could replace any previous data stored for this key")
                    if sure_to_proceed:

                        confirm_hide = bnd.hide_text(secret_txt, key1, "hide")
                        if confirm_hide["Status"]:
                            capacity = get_remaining_img_capacity()
                            messagebox.showinfo(title="Successful", message=f"Operation Successful\n "
                                                                            f"Remaining capacity to store data : {capacity}")
                        else:
                            messagebox.showerror(title="Oh oh.. ☹️",
                                                 message=f"The size required to store this data : {confirm_hide['Size_to_store_msg']}\n"
                                                         f"But the capacity that is remaining is : {confirm_hide['Remaining_Capacity']}")
                else:
                    confirm_hide = bnd.hide_text(secret_txt, key1, "hide")
                    if confirm_hide["Status"]:
                        capacity = get_remaining_img_capacity()
                        messagebox.showinfo(title="Successful", message=f"Operation Successful\n "
                                                                        f"Remaining capacity to store data : {capacity}")
                    else:
                        messagebox.showerror(title="Oh oh.. ☹️",
                                             message=f"The size required to store this data : {confirm_hide['Size_to_store_msg']}\n"
                                                     f"But the capacity that is remaining is : {confirm_hide['Remaining_Capacity']}")
        else:
            # if file type is a File
            print(secret_filepath)
            if secret_filepath:
                existing_data = bnd.show_data(k=key1)
                if existing_data["type"] in ["plaintext", "file"]:
                    sure_to_proceed = messagebox.askokcancel(title="Are you sure ?",
                                                             message="There is already some data present for this key. This could replace any previous data stored for this key")
                    if sure_to_proceed:
                        confirm_hide = bnd.hide_file(secret_filepath, key1)
                        if confirm_hide["Status"]:
                            capacity = get_remaining_img_capacity()
                            messagebox.showinfo(title="Successful", message=f"Operation Successful\n "
                                                                            f"Remaining capacity to store data : {capacity}")
                        else:
                            messagebox.showerror(title="Oh oh.. ☹️",
                                                 message=f"The size required to store this data : {confirm_hide['Size_to_store_msg']}\n"
                                                         f"But the capacity that is remaining is : {confirm_hide['Remaining_Capacity']}")
                else:
                    confirm_hide = bnd.hide_file(secret_filepath, key1)
                    if confirm_hide["Status"]:
                        capacity = get_remaining_img_capacity()
                        messagebox.showinfo(title="Successful", message=f"Operation Successful\n "
                                                                        f"Remaining capacity to store data : {capacity}")
                    else:
                        messagebox.showerror(title="Oh oh.. ☹️",
                                             message=f"The size required to store this data : {confirm_hide['Size_to_store_msg']}\n"
                                                     f"But the capacity that is remaining is : {confirm_hide['Remaining_Capacity']}")
            else:
                messagebox.showerror(title="Oh oh.. ☹ ", message="You have not chosen any file to hide")


def on_select_input_type(choice):
    global FILE_TYPE
    if choice == "File":
        browse_file_btn.grid(row=0, column=2, padx=10, pady=20)
        hide_data_textbox_hidetab.delete("0.0", "end")
        hide_data_textbox_hidetab.configure(state="disabled")
        FILE_TYPE = "File"

    else:
        browse_file_btn.grid_forget()
        hide_data_textbox_hidetab.configure(state="normal")
        hide_data_textbox_hidetab.delete("0.0", "end")
        FILE_TYPE = "Plaintext"


def on_click_browse_file_btn():
    global secret_filepath
    hide_data_textbox_hidetab.configure(state="normal")
    hide_data_textbox_hidetab.delete("0.0", "end")
    hide_data_textbox_hidetab.configure(state="disabled")
    secret_filepath = tkinter.filedialog.askopenfilename(initialdir=INITIAL_DIRECTORY, title="Select a File", filetypes=[('Any File', '*.*')])
    if secret_filepath:
        file_stats = os.stat(secret_filepath)
        # File size in MB
        file_size = file_stats.st_size / (1024 * 1024)
        print(file_size)
        if file_size < 0:
            print("ok")
            file_size = file_stats.st_size / 1024
            print(file_size)
        # Rounding file size
        file_size = round(file_size, 2)
        # print(file_size)
        hide_data_textbox_hidetab.configure(state="normal")
        hide_data_textbox_hidetab.insert("0.0", f'''
Filepath of file to hide :
----------------------------------------------
{secret_filepath}

File size : {file_size} MB
        ''')
        hide_data_textbox_hidetab.configure(state="disabled")


def on_click_hide_data_tab_clear():
    global FILE_TYPE
    enter_key_entry_hidetab.delete(0, "end")
    confirm_key_entry_hidetab.delete(0, "end")
    enter_key_entry_hidetab.configure(placeholder_text="Enter Key")
    confirm_key_entry_hidetab.configure(placeholder_text="Confirm Key")

    if FILE_TYPE == "File":
        hide_data_textbox_hidetab.configure(state="normal")
        hide_data_textbox_hidetab.delete("0.0", "end")
        hide_data_textbox_hidetab.configure(state="disabled")
    else:
        hide_data_textbox_hidetab.delete("0.0", "end")


# --------------------------------------------------------------------------------------------------------------------
# Hide Data GUI Section


hide_data_top_frame = ctk.CTkFrame(hide_data_tab, fg_color="transparent")
hide_data_top_frame.grid(row=0, column=0)


input_type_label = ctk.CTkLabel(hide_data_top_frame, text="Input type  : ")
input_type_label.grid(row=0, column=0, padx=10, pady=20, sticky='w')

input_type_menu = ctk.CTkOptionMenu(hide_data_top_frame, width=150, values=["Plaintext", "File"], command=on_select_input_type)
input_type_menu.grid(row=0, column=1, padx=10, pady=20)


browse_file_btn = ctk.CTkButton(hide_data_top_frame,  width=30, text="Open File", command=on_click_browse_file_btn)





hide_data_textbox_hidetab = ctk.CTkTextbox(hide_data_tab, border_width=3, border_color="lightblue", border_spacing=10,
                                     fg_color="transparent", height=280, width=350)
hide_data_textbox_hidetab.grid(row=1, column=0, sticky="ew", padx=10, pady=10)


hide_data_bottom_frame = ctk.CTkFrame(hide_data_tab, fg_color="transparent")
hide_data_bottom_frame.grid(row=2, column=0, pady=5)


enter_key_entry_hidetab = ctk.CTkEntry(hide_data_bottom_frame, placeholder_text="Enter Key", width=255, show="*")
enter_key_entry_hidetab.grid(row=0, column=0, sticky='nswe', padx=10, pady=5)

confirm_key_entry_hidetab = ctk.CTkEntry(hide_data_bottom_frame, placeholder_text="Confirm Key", width=255, show="*")
confirm_key_entry_hidetab.grid(row=1, column=0, sticky='nswe', padx=10, pady=5,)

hide_data_btn = ctk.CTkButton(hide_data_bottom_frame, text="Hide Data", width=30, command=onclick_hide_data_btn)
hide_data_btn.grid(row=0, column=1, rowspan=2, sticky='nswe', padx=10, pady=5)

clear_btn_hidetab = ctk.CTkButton(hide_data_tab, text="Clear All", command=on_click_hide_data_tab_clear)
clear_btn_hidetab.grid(row=3, column=0, sticky='ews', padx=10, pady=5)



def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()