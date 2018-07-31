import os
import sys
import time
import shutil
import secrets
import string
import argparse
import datetime
import hashlib
import getpass
import json
import pyudev
import tempfile
import psutil
from pathlib import Path
from Crypto.Cipher import AES


dt = datetime.datetime.now()
IV = 16 * '\x00'
mode = AES.MODE_CFB    
def cr_encr(key):
    return AES.new(key, mode, IV=IV)
    
def calc_size(path):
    total_size = 0
    for path, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return total_size
    
    

def dab(path, key):
    nfap = str(Path.home())+"/crypt/"+str(dt.year)+"_"+str(dt.month)+"_"+str(dt.day)+"_"+str(dt.hour)+"_"+str(dt.minute)+"_"+str(dt.second)
    if not os.path.exists(nfap):
        os.makedirs(nfap) 
    with tempfile.TemporaryDirectory() as tmpdirname:
        fp =[]
        c = 0
        for root,  dirs,  files in os.walk(path):
            try:
                for name in files:
                    fp.append(tempfile.NamedTemporaryFile(dir = tmpdirname,  prefix =name+"___", delete=False )) # suffix="<something>" h kataliksh
                    x = os.path.join(root, name)
                    file = open(x, "rb")
                    z = file.read()
                    fp[c].write(z)
                    fp[c].seek(0)
                    c+=1
            except Exception as err:
                print ("error", err)

        for i in fp:
            try:
                file = open(i.name,  "rb")
                file_bytes = file.read()
                file.close()
                encryptor = cr_encr(key.encode("utf-8")) 
                ciphertext = encryptor.encrypt(file_bytes)        
                fap = nfap+"/"+i.name.rsplit('/')[-1]+".enc"
                encr_file = open(fap, "wb")
                encr_file.write(ciphertext)
                encr_file.close()
            except Exception as err:
                print(err)
            try:
                shutil.copyfile(str(Path.home())+"/crypt/key.txt", nfap+"/key.txt")
            except Exception as err:
                print(err)
                #if err.errno == 28:
                #    print ("NO MORE SPACE")
    sys.exit()
        

def rem_div():
    devs = []
    context = pyudev.Context()
    removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
    for device in removable:
        partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
        for p in psutil.disk_partitions():
            if p.device in partitions:
                devs.append(p.mountpoint)
    return devs

def val_path():
    path = str(Path.home())+"/crypt" 
    file_path = str(Path.home())+"/crypt/key.txt" 
    if not os.path.exists(path):
        print ("Path does not excists mount CryptoFile or Run Cryptmount-setup")
        sys.exit
    else:
        if os.path.isfile(file_path):
            return True
        else:
            return False

def usb_file_passes(args):
    key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
    return key
#    else :        
#        first_pass = getpass.getpass("Insert Password To encrypt USB Files: ")
#        second_pass = getpass.getpass("Confirm Password : ")
#        if first_pass == second_pass:
#            return first_pass
#        else:
#            print("Passwords Does Not Match")
#            usb_file_passes(args)
  
def lock_file_passes():
    first_pass = getpass.getpass("Insert Password To unlock the Key File: ")
    second_pass = getpass.getpass("Confirm Password : ")
    if first_pass == second_pass:
        return first_pass
    else:
        print("Passwords Does Not Match")
        lock_file_passes()

def encrypt_key(password_for_usb_files,password_for_file):
    key = hashlib.sha256(password_for_file.encode('utf-8')).digest() 
    encryptor = cr_encr(key)
    file=open(str(Path.home())+"/crypt/key.txt", "wb")
    m_j =  json.dumps({"usb":password_for_usb_files, "file":password_for_file})
    file.write(encryptor.encrypt(m_j))
    file.close()
    del encryptor

    
def validate_user(password):
    key = hashlib.sha256(password.encode('utf-8')).digest()
    encryptor = cr_encr(key)
    file=open(str(Path.home())+"/crypt/key.txt", "rb")
    try:
        plain = encryptor.decrypt(file.read())
        file.close()
        f_j = json.loads(plain)
        del encryptor
        if f_j["file"] == password:
            return f_j["usb"]
        else:
            return None
    except Exception:
        print("Wrong Pass")
        time.sleep(1)
        sys.exit()
    

def create_pass_pare_keys(args):
    password_for_usb_files = usb_file_passes(args)
    password_for_file = lock_file_passes()
    if password_for_usb_files == password_for_file:
        print("Passwords Must NOT be the Same") 
        create_pass_pare_keys(args)
    else:
        encrypt_key(password_for_usb_files,password_for_file)
        return
    

def main(args, x):
    running_system = sys.platform
    blah="\|/-\|/-"
    counter=0
    while True :
        if running_system == 'linux':        
            devices = rem_div()
            if len(devices) == 0:
                sys.stdout.write(blah[counter])
                sys.stdout.flush()
                sys.stdout.write('\b')
                time.sleep(0.5)
                counter+=1
                if counter == 7:
                    counter =0
                continue
    
            else:
                for d in devices: 
                    if os.path.isdir(d):
                        dab(d, x)
                    else:
                        print("Something Goes Wrong")
        elif running_system == 'windows':
            print("windows")
        else:
            print("NO KNOWN OS")
        time.sleep(0.5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='   ')
    parser.add_argument("-k", "--key",  default=None, help="Generate New Pare of Keys", action="store_true")
    #parser.add_argument("-r", "--rund",  default=None, help="Generate Rundom Encryption Key", action="store_true")
    args = parser.parse_args()
    if os.getuid() != 0:
        print("You must run the script under root Privileges")
        sys.exit() 
    if args.key is True:
        is_ket_file = val_path()       
        if is_ket_file is True:
            inp = str(input("IMPORTANT key file already exists. New keys will overwrite the previous [y/n] :"))
            inp = inp.lower()
            if inp == "yes" or inp == "y":            
                create_pass_pare_keys(args)
            elif inp == "n" or inp == "no":
                print("Abording")
                time.sleep(1)
                sys.exit()
            else:
                print("Invalid Argument")
                time.sleep(1)
                sys.exit()
        else:
            print ("Key file does not Exists ")
            create_pass_pare_keys(args)
        passw = getpass.getpass("Insert Password to unlock Key : ")
        x = validate_user(passw)
        main(args, x)
    elif args.key is None:    
        is_ket_file = val_path()  
        if is_ket_file is False:
            print("Key file does not Exists ")
            create_pass_pare_keys(args) 
        passw = getpass.getpass("Insert Password to unlock Key : ")
        x = validate_user(passw)
        main(args, x)
