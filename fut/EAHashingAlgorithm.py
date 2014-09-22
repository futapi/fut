#!/usr/bin/env python

'''
@author     Danny Cullen
@version    1.0.1
@about      Python implementation of EA's hashing algorithm for secret answers on Ultimate Team Web App
@twitter    @dcullen88
'''

import ctypes

class EAHashingAlgorithm():

    def __init__(self):
        # shift amounts in each round
        self.r1Shifts = [ 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22 ]
        self.r2Shifts = [ 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20 ]
        self.r3Shifts = [ 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23 ]
        self.r4Shifts = [ 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21 ]

        self.hexChars = "0123456789abcdef"

    def zero_fill_right_shit(self, data, bits):
        return (data & 0xffffffff) >> bits

    def num2hex(self, num):
        '''
            Convert a decimal number to hexadecimal
        '''
        temp = ''
        for i in range(0, 4):
            x = self.hexChars[ ( num >> (i * 8 + 4) ) & 0x0F ]
            y = self.hexChars[ ( num >> (i * 8) ) & 0x0F ]
            temp += (x + y)

        return temp

    def chunkMessage(self, string):
        # TODO: ctypes.c_int32() in this method
        nblk = (( len(string) + 8) >> 6) + 1
        blks = [0] * (nblk * 16)

        for i in range(0, len(string)):
            blks[i >> 2] |= ord(string[i]) << ((i % 4) * 8)

        i = i + 1

        blks[i >> 2] |= 0x80 << ((i % 4) * 8)
        blks[nblk * 16 - 2] = len(string) * 8

        return blks

    def add(self, x, y):
        lsw = (x & 0xFFFF) + (y & 0xFFFF)
        msw = (ctypes.c_int32(x >> 16).value) + (ctypes.c_int32(y >> 16).value) + (ctypes.c_int32(lsw >> 16).value)
        return ctypes.c_int32( (ctypes.c_int32(msw << 16).value) | (lsw & 0xFFFF) ).value

    # Bitwise rotate 32bit num to left
    def bitwiseRotate(self, x, c):
        return ctypes.c_int32( ctypes.c_int32(x << c).value | self.zero_fill_right_shit(x, 32 - c) ).value

    # Basic MD5 operations
    def cmn(self, q, a, b, x, s, t):
        z1 = self.add(a, q)
        z2 = self.add(x, t)
        a1 = self.add(z1, z2)

        x1 = self.bitwiseRotate(a1, s)
        return self.add(x1, b)

    def md5_f(self, a, b, c, d, x, s, t):
        return self.cmn( ctypes.c_int32((b & c) | ((~b) & d)).value, a, b, x, s, t )

    def md5_g(self, a, b, c, d, x, s, t):
        return self.cmn( ctypes.c_int32((b & d) | (c & (~d))).value, a, b, x, s, t )

    def md5_h(self, a, b, c, d, x, s, t):
        return self.cmn( ctypes.c_int32(b ^ c ^ d).value, a, b, x, s, t )

    def md5_i(self, a, b, c, d, x, s, t):
        return self.cmn( ctypes.c_int32(c ^ (b | (~d))).value, a, b, x, s, t )

    def EAHash(self, string):
        x = self.chunkMessage(string)

        a = 1732584193
        b = -271733879
        c = -1732584194
        d = 271733878

        for i in range(0, 16, 16):
            tempA = a
            tempB = b
            tempC = c
            tempD = d

            # F
            a = self.md5_f(a, b, c, d, x[i+0], self.r1Shifts[0], -680876936)
            d = self.md5_f(d, a, b, c, x[i+1], self.r1Shifts[1], -389564586)
            c = self.md5_f(c, d, a, b, x[i+2], self.r1Shifts[2], 606105819)
            b = self.md5_f(b, c, d, a, x[i+3], self.r1Shifts[3], -1044525330)

            a = self.md5_f(a, b, c, d, x[i+4], self.r1Shifts[4], -176418897)
            d = self.md5_f(d, a, b, c, x[i+5], self.r1Shifts[5], 1200080426)
            c = self.md5_f(c, d, a, b, x[i+6], self.r1Shifts[6], -1473231341)
            b = self.md5_f(b, c, d, a, x[i+7], self.r1Shifts[7], -45705983)

            a = self.md5_f(a, b, c, d, x[i+8], self.r1Shifts[8], 1770035416)
            d = self.md5_f(d, a, b, c, x[i+9], self.r1Shifts[9], -1958414417)
            c = self.md5_f(c, d, a, b, x[i+10], self.r1Shifts[10], -42063)
            b = self.md5_f(b, c, d, a, x[i+11], self.r1Shifts[11], -1990404162)

            a = self.md5_f(a, b, c, d, x[i+12], self.r1Shifts[12], 1804603682)
            d = self.md5_f(d, a, b, c, x[i+13], self.r1Shifts[13], -40341101)
            c = self.md5_f(c, d, a, b, x[i+14], self.r1Shifts[14], -1502002290)
            b = self.md5_f(b, c, d, a, x[i+15], self.r1Shifts[15], 1236535329)

            # G
            a = self.md5_g(a, b, c, d, x[i+1], self.r2Shifts[0], -165796510)
            d = self.md5_g(d, a, b, c, x[i+6], self.r2Shifts[1], -1069501632)
            c = self.md5_g(c, d, a, b, x[i+11], self.r2Shifts[2], 643717713)
            b = self.md5_g(b, c, d, a, x[i+0], self.r2Shifts[3], -373897302)

            a = self.md5_g(a, b, c, d, x[i+5], self.r2Shifts[4], -701558691)
            d = self.md5_g(d, a, b, c, x[i+10], self.r2Shifts[5], 38016083)
            c = self.md5_g(c, d, a, b, x[i+15], self.r2Shifts[6], -660478335)
            b = self.md5_g(b, c, d, a, x[i+4], self.r2Shifts[7], -405537848)

            a = self.md5_g(a, b, c, d, x[i+9], self.r2Shifts[8], 568446438)
            d = self.md5_g(d, a, b, c, x[i+14], self.r2Shifts[9], -1019803690)
            c = self.md5_g(c, d, a, b, x[i+3], self.r2Shifts[10], -187363961)
            b = self.md5_g(b, c, d, a, x[i+8], self.r2Shifts[11], 1163531501)

            a = self.md5_g(a, b, c, d, x[i+13], self.r2Shifts[12], -1444681467)
            d = self.md5_g(d, a, b, c, x[i+2], self.r2Shifts[13], -51403784)
            c = self.md5_g(c, d, a, b, x[i+7], self.r2Shifts[14], 1735328473)
            b = self.md5_g(b, c, d, a, x[i+12], self.r2Shifts[15], -1926607734)

            # H
            a = self.md5_h(a, b, c, d, x[i+5], self.r3Shifts[0], -378558)
            d = self.md5_h(d, a, b, c, x[i+8], self.r3Shifts[1], -2022574463)
            # line below uses self.r2Shifts[2] where as MD5 would use self.r3Shifts[2]
            c = self.md5_h(c, d, a, b, x[i+11], self.r2Shifts[2], 1839030562)
            b = self.md5_h(b, c, d, a, x[i+14], self.r3Shifts[3], -35309556)

            a = self.md5_h(a, b, c, d, x[i+1], self.r3Shifts[4], -1530992060)
            d = self.md5_h(d, a, b, c, x[i+4], self.r3Shifts[5], 1272893353)
            c = self.md5_h(c, d, a, b, x[i+7], self.r3Shifts[6], -155497632)
            b = self.md5_h(b, c, d, a, x[i+10], self.r3Shifts[7], -1094730640)

            a = self.md5_h(a, b, c, d, x[i+13], self.r3Shifts[8], 681279174)
            d = self.md5_h(d, a, b, c, x[i+0], self.r3Shifts[9], -358537222)
            c = self.md5_h(c, d, a, b, x[i+3], self.r3Shifts[10], -722521979)
            b = self.md5_h(b, c, d, a, x[i+6], self.r3Shifts[11], 76029189)

            a = self.md5_h(a, b, c, d, x[i+9], self.r3Shifts[12], -640364487)
            d = self.md5_h(d, a, b, c, x[i+12], self.r3Shifts[13], -421815835)
            c = self.md5_h(c, d, a, b, x[i+15], self.r3Shifts[14], 530742520)
            b = self.md5_h(b, c, d, a, x[i+2], self.r3Shifts[15], -995338651)

            # I
            a = self.md5_i(a, b, c, d, x[i+0], self.r4Shifts[0], -198630844)
            d = self.md5_i(d, a, b, c, x[i+7], self.r4Shifts[1], 1126891415)
            c = self.md5_i(c, d, a, b, x[i+14], self.r4Shifts[2], -1416354905)
            b = self.md5_i(b, c, d, a, x[i+5], self.r4Shifts[3], -57434055)

            a = self.md5_i(a, b, c, d, x[i+12], self.r4Shifts[4], 1700485571)
            d = self.md5_i(d, a, b, c, x[i+3], self.r4Shifts[5], -1894986606)
            c = self.md5_i(c, d, a, b, x[i+10], self.r4Shifts[6], -1051523)
            b = self.md5_i(b, c, d, a, x[i+1], self.r4Shifts[7], -2054922799)

            a = self.md5_i(a, b, c, d, x[i+8], self.r4Shifts[8], 1873313359)
            d = self.md5_i(d, a, b, c, x[i+15], self.r4Shifts[9], -30611744)
            c = self.md5_i(c, d, a, b, x[i+6], self.r4Shifts[10], -1560198380)
            b = self.md5_i(b, c, d, a, x[i+13], self.r4Shifts[11], 1309151649)

            a = self.md5_i(a, b, c, d, x[i+4], self.r4Shifts[12], -145523070)
            d = self.md5_i(d, a, b, c, x[i+11], self.r4Shifts[13], -1120210379)
            c = self.md5_i(c, d, a, b, x[i+2], self.r4Shifts[14], 718787259)
            b = self.md5_i(b, c, d, a, x[i+9], self.r4Shifts[15], -343485551)
            # This line is doubled for some reason, line below is not in the MD5 version
            b = self.md5_i(b, c, d, a, x[i+ 9], self.r4Shifts[15], -343485551)

            a = self.add(a, tempA)
            b = self.add(b, tempB)
            c = self.add(c, tempC)
            d = self.add(d, tempD)

        return self.num2hex(a) + self.num2hex(b) + self.num2hex(c) + self.num2hex(d)

if __name__ == '__main__':
    hashor = EAHashingAlgorithm()
    print(hashor.EAHash('secret answer'))
