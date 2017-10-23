'''
Created on Feb 26, 2013

@author: Zoya
'''
import io
import os

def REVCfromFile (file_name, output_file_name):
    with open(file_name) as dna:
        REVC(dna, output_file_name)

def REVCfromString(cons):
    dna = io.StringIO(cons);
    output_file_name = "data/temp.txt"
    result = REVC(dna, output_file_name)
    os.remove(output_file_name)
    return result

def REVC (stream, output_file_name):
    nchar = stream.read(1)
    rna = front_appender(output_file_name)
    while nchar:
        rna.write(reverse_char(nchar))
        nchar = stream.read(1)
    rna.close()
    return open(output_file_name).read()

def reverse_char(nchar):
    if nchar.upper() == 'A':
        return 'T'
    elif nchar.upper() == 'C':
        return 'G'
    elif nchar.upper() == 'T':
        return 'A'
    elif nchar.upper() == 'G':
        return 'C'

class front_appender:
    def __init__(self, fname, mode='w'):
        self.__f = open(fname, mode)
        self.__write_queue = []

    def write(self, s):
        self.__write_queue.insert(0, s)

    def close(self):
        self.__f.writelines(self.__write_queue)
        self.__f.close()
