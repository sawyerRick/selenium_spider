from selenium import webdriver
import os, pprint

driver = webdriver.Chrome()
user_url = 'https://www.zhihu.com/people/giantchen/activities'
sex_dict = {"他":"男", "她":"女"}
data_dict = {}


def crawl_detail(url):
    driver.get(user_url)
    driver.find_element_by_xpath(r"//*[@id='ProfileHeader']/div/div[2]/div/div[2]/div[3]/button").click()
    user_id = sex = driver.find_element_by_xpath(r"//*[@id='ProfileHeader']/div/div[2]/div/div[2]/div[1]/h1/span[1]").text
    sex = driver.find_element_by_xpath(r"//*[@id='Profile-activities']/div[1]/h4/span").text[0]
    industry = driver.find_element_by_xpath(r"//*[@id='ProfileHeader']/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div").text
    career_exp = driver.find_elements_by_class_name("ProfileHeader-field")
    remark = driver.find_element_by_xpath(r"//*[@id='ProfileHeader']/div/div[2]/div/div[2]/div[2]/div/div/div[5]/div").text
    global data_dict
    data_dict = {
        "user_id": user_id,
        "sex": sex_dict[sex],
        "industry": industry,
        "career_exp": [exp.text for exp in career_exp],
        "remark": remark
    }
    

if __name__ == "__main__":
    crawl_detail(user_url)
    pprint.pprint(data_dict)
    os.system('pause')
    driver.close()