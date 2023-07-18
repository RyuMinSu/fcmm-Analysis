import re

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from mysql import insert_category_tbl, insert_product_tbl

def create_driver():
    chrome_options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# category 정보
def get_object_class(driver, css_class):
    return driver.find_element(By.CLASS_NAME, css_class)

def get_objects_class(driver, css_class):
    return driver.find_elements(By.CLASS_NAME, css_class)

def get_objects_tag(driver, html_tag):
    return driver.find_elements(By.TAG_NAME, html_tag)

def get_object_tag(driver, html_tag):
    return driver.find_element(By.TAG_NAME, html_tag)

def move_page(tag_a):
    tag_a.click()
    time.sleep(1)

def back_page(driver):
    driver.back()
    time.sleep(1)

def click_more_btn(driver):
    while True:
        try:
            more_btn = get_object_class(driver, 'btnMore')
            more_btn.click()
            time.sleep(1)
        except:
            break


def create_soup(driver):
    product_box_html = driver.page_source
    soup = bs(product_box_html, 'html.parser')
    return soup

def get_product_info(soup, tbl_dict, start_num, end_num=None):
    product_list = soup.select('div.prdList__item')
    print(len(product_list))
    for product in product_list[start_num:end_num]:
        url = product.select_one('div.name').a['href']
        name = product.select_one('div.name').a['href'].split('/')[2]
        code = product.select_one('div.name').a['href'].split('/')[3]

        sales_box = product.select_one('ul.xans-element-.xans-product.xans-product-listitem.spec')
        sales_box_text = sales_box.get_text().strip().replace('\n', '')
        if '%' in sales_box_text:
            discount_pct = sales_box_text.split('%')[0]
            discount_pct = int(re.sub(r'[^0-9]', '', discount_pct))
        else:
            discount_pct = 0

        if '할인판매가 :' in sales_box_text:
            discount_price = int(sales_box_text.split('판매가 :')[1].replace(",",""))
        else:
            discount_price = 0

        if '판매가 :' in sales_box_text:
            try:
                org_price = int(sales_box_text.split('판매가 :')[2].replace(",",""))
            except:
                org_price = int(sales_box_text.split('판매가 :')[1].replace(",",""))
        else:
            org_price = 0

        # org_price = int(int(discount_price) / (int(discount_pct)/100))
        if product.select_one("div.crema_product_reviews_score__container"):
            review_num = product.select_one("div.crema_product_reviews_score__container").get_text().split(" : ")[1]
            review_num = int(review_num)
        else:
            review_num = 0

        tbl_dict['product_name'] = name
        tbl_dict['product_code'] = code
        tbl_dict['url'] = url
        tbl_dict['discount_price'] = discount_price
        tbl_dict['discount_pct'] = discount_pct
        tbl_dict['org_price'] = org_price
        tbl_dict['review_num'] = review_num

        # print(tbl_dict)
        insert_product_tbl(tbl_dict)



def get_segments(driver, cat_tag, css_class, start_num=0):
    cat_dict= {'category':cat_tag.text}
    product_dict = {'category': cat_tag.text}

    print(cat_tag.text, cat_tag.get_attribute('href'))
    move_page(cat_tag) #카테고리로 이동

    #segment
    CSS_CLASS = css_class
    segments = get_objects_class(driver, CSS_CLASS)
    for idx in range(len(segments)):
        segments = get_objects_class(driver, CSS_CLASS)
        segment_url = get_object_tag(segments[idx], 'a')

        cat_dict['segment'] = segment_url.text
        cat_dict['subsegment'] = ''
        print(cat_dict, end="\t")

        product_dict['segment'] = segment_url.text
        product_dict['subsegment'] = ''

        # insert_category_tbl(cat_dict) #db저장
        move_page(segment_url) #세그먼트 이동

        cond1 = "FCMM x WIND AND SEA"
        cond2 = "티셔츠"
        cond3 = "팬츠"

        if cat_dict['segment'] != (cond1 or cond2 or cond3):
            soup = create_soup(driver)
            get_product_info(soup, product_dict, start_num)  # 제품정보 가져오기
            back_page(driver)
        else:
            click_more_btn(driver) #더보기
            back_page(driver)
            time.sleep(1)
            soup = create_soup(driver)
            get_product_info(soup, product_dict, start_num) #제품정보 가져오기
            back_page(driver)

        # back_page(driver)



