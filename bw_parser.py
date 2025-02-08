import csv
import sys
import re

################################################################################
# Preliminaries to set up decoding of blood work (BW) values to allow for easy
# grouping and conversion to shorthand

def get_input(
  inPrompt = "Enter cbc and/or chemistry data\n(Empty line to end input)\n>"
):
  inList = []
  count = 0
  while True:
      if count == 0:
        line = input(inPrompt)
      else:
        line = input()
      if not line:
          break
      inList.append(line)
      count += 1
  return inList

cbc_chem = get_input("Enter cbc and/or chemistry data\n(Empty line to end input)\n>")
bg = get_input("Enter BG data\n(Empty line to end input)\n>")

#Base terms for BW values
cbc_list = [
  "Plasma Protein", "HGB", "Cell Hgb", "HCT", "RBC", "MCV", "RDW", "MCHC", 
  "CHCM", "Reticulocyte auto #", "CH-Retic", "MCV-Retic", "PLT", "MPV"
]

diff_list = [
  "Nucleated Cells", "Other Cells #", "Blasts #", "Promyelocytes #", 
  "Myelocytes #", "Metamyelocytes #", "Bands #", "Neutrophils #", 
  "Lymphocytes #", "Monocytes #", "Eosinophils #", "Basophils #"
]

chem_list = [
  "GLU", "BUN", "CREAT", "PHOSPHORUS", "CALCIUM", "MAGNESIUM", "TOTAL PROTEIN", 
  "ALBUMIN", "GLOBULIN", "A/G RATIO", "CHOLESTEROL", "CK", "T-BILIRUBIN", "ALP", 
  "ALT", "AST", "GGT", "IRON", "SODIUM", "POTASSIUM", "CHLORIDE", "ANION GAP", 
  "CALCULATED OSMOLALITY", "LIPEMIA", "HEMOLYSIS", "ICTERUS"
]

vBG_list = [
    "FIO2", "ctHb", "Barometric pressure", "pH", "pCO2", "pO2", "cHCO3", 
    "ABEc", "sO2", "pH Temp corr.", "pCO2(T)c", "pO2(T)c", "calc tO2", 
    "Na", "K+", "Cl", "Anion Gap", "Ionized Calcium", "cCa++(7.4)c", 
    "Glucose", "Lactate", "Creatinine", "COHb", "MetHb"
]

#Shorthand lists
cbc_shorthand = [
    "Plasma Protein", "HGB", "Cell Hgb", "HCT", "RBC", "MCV", "RDW", "MCHC", 
    "CHCM", "Retic", "CH-Retic", "MCV-Retic", "PLT", "MPV"
]

diff_shorthand = [
  "WBC", "Other", "Blast", "Promyelocyte",  
  "Myelocyte", "Metamyelocyte", "Band", "Neut",  
  "Lymph", "Mono", "Eo", "Baso"
]

chem_shorthand = [
  "GLU", "BUN", "CREA", "PHOS", "Ca", "Mg", "TP", 
  "ALB", "GLOB", "A/G RATIO", "CHOL", "CK", "T-BILI", "ALP", 
  "ALT", "AST", "GGT", "IRON", "Na", "K", "Cl", "ANION GAP", 
  "CALC OSMOLALITY", "LIPEMIA", "HEMOLYSIS", "ICTERUS"
]

vBG_helper = [
  "FIO", "ctHb", "Baro", "pH", "pCO", "pO", "cHCO", "ABEc", "sO", 
  "pH Temp corr.", "pCOc", "pOc", "calc tO", "Na", "K+", "Cl", "AG", "iCa", 
  "Ca", "GLU", "LAC", "CREA", "COHb", "MetHb"
]

vBG_shorthand = [
  "FIO2", "ctHb", "Baro", "pH", "pCO2", "pO2", "cHCO3", "ABEc", "sO2", 
  "pH Temp corr.", "pCO2(T)c", "pO2(T)c", "calc tO2", "Na", "K+", "Cl", "AG", 
  "iCa", "cCa++(7.4)c", "GLU", "LAC", "CREA", "COHb", "MetHb"
]

all_values = cbc_list + diff_list + chem_list + vBG_helper

vBG_helper_dict = dict(zip(
  vBG_list, vBG_helper
))

shorthand_dict = dict(zip(
  (cbc_list + diff_list + chem_list + vBG_helper),
  (cbc_shorthand + diff_shorthand + chem_shorthand + vBG_shorthand)
))

################################################################################
# Main function to process BW

# TO DO - make compatible with vBG; currently issues d/t repeat keys w what is
# in the chemistry list - may need to  split the function in to one that takes
# cbc/chem and one that does vBG

def process_lab_results(
  inList = [],
  BG = False
):
  out_dict = {}
  for line in inList:
    
    if BG:
      #Modify the vBG values to make data parsable
      for vBG_term, vBG_help in vBG_helper_dict.items():
          line = line.replace(vBG_term, vBG_help)
    
    #Find values with L/H/P flags
    flagged = re.match(r"([\w\s#/\-]+)\s([LHP]?)\s([\d.]+)\s.*", line)
    #Identify term and save if in the desired term list
    if flagged:
      metric = flagged.group(1).strip()
      if metric in all_values:
        metric = shorthand_dict.get(metric)
        flag = flagged.group(2)
        value = flagged.group(3)
        #Format the value with flag
        formatted_value = f"<b>{metric} {value} ({flag})</b>"
        out_dict[metric] = formatted_value
    else:
      #Find values that are not flagged
      not_flagged = re.match(r"([\D]+)(\s)(\S+).*", line)
      if not_flagged:
        metric = not_flagged.group(1).strip()
        if metric in all_values:
          #Clean the metric
          metric = shorthand_dict.get(metric)
          value = not_flagged.group(3)
          out_dict[metric] = f"{metric} {value}"

  #Remove 0s
  out_dict = {
    key: value for key, value in out_dict.items() 
    if not any(entry in value.split() for entry in ['0', '0.0'])
  }
  return out_dict


#Run and print results
outdict1 = process_lab_results(inList = cbc_chem)
outdict2 = process_lab_results(inList = bg, BG = True)

#Split outdict by BW
cbc_outdict = {key: outdict1[key] for key in cbc_shorthand if key in outdict1}
diff_outdict = {key: outdict1[key] for key in diff_shorthand if key in outdict1}
chem_outdict = {key: outdict1[key] for key in chem_shorthand if key in outdict1}
vBG_outdict = {key: outdict2[key] for key in vBG_shorthand if key in outdict2}


# Printing the resulting dictionaries
cbc_output = '; '.join([f'{value}' for value in cbc_outdict.values()])
diff_output = '; '.join([f'{value}' for value in diff_outdict.values()])
chem_output = '; '.join([f'{value}' for value in chem_outdict.values()])
vBG_output = '; '.join([f'{value}' for value in vBG_outdict.values()])

html_content = f"""
<html>
<head>
  <style>
      body {{ font-family: Calibri, sans-serif; font-size: 15px; }}
  </style>
</head>
<body>
  <ul>
  <li>CBC:</li>
  <li>{diff_output}</li>
  <li>{cbc_output}</li>
  <li>Chem:</li>
  <li>{chem_output}</li>
  <li>vBG:</li>
  <li>{vBG_output}</li>
  </ul>
</body>
</html>
"""

with open("output.html", "w") as file:
  file.write(html_content)