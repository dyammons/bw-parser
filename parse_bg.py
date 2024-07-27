import csv
import sys

#options
onlyONL = True

keepVals = ["ctHb", "BAROM", "BldpH", "pCO2", "pO2", "cHCO3", "cABE", "SO2", "cTO2", "pCO2tc", "pO2tc", "BldNA", "BldK+", "BldCL", "cAnGap", "cCa+", "corrCA", "cGLU", "cLAC", "cBldpH", "cCa++(7.4)c", "Glucose", "Lactate", "Creatinine", "COHb", "MetHb", "Barometric", "Anion" "Ionized"]

keepVals = ["Temp", "FIO2", "ctHb", "Barometric", "pH", "pCO2", "pO2", "cHCO3", "ABEc", "sO2", "pCO2(T)c", "pO2(T)c", "calc", "Na", "K+", "Cl", "Anion", "Ionized", "cCa++(7.4)c", "Glucose", "Lactate", "Creatinine", "COHb", "MetHb"]

printed = []
with open('output.txt', 'w') as outs:
    sys.stdout = outs
    with open("./vBG_test.txt", "r") as txt:
        datas = csv.reader(txt, delimiter=' ')
        for row in datas:
            if row[0] in keepVals:
                if not row[0] in printed:
                    printed.append(row[0])
                    if row[0] == "pH":
                        if row[1] == "H" or row[1] == "L":
                            print(f"{row[0]}: {row[2]} ({row[1]})", end = '; ')
                        else:
                            print(f"{row[0]}: {row[2]}", end = '; ')
                    elif len(row) == 6:
                            if not onlyONL:
                                print(f"{row[0]}: {row[1]} {row[5]}", end = '; ')
                    elif len(row) == 5:
                            if not onlyONL:
                                print(f"{row[0]}: {row[1]}", end = '; ')
                    elif row[1] == "H" or row[1] == "L":
                        print(f"{row[0]}: {row[2]} {row[6]} ({row[1]})", end = '; ')
                    elif row[0] == "Temp":
                        if len(row) == 7:
                            if not onlyONL:
                                print(f"{row[0]}: {row[1]} {row[6]}", end = '; ')
                    elif row[0] == "Anion" or row[0] == "Ionized":
                        if row[2] == "H" or row[2] == "L":
                            print(f"{row[0]} {row[1]}: {row[4]} {row[7]} ({row[2]})", end = '; ')
                        else:
                            if not onlyONL:
                                print(f"{row[0]} {row[1]}: {row[2]} {row[6]}", end = '; ')

