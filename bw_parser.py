import csv
import sys
import re

################################################################################
# Preliminaries to set up decoding of blood work (BW) values to allow for easy
# grouping and conversion to shorthand

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

all_values = cbc_list + diff_list + chem_list

#Shorthand lists
cbc_shorthand = [
    "Plasma Protein", "HGB", "Cell Hgb", "HCT", "RBC", "MCV", "RDW", "MCHC", 
    "CHCM", "Retic", "CH-Retic", "MCV-Retic", "PLT", "MPV"
]

diff_shorthand = [
  "Nucleated", "Other", "Blasts", "Promyelocytes",  
  "Myelocytes", "Metamyelocytes", "Bands", "Neuts",  
  "Lymphs", "Monos", "Eos", "Basos"
]

chem_shorthand = [
  "GLU", "BUN", "CREAT", "PHOS", "Ca", "Mg", "TP", 
  "ALB", "GLOB", "A/G RATIO", "CHOL", "CK", "T-BILI", "ALP", 
  "ALT", "AST", "GGT", "IRON", "Na", "K", "Cl", "ANION GAP", 
  "CALCULATED OSMOLALITY", "LIPEMIA", "HEMOLYSIS", "ICTERUS"
]

shorthand_dict = dict(zip(
  (cbc_list + diff_list + chem_list),
  (cbc_shorthand + diff_shorthand + chem_shorthand)
))

################################################################################
# Main function to process BW

def process_lab_results(
  inFile = "cbc_chem_test.txt",
  outFile = 'output.txt'
):
  with open(inFile, "r") as file:
    out_dict = {}
    for line in file:
      
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
          formatted_value = f"{value} ({flag})"
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
            out_dict[metric] = value
  
  #Remove 0s
  out_dict = {key: value for key, value in out_dict.items() if value not in ['0', '0.0']}
  return out_dict


#Run and print results
outdict = process_lab_results()

#Split outdict by BW
cbc_outdict = {key: outdict[key] for key in cbc_shorthand if key in outdict}
diff_outdict = {key: outdict[key] for key in diff_shorthand if key in outdict}
chem_outdict = {key: outdict[key] for key in chem_shorthand if key in outdict}

# Printing the resulting dictionaries
print("CBC Dictionary:\n",
      '; '.join([f'{key} {value}' for key, value in cbc_outdict.items()]))
print("Diff Dictionary:\n",
      '; '.join([f'{key} {value}' for key, value in diff_outdict.items()]))
print("Chem Dictionary:\n",
      '; '.join([f'{key} {value}' for key, value in chem_outdict.items()]))

