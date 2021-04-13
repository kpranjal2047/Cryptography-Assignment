import string

playfairmap = (24, 23, 22, 21, 20, 15, 10, 5, 0, 1, 2, 3, 4,
			   9, 14, 19, 18, 17, 16, 11, 6, 7, 8, 13, 12)


def playfair(key):
	lst = []
	for char in key:
		if char not in lst:
			lst.append(char)
	key = ''.join(lst)

	mat = []
	for _ in range(5):
		mat.append([0, 0, 0, 0, 0])

	alpha = set(string.ascii_lowercase)
	charset = set(key)
	if 'j' in charset:
		alpha.remove('i')
	else:
		alpha.remove('j')
	alpha = sorted(list(alpha.difference(charset)))
	fill = key + ''.join(alpha)

	for index, val in zip(playfairmap, fill):
		mat[index // 5][index % 5] = val

	return mat


def changematrix(mat, railfencekey):
	mat_str = ''
	for row in mat:
		mat_str += ''.join(row)

	if railfencekey > 1:
		railfencemat = []
		for _ in range(railfencekey):
			railfencemat.append([])

		index = 0
		inc = True

		for char in mat_str:
			railfencemat[index].append(char)
			if inc and index == railfencekey-1:
				inc = False
			elif not inc and index == 0:
				inc = True
			index += (2 * inc - 1)

		mat_str = ''
		for row in railfencemat:
			mat_str += ''.join(row)

	return playfair(mat_str)


def processtext(text, playfairkey):
	if 'j' in playfairkey:
		text = text.replace('i', 'j')
	else:
		text = text.replace('j', 'i')
	if len(text) == 1:
		if text == 'z':
			return 'zy'
		else:
			return text + 'z'
	else:
		lst = list(text)
		i = 1
		while i < len(lst):
			if lst[i] == lst[i-1]:
				if lst[i] == 'z':
					lst.insert(i, 'y')
				else:
					lst.insert(i, 'z')
			i += 1
		text = ''.join(lst)
		if len(text) % 2 == 1:
			text += ('y' if text[-1] == 'z' else 'z')
		return text


def encode(plaintext, cyphermat):
	mat_str = ''
	for row in cyphermat:
		mat_str += ''.join(row)

	cyphertext = ''

	for i in range(0, len(plaintext), 2):
		a, b = plaintext[i:i+2]
		pos_a = mat_str.index(a)
		pos_b = mat_str.index(b)

		r1, c1 = pos_a // 5, pos_a % 5
		r2, c2 = pos_b // 5, pos_b % 5

		if c1 == c2:
			cyphertext += cyphermat[(r1 + 1) % 5][c1] + cyphermat[(r2 + 1) % 5][c2]

		elif r1 == r2:
			cyphertext += cyphermat[r1][(c1 + 1) % 5] + cyphermat[r2][(c2 + 1) % 5]

		else:
			cyphertext += cyphermat[r1][c2] + cyphermat[r2][c1]

	return cyphertext


if __name__ == '__main__':

	testcases = int(input())
	for _ in range(testcases):
		railfencekey = int(input())
		playfairkey = input()
		num_change = int(input())
		plaintext = input()

		cyphermat = playfair(playfairkey)

		for _ in range(num_change):
			cyphermat = changematrix(cyphermat, railfencekey)

		for row in cyphermat:
			print(' '.join(row))

		plaintext = processtext(plaintext, playfairkey)
		print(encode(plaintext, cyphermat))
