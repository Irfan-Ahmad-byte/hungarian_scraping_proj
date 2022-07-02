import random
import subprocess
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome, ChromeOptions, Remote
import time
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
from scraper import Support

options = ChromeOptions()
# add anti_captch plugin
# options.add_extension('anticaptcha-plugin_v0.62.crx')
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("start-maximized")
# options.add_argument("disable-infobars")
# options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")


'''
This module will:
1- find support URL
2- open support URL
3- save page source, get all topics
4- for each topic URL
    i- open URL
    ii- save page source
    iii- get support URLs and their titles
'''

class Ryobi(Support):
    
    def __init__(self) -> None:
        super().__init__()
        self.ryo_ini = 0
        self.cat_ini = 1
        self.sub_cat_ini = 10
        self.sub_sub_cat_ini = 0
        self.cat_len = 0
        self.sub_cat_len = 0
        self.sub_sub_cat_len = 0      
        self.link_counter = 0  

    def ryo_menu(self) -> None:
        '''
        get all the categories and sub-categories
        '''
        self.action = ActionChains(self.driver)
        self.driver.execute_script(f"window.scrollTo(0,-document.body.offsetHeight)")
        self.item_cats = []
        time.sleep(.5)
        print('current link:===========>>>>>>>>:  ', self.driver.current_url)
        menu_btn = self.driver.find_element(By.CLASS_NAME, 'MainNavigationstyles__IconsItems-sc-1hrwdht-11').find_elements(By.TAG_NAME, 'div')
        try:
            menu_btn[4].click()
        except:
            menu_btn[5].click()
        time.sleep(.1)
        # self.cat_dropdown = self.driver.find_element(By.CLASS_NAME, 'MobileCategoryDropdownstyles__MobileDropdown-sc-1db5zuy-0').find_element(By.TAG_NAME, 'ul')

        manu_cursor = self.driver.find_elements(By.CLASS_NAME, 'CategoryDropdownstyles__Link-kkzqgd-9')
        i = 0
        for mn in manu_cursor:
            print(mn.text)
            mn.click()
            if i == 0:
                break

        self.cats1 = self.driver.find_elements(By.CLASS_NAME, 'CategoryDropdownstyles__Link-kkzqgd-9')


    def ryo_products(self):
        products = []
        self.driver.execute_script(f"window.scrollTo(0, document.body.offsetHeight)")
        # self.driver.execute_script(f"window.scrollTo(0, (window.scrollY-(window.innerHeight/2)))")
        pagers_ls = self.pager(1)
        i = 1
        while True:
            if i == 1:
                ...
            else:
                scroll_y = self.driver.execute_script('return window.scrollY')
                outer_height = self.driver.execute_script('return window.outerHeight')
                scroll = (scroll_y-outer_height)+250
                self.driver.execute_script(f'window.scrollTo(0, {scroll})')

                pagers_ls = self.pager(i)
                if  len(pagers_ls)==0:
                    break

                print(f'***====>>> THIS IS PAGE NUMBER: {pagers_ls[0].text}')
                # self.action.move_to_element(pagers_ls[0]).perform()
                # pagers_ls[0].click()
                # self.action.click(pagers_ls[0]).perform()
                # self.driver.execute_script('window.scrollTo(0, window.scrollY-window.innerHeight/2)')

            i+=1
            # self.driver.execute_script(f"window.scrollTo(0, document.body.offsetHeight)")
                
            time.sleep(.03)
            product_cards = None
            try:
                product_cards = self.driver.find_elements(By.CLASS_NAME, 'ProductCardstyles__Card-oapqic-0')
            except:
                ...
            if product_cards:
                for p in product_cards:
                    href = p.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    products.append(href)
        return products

    def ryo_explore(self):
        '''
        this will explore the menu using ryo_menu method return when needed
        '''
        cur_dir = os.curdir

        self.ryo_menu()

        time.sleep(.3)
        while True:

            categories = self.driver.find_elements(By.CLASS_NAME, 'CategoryDropdownstyles__Link-kkzqgd-9')
            if self.cat_len ==0:
                self.cat_len = (categories)
            categories[self.cat_ini].click()
            print(f'now on category: {self.cat_ini}')
            
            sub_cats = self.driver.find_elements(By.CLASS_NAME, 'CategoryDropdownstyles__Link-kkzqgd-9')
            if self.sub_cat_len == 0:
                self.sub_cat_len = len(sub_cats)
            sub_cats[self.sub_cat_ini].click()
            
            sub_sub_cats = []
            try:
                sub_sub_cats = self.driver.find_elements(By.CLASS_NAME, 'CategoryDropdownstyles__Link-kkzqgd-9')
            except:
                ...
            print(f'now on sub category: {self.sub_cat_ini}')

            if len(sub_sub_cats)>0 and self.sub_sub_cat_len == 0:
                self.sub_sub_cat_len = len(sub_sub_cats)
            if len(sub_sub_cats)>0:
                sub_sub_cats[self.sub_sub_cat_ini].click()
                print(f'now on sub sub category: {self.sub_sub_cat_ini}')

                self.sub_sub_cat_ini += 1


            time.sleep(1)
            products = self.ryo_products()

            # for prd in products:
            #     self.products_links.append(prd)

            print(f'saved {len(products)} for current itteration')
            i = 1
            for link in products:
                if 'https://hu.ryobitools.eu/kerti-szerszamok/gyepgondozas/funyirok/ry18lmx37a/ry18lmx37a-150/' in link:
                    self.link_counter +=1
                if self.link_counter>0:
                    print(f'saving record number: {i}, in the dataset for the link: ', link)
                    ryo = os.path.join(cur_dir, f'scraped_data/hu.ryobytools.eu-sample.xlsx')
                    self.get_details(link, ryo, which='ryobi')
                    i+=1

        #     13- if sub_sub_cat_ini == sub_sub_cat_len:
            if self.sub_sub_cat_ini == self.sub_sub_cat_len:
                self.sub_sub_cat_ini = 0
                self.sub_sub_cat_len = 0
                self.sub_cat_ini += 1
        #     16- if sub_cat_ini == sub_cat_len:
            if self.sub_cat_ini == self.sub_cat_len:
                self.sub_cat_ini = 0
                self.sub_cat_len = 0
                self.cat_ini += 1
        #     19- if cat_ini == cat_len:
        #             break
            if self.cat_ini == self.cat_len:
                break

            self.driver.execute_script(f"window.scrollTo(0, document.body.offsetHeight-document.body.clientHeight)")            
            self.ryo_menu()


if __name__ == "__main__":

    official_links = ['https://hu.milwaukeetool.eu', 'https://hu.ryobitools.eu',
                            'https://www.aeg-powertools.eu/hu-hu']

    # RYOBY **************
    ryo = Ryobi()
    name_link = ryo.open_url(official_links[1])
    time.sleep(5)
    ryo.ryo_explore()
    ryo.driver.quit()
