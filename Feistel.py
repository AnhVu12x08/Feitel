'''
Chương trình mã hóa và giải mã Feistel của nhóm 03
'''
def convert_to_binary(text):
    binary_text = ''  
    for char in text:
        binary_char = format(ord(char), '08b')# Hàm format để chuyển đổi số nguyên thành chuỗi nhị phân, ord() để chuyển đổi ký tự thành số nguyên
        binary_text += binary_char
    return binary_text


def convert_to_text(binary_text):
    text = ''  
    binary_chunks = [binary_text[i:i+8] for i in range(0, len(binary_text), 8)]
    for chunk in binary_chunks:
        char = chr(int(chunk, 2))#Hàm chr() để chuyển đổi số nguyên thành ký tự, int() để chuyển đổi chuỗi nhị phân thành số nguyên
        text += char
    return text


def format_key(key, plaintext):
    '''Cắt đuôi chuỗi Key cho có độ dài bằng L và R'''
    if len(key) > len(plaintext)//2:
        key = key[:len(plaintext)//2] 
    return key


def shift_left(key, rounds):#Hàm dịch Key sang trái 1 đơn vị rồi lưu vào List
    shifted_keys = []  
    shifted_key = key 
    for _ in range(rounds):
        shifted_key = shifted_key[1:] + shifted_key[0]
        shifted_keys.append(shifted_key)
    return shifted_keys


def xor(a, b):
    temp = "" 
    for i in range(len(a)):
        if (a[i] == b[i]):
            temp += "0"    
        else: 
            temp += "1"   
    return temp


def feistel(plaintext, key, rounds):
    L = plaintext[:len(plaintext)//2]
    R = plaintext[len(plaintext)//2:]  
    K = shift_left(key, rounds)
    L_new = ''
    R_new = ''
    
    for i in range(rounds):
        L_new = R
        f = xor(R, K[i])
        R_new = xor(f, L)
        L = L_new
        R = R_new
    return R + L


def decrypt_feistel(ciphertext, key, rounds):
    L = ciphertext[:len(ciphertext)//2]
    R = ciphertext[len(ciphertext)//2:]
    
    K = shift_left(key, rounds)
    L_new = ''
    R_new = ''
    
    for i in range(rounds):
        L_new = R
        f = xor(R, K[rounds - i - 1]) #Lấy Key từ cuối về đầu để giải mã
        R_new = xor(f, L)#Lấy R từ bước trước để giải mã
        L = L_new
        R = R_new
    return R + L




def main():
    while True: 
        print('----------------THUẬT TOÁN MÃ HÓA FEISTEL----------------')
        while True:
            print('Vui lòng chọn chức năng:')
            print("---Mã hóa: e \n---Giải mã: d ")
            choice = input().lower()
            if choice == 'e' or choice == 'd':
                break
            else:
                print("Lựa chọn không hợp lệ. Chọn 'e' để Mã hóa hoặc 'd' để Giải mã.")

        if choice == 'e':
            print('----------------')
            plain_text = input("Nhập vào PlainText: ")
            while True:
                key = input("Nhập Key: ")

                if len(plain_text) % 2 == 0:
                    if len(key) >= (len(plain_text) // 2):
                        break
                    else:
                        print("Độ dài Key phải bằng hoặc lớn hơn một nửa độ dài của PlainText. Vui lòng nhập lại.")

                else:
                    if len(key) >= ((len(plain_text) + 1) // 2):
                        break
                    else:
                        print("Độ dài Key phải bằng hoặc lớn hơn một nửa độ dài của PlainText. Vui lòng nhập lại.")

            rounds = int(input("Nhập vào số vòng: "))

            binary_plain_text = convert_to_binary(plain_text)
            binary_key = convert_to_binary(key)
            fk = format_key(binary_key, binary_plain_text) #Chuẩn hóa Key trước khi đưa vào hàm mã hóa

            ciphertext = feistel(binary_plain_text, fk, rounds)
            print('----------------')
            print('Plain text:', plain_text)
            print('Plain text in binary:', binary_plain_text)
            print('Key:', key)
            print('Key in binary:', fk)
            print('Cipher text in binary:', ciphertext)
            print('Ciphertext:', convert_to_text(ciphertext))
            
        if choice == 'd':
            print('----------------')
            cipher_text = input("Nhập vào CipherText: ")
            while True:
                key = input("Nhập Key: ")

                if len(cipher_text) % 2 == 0:
                    if len(key) >= (len(cipher_text) // 2):
                        break
                    else:
                        print("Độ dài Key phải bằng hoặc lớn hơn một nửa độ dài của CipherText. Vui lòng nhập lại.")
                else:
                    if len(key) >= ((len(cipher_text) + 1) // 2):
                        break
                    else:
                        print("Độ dài Key phải bằng hoặc lớn hơn một nửa độ dài của CipherText. Vui lòng nhập lại.")
            rounds = int(input("Nhập vào số vòng: "))

            binary_cipher_text = convert_to_binary(cipher_text)
            binary_key = convert_to_binary(key)
            fk = format_key(binary_key, binary_cipher_text) #Chuẩn hóa Key trước khi đưa vào hàm giải mã

            plaintext = decrypt_feistel(binary_cipher_text, fk, rounds)
            print("----------------")
            print('Cipher text:', cipher_text)
            print('Cipher text in binary:', binary_cipher_text)
            print('Key:', key)
            print('Key in binary:', fk)
            print('Plaintext in binary', plaintext)
            print('Plaintext:', convert_to_text(plaintext))

if __name__ == '__main__':
    main()

