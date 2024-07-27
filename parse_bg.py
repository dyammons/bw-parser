import csv
import sys

keepVals = ["FIO2", "ctHb", "pH", "pCO2", "pO2", "cHCO3", "ABEc", "sO2", "pCO2(T)c", "pO2(T)c", "Na", "K+", "Cl", "Anion", "Ionized", "cCa++(7.4)c", "Glucose", "Lactate", "Creatinine", "COHb", "MetHb"]
corVals = ["Anion", "Ionized"]

def parse_vBG(inFile = "vBG_test.txt", outFile = 'output_vBG.txt', onlyONL = False):
    printed = []
    with open(outFile, 'w') as outs:
        sys.stdout = outs
        with open(inFile, "r") as txt:
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
                        elif row[0] in corVals:
                            if row[2] == "H" or row[2] == "L":
                                print(f"{row[0]} {row[1]}: {row[4]} {row[7]} ({row[2]})", end = '; ')
                            else:
                                if not onlyONL:
                                    print(f"{row[0]} {row[1]}: {row[2]} {row[6]}", end = '; ')

parse_vBG()

keepVals = ["Plasma", "HGB", "HCT", "RBC", "MCV", "RDW", "MCHC", "CHCM", "PLT", "MPV", "Nucleated"]
corVals = ["Nucleated", "Plasma"]

def parse_cbc(inFile = "cbc_chem_test.txt", outFile = 'output_cbc.txt', onlyONL = True):
    printed = []
    with open(outFile, 'w') as outs:
        sys.stdout = outs
        with open(inFile, "r") as txt:
            datas = csv.reader(txt, delimiter=' ')
            for row in datas:
                if row[0] in keepVals:
                    if not row[0] in printed:
                        printed.append(row[0])
                        if len(row) == 6:
                                if not onlyONL:
                                    print(f"{row[0]}: {row[1]} {row[5]}", end = '; ')
                        elif row[1] == "H" or row[1] == "L":
                            print(f"{row[0]}: {row[2]} {row[6]} ({row[1]})", end = '; ')
                        elif row[0] in corVals:
                            if row[2] == "H" or row[2] == "L":
                                print(f"{row[0]} {row[1]}: {row[4]} {row[7]} ({row[2]})", end = '; ')
                            else:
                                if not onlyONL:
                                    print(f"{row[0]} {row[1]}: {row[2]} {row[6]}", end = '; ')

parse_cbc()
            
