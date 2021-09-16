table = {}
class node:
    def __init__(self,char,huff, end ,left = None, right = None ):
        self.char = char
        self.left = left
        self.right =right
        self.endnode = end
        self.huff = huff
        self.level = len(huff) 
        


def decode(codes,nodes,file):
    current = nodes
    char = []
    for byte in codes:
        n = 7
        while(n>=0):
            i = (byte>>n) & 1
            if i == False:
                current = current.left 
            if i == True:
                current = current.right
            if current.endnode:
                if current.char == 'x':
                    file.write('\n')
                    current = nodes
                    break
                else:
                    file.write(current.char)
                current = nodes
            n-=1

key = []
val = []


with open('huff.txt','rt') as file:
    length = int(file.readline())
    for i in range(length):
        key.append(file.readline().replace('\n',''))
    for i in range(length):
        val.append(file.readline().replace('\n',''))

nodes = []
for i in range(length):
    nodes.append(node(key[i],val[i],True))


while len(nodes)>1 :
    nodes = sorted(nodes, key=lambda x: x.level,reverse=True)
    k = nodes[0].huff[:-1]
    for i in nodes[1:]:
        if k == i.huff[:-1]:
            break
    if nodes[0].huff[-1] == "0":
        left = nodes[0]
        right = i
    else:
        left = i
        right = nodes[0]
    nodes.remove(left)
    nodes.remove(right)
    nodes.append(node('',k,False, left = left, right=right))    
code = open('compressed.bin','rb')
file = open('decoded.csv','w')
while True:
    codes = code.read(1000)
    decode(codes,nodes[0],file)
    if codes == b'':
        break
file.close
code.close





    





