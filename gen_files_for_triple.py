import argparse
import os
import json
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def delete_first_line(QAs_path):
    #tsv파일의 칼럼(q, a)을 나타내는 첫 열을 삭제하는 함수 delete_first_line
    with open(QAs_path,'r') as f1:
        QAs = [line for line in f1][1:]
        f1.close()
    with open(QAs_path,'w') as f2:
        for line in QAs:
            f2.write(line)
        f2.close()

def generate_multi_turn_files(args):
    input_path = args.input_path
    file_list = os.listdir(input_path) #input_path 내의 파일 목록을 받아옴

    QAs = pd.DataFrame(columns=["q","a"]) #질문 q와 그에 따른 응답 a를 쌍으로 담는 데이터프레임 QAs
    ids = []                              #QA 질문 쌍이 같은 대화 뭉치에서 나왔는지를 구분하는 리스트 ids

    #json 파일별 utterance 추출
    idx = 0
    for file_name in file_list:
        if file_name[-5:] != ".json": continue              #json 파일이 아니면 pass
        file_path = input_path + '/' + file_name
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            json_data = json.load(f)
        try:
            utterances = [data[-1]['utterance'] for data in json_data]
        except:
            utterances = [data[-1]['utterence'] for data in json_data]  #json 파일 중 utterance가 utterence로 오타난 경우가 있어 예외 처리
        sentences = []
        for i in range(0, len(utterances)-2):
            if " " in utterances[i:i+3] or "" in utterances[i:i+3]: continue    #빈 문장이 있으면 pass
            sentences.extend([{'q': utterances[i], 'a': utterances[i+1]}, {'q': utterances[i+2], 'a': ""}])
            ids.extend(['id_'+str(idx)]*2)
            idx+=1
        QAs = QAs.append(sentences, ignore_index=True)
        f.close()
    
    #QAs를 tsv파일로 추출
    QAs_path = args.output_path + '/' + args.qas_name
    QAs.to_csv(QAs_path, sep='\t', index=False)
    delete_first_line(QAs_path) #칼럼(q, a)을 나타내는 첫 열 삭제

    #ids를 txt파일로 추출
    ids_path = args.output_path + '/' + args.ids_name
    f = open(ids_path, 'w')
    for i in range(len(ids)):
        f.write(ids[i]+'\n')
    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, default="/Users/dannykm/Downloads/[솔트룩스] 대화 데이터 샘플 v2.0")
    parser.add_argument("--output_path", type=str, default="/Users/dannykm/Downloads")
    parser.add_argument("--qas_name", type=str, default="Multi_turn_QA.tsv")
    parser.add_argument("--ids_name", type=str, default="ID.txt")
    args = parser.parse_args()

    generate_multi_turn_files(args)