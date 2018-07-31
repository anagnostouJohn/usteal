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

    #path = str(Path.home())+"/crypt" 
    #file_path = str(Path.home())+"/crypt/key.txt" 
    if path == None:
        return
    else:
        if not os.path.exists(path):
            print ("Path "+path+" does not excists")
            sys.exit()
        else:
            if os.path.isfile(path):
                return True
            else:
                return False
            
def validate_user(password,  key_path):
    key = hashlib.sha256(password.encode('utf-8')).digest()
    encryptor = cr_encr(key)
    file=open(key_path, "rb")
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
    if os.path.isfile(inp):
        f_inp = inp.rsplit('/', 1)[1]
        print(f_inp, "AAAAAAAAAAAAAAAAA")
        counter = 0
        encryptor = cr_encr(x)
        name = f_inp.split("___")[0]
        f_path = out+"/"+name
        print("XXXXX>>>", f_path)
        if os.path.exists(f_path):            
            f_path = out+f"/{counter}"+name
            counter+=1
        e_file = open(inp,  "rb")
        e_bytes = e_file.read()
        e_file.close()
        d_bytes = encryptor.decrypt(e_bytes)
        s_file = open(f_path,  "wb")
        s_file.write(d_bytes)
        s_file.close()
        del encryptor  
        
    elif os.path.isdir(inp):
        counter = 0
        print(inp)
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

            
def main(out, f_p,  x):
    if out is None:      
        out_path = str(Path.home())+"/Desktop/"+str(dt.year)+"_"+str(dt.month)+"_"+str(dt.day)+"_"+str(dt.hour)+"_"+str(dt.minute)+"_"+str(dt.second)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
    else:
        if not os.path.exists(out):
            out_path = str(Path.home())+"/Desktop/"+str(dt.year)+"_"+str(dt.month)+"_"+str(dt.day)+"_"+str(dt.hour)+"_"+str(dt.minute)+"_"+str(dt.second)
            if not os.path.exists(out_path):
                os.makedirs(out_path)

        else:
            out_path = out
    udab(f_p,  out_path, x)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decrypt Encrypted Files from usteal')
    parser.add_argument("-p", "--path",  default=None, help="Give path of location")
    parser.add_argument("-k", "--key",  default=None, help="Give Stored File of the Encryption Key")
    parser.add_argument("-f", "--file",  default=None, help="Give Single File location ")
    parser.add_argument("-o", "--out",  default=None, help="Give Output Results")
    args = parser.parse_args()
    #print(args)
    if os.getuid() != 0:
        print("You must run the script under root Privileges")
        sys.exit()    
    if args.key is not None:
        is_path = val_path(args.key)
        if is_path == None:
            print ("Wrong Key Path")
            sys.exit()
    if args.path is not None and args.file is not None:        
        print("Please provide either path or individual File, Both given")
        time.sleep(1)
        sys.exit()
    elif args.path is None and args.file is None:
        print("Please provide either path or individual File, None Given")
        time.sleep(1)
        sys.exit()
    elif args.path is None and args.file is not None and args.key is None:
        print("HI")
        new_key = args.file.rsplit('/', 1)[0]
        args.key = new_key+"/key.txt"
    elif args.path is not None and args.file is None and args.key is None:
        print (args.path)
        args.key =  args.path+"/key.txt"
    
    
    try:
        is_path = val_path(args.key)
        if is_path is None:
            print ("NO Crypto Key Path")
            sys.exit()
        else:
            passw = getpass.getpass("Insert Password to unlock Key : ")
            x = validate_user(passw,  args.key)
    except Exception as err:
        print(err)
    
    try:
        if args.path is None and args.file is not None:
            is_path = val_path(args.file)
            f_p = args.file
        elif args.path is not None and args.file is None:
            is_path = val_path(args.path)
            f_p = args.path
    except Exception as err:
        print(err)
        
    main(args.out, f_p ,  x)
#    
#    print (is_path, is_path1, is_path2)
    #print (is_path, is_path1)
    #x = validate_user(passw,  args.key)
    
    
    
    
    
    
    
    
#    if args.key == None:
#        try:
#            print(new_key)
#            is_path = val_path(new_key)
#            if is_path == True:
#                
#                main(args,  x)
#            else:
#                print("No Crypto Key")
#        except Exception as err:
#            print(err)
#    elif args.key is not None:
#        try:
#            print("XXXXX", args.key)
#            is_path = val_path(args)
#
#            if is_path == True:
#               
#                main(args,  x)
#            else:
#                print("No Proper Key Path given")                
#        except Exception as err:
#            print(err)
            
        
            
    
