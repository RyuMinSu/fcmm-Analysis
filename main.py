from expactor.fcmm import *
from expactor.mysql import insert_category_tbl



#접속
url = "https://www.fcmm.kr/index.html"

driver = create_driver()

driver.get(url)
driver.maximize_window()
driver.implicitly_wait(5)

CATEGORY_CSS_CLASS = "xans-element-.xans-layout.xans-layout-category.top_category"
navbar = get_object_class(driver, CATEGORY_CSS_CLASS)
navbar_btns = get_objects_tag(navbar, "li") #네비게이션 버튼 가져오기

for index in range(6, len(navbar_btns)-1): #순회하며 정보 가져오기
# for index in range(4,5):
    navbar = get_object_class(driver, CATEGORY_CSS_CLASS)
    navbar_btn = get_objects_tag(navbar, "li")[index]

    #category
    cat_btn = navbar_btn.find_element(By.TAG_NAME, 'a')
    SEGMENT_CSS_CLASS = "xans-element-.xans-product.xans-product-displaycategory.xans-record-"

    if cat_btn.text == "럭키데이":
        get_segments(driver, cat_btn, SEGMENT_CSS_CLASS, 1)
    elif cat_btn.text == '베스트':
        cat_dict = {'category':cat_btn.text, 'segment': '', 'subsegment': ''}
        product_dict = {'category':cat_btn.text, 'segment': '', 'subsegment': ''}
        print(cat_dict)
        # insert_category_tbl(cat_dict) #db저장
        move_page(cat_btn) #카테고리로 이동
        time.sleep(1)
        click_more_btn(driver)
        back_page(driver)
        soup = create_soup(driver)
        get_product_info(soup, product_dict, 0, end_num=-1)
        back_page(driver)
    elif cat_btn.text == '신상품':
        cat_dict = {'category': cat_btn.text, 'segment': '', 'subsegment': ''}
        product_dict = {'category': cat_btn.text, 'segment': '', 'subsegment': ''}
        print(cat_dict)
        # insert_category_tbl(cat_dict)  # db저장
        move_page(cat_btn)  # 카테고리로 이동
        time.sleep(1)
        click_more_btn(driver) #더보기
        back_page(driver)
        soup = create_soup(driver)
        get_product_info(soup, product_dict, 1)
        back_page(driver)
    elif cat_btn.text == '프로모션':
        cat_dict = {'category': cat_btn.text, 'segment': '', 'subsegment': ''}
        product_dict = {'category': cat_btn.text, 'segment': '', 'subsegment': ''}
        print(cat_dict)
        # insert_category_tbl(cat_dict)  # db저장
        move_page(cat_btn)  # 카테고리로 이동
        time.sleep(1)
        soup = create_soup(driver)
        get_product_info(soup, product_dict, 1)
        back_page(driver)
    elif cat_btn.text == '라이프스타일 웨어':
        get_sub_segments(driver, cat_btn, SEGMENT_CSS_CLASS)
        back_page(driver)
    elif cat_btn.text == '스포츠 웨어':
        get_sub_segments_sports(driver, cat_btn, SEGMENT_CSS_CLASS)
        back_page(driver)
    else:
        get_segments(driver, cat_btn, SEGMENT_CSS_CLASS, 0)




























