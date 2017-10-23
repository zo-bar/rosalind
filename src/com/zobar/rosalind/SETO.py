'''
Created on Jul 26, 2013

@author: Zoya
'''
def SETO(input_file, output_file):
    with open(input_file) as resource:
        c = resource.readline()
        A = resource.readline().replace("{", "").replace("}", "").rstrip().split(", ")
        B = resource.readline().replace("{", "").replace("}", "").rstrip().split(", ")
    with open(output_file, "w") as result:
        AunionB = [x for x in A]
        AinterB = [x for x in A]
        AminusB = [x for x in A]
        BminusA = [x for x in B]
        for b in B:
            if AunionB.count(b) == 0:
                AunionB.append(b)
            if AminusB.count(b) != 0:
                AminusB.remove(AminusB[AminusB.index(b)])
        for a in A:
            if B.count(a) == 0:
                AinterB.remove(AinterB[AinterB.index(a)])
            if BminusA.count(a) != 0:
                BminusA.remove(BminusA[BminusA.index(a)])
        Acompliment = []
        Bcompliment = []
        for i in xrange(1, int(c) + 1):
            if (A.count(str(i)) == 0):
                Acompliment.append(str(i))
            if (B.count(str(i)) == 0):
                Bcompliment.append(str(i))
        result.write("{" + ", ".join(AunionB) + "}\n")
        result.write("{" + ", ".join(AinterB) + "}\n")
        result.write("{" + ", ".join(AminusB) + "}\n")
        result.write("{" + ", ".join(BminusA) + "}\n")
        result.write("{" + ", ".join(Acompliment) + "}\n")
        result.write("{" + ", ".join(Bcompliment) + "}") 
               
SETO("data/rosalind_seto.txt", "data/rosalind_seto_result.txt")
