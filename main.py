
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from bots.twitter_bot import follow_twitter_user, retweet, get_twitter_api_auth
from bots.youtube_bot import get_authenticated_service, add_subscription
from bots.telegram_bot import join_telegram_channel
from bots.facebook_bot import create_facebook_instance, like_facebook_page
import asyncio
import ctypes
import time

from misc import close_active_tab, switch_to_tab

def login_to_cmc(driver, username, password):
        login_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-111rrsy-0.qbrWo > button.x0o17e-0.qrNYy"))
            )
        driver.execute_script("arguments[0].click();", login_button)
        WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            )
        driver.find_element_by_xpath("//input[@type='email']").send_keys(username)
        driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
        driver.find_element_by_css_selector('button.x0o17e-0.ffwHVz').click()

def main(accounts_index_arr):
    for index in accounts_index_arr:
        

        load_dotenv()

        MessageBox = ctypes.windll.user32.MessageBoxW
        youtube_service = get_authenticated_service('client_secret_' + index + '.json')
        link_to_retweeted_post = ''
        error_messages = []

        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(chrome_options=chrome_options)

        # Login to facebook
        create_facebook_instance(driver, os.getenv('FB_USERNAME_' + index), os.getenv('FB_PASS_' + index))

        twitter_api_auth = get_twitter_api_auth(
            os.getenv('TWITTER_API_KEY_' + index), 
            os.getenv('TWITTER_API_KEY_SECRET_' + index),
            os.getenv('TWITTER_ACCESS_TOKEN_' + index),
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET_' + index)
        )

        driver.get("https://coinmarketcap.com" + "/airdrop/ongoing/")

        table = driver.find_element_by_class_name("cmc-table")
        table_body = table.find_element_by_tag_name("tbody")
        projects = table_body.find_elements_by_tag_name("tr")

        links_to_projects = []

        for project in projects:
            link = project.find_element_by_css_selector("td > a").get_attribute('href')
            links_to_projects.append(link)


        login_to_cmc(driver, os.getenv('CMC_USERNAME_' + index), os.getenv('CMC_PASS_' + index))
        WebDriverWait(driver, 120).until_not(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.t8xka3-0.clxZon.modalOpened"))
                        )
        try:
            for link in links_to_projects:
                driver.get(link)

                coin_name = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.sc-16r8icm-0.gpRPnR.nameHeader > h2"))
                )
                coin_name = coin_name.text
                print('')
                print('##############################################################')
                print("PROCESSING: " + coin_name)
                print('##############################################################')     

                # Get JOIN THIS AIRDROP BUTTON
                try:
                    button = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "button.x0o17e-0.kzspeM"))
                        )
                    driver.execute_script("arguments[0].click();", button)
                except Exception as e:
                    print('Already participated in coin: ' + str(coin_name))
                    continue

                # Get action tasks from modal
                WebDriverWait(driver, 120).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.qgaiwz-0.hMjMnh > div"))
                    )
                actions = driver.find_elements_by_css_selector('div.qgaiwz-0.hMjMnh > div')

                error_happened = False
                for action in actions:
                    is_requirement_action = True
                    is_input_field_action = True
                    is_checkbox_action = True

                    instruction = None
                    action_element = None
                    try:
                        instruction = action.find_element_by_css_selector('span').text
                        action_element = action.find_element_by_css_selector('button')
                    except Exception as e:
                        is_requirement_action = False
                        try:
                            instruction = action.find_element_by_css_selector('p').text
                            action_element = action.find_element_by_css_selector('input')
                        except Exception as e:
                            is_input_field_action = False
                            try:
                                action_element = action.find_element_by_css_selector('label')
                            except Exception as e:
                                is_checkbox_action = False
                    if(instruction != None):
                        print('\n' + instruction)

                    if (is_requirement_action):
                        if all(words in instruction for words in ['Add', 'Watchlist']):
                            action_element.click()

                        elif all(words in instruction for words in ['Follow', 'Twitter']):
                            link_to_follow = action_element.find_element_by_css_selector("a").get_attribute('href')
                            page_to_follow = link_to_follow.split('/')[-1]
                            follow_twitter_user(page_to_follow, twitter_api_auth)

                        elif all(words in instruction for words in ['Retweet', 'post']):
                            link_to_retweet = action_element.find_element_by_css_selector("a").get_attribute('href')
                            page_to_retweet = link_to_retweet.split('/')[-1].split('?')[0]
                            retweet(page_to_retweet, twitter_api_auth)
                            link_to_retweeted_post = link_to_retweet

                        elif all(words in instruction for words in ['Follow', 'YouTube']):
                            link = action_element.find_element_by_css_selector("a").get_attribute('href')
                            id = link.split('/')[-1]
                            add_subscription(youtube_service, id)

                        elif all(words in instruction for words in ['Join', 'Telegram']):
                            link = action_element.find_element_by_css_selector("a").get_attribute('href')
                            id = link.split('/')[-1]
                            asyncio.run(join_telegram_channel([id], os.getenv('TELEGRAM_API_ID_' + index), os.getenv('TELEGRAM_API_HASH_' + index)))

                        elif all(words in instruction for words in ['Follow ', 'Facebook']):
                            link = action_element.find_element_by_css_selector("a").get_attribute('href')
                            id = link.split('/')[-1]
                            success = like_facebook_page(driver, link)
                            if(not success):
                                error_messages.append(coin_name)
                                error_messages.append('Failed to like facebook page using link: ' + link + "\n")
                                error_happened = True
                                break
                        else:
                            print('Cannot find instruction: ' + instruction)
                            error_messages.append(coin_name)
                            error_messages.append(instruction + "\n")
                            error_happened = True
                            break
                    elif(is_input_field_action): 
                        if "Binance Smart Chain Wallet Address" in instruction:
                            action_element.send_keys(os.getenv('BINANCE_SMART_CHAIN_WALLET_ADDRESS_' + index))
                        elif "Ethereum Wallet Address" in instruction:
                            action_element.send_keys(os.getenv('ETH_WALLET_ADDRESS_' + index))
                        elif "Twitter Handle" in instruction:
                            action_element.send_keys(os.getenv('TWITTER_HANDLE_' + index))
                        elif "Facebook Handle" in instruction:
                            action_element.send_keys(os.getenv('FACEBOOK_HANDLE_' + index))
                        elif "YouTube Handle" in instruction:
                            action_element.send_keys(os.getenv('YOUTUBE_HANDLE_' + index))
                        elif "Telegram Handle" in instruction:
                            action_element.send_keys(os.getenv('TELEGRAM_HANDLE_' + index))
                        elif "Link to retweeted post" in instruction:
                            if(link_to_retweeted_post == ''):
                                print('Retweeted post is empty: ' + instruction)
                                error_messages.append("coin: " + coin_name)
                                error_messages.append("instruction: " + instruction + "\n")
                                error_happened = True
                                break
                            action_element.send_keys(link_to_retweeted_post)
                        else:
                            print('Cannot find instruction: ' + instruction)
                            error_messages.append(coin_name)
                            error_messages.append(instruction + "\n")
                            error_happened = True
                            break
                    elif (is_checkbox_action): # checkboxes part
                        try:
                            driver.execute_script("arguments[0].click();", action_element)
                        except Exception as e:
                            action_element.click() 

                if (not error_happened):
                    time.sleep(1)
                    join_airdrop_button = driver.find_element_by_css_selector('div.t8xka3-0.clxZon.modalOpened > div > div.t8xka3-3.jKeeFQ > p > button')    
                    driver.execute_script("arguments[0].click();", join_airdrop_button)
                    # join_airdrop_button.click()
                    time.sleep(1)
                    #Sometimes captcha is required to solve here
                    WebDriverWait(driver, 600).until_not(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.t8xka3-0.clxZon.modalOpened"))
                        )
        except Exception as e:
            print(e)
            print("####################\n" + "FAILED COINS\n" + "####################")
            for message in error_messages:
                print(message)

        for message in error_messages:
            print(message)

        switch_to_tab(driver, 1)
        close_active_tab(driver)
        driver.close()

main(["2"])