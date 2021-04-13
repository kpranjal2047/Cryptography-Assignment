import numpy as np

cyphertext = input()
encoded_th, encoded_he = input().split()
ctlength = len(cyphertext)

enc_matrix = np.array([[ord(char) - 65 for char in encoded_th],
                       [ord(char) - 65 for char in encoded_he]])
dec_matrix = np.array([[19, 7], [7, 4]])

det_enc_matrix = round(float(np.linalg.det(enc_matrix)))
inv_det = pow(det_enc_matrix, -1, 26)

adj_enc_matrix = np.array(
    [[enc_matrix[1, 1], -enc_matrix[0, 1]], [-enc_matrix[1, 0], enc_matrix[0, 0]]])

dec_key = np.mod(inv_det * (adj_enc_matrix @ dec_matrix), 26)

ct = np.array([ord(char) - 65 for char in cyphertext])
ct_matrix = np.resize(ct, ((ctlength+1)//2, 2))

pt = np.mod(ct_matrix @ dec_key, 26).flatten()
plaintext = ''.join([chr(char + 65) for char in pt[:ctlength]])
print(plaintext)
