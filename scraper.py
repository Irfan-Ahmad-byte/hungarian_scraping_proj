from lib2to3.pgen2 import driver
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
from concurrent.futures import ProcessPoolExecutor

options = ChromeOptions()
# add anti_captch plugin
# options.add_extension('anticaptcha-plugin_v0.62.crx')
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("start-maximized")
# options.add_argument("disable-infobars")
# options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
# options.add_experimental_option("detach", True)

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

class Support():
    
    def __init__(self) -> None:
        super().__init__()
        self.official_links = ['https://hu.milwaukeetool.eu', 'https://hu.ryobitools.eu',
                                'https://www.aeg-powertools.eu/hu-hu']
    
        self.cur_dir = os.curdir
        self.driver_path = os.path.join(self.cur_dir, 'chromedriver')


        self.pages = []         # list containing page sources of elements to fetch articles from
        self.sleeps = np.random.randint(1, 5, 5)

        self.products_links = []

        self.driver = Remote(
            command_executor='http://localhost:4444',
            options=options, keep_alive=True
            )
        self.session_id = self.driver.session_id
        self.driver.maximize_window()

    def open_url(self, url) -> None:
        '''
        This method tries different support URLs for the platform specified. If any of the specified URls works,
        it'll return that with platform name. Otherwise it'll try Google search to find out.
        params:
                name: str: name of the platform
        returns:
                name
                supportURL
        '''
        # self.driver = Chrome()
        
        time.sleep(0.2)
        try:
            self.driver.get(url)
            # WebDriverWait(self.driver, 10, 3)
        except:
            # self.driver = Remote(
            #     command_executor='http://localhost:4444',
            #     options=options, keep_alive=True
            #     )
            # try:
            #     # self.driver.start_session({'session id': self.session_id})
            # except:
            self.driver.start_session({})

            self.driver.maximize_window()        # WebDriverWait(self.driver, 10, 3)
            time.sleep(0.2)
            self.driver.get(url)

        time.sleep(.1)

        try:
            Alert(self.driver).dismiss()
        except:
            ...

        # cookie handler for maliwa
        try:
            self.driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
            # main-menus = MainNavigationstyles__Dropdowns-sc-1hrwdht-10
            time.sleep(random.choice(self.sleeps))
        except:
            ...

        return self.driver.current_url

    def menus(self, which='maliwa') -> None:
        '''
        get all the categories and sub-categories
        '''
        # milwaku==>

        self.action = ActionChains(self.driver)

        self.item_cats = []

        manu_cursor = self.driver.find_element(By.CLASS_NAME, 'SiteNavigationstyles__TopLinks-sc-1oyb1pz-2').find_elements(By.TAG_NAME, 'span')[0]
        self.action.move_to_element(manu_cursor)
        menu_container = self.driver.find_element(By.CLASS_NAME, 'SiteNavigationstyles__DropdownLinks-sc-1oyb1pz-8')
        menu_sub_containers = menu_container.find_elements(By.CLASS_NAME, 'SiteNavigationstyles__Subnav-sc-1oyb1pz-9')

        for con in menu_sub_containers:
            cont = con.find_elements(By.TAG_NAME, 'a')
            for sb in cont:
                href = sb.get_attribute('href')
                self.item_cats.append(href)

        # menu_elements_cats = menu_elements = menu_elements > div [class = 'CategoryDropdownstyles__LinksArea-sddvhv-1'] > div [find all]

    def get_details(self, product_link, file_name, which='maliwa'):
        '''
        this method will get details of the product
        '''

        milwa = pd.read_excel(file_name)

        weight = None
        try:
            weight = milwa['Tömeg / Weight']
        except:
            milwa['Tömeg / Weight'] = None
            

        
        '''
        Product number
        product code
        product name
        Rövid Leírás = short description
        Tulajdonságok = properties
        Tömeg / Weight
        Link
        '''

        if which == 'ryobi':
            self.open_url(product_link)
            time.sleep(4)
            '''
            Product number
            product code
            product name
            Rövid Leírás = short description
            Tulajdonságok = properties
            Tömeg / Weight
            Link
            '''
            number = None
            code = None
            name = None
            description = None
            preperties = None
            this_weight = None
            link = product_link

            innerheight = self.driver.execute_script('return window.innerHeight')
            scroll = (innerheight/2) +100
            self.driver.execute_script(f"window.scrollTo(0, {scroll})")
            time.sleep(0.5)
            table = None
            try:
                table = self.driver.find_elements(By.CLASS_NAME, 'Gridstyles__ContentWithLeftAside-y0t80q-9')[0].find_element(By.CLASS_NAME, 'ProductDetailSpecificationsstyles__SpecTable-gaf953-2')
            except:
                table = self.driver.find_elements(By.CLASS_NAME, 'Gridstyles__ContentWithLeftAside-y0t80q-9')[1].find_element(By.CLASS_NAME, 'ProductDetailSpecificationsstyles__SpecTable-gaf953-2')
            if not table:
                return
            # self.driver.execute_script(f"arguments[0].scrollIntoView();", table)
            info_cells = table.find_elements(By.CLASS_NAME, 'ProductDetailSpecificationsstyles__Header-gaf953-4')
            time.sleep(.3)
            print(f'*********** INFO CELLS ===>: {len(info_cells)}')
            # jump = 100
            for ic in info_cells:
                try:
                    ic.click()
                except:
                    self.action.click(ic).perform()
                # self.action.move_to_element(ic).perform()
                # self.driver.execute_script(f"window.scrollTo(0, window.innerHeight/2+{jump})")
                # jump+=100

            detail = self.driver.find_elements(By.CLASS_NAME, 'ProductDetailSpecificationsstyles__Content-gaf953-5')
            print(f'*********** DETAIL CELLS ===>: {len(detail)}')
            for dt in detail:
                divs = dt.find_elements(By.CLASS_NAME, 'ProductDetailSpecificationsstyles__Attribute-gaf953-6')
                for dv in divs:
                    spans = dv.find_elements(By.TAG_NAME, 'span')
                    # print(f'*************************************************{spans[0].text}: {spans[1].text}******************')
                    if spans[0].text == 'Cikkszám':
                        number = spans[1].text
                        # print(f'*************************************************{spans[0].text}: {number}******************')
                    elif 'Súly' in spans[0].text:
                        this_weight = spans[1].text
                        # print(f'*************************************************{spans[0].text}: {this_weight}******************')
                    # ic.click()

            code = self.driver.find_element(By.CLASS_NAME, 'ProductDetailsstyles__Model-hb5d0o-3').text
            name = self.driver.find_element(By.CLASS_NAME, 'ProductDetailsstyles__Title-hb5d0o-2').text

            try:
                self.driver.find_element(By.CLASS_NAME, 'ReadMorestyles__Button-cmut7d-2').click()
            except:
                ...
            try:
                description = self.driver.find_element(By.CLASS_NAME, 'ReadMorestyles__Container-cmut7d-1').get_attribute('innerHTML').split('</h4>')[1]
            except:
                ...

            preperties = table.get_attribute('innerHTML')

            dd= pd.DataFrame({'Product number/Cikkszám':[number], 'Product Code':[code], 'Product name':[name],
                                'Rövid Leírás':[description], 'Tulajdonságok':[preperties], 
                                'Tömeg / Weight':[this_weight], 'Link':[link]})

            df = pd.concat([milwa,dd], axis=0, ignore_index=True)

            df.to_excel('scraped_data/hu.ryobytools.eu-sample.xlsx', index=False)
            # images

            image_links = []
            imgs = self.driver.find_elements(By.CLASS_NAME, 'ProductHeroCarouselstyles__Wrapper-sc-1f8ohem-7')[0].find_elements(By.TAG_NAME, 'img')
            for im in imgs:
                src = im.get_attribute('src')
                image_links.append(src)

            # with ProcessPoolExecutor(6) as exe:
            #     exe.map(self.get_images, images_links, [number for _ in range(len(images_links))], ['ryoby' for _ in range(len(images_links))])

            self.get_images(image_links, number, 'ryoby')


        elif which == 'aeg':
            self.open_url(product_link)
            time.sleep(4)
            '''
            Product number
            product code
            product name
            Rövid Leírás = short description
            Tulajdonságok = properties
            Tömeg / Weight
            Link
            '''
            number = None
            code = None
            name = None
            description = None
            properties = None
            this_weight = None
            link = product_link

            content = self.driver.find_element(By.CLASS_NAME, 'aeg-product-content')

            name = content.find_element(By.TAG_NAME, 'h1').text
            code = content.find_element(By.TAG_NAME, 'h3').text

            table = self.driver.find_element(By.CLASS_NAME, 'aeg-comparison-table')
            props_headers = table.find_element(By.CLASS_NAME, 'ct-headers').find_element(By.CLASS_NAME, 'ct-specifications-list').find_elements(By.TAG_NAME, 'li')

            num_ct = 0
            sl_ct = 0
            i=0
            for nm in props_headers:
                if nm.text == 'Cikkszám' : num_ct = i
                if 'Súly' in nm.text and '(kg)' in nm.text: sl_ct = i
                i += 1

            props_vals = table.find_element(By.CLASS_NAME, 'ct-products').find_element(By.CLASS_NAME, 'ct-specifications-list').find_elements(By.TAG_NAME, 'li')
            number = props_vals[num_ct].text
            this_weight = props_vals[sl_ct].text

            description = self.driver.find_element(By.CLASS_NAME, 'aeg-product-content').get_attribute('innerHTML')
            properties = table.get_attribute('innerHTML')

            dd= pd.DataFrame([[number,code, name, description, properties, this_weight, link]], 
                                columns=['Product number/Cikkszám', 'Product Code', 'Product name','Rövid Leírás', 'Tulajdonságok','Tömeg / Weight', 'Link']
                                )

            df = pd.concat([milwa,dd], axis=0, ignore_index=True)

            df.to_excel('scraped_data/aeg-powertools.eu hu-hu-sample.xlsx', index=False)

            images_links = []
            imgs = self.driver.find_elements(By.CLASS_NAME, 'aeg-product-image-thumbnail-gallery-image')

            print(f'Found {len(imgs)} images for number: {number}')

            for im in imgs:
                img = im.find_element(By.TAG_NAME, 'img').get_attribute('src')
                images_links.append(img)

            # with ProcessPoolExecutor(6) as exe:
            #     exe.map(self.get_images, images_links, [number for _ in range(len(images_links))], ['aeg' for _ in range(len(images_links))])
            self.get_images(images_links, number, 'aeg')
            

    def get_images(self, imgs_links:list, number, dir):
        cur_dir = os.curdir
        img_dir = os.path.join(cur_dir, f'scraped_data/images/{dir}')

        i = 1
        for link in imgs_links:
            if i == 1:
                img_name = str(number)
            else:
                img_name = str(number) + '_altpic' + str(i-1)
            ext = link.split('?')[0].split('.')[-1]
            i+=1

            subprocess.run(f'wget -O {img_dir}/{img_name}.{ext} {link}', shell=True)

    def pager(self, count) -> list:
        pagers_ls = []
        pagers = None
        try:
            pagers = self.driver.find_element(By.CLASS_NAME, 'ProductListstyles__Pagination-gvaq0h-13').find_elements(By.TAG_NAME, 'li')
            pagers = [pg.find_element(By.TAG_NAME, 'a') for pg in pagers]
        except:
            ...
        if pagers:
            for pg in pagers:
                # lab = pg.find_element(By.CLASS_NAME, 'a').get_attribute('aria-label')
                if pg.text == count or pg.text == str(count):
                    try:
                        pg.click()
                    except:
                        ...
                    pagers_ls.append(pg)
                
        return pagers_ls

    def get_products(self, link):
        '''
        this method will get prodcust from a category
        '''

        self.driver.get(link)

        time.sleep(5)

        self.driver.execute_script(f"window.scrollTo(0, document.body.offsetHeight)")  # scroll
        time.sleep(5)


        try:
            self.action.move_to_element(self.driver.find_element(By.CLASS_NAME, 'btn-show-more')).click()
            time.sleep(2)
        except:
            ...

        products_container = self.driver.find_element(By.CLASS_NAME, 'aeg-product-list__container')
        product_cards = products_container.find_elements(By.CLASS_NAME, 'aeg-product')

        for p in product_cards:
            href = p.find_element(By.TAG_NAME, 'a').get_attribute('href')
            self.products_links.append(href)

        
    def get_data(self):
        '''
        this method will apply get_details or get_products
        '''

        cur_dir = os.curdir
        scrap_dir = os.path.join(cur_dir, 'scraped_data')


        for cat in self.item_cats:
            self.get_products(cat)
            for link in self.products_links:
                aeg = os.path.join(cur_dir, f'scraped_data/aeg-powertools.eu hu-hu-sample.xlsx')
                self.get_details(link, aeg, which='aeg')


if __name__ == "__main__":
    official_links = ['https://hu.milwaukeetool.eu', 'https://hu.ryobitools.eu',
                            'https://www.aeg-powertools.eu/hu-hu']

    # AEG **************
    support = Support()
    name_link = support.open_url(official_links[2])
    support.menus()
    support.get_data()
    support.driver.quit()
