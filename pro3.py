from math import log10, sqrt
import copy
from statistics import mean

NBV = 16

def readData(myFile):
    myfile = open(myFile, "r")
    structList = ["H", "C", "E"]
    acidList = "ARDNCEQGHILKMFPSTWYV"
    struct_count = {"H" : 0, "C" : 0, "E" : 0}
    affiliate = {}
    voisins = {}
    probaVoisins = {}
    for S in structList:
        voisins[S] = {}
        probaVoisins[S] = {}
        for AA in acidList:
            voisins[S][AA] = {}
            probaVoisins[S][AA] = {}
            for AA2 in acidList:
                voisins[S][AA][AA2] = 0
                probaVoisins[S][AA][AA2] = {}
    I = {}
    individuel = {}
    for R in acidList:
        affiliate[R] = {"H" : 0, "C" : 0, "E" : 0}
        individuel[R] = {"H" : 0, "C" : 0, "E" : 0}
        I[R] = {"H" : 0, "C" : 0, "E" : 0}
    i = 0
    struct = ""
    chaine = ""
    for line in myfile:
        if i == 9002:
            break
        line = line.replace("\n", "")
        if i%3 == 1:
            chaine = line
        elif i%3 == 2:
            struct = line
        else:
            if chaine != "":
                for j in range(len(chaine)-1):
                    struct_count[struct[j]] += 1
                    affiliate[chaine[j]][struct[j]] += 1
                    for k in range(-8, 9):
                        if j+k >= 0 and j+k <= len(chaine)-1 and k!= 0:
                            voisins[struct[j]][chaine[j]][chaine[j+k]] += 1

            chaine = ""
            struct = ""
        i +=1
    myfile.close()
    print(voisins)


    for R in acidList:
        for S in range(len(structList)):
            fsr  = float(affiliate[R][structList[S]])
            fnsr = float(affiliate[R][structList[(S+1)%3]] + affiliate[R][structList[(S+2)%3]])
            fns  = float(struct_count[structList[(S+1)%3]] + struct_count[structList[(S+2)%3]])
            fs   = float(struct_count[structList[S]])
            if fnsr != 0 and fs != 0 and fsr != 0 and fns != 0:
                individuel[R][structList[S]] = log10(fsr/fnsr) + log10(fns/fs)


    for S in structList:
        for AA in acidList:
            for AA2 in acidList:
                fsr  = float(voisins[S][AA][AA2])
                if S == "H":
                    fnsr = float(voisins["E"][AA][AA2] + voisins["C"][AA][AA2])
                    fns  = float(affiliate[AA]["E"] + affiliate[AA]["C"])
                elif S == "C":
                    fnsr = float(voisins["E"][AA][AA2] + voisins["H"][AA][AA2])
                    fns  = float(affiliate[AA]["E"] + affiliate[AA]["H"])
                elif S == "E":
                    fnsr = float(voisins["H"][AA][AA2] + voisins["C"][AA][AA2])
                    fns  = float(affiliate[AA]["H"] + affiliate[AA]["C"])
                fs   = float(affiliate[AA][S])
                if fnsr != 0 and fs != 0 and fsr != 0 and fns != 0:
                    probaVoisins[S][AA][AA2] = log10(fsr/fnsr) + log10(fns/fs)


    print(probaVoisins["C"]["Y"]["W"])
    myfile = open(myFile, "r")
    i = 0
    Q3 = []
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for line in myfile:
        if i >= 9002:
            line = line.replace("\n", "")
            if i%3 == 1:
                chaine = line
            elif i % 3 == 2:
                struct = line
            else:
                if chaine != "":
                    nice = 0
                    for j in range(len(chaine)):
                        structValues = []
                        for S in structList:
                            val = individuel[chaine[j]][S]
                            for k in range(-8, 9):
                                if j+k >= 0 and j+k <= len(chaine)-1 and k!= 0:
                                    val += probaVoisins[S][chaine[j]][chaine[j+k]]
                            structValues.append(val)

                        myGuess = structList[structValues.index(max(structValues))]
                        if myGuess == struct[j]:
                            nice += 1
                            if struct[j] == "H":
                                TP += 1
                            elif struct[j] == "E" or struct[j] == "C":
                                TN += 1
                        else:
                            if myGuess == "H" and (struct[j] == "E" or struct[j] == "C"):
                                FN += 1
                            elif (myGuess == "C" or myGuess == "E") and struct[j] == "H":
                                FP += 1
                            elif (myGuess == "C" and struct[j] == "E") or (myGuess == "E" and struct[j] == "C"):
                                TN += 1

                    Q3.append(nice/len(chaine))
                chaine = ""
                struct = ""
        i += 1

    print(mean(Q3))
    MCC = (TP*TN - FP*FN) / sqrt((TP+FP)*(TP+FN)*(TN*FP)*(TN+FN))
    print(MCC)

    
        

def main(myFile):
    x = readData(myFile)


File = "data.txt"
main(File)
