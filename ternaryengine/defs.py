trit_chars = 'nzp'
tredecimal = '0123456789abcd'
trits_per_tryte = 9

tN = trit_chars[0]
tZ = trit_chars[1]
tP = trit_chars[2]

decimal_index = [
    tZ,
    tP,
    tP+tN,
    tP+tZ,
    tP+tP,
    tP+tN+tN,
    tP+tN+tZ,
    tP+tN+tP,
    tP+tZ+tN,
    tP+tZ+tZ
    ]