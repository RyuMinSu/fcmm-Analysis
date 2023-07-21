import pandas as pd
import numpy as np
from konlpy.tag import Okt
from collections import Counter

df = pd.read_excel("fcmm_review_cleaning.xlsx", index_col=0, sheet_name="cleaning2")
print(df.shape) #(11821, 8)

review_df = df[['id', 'product_code', 'writer', 'content']] #필요 컬럼만 추출
# print(review_df.isnull().sum()) # content에 499개 null값 존재

final_df = review_df.dropna() #null row 제거
print(final_df.shape) #(11322, 4)

okt = Okt()
words_list = []
for content in final_df['content']:
    words = [word for word in okt.morphs(content) if len(word)>1] #형태소로 분리 후 글자수가 1이상인 단어만
    for word in words:
        words_list.append(word)

word_dict = Counter(words_list)

word_count_df = pd.DataFrame.from_dict(word_dict, orient='index').reset_index() #데이터프레임으로 변환
word_count_df.rename(columns={"index": "word", 0:"freq"}, inplace=True)
word_count_df.sort_values(by=['freq'], ascending=False, inplace=True)
word_count_df.to_excel("review_word_freq.xlsx", index=False) #엑셀저장