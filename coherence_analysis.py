from sqlalchemy import create_engine
from tqdm import tqdm

from mysql import read_url
import pandas as pd
import numpy as np




engine = create_engine("mysql+pymysql://root:123123@localhost/fcmm")

data_sql = """
    select * from dtm
"""
column_sql = """
    SELECT COLUMN_NAME
    FROM (
        SELECT *
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE 1=1 AND TABLE_NAME='dtm'
        ) C;
"""

result = read_url(data_sql)
columns = read_url(column_sql)
columns = [col[0] for col in columns]
df = pd.DataFrame(result, columns=columns)
print(df.shape)

df_cols = list(df)


#-----단어 빈도수 저장할 dictionary
count_dict = {}
for doc_number in tqdm(range(df.shape[0])):
    row = df.loc[doc_number] # 로우 가져오기
    for i, word1 in enumerate(df_cols): #컬럼 순회
        if row[word1]: #첫번째 단어 있으면
            for j in range(i+1, len(df_cols)): #두번째 컬럼 부터 순회
                if row[df_cols[j]]: #두번째 단어 있으면
                    # print(df_cols[i], df_cols[j]) #있는 애들끼리 출력
                    #dict에 저장
                    count_dict[df_cols[i], df_cols[j]] = count_dict.get((df_cols[i], df_cols[j]), 0) + max(row[word1], row[df_cols[j]])
# print(count_dict)


#-----word1, word2, freq형태로 저장
count_list = []
for words in count_dict: #키만 출력
    count_list.append([words[0], words[1], count_dict[words]])

#-----동시출현빈도 df저장
df = pd.DataFrame(count_list, columns=['word1','word2','freq'])
df = df.sort_values(by=['freq'], ascending=False)
df = df.reset_index(drop=True)
print(df.head())

df.to_sql("coherence", con=engine, index=False, if_exists="replace")
print("완료")







