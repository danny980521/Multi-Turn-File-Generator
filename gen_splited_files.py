import argparse
import os
import json
import pandas as pd
import warnings
import random
from tqdm import tqdm
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
    all_files = []
    input_path = args.input_path
    dir_list = os.listdir(input_path) #input_path 내의 디렉토리 목록을 받아옴
    for dir_name in dir_list:     
        if dir_name ==  ".DS_Store": continue
        dir_path = input_path + '/' + dir_name
        file_list = os.listdir(dir_path) #디렉토리 내의 json 파일 목록을 받아옴
        for file_name in file_list:
            if file_name[-5:] != ".json": continue    #json 파일이 아니면 pass
            file_path = dir_path + '/' + file_name
            all_files.append(file_path)

    #all_files를 train, vaild, test용으로 나누기
    num_all_files = len(all_files)
    num_train_files = int(num_all_files*args.train_ratio/(args.train_ratio+args.val_ratio+args.test_ratio))
    num_valid_files = int((num_all_files-num_train_files)*args.val_ratio/(args.val_ratio+args.test_ratio))
    random.shuffle(all_files)
    train_files = all_files[:num_train_files]
    valid_files = all_files[num_train_files:num_train_files+num_valid_files]
    test_files = all_files[num_train_files+num_valid_files:]
    splited_file_list = [train_files, valid_files, test_files]
    identifiers = ["_train", "_val", "_test"]
    
    #train, vaild, test별 utterance 추출
    for idx, file_list in enumerate(splited_file_list):
        sentences = []                        #[q,a]들을 원소로 가지는 2차원 리스트 sentences
        ids = []                              #QA 질문 쌍이 같은 대화 뭉치에서 나왔는지를 구분하는 리스트 ids
        id = 0
        for file_path in tqdm(file_list):
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                json_data = json.load(f)
            try:
                utterances = [data['utterance'].strip() for data in json_data]
            except:
                utterances = [data['utterence'].strip() for data in json_data]  #json 파일 중 utterance가 utterence로 오타난 경우가 있어 예외 처리
            if "" in utterances: continue                                       #빈 문장이 있는 대화 pass
            len_utter = len(utterances)
            for i in range(0, len_utter-1, 2):
                sentences.append({'q': utterances[i], 'a': utterances[i+1]})
                ids.append('id_'+str(id))
            if len_utter%2:                                                 #대화의 마지막이 q로 끝날 경우 a를 빈 문장으로 채우기
                sentences.append({'q': utterances[-1], 'a': ""})
                ids.append('id_'+str(id))
            id+=1          
            f.close()

        QAs = pd.DataFrame(sentences, columns=["q","a"])    #질문 q와 그에 따른 응답 a를 쌍으로 담는 데이터프레임 QAs
        
        #QAs를 tsv파일로 추출
        QAs_path = args.output_path + '/' + args.qas_name + identifiers[idx] + ".tsv"
        QAs.to_csv(QAs_path, sep='\t', index=False)
        delete_first_line(QAs_path)     #칼럼(q, a)을 나타내는 첫 열 삭제

        #ids를 txt파일로 추출
        ids_path = args.output_path + '/' + args.ids_name + identifiers[idx] + ".txt"
        f = open(ids_path, 'w')
        for i in range(len(ids)):
            f.write(ids[i]+'\n')
        f.close()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, default="/Users/dannykm/Downloads/한국어 멀티턴 일상 대화 데이터셋 2022 v1.0 2")
    parser.add_argument("--output_path", type=str, default="/Users/dannykm/Downloads")
    parser.add_argument("--qas_name", type=str, default="Multi_turn_QA")
    parser.add_argument("--ids_name", type=str, default="ID")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train_ratio", type=float, default=90)
    parser.add_argument("--val_ratio", type=float, default=8)
    parser.add_argument("--test_ratio", type=float, default=2)
    args = parser.parse_args()

    random.seed(args.seed)
    generate_multi_turn_files(args)