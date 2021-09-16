
class Node:
    def __init__(self,char,freq, left = None, right = None ):
        self.char = char
        self.freq = freq
        self.left = left
        self.right =right
        self.huff = []
class TableGenerator:
    def __init__(self, strings = None):
        self.table = {}
        try:
            if strings:
                self.generate_table(strings)
            else:
                with open('huff.txt','r') as file:
                    self.read_table(file)
        except FileNotFoundError:
            raise ValueError('Huffman Codes not defined')
    
    def read_table(self, file):
        key = []
        length = int(file.readline())
        for i in range(length):
            key.append(file.readline().replace('\n',''))
        for i in range(length):
            code = [] 
            for a in file.readline().replace('\n',''):
                if a =='1':
                    code.append(True)
                else:
                    code.append(False)
            self.table[key[i]] = code
        with open('huff.txt','wt') as file:
            file.write(str(len(self.table)) + "\n")
            for a in list(self.table.keys()):
                file.write(str(a) + "\n")
            for i in list(self.table.keys()):
                for codes in self.table[i]:
                    file.write(str(int(codes)))
                file.write("\n")
            file.close


    def generate_table(self,strings):
        freq = self.check_frequency(strings)
        print(strings)
        nodes = []
        for x in freq.keys():
            nodes.append(Node(x,freq[x]))
        while len(nodes) > 1 :
            nodes = sorted(nodes, key=lambda x: x.freq)
            left = nodes[0]
            right = nodes[1]
            left.huff.append(False)
            right.huff.append(True)
            nodes.append(Node('', left.freq+right.freq, left,right))
            nodes.remove(left)
            nodes.remove(right)
        self.generate(nodes[0])
    
    def write_file(self):
        with open('huff.txt','wt') as file:
            c = str(len(self.table)) + "\n"
            file.write(c)
            for a in list(self.table.keys()):
                file.write(str(a) + "\n")
            for i in list(self.table.keys()):
                for codes in self.table[i]:
                    file.write(str(int(codes)))
                file.write("\n")
            file.close()
            
    def generate(self,node, val =[]):
        val = val + node.huff
        if(node.left):
            self.generate(node.left,val)
        if(node.right):
            self.generate(node.right,val) 
        if(not node.left and not node.right):
            self.table[node.char] = val


    def check_frequency(self,string):
        freq ={}
        freq['0'] = 1
        freq['1'] = 1
        freq['2'] = 1
        freq['3'] = 1
        freq['4'] = 1
        freq['5'] = 1
        freq['6'] = 1
        freq['7'] = 1
        freq['8'] = 1
        freq['9'] = 1
        for a in string:
            if a in freq:
                freq[a]+= 1
            else:
                freq[a] = 1
        return freq



