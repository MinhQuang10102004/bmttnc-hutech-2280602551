import hashlib
def calculate_sha256_hash(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()
data_to_hash = input("Nhập dữ liệu để hash bằng SHA-256: ")
sha256_hash = calculate_sha256_hash(data_to_hash)
print("Giá trị hash SHA-256:", sha256_hash)