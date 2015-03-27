# ------------------------------------------------------------------------------------------------------#
#   Compiler:                                                                                           #
#   Source Language: ANSI C, Implementation Language: Python, Target Language: MIPS                     #
#                                                                                                       #
#   Authors: Rohit Sahu, Tarun Chauhan, Vikram Rathi, Vivek Gupta                                       #
#   Group Number: A17                                                                                   #
#   File: SymbolTable.py                                                                                     #
# ------------------------------------------------------------------------------------------------------#
TableNumber = 1
class SymbolTable:
    def __init__(self,thefather):
        global TableNumber
        self.symbols=[]
        self.attributes=[]
        self.father = thefather
        self.tableNumber = TableNumber
        TableNumber += 1
        if(thefather==-1):
            self.depth=0
            self.offset=[]
            self.offset_count=0
        else:
            self.depth = thefather.depth+1
            #self.offset = thefather.offset
            self.offset = []
            self.offset_count=thefather.offset_count
    def lookup(self,mystring):
        table = self
        while(not(table==-1)):
            #print "depth=",table.depth
            if(mystring in table.symbols):
                myindex = table.symbols.index(mystring)
                return {"attributes":table.attributes[myindex],'offset':table.offset[myindex],'TABLE':table.tableNumber}
            table = table.father
        return False
    
    def lookupCurrentTable(self,mystring):
        table = self
        if(mystring in table.symbols):
            myindex = table.symbols.index(mystring)
            return {"attributes":table.attributes[myindex],'offset':table.offset[myindex],'TABLE':table.tableNumber}
        return False
    
    def insert(self,mystring,attributes_new):
        if(self.lookupCurrentTable(mystring)==False):
            self.symbols += [mystring]
            attributes_new['NAME'] = mystring
            self.attributes += [attributes_new]
            self.offset += [self.offset_count]
            data_size=0

            if(self.attributes[-1]['ARRAY_DIMENTION'] == 0):
                if(self.attributes[-1]['TYPE']=='int') :data_size=4
                elif(self.attributes[-1]['TYPE']=='LONG') : data_size=8
                elif(self.attributes[-1]['TYPE']=='LONG INT') : data_size=8
                elif(self.attributes[-1]['TYPE']=='float') : data_size=8
            elif(self.attributes[-1]['ARRAY'] == 1):
                totalIndex = int(self.attributes[-1]['INDEX1'])
                if(self.attributes[-1]['TYPE']=='int') :data_size=4*totalIndex
                elif(self.attributes[-1]['TYPE']=='LONG') : data_size=8*totalIndex
                elif(self.attributes[-1]['TYPE']=='LONG INT') : data_size=8*totalIndex
                elif(self.attributes[-1]['TYPE']=='float') : data_size=8*totalIndex
            elif(self.attributes[-1]['ARRAY'] == 2):
                totalIndex = int(self.attributes[-1]['INDEX1'])
                totalIndex *= int(self.attributes[-1]['INDEX2'])
                #print totalIndex
                if(self.attributes[-1]['TYPE']=='int') :data_size=4*totalIndex
                elif(self.attributes[-1]['TYPE']=='LONG') : data_size=8*totalIndex
                elif(self.attributes[-1]['TYPE']=='LONG INT') : data_size=8*totalIndex
                elif(self.attributes[-1]['TYPE']=='float') : data_size=8*totalIndex
                
            self.offset_count = self.offset_count + data_size
            return True
        else : return False