keepVals = ["Other", "Blasts", "Promyelocytes", "Myelocytes", "Metamyelocytes", "Bands", "Neutrophils", "Lymphocytes", "Monocytes", "Eosinophils", "Basophils", "nRBC#", "nRBC%", "Clumped"]
corVals = ["Other", "nRBC#", "nRBC%"]
def parse_diff_cnt(inFile = "cbc_chem_test.txt", outFile = 'output_diff.txt', onlyONL = True, ignoreZeros = True, dataType = "cnt"):
    printed = []
    with open(outFile, 'w') as outs:
        sys.stdout = outs
        with open(inFile, "r") as txt:
            datas = csv.reader(txt, delimiter=' ')
            for row in datas:
                if row[0] in keepVals:
                    if dataType == "pct":
                        if row[1] == "%" or row[0] in corVals:
                            if not row[0] in printed:
                                printed.append(row[0])
                                if len(row) == 7:
                                    if not onlyONL:
                                        if ignoreZeros == False:
                                            print(f"{row[0]}: {row[2]} {row[6]}", end = '; ')
                                        else:
                                            if float(row[2]) != 0:
                                                print(f"{row[0]}: {row[2]} {row[6]}", end = '; ')
                                elif row[2] in ["H", "L"]:
                                    print(f"{row[0]}: {row[3]} {row[7]} ({row[2]})", end = '; ')
                        elif row[0] == corVals[0]:
                            if row[2] in ["H", "L"]:
                                print(f"{row[0]} {row[1]}: {row[3]} {row[7]} ({row[2]})", end = '; ')
                            else:
                                if not onlyONL:
                                    if ignoreZeros == False:
                                        print(f"{row[0]} {row[1]}: {row[3]} {row[7]}", end = '; ')
                                    else:
                                        if float(row[3]) != 0:
                                            print(f"{row[0]} {row[1]}: {row[3]} {row[7]}", end = '; ')
                        elif row[0] == corVals[2]:
                            if row[2] in ["H", "L"]:
                                print(f"nRBC: {row[2]} {row[6]} ({row[1]})", end = '; ')
                            else:
                                if not onlyONL:
                                    if ignoreZeros == False:
                                        print(f"nRBC: {row[1]} {row[5]}", end = '; ')
                                    else:
                                        if float(row[1]) != 0:
                                            print(f"nRBC: {row[1]} {row[5]}", end = '; ')
                    else:
                        if row[1] == "#" or row[0] in corVals:
                            if not row[0] in printed:
                                printed.append(row[0])
                                if len(row) == 7:
                                    if not onlyONL:
                                        if ignoreZeros == False:
                                            print(f"{row[0]}: {row[2]} {row[6]}", end = '; ')
                                        else:
                                            if float(row[2]) != 0:
                                                print(f"{row[0]}: {row[2]} {row[6]}", end = '; ')
                                elif row[2] in ["H", "L"]:
                                    print(f"{row[0]}: {row[3]} {row[7]} ({row[2]})", end = '; ')
                        elif row[0] == corVals[0]:
                            if row[2] in ["H", "L"]:
                                print(f"{row[0]} {row[1]}: {row[3]} {row[7]} ({row[2]})", end = '; ')
                            else:
                                if not onlyONL:
                                    if ignoreZeros == False:
                                        print(f"{row[0]} {row[1]}: {row[3]} {row[7]}", end = '; ')
                                    else:
                                        if float(row[3]) != 0:
                                            print(f"{row[0]} {row[1]}: {row[3]} {row[7]}", end = '; ')
                        elif row[0] == corVals[1]:
                            if row[2] in ["H", "L"]:
                                print(f"nRBC: {row[2]} {row[6]} ({row[1]})", end = '; ')
                            else:
                                if not onlyONL:
                                    if ignoreZeros == False:
                                        print(f"nRBC: {row[1]} {row[5]}", end = '; ')
                                    else:
                                        if float(row[1]) != 0:
                                            print(f"nRBC: {row[1]} {row[5]}", end = '; ')                                             
parse_diff_cnt()

keepVals = ["GLU", "BUN", "CREAT", "PHOSPHORUS", "CALCIUM", "MAGNESIUM", "TOTAL", "ALBUMIN", "GLOBULIN", "A/G", "CHOLESTEROL",
            "CK", "T-BILIRUBIN", "ALP", "ALT", "AST", "GGT", "SODIUM", "POTASSIUM", "CHLORIDE", "BICARBONATE", "ANION", "CALCULATED"]
corVals = ["TOTAL", "A/G", "BICARBONATE", "ANION", "CALCULATED"]

def parse_chem(inFile = "cbc_chem_test.txt", outFile = 'output_chem.txt', onlyONL = False):
    printed = []
    with open(outFile, 'w') as outs:
        sys.stdout = outs
        with open(inFile, "r") as txt:
            datas = csv.reader(txt, delimiter=' ')
            for row in datas:
                if row[0] in keepVals:
                    if not row[0] in printed:
                        printed.append(row[0])
                        if len(row) == 7 and row[0] not in corVals:
                            print(f"{row[0]}: {row[2]} {row[6]} ({row[1]})", end = '; ')
                        elif len(row) == 6 and row[1] != "H" and row[1] != "L":
                                if not onlyONL:
                                    print(f"{row[0]}: {row[1]} {row[5]}", end = '; ')
                        elif len(row) == 6 and row[1] in ["H", "L"]:
                            print(f"{row[0]}: {row[2]} ({row[1]})", end = '; ')
                        elif len(row) == 5:
                                if not onlyONL:
                                    print(f"{row[0]}: {row[1]}", end = '; ')
                                elif row[1] == "H" or row[1] == "L":
                                    print(f"{row[0]}: {row[1]} ({row[2]})", end = '; ')
                        elif row[0] in corVals:
                            if len(row) == 7:
                                if not onlyONL:
                                    print(f"{row[0]} {row[1]}: {row[2]} {row[6]}", end = '; ')
                            if len(row) == 8:
                                print(f"{row[0]} {row[1]}: {row[3]} {row[7]} ({row[2]})", end = '; ')
parse_chem()
