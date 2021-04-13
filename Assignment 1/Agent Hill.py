import numpy as np

keytext = input()
plaintext = input()

key = np.array([ord(char) - 97 for char in keytext]).reshape(3, 3)
pt = np.array([ord(char) - 97 for char in plaintext])

ct = np.mod(np.matmul(key, pt.T), 26)
cyphertext = ''.join([chr(char + 97) for char in ct])
print(cyphertext)
