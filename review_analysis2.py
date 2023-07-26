import pandas as pd
import numpy as np
from konlpy.tag import Okt
from collections import Counter

from sqlalchemy import create_engine
from tqdm import tqdm
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer

from analysis import get_dtm_array, get_words_freq



engine = create_engine("mysql+pymysql://root:123123@localhost/fcmm")


df = pd.read_excel("result/fcmm_review_cleaning.xlsx", index_col=0, sheet_name="cleaning2")
print(df.shape) #(11821, 8)

review_df = df[['id', 'product_code', 'writer', 'content']] #필요 컬럼만 추출
# print(review_df.isnull().sum()) # content에 499개 null값 존재

final_df = review_df.dropna() #null row 제거
print(final_df.shape) #(11338, 4)

okt = Okt()
words_list = []
cv = CountVectorizer() #객체선언

# 댓글 하나당 명사추출 후 문자열로 저장
sentence_num = final_df.shape[0]
# sentence_num = 1000
dtm_array, all_features = get_dtm_array(final_df, okt, cv, sentence_num, words_list)
#
# #분리된 모든 명사 txt파일로 저장
# # np.savetxt('result/all_words.txt', all_features, fmt='%s', delimiter=',', header='all_words', encoding='utf-8')

#dtm 저장
dtm_df = pd.DataFrame(dtm_array, columns=all_features) #데이터프레임 변환
print(f"original dtm_df shape: {dtm_df.shape}")


#-----불용어 가져오기
stopwords_file = open('result/stopwords.txt', 'r', encoding='utf-8')
stopwords_list = []
for line in stopwords_file.readlines()[1:]:
    stopwords_list.append(line.strip())
stopwords_file.close()
stopwords_list = [word for i, word in enumerate(stopwords_list) if not stopwords_list[i]==""]


#-----불용어 컬럼에서 제거
dtm_df = dtm_df.drop(stopwords_list, axis='columns')
print(f"remove stopwords dtm_df shape: {dtm_df.shape}")


#-----실제 dtm_df
real_col = [col for col in list(dtm_df) if dtm_df[col].sum() > 1]
dtm_df = dtm_df[real_col]
print(f"real dtm_df shape: {dtm_df.shape}")
# db저장
dtm_df.to_sql(name="dtm", con=engine, index=False, if_exists="replace")









    # words = [word for word in okt.nouns(content) if len(word)>1] #형태소로 분리 후 글자수가 1이상인 단어만
    # for word in words:
    #     words_list.append(word)


#--------------------------- wordcloud
# word_dict = Counter(words_list)
# tags = word_dict.most_common()
# print(dict(tags))

# wc = WordCloud(font_path='C:/Windows/Fonts/HMFMMUEX.TTC', background_color='white', width=800, height=600)
# cloud = wc.generate_from_frequencies(dict(tags))
# # cloud = wc.generate_from_frequencies(nouns_df_dict['freq'])
# plt.figure(figsize=(10, 8))
# plt.axis('off')
# plt.imshow(cloud)
# plt.show()
#------------------------------------


#-------------------------------- 단어 빈도분석
# word_count_df = pd.DataFrame.from_dict(word_dict, orient='index').reset_index() #데이터프레임으로 변환
# word_count_df.rename(columns={"index": "word", 0:"freq"}, inplace=True)
# word_count_df.sort_values(by=['freq'], ascending=False, inplace=True)
# word_count_df.to_excel("review_word_freq.xlsx", index=False) #엑셀저장
# word_count_df.to_excel("review_word_nouns_freq.xlsx", index=False) #엑셀저장
#------------------------------------












