from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import hashlib

sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever_socket.bind(('localhost', 12345))
sever_socket.listen(5)

sever_key = RSA.generate(2048)

clients = []

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_text = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv, cipher_text

def decrypt_message(key, encrypt_message):
    iv = encrypt_message[:AES.block_size]
    ciphertext = encrypt_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

def handle_client(client_socket, client_address):
    print(f'Connected to {client_address}')
    client_socket.send(sever_key.publickey().export_key(format='PEM'))
    client_received_key = RSA.import_key(client_socket.recv(2048))
    aes_key = get_random_bytes(16)
    cipher_key = PKCS1_OAEP.new(client_received_key)
    encrypted_aes_key = cipher_key.encrypt(aes_key)
    client_socket.send(encrypted_aes_key)
    clients.append(client_socket, aes_key)
    while True:
        encrypt_message = client_socket.recv(1024)
        decrypt_message = decrypt_message(aes_key, encrypt_message)
        print(f'Received from {client_address}: {decrypt_message}')
        for client, key in clients:
            if client != client_socket:
                encrypted = encrypt_message(key, decrypt_message)
                client.send(encrypted)
            if decrypt_message == 'exit':
                break
    client.remove((client_socket, aes_key))        
    client_socket.close()    
    print(f'Connection closed with {client_address}')
    while True:
        client_socket, client_address = sever_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()            