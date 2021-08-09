import subprocess
import re
import time

# Saving passwords 
wifi_saved_passwords = []

# Running the netsh command 
wifi_profiles = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()

# Getting wifi names 
wifi_names_pattern = re.compile(":\W(.*)\r")
wifi_names = wifi_names_pattern.findall(wifi_profiles)

## Get present status 
present_status_pattern = re.compile("Security key *\W:(.*)\r")
key_content_pattern = re.compile("Key Content *\W:\W(.*)\r")

# For each of the wifi name show profile 
for wifi_ssid in wifi_names:
    ssid_profile = subprocess.run(["netsh", "wlan", "show", "profile", wifi_ssid], capture_output=True).stdout.decode()
    is_present = present_status_pattern.findall(ssid_profile)
    if (len(is_present)):
        # Run key=clear 
        ssid_profile_key_clear = subprocess.run(["netsh", "wlan", "show", "profile", "{0}".format(wifi_ssid), "key=clear"], capture_output=True).stdout.decode()
        key_content = key_content_pattern.findall(ssid_profile_key_clear)
        # Save content
        if(len(key_content)):
            password = key_content[0]
        else: password = "No password"

        this_wifi_data = {
            "ssid": wifi_ssid,
            "password": password
        }
        wifi_saved_passwords.append(this_wifi_data)
        print(this_wifi_data)

# Print all the passwords 
# for item in wifi_saved_passwords:
#     ssid = item["ssid"]
#     password = item["password"] 


#     print("SSID:{0:20s} password:{1:20s}".format(ssid, password))