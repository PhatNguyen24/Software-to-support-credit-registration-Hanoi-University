import tkinter as tk
from tkinter import messagebox
import requests
import xml.etree.ElementTree as ET
import os

def save_config(username, password, id_to_hoc_list):
    root = ET.Element("config")
    ET.SubElement(root, "username").text = username
    ET.SubElement(root, "password").text = password
    ids = ET.SubElement(root, "ids")
    for id_to_hoc in id_to_hoc_list:
        ET.SubElement(ids, "id").text = id_to_hoc
    tree = ET.ElementTree(root)
    with open("config.xml", "wb") as file:
        tree.write(file)

def load_config():
    if not os.path.exists("config.xml"):
        return "", "", []
    tree = ET.parse("config.xml")
    root = tree.getroot()
    username = root.find("username").text
    password = root.find("password").text
    id_to_hoc_list = [id_elem.text for id_elem in root.find("ids")]
    return username, password, id_to_hoc_list

def login(username, password):
    login_payload = {
        'username': username,
        'password': password,
        'grant_type': 'password'
    }
    login_url = 'http://qldt.hanu.vn/api/auth/login'
    login_response = requests.post(login_url, data=login_payload)

    if login_response.status_code == 200:
        print('Đăng nhập thành công!')
        return login_response.json().get('access_token')
    else:
        print('Đăng nhập thất bại!')
        print('Mã lỗi:', login_response.status_code)
        print('Nội dung:', login_response.text)
        return None

def send_request(token, id_to_hoc):
    request_payload = {
        'filter': {
            'id_to_hoc': id_to_hoc,
            'is_checked': True,
            'sv_nganh': 1
        }
    }
    request_url = 'http://qldt.hanu.vn/api/dkmh/w-xulydkmhsinhvien'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(request_url, json=request_payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json().get('data', {})
        is_thanh_cong = response_data.get('is_thanh_cong', False)
        thong_bao_loi = response_data.get('thong_bao_loi', '')
        if is_thanh_cong:
            messagebox.showinfo("Thành công", f"Đăng ký id_to_hoc {id_to_hoc} thành công!")
        else:
            messagebox.showerror("Lỗi", f"Lỗi khi đăng ký id_to_hoc {id_to_hoc}: {thong_bao_loi}")
    else:
        messagebox.showerror("Lỗi", f"Yêu cầu với id_to_hoc {id_to_hoc} thất bại!\nMã lỗi: {response.status_code}\nNội dung: {response.text}")

def main(username, password, id_to_hoc_list):
    token = login(username, password)
    if token:
        for id_to_hoc in id_to_hoc_list:
            send_request(token, id_to_hoc)

def on_submit():
    username = username_entry.get()
    password = password_entry.get()
    id_to_hoc_list = id_to_hoc_text.get("1.0", tk.END).strip().split("\n")
    save_config(username, password, id_to_hoc_list)
    main(username, password, id_to_hoc_list)

# Load previous config
saved_username, saved_password, saved_id_to_hoc_list = load_config()

# Create the main window
root = tk.Tk()
root.title("Đăng ký môn học")

# Username label and entry
tk.Label(root, text="Username:").grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=5, pady=5)
username_entry.insert(0, saved_username)

# Password label and entry
tk.Label(root, text="Password:").grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)
password_entry.insert(0, saved_password)

# id_to_hoc label and text box
tk.Label(root, text="ID to Học (mỗi dòng một ID):").grid(row=2, column=0, padx=5, pady=5)
id_to_hoc_text = tk.Text(root, height=10, width=30)
id_to_hoc_text.grid(row=2, column=1, padx=5, pady=5)
id_to_hoc_text.insert(tk.END, "\n".join(saved_id_to_hoc_list))

# Submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=3, column=1, padx=5, pady=5)

# Run the application
root.mainloop()
