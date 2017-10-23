'''
Created on Mar 3, 2013

@author: Zoya
'''

def dominantPercent(k, m, n):
    # k-both dominant
    # m-half dominant
    # n-recessive

    total = k + m + n + 0.0
    totalPair = total * (total - 1)

    mm = m * (m - 1) / totalPair
    nn = n * (n - 1) / totalPair
    mn = n * m / totalPair
     
    # mn - one is m one is n, 1/2 for recessive count, 2 for order mn or nm
    recessive = nn + 0.5 * 2 * mn + 0.25 * mm
    
    return 1 - recessive

print (dominantPercent(19, 17, 25))
