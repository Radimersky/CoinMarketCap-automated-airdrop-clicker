from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

def open_new_tab(driver, tab_index):
    # Open a new window
    driver.execute_script("window.open('');")
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[tab_index])
    time.sleep(2)

def close_active_tab(driver):
    # close the active tab
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)

def switch_to_tab(driver, tab_index):
    driver.switch_to.window(driver.window_handles[tab_index])
    time.sleep(2)
    