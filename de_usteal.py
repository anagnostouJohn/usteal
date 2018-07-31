from pathlib import Path
import argparse
import getpass
import os
import sys
import hashlib
import json
import time
import datetime
from Crypto.Cipher import AES

dt = datetime.datetime.now()
IV = 16 * '\x00'
mode = AES.MODE_CFB    

def cr_encr(key):
    return AES.new(key, mode, IV=IV)

def val_path(path):
    path = str(Path.home())+"/crypt" 
    file_path = str(Path.home())+"/crypt/key.txt" 
    if not os.path.exists(path):
        print ("Path does not excists Key Missing")
        sys.exit
    else:
        if os.path.isfile(file_path):
            return True
        else:
            return False
            
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
            
def udab(inp,  out,  x):
    counter = 0
    for path, dirs, files in os.walk(inp):
        for file in files:
            fp = os.path.join(path, file)
            if file == "key.txt":
                continue
            else:
                encryptor = cr_encr(x)
                name = file.split("___")[0]
                f_path = out+"/"+name
                if os.path.exists(f_path):
                    f_path = out+f"/{counter}"+name
                    counter+=1
                e_file = open(fp,  "rb")
                e_bytes = e_file.read()
                e_file.close()
                d_bytes = encryptor.decrypt(e_bytes)
                s_file = open(f_path,  "wb")
                s_file.write(d_bytes)
                s_file.close()
                del encryptor            
    print(f"All files Decrypted located in {out}") 

            
def main(args, x):
    if args.out is None:      
        out_path = str(Path.home())+"/Desktop/"+str(dt.year)+"_"+str(dt.month)+"_"+str(dt.day)+"_"+str(dt.hour)+"_"+str(dt.minute)+"_"+str(dt.second)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
    else:
        if not os.path.exists(args.out):
            out_path = str(Path.home())+"/Desktop/"+str(dt.year)+"_"+str(dt.month)+"_"+str(dt.day)+"_"+str(dt.hour)+"_"+str(dt.minute)+"_"+str(dt.second)
            if not os.path.exists(out_path):
                os.makedirs(out_path)

        else:
            out_path = args.out
    udab(args.path,  out_path, x)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decrypt Encrypted Files from usteal')
    parser.add_argument("-p", "--path",  default=None, help="Give path of location",  required = True)
    parser.add_argument("-k", "--key",  default=None, help="Give Stored File of the Encryption Key")
    parser.add_argument("-f", "--file",  default=None, help="Give Single File location ")
    parser.add_argument("-o", "--out",  default=None, help="Give Output Results")
    args = parser.parse_args()
    if os.getuid() != 0:
        print("You must run the script under root Privileges")
        sys.exit()     
    if args.path is not None and args.file is not None:        
        print("Please provide either path or individual File")
        time.sleep(1)
        sys.exit()
    passw = getpass.getpass("Insert Password to unlock Key : ")
    if args.key == None:
        try:
            key_path = args.path+"/key.txt"
            is_path = val_path(key_path)
            if is_path == True:
                x = validate_user(passw)
                main(args,  x)
            else:
                print("No Crypto Key")
        except Exception as err:
            print(err)
    elif args.key is not None:
        try:
            is_path = val_path(args.key)
            if is_path == True:
                x = validate_user(passw)
                main(args,  x)
            else:
                print("No Proper Key Path given")                
        except Exception as err:
            print(err)
            
        
            
    
