import re

from expactor.mysql import *
import pandas as pd
import numpy



sql = """
    SELECT * FROM REVIEW
"""
sql_col = """
    SELECT COLUMN_NAME
    FROM (
        SELECT *
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE 1=1 AND TABLE_NAME='REVIEW'
        ) C;
"""

result = read_url(sql)
columns = read_url(sql_col)
columns = [obj[0] for obj in columns]

df = pd.DataFrame(result, columns=columns)
df.columns = map(lambda x: x.lower(), df.columns) #컬럼 소문자로
print(df.shape)
#
# print(len(df[(df['writer']=="FCMM*")]['content']))
#
content_nums = df[(df['writer']=="FCMM*")]['content'].index
print(len(content_nums))
#
for num in content_nums:
    # print("org:", df.loc[num, 'content'])
    if "포토후기키" in df.loc[num, 'content']:
        content0 = df.loc[num, 'content'].split('포토후기')[0]
        content1 = df.loc[num, 'content'].split('포토후기')[1].replace('cm','').replace("kg","")
        if '서포터즈' in content0:
            if "쇼핑몰 추천" in content0.split('서포터즈')[0]:
                # print("서포터즈:", "")
                df.loc[num, 'content'] = ""
            else:
                # print('서포터즈:', content0.split('서포터즈')[0])
                df.loc[num, 'content'] = content0.split('서포터즈')[0]

        # print("포토후기키:", content1)
        df.loc[num, 'writer_option'] = content1

    elif "포토후기" in df.loc[num, 'content']:
        content0 = df.loc[num, 'content'].split('포토후기')[0]
        content1 = df.loc[num, 'content'].split('포토후기')[1].replace('cm','').replace("kg","")
        if '서포터즈' in content0:
            if "쇼핑몰 추천 리뷰" in content0.split('서포터즈')[0]:
                # print("서포터즈:", "")
                df.loc[num, 'content'] = ""
            else:
                # print("서포터즈:", content0.split('서포터즈')[0])
                df.loc[num, 'content'] = content0.split('서포터즈')[0]
        # print("포토후기:", content1)
        df.loc[num, 'writer_option'] = content1

print(df.shape)

writer = pd.ExcelWriter('fcmm_review_cleaning.xlsx')
df.to_excel(writer, sheet_name='cleaning1')


writer_options = df['writer'].index
for idx in writer_options:
    #writer_option 클리닝
    if '착용' in str(df.loc[idx, 'writer_option']):
        df.loc[idx, 'content'] = df.loc[idx, 'writer_option'].split('착용')[1]
        df.loc[idx, 'writer_option'] = df.loc[idx, 'writer_option'].split('착용')[0]

    #불용어 제거
    df.loc[idx, 'writer_option'] = str(df.loc[idx, 'writer_option']).replace('cm', '').replace('kg', '')

    #content 숫자와 영어 제거
    df.loc[idx, 'content'] = re.sub('[^가-힣 ]', '', str(df.loc[idx, 'content']))


df.to_excel(writer, sheet_name='cleaning2')
writer.close()










