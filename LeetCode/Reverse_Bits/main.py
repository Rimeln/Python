class Solution:
    def reverseBits(self, n: int) -> int:
        n2=bin(n)[2:]
        sn2= str(n2)
        n2r=sn2[::-1]
        while len(n2r)<32:
            n2r=n2r+'0'
        r = int(n2r,2)
        return r

        