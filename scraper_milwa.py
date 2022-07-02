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
from scraper import Support


class Milwa(Support):
    
    def __init__(self) -> None:
        super().__init__()
        self.names = []
        self.milwa = pd.read_excel('scraped_data/humilwaukeetooeu_data.xlsx')

        weight = None
        try:
            weight = self.milwa['Tömeg / Weight']
        except:
            self.milwa['Tömeg / Weight'] = None
            

       
    def milwa_menus(self) -> None:
        '''
        get all the categories and sub-categories
        '''
        # milwaku==>

        self.action = ActionChains(self.driver)

        self.item_cats = []
        
        time.sleep(1)

        head_menus = self.driver.find_element(By.CLASS_NAME, 'MainNavigationstyles__MenuContent-sc-1hrwdht-5').find_elements(By.CLASS_NAME, 'MainNavigationstyles__DesktopLink-sc-1hrwdht-7')[:2]
        print('head menus========>: ',len(head_menus))
        time.sleep(0.5)
        # menu_div = self.driver.find_element(By.CLASS_NAME, 'MainNavigationstyles__Dropdowns-sc-1hrwdht-10')

        # time.sleep(0.5)

        # menu_elements = main_menu > div [class = 'MainNavigationstyles__Dropdown-sc-1hrwdht-11'] [find all] -- for each > div [class= 'CategoryDropdownstyles__Wrapper-sddvhv-0']
        i = 0
        for item in head_menus:
        # menu_title = menu_elements > div [class = 'DropdownPromostyles__Promo-sc-17w56ch-0'].text
            menu_items = self.driver.find_elements(By.CLASS_NAME, 'MainNavigationstyles__Dropdown-sc-1hrwdht-11')
            print('menu div========>: ',len(menu_items))
            print(item.text)
            self.action.move_to_element(item).perform()
            time.sleep(0.02)
            menu = menu_items[i].find_element(By.CLASS_NAME, 'CategoryDropdownstyles__LinksArea-sddvhv-1').find_elements(By.TAG_NAME, 'div')
            for d in menu[0].find_elements(By.TAG_NAME, 'li'):
                self.action.move_to_element(d).perform()
                time.sleep(0.01)
                for d2 in menu[1].find_elements(By.TAG_NAME, 'li'):
                    self.action.move_to_element(d2).perform()
                    time.sleep(0.01)
                    sub_sub_menus = menu[2].find_elements(By.TAG_NAME, 'li')
                    if len(sub_sub_menus)==0:
                        for sub in sub_sub_menus:
                            hrefs = sub.find_element(By.TAG_NAME, 'a').get_attribute('href')
                            self.products_links.append(hrefs)
                    else:
                        for d3 in sub_sub_menus:
                            time.sleep(0.01)
                            hrefs = d3.find_element(By.TAG_NAME, 'a').get_attribute('href')
                            self.item_cats.append(hrefs)
        
            # print('we have got following categories', len(self.item_cats))

    # def direct(self, prod_no, dataframe) -> list:
    def direct(self) -> list:

        number = None
        code = None 
        name = None 
        description = None 
        props =None

        image_links = []

        link = self.driver.current_url

        jj = 0

        time.sleep(1)

        info_block = self.driver.find_element(By.CLASS_NAME, 'Containersstyles__Wide-sc-4y3gh1-2')
        desc = info_block.find_element(By.CLASS_NAME, 'MxFuelProductHerostyles__SidebarWrapper-sc-18aebu1-7')
        # images_block = info_block.find_element(By.CLASS_NAME, 'MxFuelProductHerostyles__MediaGrid-sc-18aebu1-2')

        name = desc.find_element(By.CLASS_NAME, 'MxFuelProductHerostyles__ProductTitle-sc-18aebu1-10').text
        self.milwa['Product name'][self.z]=name
        # code = desc.find_element(By.TAG_NAME, 'aside').find_element(By.TAG_NAME, 'small').text

        descript = desc.find_element(By.TAG_NAME, 'aside').find_element(By.CLASS_NAME, 'CollapsibleContentstyles__Container-sc-1skinik-0')

        descript.find_element(By.CLASS_NAME, 'CollapsibleContentstyles__OverlayContainer-sc-1skinik-3').find_element(By.TAG_NAME, 'button').click()

        # time.sleep(1)

        pps = descript.find_element(By.CLASS_NAME, 'CollapsibleContentstyles__ContentWrapper-sc-1skinik-1').find_element(By.CLASS_NAME, 'CollapsibleContentstyles__Content-sc-1skinik-2').find_elements(By.TAG_NAME, 'li')
        ele = '<ul>'
        for p in pps:
            li = '<li>'+p.text+'</li>'
            ele+=li
        ele+='</ul>'

        description = ele
        self.milwa['Rövid Leírás'][self.z]=description

        # props = self.driver.find_element(By.CLASS_NAME, 'mx-product-spec-section__inner').find_element(By.CLASS_NAME, "mx-product-spec__table").get_attribute('innerHTML')
        specs = self.driver.find_element(By.CLASS_NAME, 'mx-product-spec-section__inner').find_element(By.CLASS_NAME, 'mx-product-spec__table').find_elements(By.CLASS_NAME, "mx-product-spec__details-split")

        ele = '<ul>'
        for tr in specs:
            print('**************************************************======>: ', tr.text)
            divs = tr.find_elements(By.TAG_NAME, "div")
            th=  ''
            td= ''
            try:
                th = divs[0].text
                td = divs[1].text
            except:
                ...
            li = '<li><span>'+th+'</span><span>'+td+'</span></li>'
            ele+=li

        ele+='</ul>'
        props = ele
        self.milwa['Tulajdonságok'][self.z]=props
        
        print(f'\n+++++++   GOT THESE DETAILS:\n\nname: {name}\nPROPS: {props}\ndescription: {description} \t====================================')

        # wt = None

        # while True:
        #     if (wt and number) or jj==5:
        #         break
        #     for sp in specs:
        #         if 'SÚLY (KG)' in sp.text or 'Súly (kg)' in sp.text:
        #             wt = sp.find_elements(By.TAG_NAME, "div")[prod_no].text
        #         if 'Cikkszám' in sp.text or 'CIKKSZÁM' in sp.text:
        #             number = sp.find_elements(By.TAG_NAME, "div")[prod_no].text
        #     jj += 1

        # # images
        # time.sleep(1)
        # imgs = images_block.find_elements(By.TAG_NAME, "img")
        # for im in imgs:
        #     image_links.append(im.get_attribute('src'))

        # dd= pd.DataFrame({'Product number/Cikkszám':[number], 'Product Code':[code], 'Product name':[name],
        #                         'Rövid Leírás':[description], 'Tulajdonságok':[props], 
        #                         'Tömeg / Weight':[wt], 'Link':[link]})

        # df = pd.concat([dataframe,dd], axis=0, ignore_index=True)

        self.milwa.to_excel('scraped_data/humilwaukeetooeu_data.xlsx', index=False)

        # self.get_images(image_links, number, 'milwa')

        
    # def indirect(self, prod_no, dataframe, fuel=False):
    def indirect(self, prod_no, fuel=False):

        number = None
        code = None 
        name = None 
        description = None 
        props =None

        image_links = []

        link = self.driver.current_url

        time.sleep(1)

        if fuel==False:

            # images_block = self.driver.find_element(By.CLASS_NAME, 'product__carousel-container')

            descript = self.driver.find_element(By.CLASS_NAME, 'product__description-container')
            name = self.driver.find_element(By.CLASS_NAME, 'product__heading-title').find_element(By.TAG_NAME, 'h1').text
            self.milwa['Product name'][self.z]=name
            # code = descript.find_element(By.ID, 'p_lt_ctl01_pageplaceholder_p_lt_ctl01_MilwaukeeProductFeatures_ctl01').find_elements(By.TAG_NAME, 'h3')[1].text

            try:
                descript.find_element(By.CLASS_NAME, 'p_lt_ctl01_pageplaceholder_p_lt_ctl01_MilwaukeeProductFeatures_pnlFeatues').find_element(By.CLASS_NAME, 'product__description-expand').click()
            except:
                ...

            time.sleep(1)

            description = descript.find_element(By.CLASS_NAME, 'product__description-content').get_attribute('innerHTML')

            table = self.driver.find_element(By.CLASS_NAME, 'product__detail-table-container').find_element(By.CLASS_NAME, 'table-responsive')
            props = table.find_elements(By.TAG_NAME, "table")[1].get_attribute('innerHTML')

            specs = table.find_elements(By.TAG_NAME, "table")[1].find_elements(By.TAG_NAME, "tr")

            # soup = bs(props, 'html.parser')
            # trs = soup.find_all('tr')
            ele = '<ul>'
            for tr in specs[1:]:
                button = None
                try:
                    button = tr.find_element(By.TAG_NAME, "button")
                except:
                    ...
                if 'Letöltések'.upper() in tr.text or 'Letöltések' in tr.text or button:
                    break
                else:
                    print('**************************************************======>: ', tr.text)
                    th=  ''
                    td= ''
                    try:
                        th = tr.find_element(By.TAG_NAME, "th").text
                        # td = tr.find_elements(By.TAG_NAME, "td")[prod_no].text
                        td = tr.find_element(By.TAG_NAME, "td").text
                    except:
                        ...
                    li = '<li><span>'+th+'</span><span>'+td+'</span></li>'
                    ele+=li

            ele+='</ul>'

            props = ele
            self.milwa['Tulajdonságok'][self.z]=props

            pps = descript.find_element(By.CLASS_NAME, 'product__description-content').find_elements(By.TAG_NAME, "p")
            ele = '<ul>'
            for p in pps:
                li = '<li>'+p.text+'</li>'
                ele+=li
            ele+='</ul>'

            description = ele
            self.milwa['Rövid Leírás'][self.z]=description


            # time.sleep(1)

            # wt = None

            # jj = 0
            # while True:
            #     if (wt and number) or jj==10:
            #         break
            #     for sp in specs:
            #         if 'Súly' in sp.find_element(By.TAG_NAME, "th").text:
            #             wt = sp.find_elements(By.TAG_NAME, "td")[prod_no].text
            #         if 'Cikkszám' == sp.find_element(By.TAG_NAME, "th").text:
            #             number = sp.find_elements(By.TAG_NAME, "td")[prod_no].text
            #     jj += 1
            #     if jj == 5:
            #         break

            # images
            # imgs = images_block.find_element(By.CLASS_NAME, "product__carousel-nav-holder").find_element(By.CLASS_NAME, "slick-track").find_elements(By.TAG_NAME, "img")
            # for im in imgs:
            #     image_links.append(im.get_attribute('src'))

        elif fuel:
            images_block = self.driver.find_element(By.CLASS_NAME, 'ProductToolOverviewstyles__Media-yjlkwn-1')

            time.sleep(1)

            descript = self.driver.find_element(By.CLASS_NAME, 'ProductToolOverviewstyles__Content-yjlkwn-2').find_element(By.CLASS_NAME, 'ProductDetailsContentstyles__Container-x8zwy7-0')
            descript_divs = descript.find_elements(By.CLASS_NAME, 'ProductDetailsContentstyles__Section-x8zwy7-6')
            name = descript_divs[0].find_element(By.TAG_NAME, 'h1').text
            code = descript_divs[2].find_element(By.TAG_NAME, 'h3').text

            try:
                descript.find_element(By.CLASS_NAME, 'p_lt_ctl01_pageplaceholder_p_lt_ctl01_MilwaukeeProductFeatures_pnlFeatues').find_element(By.CLASS_NAME, 'product__description-expand').click()
            except:
                ...

            time.sleep(1)

            description = self.driver.find_element(By.CLASS_NAME, 'ProductFeaturesTextstyles__FeatureListWrapper-fxqvf2-2').get_attribute('innerHTML')

            self.driver.execute_script(f"window.scrollTo(0, 1000)")
            # self.driver.find_elements(By.CLASS_NAME, 'ProductNavigationstyles__Item-u9dnmk-3')[2].find_elements(By.TAG_NAME, 'a')[0].click()
            self.driver.execute_script("document.getElementsByClassName('ProductNavigationstyles__Item-u9dnmk-3')[2].getElementsByTagName('a')[0].click()")
            
            # try:
            #     self.action.move_to_element(technical).perform()
            # except:
            #     ...
            # technical.find_element(By.TAG_NAME, 'a').click()
            time.sleep(1)
            
            # technical_portion = technical_data.find_elements(By.CLASS_NAME, 'Gridstyles__Full-y0t80q-3')[1]
            spec_container = self.driver.find_element(By.CLASS_NAME, 'ProductSpecificationsstyles__Container-sc-1lyanq9-12')
            spec_divs = spec_container.find_elements(By.CLASS_NAME, 'ProductSpecificationsstyles__HeaderRow-sc-1lyanq9-8')
            for spec in spec_divs[1:]:
                spec.click()
                time.sleep(.5)

            spec_props = self.driver.find_elements(By.CLASS_NAME, 'ProductSpecificationsstyles__Row-sc-1lyanq9-9')

            time.sleep(1)

            wt = None
            jj = 0
            while True:
                if (wt and number) or jj==5:
                    break
                for spp in spec_props:
                    spans = spp.find_elements(By.TAG_NAME, 'span')
                    if spans[0].text=='CIKKSZÁM' or spans[0].text=='Cikkszám':
                        number=spans[1].text
                    if 'SÚLY' in spans[0].text or 'Súly ' in spans[0].text:
                        wt=spans[1].text
                jj += 1
                if jj == 5:
                    break

            props = self.driver.find_element(By.CLASS_NAME, "ProductSpecificationsstyles__Table-sc-1lyanq9-3").get_attribute('innerHTML')


            # images
            imgs = images_block.find_elements(By.TAG_NAME, "img")
            for im in imgs:
                image_links.append(im.get_attribute('src'))

        print(f'\n+++++++   GOT THESE DETAILS:\n\nname: {name}\nPROPS: {props}\ndescription: {description} \t====================================')

        # dd= pd.DataFrame({'Product number/Cikkszám':[number], 'Product Code':[code], 'Product name':[name],
        #                         'Rövid Leírás':[description], 'Tulajdonságok':[props], 
        #                         'Tömeg / Weight':[wt], 'Link':[link]})

        # df = pd.concat([dataframe,dd], axis=0, ignore_index=True)

        # df.to_excel('scraped_data/hu.milwaukeetoo.eu-sample.xlsx', index=False)
        self.milwa.to_excel('scraped_data/humilwaukeetooeu_data.xlsx', index=False)

        # self.get_images(image_links, number, 'milwa')
        


    # def milwa_details(self, product_link, file_name):
    def milwa_details(self, product_link):
        '''
        this method will get details of the product
        '''

        # milwa = pd.read_excel(file_name)

        
        '''
        Product number
        product code
        product name
        Rövid Leírás = short description
        Tulajdonságok = properties
        Tömeg / Weight
        Link
        '''

        # product_cards = self.milwa_products(product_link)

        # if product_cards or len(product_cards)>0:
        #     for p in product_cards:
        #         href = p.find_element(By.TAG_NAME, 'a').get_attribute('href')
        #         self.milwa_details(href, file_name=file_name)
        # else:


        # products = self.milwa_products(product_link)
        # if len(products)>0:
        #     for pr in products:
        #         self.products_links.append(pr)
        # else:
        self.open_url(product_link)
        time.sleep(1)

            # try:
            #     self.driver.find_element(By.CLASS_NAME, 'MxFuelProductHerostyles__DropdownItem-sc-18aebu1-15').click()
            #     time.sleep(1)
            # except:
            #     ...
            
        vars = None
        try:
            time.sleep(1)
            vars = self.driver.find_elements(By.CLASS_NAME, 'MxFuelProductHerostyles__DropdownItem-sc-18aebu1-15')
            vars_count = len(vars)
        except:
            ...
        
        if vars:
            #     for i in range(vars_count):
            #         self.driver.find_elements(By.CLASS_NAME, 'MxFuelProductHerostyles__DropdownItem-sc-18aebu1-15')[i].click()
            #         time.sleep(1)

            self.direct()

                    # self.driver.find_element(By.CLASS_NAME, 'MxFuelProductHerostyles__DropdownItem-sc-18aebu1-15').click()
                    # vars = self.driver.find_elements(By.CLASS_NAME, 'MxFuelProductHerostyles__DropdownItem-sc-18aebu1-15')

        else:
            try:
                time.sleep(1)
                    # vars = self.driver.find_element(By.CLASS_NAME, 'product__description-container').find_element(By.ID, 'p_lt_ctl01_pageplaceholder_p_lt_ctl01_MilwaukeeProductFeatures_ucVariantsList').find_element(By.CLASS_NAME, 'slick-list').find_elements(By.TAG_NAME, 'slick-slide')
                vars = self.driver.find_element(By.CLASS_NAME, 'product__description-container')
            except:
                ...

            if vars:
                #     vars_count = len(vars)
                #     for i in range(vars_count):
                #         vars[i].click()
                #         time.sleep(1)

                self.indirect(0)

                # else:
                #     try:
                #         time.sleep(1)
                #         vars = self.driver.find_element(By.CLASS_NAME, 'ProductDetailsContentstyles__Variants-x8zwy7-9').find_elements(By.CLASS_NAME, 'ProductDetailsContentstyles__VariantCard-x8zwy7-10')
                #         vars_count = len(vars)
                #     except:
                #         ...

                #     # try:
                #     if len(vars)>0:
                #     #         for i in range(vars_count):
                #     #             vars[i].click()
                #         time.sleep(1)

                #         self.indirect(0, milwa, True)

                    # except:
                    #     ...

        print(f'**********>>>   NOW TOTAL RECORDS IN OUR EXCEL FILE: {self.milwa.shape[0]} **')

                
    def milwa_products(self, link):
        '''
        this method will get prodcust from a category
        '''

        self.open_url(link)

        time.sleep(.5)

        self.driver.execute_script(f"window.scrollTo(0, window.scrollY-window.outerHeight)")  # scroll
        time.sleep(.03)

        try:
            self.driver.find_element(By.CLASS_NAME, 'product-listing__footer').click()
        except:
            ...


        product_cards = []
        y = 0
        while True:
            time.sleep(.5)
            try:
                product_cards = self.driver.find_element(By.CLASS_NAME, 'ProductListstyles__ProductList-gvaq0h-12').find_elements(By.CLASS_NAME, 'ProductCardstyles__Card-s4r2k5-0')
            except:
                ...
            y += 1
            if len(product_cards)>0 or y==5:
                break

        for p in product_cards:
            href = p.find_element(By.TAG_NAME, 'a').get_attribute('href')
            self.products_links.append(href)
        print(f'****=========>>>> Received {len(product_cards)} products from the link: {link}')
        
        return product_cards
            
    def milwa_data(self):
        '''
        this method will apply get_details or get_products
        '''

        # cur_dir = os.curdir
        # scrap_dir = os.path.join(cur_dir, 'scraped_data')

        # maliwa = os.path.join(cur_dir, f'scraped_data/humilwaukeetooeu_data.xlsx')
        # for cat in self.item_cats:
        #     self.milwa_products(cat)
        self.z=1
        # self.products_links = pd.read_csv('milwa_products_links.csv')['product_links']
        self.products_links = self.milwa['Link']
        # link_count = 0
        for link in self.products_links[self.z:68]:
            # self.milwa_details(link, maliwa)
            print(f'============>>>     ITTERATION: {self.z}, LINK: {link}')
            self.milwa_details(link)
            self.z+=1
            # if link == 'https://hu.milwaukeetool.eu/hu-hu/ontolasos-furok/':
            #     link_count+=1
            # if link_count>0:
            # links_data = pd.DataFrame({'product_links':self.products_links})
            # links_data.to_csv('milwa_products_links.csv', index=True)


if __name__ == "__main__":
    official_links = ['https://hu.milwaukeetool.eu', 'https://hu.ryobitools.eu',
                            'https://www.aeg-powertools.eu/hu-hu']

    # MILWA **************
    milwa = Milwa()
    name_link = milwa.open_url(official_links[0])
    # milwa.milwa_menus()
    milwa.milwa_data()
    milwa.driver.quit()