def get_sub_segments(driver, cat_tag, css_class, start_num=None):
    print(cat_tag.text, cat_tag.get_attribute('href'))
    cat_dict = {'category': cat_tag.text}
    product_dict = {'category': cat_tag.text}
    move_page(cat_tag)  # 카테고리로 이동

    # segment
    segments = get_objects_class(driver, css_class)
    for idx in range(len(segments)):
        segments = get_objects_class(driver, css_class)
        segment_url = get_object_tag(segments[idx], 'a')
        cat_dict['segment'] = segment_url.text
        product_dict['segment'] = segment_url.text
        move_page(segment_url)  #세그먼트 클릭함

        SUB_SEGMENT_CSS_CLASS = "xans-element-.xans-product.xans-product-displaycategory.xans-record-"
        sub_segments = get_objects_class(driver, SUB_SEGMENT_CSS_CLASS)
        for idx in range(len(sub_segments)):
            sub_segments = get_objects_class(driver, SUB_SEGMENT_CSS_CLASS)
            sub_segment_url = get_object_tag(sub_segments[idx], 'a')
            # print('\t\t', sub_segment_url.text, sub_segment_url.get_attribute('href'))
            cat_dict['subsegment'] = sub_segment_url.text
            product_dict['subsegment'] = sub_segment_url.text
            print(cat_dict, end='\t')
            # insert_category_tbl(cat_dict) #db저장
            sub_segment_url.click() #서브세그먼트 클릭
            time.sleep(1)

            cond1 = "패딩"
            cond2 = '롱슬리브'
            cond3 = '레깅스'
            cond4 = '가방'
            cond5 = '양말'

            if cat_dict['subsegment'] == "이너웨어":
                pass

            if cat_dict['subsegment'] == (cond1)or(cond2)or(cond3)or(cond4)or(cond5):
                soup = create_soup(driver) #페이지정보 가져오기
                time.sleep(1)
                get_product_info(soup, product_dict, start_num) #제품정보 가져오기
                back_page(driver)
            else:
                click_more_btn(driver)  # 더보기 클릭
                back_page(driver)
                soup = create_soup(driver)  # 페이지정보 가져오기
                get_product_info(soup, product_dict, start_num)  # 제품정보 가져오기
                time.sleep(1)
                back_page(driver)
        back_page(driver)


def get_sub_segments_sports(driver, cat_tag, css_class, start_num=None):
    print(cat_tag.text, cat_tag.get_attribute('href'))
    cat_dict = {'category': cat_tag.text}
    product_dict = {'category': cat_tag.text}

    move_page(cat_tag)  # 카테고리로 이동

    # segment
    segments = get_objects_class(driver, css_class)
    for idx in range(1,len(segments)):
        segments = get_objects_class(driver, css_class)
        segment_url = get_object_tag(segments[idx], 'a')
        # print('\t', segment_url.text, segment_url.get_attribute('href'))
        cat_dict['segment'] = segment_url.text
        product_dict['segment'] = segment_url.text
        move_page(segment_url)  #세그먼트 클릭함

        SUB_SEGMENT_CSS_CLASS = "xans-element-.xans-product.xans-product-displaycategory.xans-record-"
        sub_segments = get_objects_class(driver, SUB_SEGMENT_CSS_CLASS)
        for idx in range(len(sub_segments)):
            sub_segments = get_objects_class(driver, SUB_SEGMENT_CSS_CLASS)
            sub_segment_url = get_object_tag(sub_segments[idx], 'a')
            # print('\t\t', sub_segment_url.text, sub_segment_url.get_attribute('href'))
            cat_dict['subsegment'] = sub_segment_url.text
            print(cat_dict, end='\t')
            product_dict['subsegment'] = sub_segment_url.text
            # insert_category_tbl(cat_dict) #db저장
            sub_segment_url.click() #서브세그먼트 클릭
            time.sleep(1)
            if not cat_dict['subsegment'] == '용품':
                click_more_btn(driver)
                back_page(driver)
                soup = create_soup(driver)  # 페이지정보 가져오기
                get_product_info(soup, product_dict, start_num)  # 제품정보 가져오기
                back_page(driver)
            else:
                soup = create_soup(driver)  # 페이지정보 가져오기
                get_product_info(soup, product_dict, start_num)  # 제품정보 가져오기
                back_page(driver)
        back_page(driver)



# def get_review():




