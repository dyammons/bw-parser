import re

# Purpose -
# Process laboratory blood work (BW) results by extracting and 
# formatting key values from user input, then save values as formatted HTML 
# output with values out of reverence intervals bolded for easy viewing.

# Required input -
# CSU CBC, Chemistry, or blood gas (currently only supports ABL800 BG samples).
# Input should be copied from "Orders" tab on string soft then pasted into 
# command line interface

################################################################################
# Define function to accept pasted input values

def get_input(
  inPrompt = ""
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

################################################################################
# Define base terms for BW values

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

# Shorthand lists
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
# Define function to parse blood work

def process_lab_results(
  inList = None,
  BG = False
):
  
  # Check user input
  if inList is None:
    return "Error: No input data provided. Please provide a list of lab results."
  out_dict = {}
  
  for line in inList:  
    if BG:
      # Modify the vBG values to make data parsable
      for vBG_term, vBG_help in vBG_helper_dict.items():
          line = line.replace(vBG_term, vBG_help)
    
    # Find values with L/H/P flags
    flagged = re.match(r"([\w\s#/\-]+)\s([LHP]?)\s([\d.]+)\s.*", line)
    # Or those not flagged
    not_flagged = re.match(r"([\D]+)(\s)(\S+).*", line)

    # Identify term and save if in the desired term list
    if flagged:
      metric = flagged.group(1).strip()
      metric_short = shorthand_dict.get(metric)
      if metric in all_values and metric_short not in out_dict:
        flag = flagged.group(2)
        value = flagged.group(3)
        #format with flag
        formatted_value = f"<b>{metric_short} {value} ({flag})</b>"
        out_dict[metric_short] = formatted_value

    if not_flagged:
      metric = not_flagged.group(1).strip()
      metric_short = shorthand_dict.get(metric)
      if metric in all_values and metric_short not in out_dict:
        #clean the output
        value = not_flagged.group(3)
        out_dict[metric_short] = f"{metric_short} {value}"

  # Remove 0s
  out_dict = {
    key: value for key, value in out_dict.items() 
    if not any(entry in value.split() for entry in ['0', '0.0'])
  }
  return out_dict


################################################################################
# Main function
def main():
    """Main execution function to gather input, process lab results, and save 
    output as HTML."""
    cbc_chem = get_input("Enter CBC and/or chemistry data\n(Empty line to end input)\n>")
    bg = get_input("Enter BG data\n(Empty line to end input)\n>")
    
    #Run and print results
    outdict1 = process_lab_results(inList = cbc_chem)
    outdict2 = process_lab_results(inList = bg, BG = True)

    #Split outdict by BW
    sections = {
        "DIFF": {key: outdict1[key] for key in diff_shorthand if key in outdict1},
        "CBC": {key: outdict1[key] for key in cbc_shorthand if key in outdict1},
        "CHEM": {key: outdict1[key] for key in chem_shorthand if key in outdict1},
        "vBG": {key: outdict2[key] for key in vBG_shorthand if key in outdict2}
    }

    html_content = f"""
    <html>
    <head>
      <style>
          body {{ font-family: Calibri, sans-serif; font-size: 15px; }}
      </style>
    </head>
    <body>
      <ul>
        {''.join(f"<li>{category}: {'; '.join(values.values())}</li>" 
                for category, values in sections.items() if values)}
      </ul>
    </body>
    </html>
    """

    with open("output.html", "w") as file:
      file.write(html_content)

if __name__ == "__main__":
    main()