import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from misc import open_new_tab, switch_to_tab

#Your Access Keys
# page_id_1 = 'ondrej.plasil.714'
# facebook_access_token_1 = 'EAADydX7GE7MBALBtnyqrMs3oPMZBo0oG9RmCnedIZAofxdgrQ4qSvj3Pk6IZC8GaJ3pkuhm8cKR8DMnY8YbSN0qE3EfL5r0WT652M31EFsmfyIPyUb4WQGrUyqI0Hy1qsLRbpEVixc8k9YfZAXAZBmfEaOZB4p6uoW4B0EM9MpAs85R3bmWee2swilK9I4IEZBjuqZB4VuFO7AZDZD'
# msg = 'Purple Ombre Bob Lace Wig Natural Human Hair now available on https://lace-wigs.co.za/'
# post_url = 'https://graph.facebook.com/{}/feed'.format(page_id_1)
# payload = {
# 'message': msg,
# 'access_token': facebook_access_token_1
# }
# r = requests.post(post_url, data=payload)
# print(r.text)


def create_facebook_instance(driver, username, password):
    open_new_tab(driver, 1)
    login(driver, username, password)
    switch_to_tab(driver, 0)

def login(driver, username, password):
    WEBSITE_URL = "https://facebook.com"
    driver.get(WEBSITE_URL)

    button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button._42ft._4jy0._9o-t._4jy3._4jy1.selected._51sy"))
    )
    button.click()

    driver.find_element_by_xpath("//input[@type='text']").send_keys(username)
    driver.find_element_by_xpath("//input[@type='password']").send_keys(password)

    button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button._42ft._4jy0._6lth._4jy6._4jy1.selected._51sy"))
    )
    button.click()

# FB instance must exists before running this function
def like_facebook_page(driver, url):
    switch_to_tab(driver, 1)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.j83agx80.btwxx1t3.taijpn5t"))
    )

    driver.get(url)

    like_button_selector = "div.j83agx80.bp9cbjyn > div.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.pq6dq46d.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.n00je7tq.arfg74bv.qs9ysxi8.k77z8yql.l9j0dhe7.abiwlrkh.p8dawk7l.cbu4d94t.taijpn5t.k4urcfbm"

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, like_button_selector))
        )

        like_button = driver.find_element_by_css_selector(like_button_selector)
        if("To se mi líbí" in like_button.text or "Přidat se ke skupině" in like_button.text):
            like_button.click()
    except Exception as e:
        switch_to_tab(driver, 0)
        return False

    switch_to_tab(driver, 0)
    return True
    

