
#   Compiler Project:                                                                                           
#                                                                                                       
#   Authors: SAHIL SOLANKI, ABHAY KUMAR, SWAROOP SINGH                                       
#   Group Number: A28                                                                                  
#   File: SymbolTable.py                                                                                   
# ------------------------------------------------------------------------------------------------------#
TableNo = 1
# def __init__(self,father):
#     global TableNo

class SymbolTable:
    def __init__(self,father):
        global TableNo
        self.symbols=[]
        self.attributes=[]
        self.father = father
        self.tableNumber = TableNo
        TableNo = TableNo + 1
        if(father==-1):
            self.depth=0
            self.offset=[]
            self.offset_count=0
        else:
            self.depth = father.depth+1
            self.offset = []
            self.offset_count=father.offset_count
    def lookup(self,mystring):
        table = self
        while(table!=-1):

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
                if(self.attributes[-1]['DATA_TYPE']=='int') :data_size=4
                elif(self.attributes[-1]['DATA_TYPE']=='LONG') : data_size=8
                elif(self.attributes[-1]['DATA_TYPE']=='LONG INT') : data_size=8
                elif(self.attributes[-1]['DATA_TYPE']=='float') : data_size=8
            elif(self.attributes[-1]['ARRAY'] == 1):
                totalIndex = int(self.attributes[-1]['VAL1'])
                if(self.attributes[-1]['DATA_TYPE']=='int') :data_size=4*totalIndex
                elif(self.attributes[-1]['DATA_TYPE']=='LONG') : data_size=8*totalIndex
                elif(self.attributes[-1]['DATA_TYPE']=='LONG INT') : data_size=8*totalIndex
                elif(self.attributes[-1]['DATA_TYPE']=='float') : data_size=8*totalIndex
            elif(self.attributes[-1]['ARRAY'] == 2):
                totalIndex = int(self.attributes[-1]['VAL1'])
                totalIndex *= int(self.attributes[-1]['VAL2'])
                #print totalIndex
                if(self.attributes[-1]['DATA_TYPE']=='int') :data_size=4*totalIndex
                elif(self.attributes[-1]['DATA_TYPE']=='LONG') : data_size=8*totalIndex
                elif(self.attributes[-1]['DATA_TYPE']=='LONG INT') : data_size=8*totalIndex
                elif(self.attributes[-1]['DATA_TYPE']=='float') : data_size=8*totalIndex
                
            self.offset_count = self.offset_count + data_size
            return True
        else : return False
