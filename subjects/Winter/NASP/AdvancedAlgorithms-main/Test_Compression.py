import unittest
from LZ77 import LZ77Encode,LZ77Decode,generateTest,testCompressedSequence,searchString

class MyTestCase(unittest.TestCase):
    def test_LZ77(self):
        s=generateTest()
        _d,_a=6,3
        r=LZ77Encode(s,pow(2,_d),pow(2,_a))
        (rb,rl)=testCompressedSequence(r)
        if not rb:
            for s in rl: print(s)
            self.assertTrue(rb)
        else:
            d=LZ77Decode(r,pow(2,_d),pow(2,_a))
            print("Input {}".format(s))
            print("Decompressed {}".format(d))
            print("{} bits uncompressed, {} bits compressed".format(8*len(s),8+(8+_d+_a)*(len(r)-1)))
            self.assertEqual(d, s)

    def test_LZ772(self):
        r1=LZ77Encode("RIBARIBIGRIZEREP",6,4)
        print(r1)
        r2=LZ77Encode("MICMICMICMVAUIC",4,4)
        print(r2)

if __name__ == '__main__':
    unittest.main()
