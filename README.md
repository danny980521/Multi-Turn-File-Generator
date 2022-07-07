# Multi-Turn-File-Generator
json 형식의 파일을 담고 있는 디렉토리부터 멀티턴 대화 파일을 추출하는 프로그램 

## 설치
- python module: requirements.txt
  
  ```
  pip install -r requirements.txt
  ```
## tsv & txt 파일 추출
- **input_path**: json 파일을 담고 있는 디렉토리의 주소
- **output_path**: 생성한 tsv와 txt 파일을 저장할 주소
- **qas_name**: q-a 쌍들로 이루어진 tsv 파일 이름 (default: "Multi_turn_QA.tsv")
- **ids_name**: tsv 파일의 각 열에 대응하는 멀티턴 대화로 이루어진 txt 파일 이름 (default: "ID.txt")
  
  ```
  python gen_files.py --input_path {DIR_PATH} --output_path {PATH} --qas_name {TSV_NAME} --ids_name {TXT_NAME}
  ```
