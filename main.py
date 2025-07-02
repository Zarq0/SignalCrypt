import os
import shutil
import subprocess
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type
import secrets
import getpass
import psutil
import sys

def checkForSignal():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == "Signal.exe":
            return True
    return False

def cls():
    os.system('cls')

def title(title):
    title = title.replace("|", "^|")  # Escape the | character so Windows doesn't treat it as a pipe
    os.system(f"title {title}")

def close():
    os.system('pause')
    sys.exit()

def init():
    if os.name == 'nt':
        title('SignalCrypt')
        cls()
    else:
        print("This tool is currently not compatible with Unix based systems. Feel free to contribute to change that at https://github.com/Zarq0/SignalCrypt")
        sys.exit()

init()
agreement = input("This tool will encrypt all of your Signal Desktop user data.\n"
                  "It CANNOT be recovered if you forget the password used to encrypt the Signal Desktop user data, "
                  "you will have to login to Signal Desktop again in order to recover it.\n"
                  "Type 'I understand' if you understand the risk: "
)

if agreement == "I understand":
    cls()
    
    try:
        subprocess.run(["7z"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: 7z executable not found. This tool requires it to run properly. Please install 7-Zip and ensure it is added to your PATH.")
        close()
    
    print("1. Encryption")
    print("2. Decryption")

    mode = input("Please select the mode (1 or 2): ")
    home_dir = os.path.expanduser("~")
    
    if mode:
        if mode == '1':
            title("SignalCrypt | Encryption Mode")
            
            if checkForSignal():
                try:
                    print("Running Signal Desktop instance detected. Attempting to terminate...\n")
                    os.system('taskkill /f /IM Signal.exe')
                except Exception as e:
                    print(f"\nUnable to terminate Signal Desktop instance: {e}")
                    print("Please fully exit your running Signal Desktop instance before continuing.")
                    os.system('pause')
                
            
            pswrd = getpass.getpass("\nPlease enter the password you want to use to encrypt Signal data: ")
            print("Encrypting Signal Desktop user data. Please wait...")
            
            signal_data = os.path.join(home_dir, "AppData", "Roaming", "Signal")
            archive_file = "signal.7z"
            password = pswrd.encode()
            salt = secrets.token_bytes(16)
            
            compress_command = ["7z", "a", "-t7z", archive_file, signal_data, "-mx=9"]
            result = subprocess.run(compress_command, capture_output=True)
            if result.returncode != 0:
                print("7-Zip compression failed: ")
                print(result.stderr.decode())
                close()

            shutil.rmtree(signal_data)
            
            key = hash_secret_raw(
                secret=password,
                salt=salt,
                time_cost=4,
                memory_cost=102400,
                parallelism=8,
                hash_len=32,
                type=Type.ID,
            )

            with open(archive_file, "rb") as f:
                data = f.read()

            aesgcm = AESGCM(key)
            nonce = secrets.token_bytes(12)
            encrypted_data = aesgcm.encrypt(nonce, data, None)

            with open("signal.7z.enc", "wb") as f:
                f.write(salt + nonce + encrypted_data)

            os.remove(archive_file)
            
            print("Signal data encryption completed.")
            close()
        elif mode == '2':
            title("SignalCrypt | Decryption Mode")
            
            if checkForSignal():
                try:
                    print("Running Signal Desktop instance detected. Attempting to terminate...\n")
                    os.system('taskkill /f /IM Signal.exe')
                except Exception as e:
                    print(f"\nUnable to terminate Signal Desktop instance: {e}")
                    print("Please fully exit your running Signal Desktop instance before continuing.")
                    os.system('pause')
                    
            pswrd = getpass.getpass("\nPlease enter the password you used to encrypt Signal data: ")
            
            print("Decrypting Signal Desktop user data. Please wait...")
            password = pswrd.encode()
            
            encrypted_path = "signal.7z.enc"
            output_7z_path = "signal.7z"
            extract_dir = os.path.join(home_dir, "AppData", "Roaming")

            if os.path.exists(encrypted_path):
                with open(encrypted_path, "rb") as f:
                    data = f.read()

                salt = data[:16]
                nonce = data[16:28]
                ciphertext = data[28:]

                key = hash_secret_raw(
                    secret=password,
                    salt=salt,
                    time_cost=4,
                    memory_cost=102400,
                    parallelism=8,
                    hash_len=32,
                    type=Type.ID,
                )

                aesgcm = AESGCM(key)

                try:
                    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
                except Exception as e:
                    print("Data decryption failed. Wrong password given or encrypted data file is corrupted.")
                    close()

                with open(output_7z_path, "wb") as f:
                    f.write(plaintext)

                extract_command = ["7z", "x", output_7z_path, f"-o{extract_dir}", "-y"]
                extract_result = subprocess.run(extract_command, capture_output=True)
                if extract_result.returncode != 0:
                    print("7-Zip extraction failed:")
                    print(extract_result.stderr.decode())
                    close()
                    
                try:
                    os.remove(encrypted_path)
                except Exception as e:
                    print(f"Failed to delete encrypted file: {e}")

                try:
                    os.remove(output_7z_path)
                except Exception as e:
                    print(f"Failed to delete decrypted archive: {e}")
                
                print("Signal Desktop data decryption completed.")
                close()
            else:
                print("Encrypted Signal Desktop data not found. Please run encryption mode first, or check the encrypted data file name.")
                close()
        else:
            print("Invalid mode provided.")
            close()
else:
    print("You did not agree to the terms.")
    close()
