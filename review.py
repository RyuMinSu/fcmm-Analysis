import traceback

from expactor.mysql import read_url, insert_review_tbl
from expactor.fcmm import *
import pandas as pd

import time
import re

sql = """
    SELECT *
    FROM (
        SELECT category, segment, subsegment, PRODUCT_CODE, REVIEW_NUM, SUBSTRING_INDEX(URL, '/', 4) AS new_url, ROW_NUMBER() OVER(PARTITION BY PRODUCT_CODE ORDER BY category) AS RNUM
        FROM PRODUCT
        ) S
    WHERE S.RNUM=1 AND REVIEW_NUM>=1;
"""

result = read_url(sql) # 튜플

driver = create_driver()

df = pd.DataFrame(result, columns=['category', 'segment', 'subsegment', 'product_code', 'review_num', 'new_url', 'rnum'])
print(df.shape)

product_codes = df['product_code'].tolist()
for idx, code in enumerate(product_codes):
    review_dict = {'code': code}

    url = f"https://review5.cre.ma/fcmm.kr/products/reviews?product_code={code}"
    print(idx, url)

    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(5)

    while True:
        try:
            soup = create_soup(driver)  # 박스정보 가져오기
            total_rate = soup.select_one('span.products_reviews_summary_v2__score_text').get_text().replace('.0','')
            reviews = soup.select("li.js-review-container")
            for review in reviews:
                writer_rate = review.select_one("div.review_list_v2__score_star span").get_text().split(": ")[1].replace("점","")
                title = review.select_one("div.review_list_v2__score_text").get_text().strip()
                content = review.select_one(
                    "div.review_list_v2__message.js-collapsed-review-content.js-translate-text").get_text().strip()
                content = re.sub('[^가-힣a-zA-Z0-9 ]','', content)

                writer = review.select_one(
                    "div.review_list_v2__user_name_message"
                ).get_text().strip().split("님의 리뷰입니다.")[0]
                if review.select_one("div.review_list_v2__options_section"):
                    writer_option = review.select_one(
                        "div.review_list_v2__options_section"
                    ).get_text().strip().replace("\n", ":").replace(":::::", ":::")
                else:
                    writer_option = ""

                review_dict['total_rate'] = total_rate
                review_dict["writer"] = writer
                review_dict["writer_rate"] = writer_rate
                review_dict["title"] = title
                review_dict['content'] = content
                review_dict['writer_option'] = writer_option
                print(review_dict)
                # print(idx, code, total_rate, writer, writer_rate, content,writer_option)

                insert_review_tbl(review_dict)

            next_btn = get_object_class(driver, "pagination__button.pagination__button--next")
            next_btn.click()
            time.sleep(.5)
        except Exception as ex:
            break
