# Multi-Turn-File-Generator
multi-turn conversation files generator from a directory with json files

## Installation
- python module: requirements.txt
  
  ```
  pip install -r requirements.txt
  ```
## Generating Files (.tsv & .txt)
- **input_path**: path of the directory contains json files
- **output_path**: path to save tsv and txt files
- **qas_name**: name of the tsv file contains q-a pairs (default: "Multi_turn_QA.tsv")
- **ids_name**: name of the txt file contains IDs. IDs correspond to the q-a pairs in the tsv file. (default: "ID.txt")
  
  ```
  python gen_files.py --input_path {DIR_PATH} --output_path {PATH} --qas_name {TSV_NAME} --ids_name {TXT_NAME}
  ```
