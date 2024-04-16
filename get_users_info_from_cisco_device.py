import os
from colorama import Fore
from datetime import datetime
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

def str_date_time():
    now = datetime.now()
    str_date = now.strftime("%Y%m%d")
    str_time = now.strftime("%H%M%S")
    return "_" + str_date + "_" + str_time

if not os.path.exists("configs"):
    os.mkdir("configs")
if not os.path.exists("configs\\device_ip.txt"):
    file = open("configs\\device_ip.txt", 'a')
    print (Fore.RED + "Please add IP Addresses to configs\\device_ip.txt" + Fore.WHITE)
    file.close()
    exit()
    
with open ("configs\\device_ip.txt",'r') as f:
    devices_list = f.read().splitlines()
    f.close()
for ip_address in devices_list:
    Switch = { 
            "hostname": ip_address,
            "username": "username",
            "password": "password",
            "optional_args": {"secret": "password"} 
            }
   
    try:
        print(Fore.WHITE + f"{'=' * 50}\nConnecting to the Device {Switch['hostname']}")
        driver = get_network_driver('ios')
        Device = driver(**Switch)
        Device.open()
    except (ConnectionException):
        print(Fore.RED + f"Connecting Failed on {Switch['hostname']}" + Fore.WHITE)
    except (NetmikoAuthenticationException):
        print(Fore.RED + f"Authentication failed. {Switch['hostname']}" + Fore.WHITE)
    except:
        print(Fore.RED + f"Unknown Err!. {Switch['hostname']}" + Fore.WHITE)
    else:
        # Make output file
        output_file_name = "configs\\device_users.csv"
        with open ( output_file_name, 'a') as f:
            print (Fore.GREEN + "Connected....")
            users_dict = Device.get_users()
            for user in users_dict:
                # Add 1 line in file with comma seprator for each cisco device
                print (Switch['hostname']+ "," + user +  "," + str(users_dict[user]["level"]) + "," + users_dict[user]["password"],file=f )
            print(Fore.GREEN + "Pass...." + Fore.WHITE)
            f.close()
            Device.close()