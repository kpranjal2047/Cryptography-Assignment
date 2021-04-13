cyphertext = input()
ctlength = len(cyphertext)

ptlength = (ctlength + 1) // 2
pt_hex = [int(char, 16) for char in cyphertext[:ptlength]]
for i in range(ptlength-1, 0, -1):
    pt_hex[i] = pt_hex[i] ^ pt_hex[i-1]

plaintext = ''.join([hex(num)[2] for num in pt_hex])
print(plaintext)
