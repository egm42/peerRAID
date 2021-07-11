import os
from cryptography.fernet import Fernet

CHUNK_SIZE = 1024 * 1024

class file:
    def __init__(self, path, key):
        self.name = os.path.basename(path)
        self.dirname = os.path.dirname(path)
        self.path = path
        self.key = key
        self.chunks = []

class peerRAID:
    def __init__(self, username, key=None):
        self.username = username
        self.files = []
        self.key = key
        print('*****************\nStarting peerRAID\n*****************')

        if (not self.key):
            self.key = Fernet.generate_key()
    
    def getFiles(self):
        return self.files
    
    def addFolder(self, path):
        #TODO: implement ability to a add whole folder
        pass

    def addFile(self, path):
        newFile = file(path, self.key)
        self.files.append(newFile)

        self.encrypt(newFile)

        self.blockify(newFile)

        #TODO: delete temp file after converting chunks

        self.upload(newFile)

        #TODO: delete chunks

    def encrypt(self, file):
        fernet = Fernet(file.key)

        with open(file.path, 'rb') as f:
            original = f.read()

        encrypted = fernet.encrypt(original)

        #TODO: Create unique filename
        filename = 'test.file'
        with open(filename, 'wb') as enc_file:
            enc_file.write(encrypted)
        
        file.enc_file = filename
        

    def decrypt(self, file, dir):
        fernet = Fernet(self.key)

        with open(file.enc_file, 'rb') as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)

        with open(os.path.join(dir, file.name), 'wb') as dec_file:
            dec_file.write(decrypted)


    def blockify(self, file):
        i = 1
        with open(file.enc_file, 'rb') as f:
            chunk = f.read(CHUNK_SIZE)
            while chunk:
                #TODO: create unique filename for each chunk, add to DB, save chunk to temp folder
                chunk_name = os.path.basename(file.enc_file) + str(i)
                with open(chunk_name, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                i += 1
                file.chunks.append(chunk_name)
                chunk = f.read(CHUNK_SIZE)

    def upload(self, file):
        #TODO: upload file to remote location
        pass