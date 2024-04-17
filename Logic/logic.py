data_set = set() #set data_set chua KB va phu dinh alpha
new = set() #new chua menh de ban dau va cac menh de sau khi hop giai
write_result = [] #Mang 2 chieu de chua cac bo ket qua cuoi cung

def readFile(data_set, numFile):
    #mo file de doc
    f = open("./input" + str(numFile) + ".txt", 'r')

    alphaTmp = f.readline().strip().split("OR") #lay ra cac literal tu menh de alpha
    alphaTmp = sorted(alphaTmp, key=lambda x:x.strip(' -').lower()) #Sap xep theo thu tu chu cai
    alpha = tuple(value.strip() for value in alphaTmp) #Chuyen sang tuple
    alpha = tuple(item[1:] if item.startswith('-') else '-'+item for item in alpha)#Lay phu dinh alpha

    #doc tung clause trong KB va luu vao data_set
    numClauses = int(f.readline())
    for i in range(0, numClauses):
        clauseTmp = f.readline().strip().split("OR") #lay ra cac literal tu menh de
        clauseTmp = sorted(clauseTmp, key=lambda x:x.strip(' -').lower()) #Sap xep theo thu tu chu cai
        clause = tuple(value.strip() for value in clauseTmp) #Chuyen sang tuple
        data_set.add(clause) #Lay phu dinh

    # luu gia tri phu dinh alpha vao data_set
    for element in alpha:
        data_set.add((element,))
    # data_set.add(alpha)

def PL_Resolve(clause1, clause2):
    clause3 = tuple(set(clause1).union(set(clause2))) #Hop cua 2 clause

    count = 0
    resolvents = {clause1, clause2}
    #Duyet qua tung cap literal trong clause3
    for i in range(0,len(clause3)):
        for j in range(i+1, len(clause3)):
            #Neu co cac cap doi nhau thi xoa khoi clause3
            if(clause3[i][0] == '-' and clause3[j][0] != '-' and clause3[i][1:] == clause3[j] or
               clause3[j][0] == '-' and clause3[i][0] != '-' and clause3[j][1:] == clause3[i]):
                index_remove = [i, j]
                temp = tuple(item for i, item in enumerate(clause3) if i not in index_remove)
                temp = tuple(sorted(temp, key=lambda x: x.strip('-').lower())) #Sap xep theo thu tu chu cai
                resolvents = {temp}
                count += 1

    if(count > 1):
        resolvents = {clause1, clause2}
    return resolvents


def PL_Resolution(data_set,new,write_result):
    while True:
        clause_result = [] #Cac menh de phat sinh mới trong moi vong lap
        count = 0
        #Duyet qua tung cap clause trong data_set
        for i, clause1 in enumerate(data_set):
            for clause2 in list(data_set)[i+1:]:
                resolvents = PL_Resolve(clause1, clause2) #Tim hop giai
                if(len(resolvents) == 1): #Tim ra cac menh de moi sau hop giai
                    for element in resolvents:
                        if((element not in data_set) and (element not in new)):
                            clause_result.append(element)
                            count += 1
                new = new.union(resolvents) #Cap nhat cac menh de vao new
        clause_result.insert(0,count)
        write_result.append(clause_result)
        if () in new: #Neu ton tai menh de rong thi tra ve TRUE
            return True
        if(new <= data_set): #Neu khong phat sinh duoc menh de nao moi thi tra ve FALSE
            return False
        data_set = data_set.union(new)

def write2File(write_result, result, numFile):
    f = open("./output" + str(numFile) + ".txt", 'w')

    for i in range(0, len(write_result)):
        for j in range(0, len(write_result[i])):
            if(isinstance(write_result[i][j], tuple)):
                temp = ""
                for item in write_result[i][j]:
                    temp += item + " OR "
                temp = temp[:-4]
                f.write(temp+"\n" if temp != "" else "{}\n")
            else:
                f.write(str(write_result[i][j]) + "\n")


    if(result == True):
        f.write("YES")
    else:
        f.write("NO")


if __name__ == '__main__':
    numFile = int(input("Input number of file (Examples - number 1 is input1.txt): "))
    readFile(data_set, numFile)
    print(data_set)
    result = PL_Resolution(data_set, new, write_result)
    write2File(write_result, result, numFile)
    