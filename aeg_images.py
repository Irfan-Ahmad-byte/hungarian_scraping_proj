import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver import Remote
import time
import pandas as pd
from scraper import Support

sup = Support()

aeg = pd.read_excel('./scraped_data/aeg_cp_data.xlsx')

i = 0
for _ in aeg['Product number/Cikkszám']:
    num = aeg['Product number/Cikkszám'][i]
    link = aeg['Link'][i]
    
    print(f'******* Now extracting IMAGES for result number: {i+1} *******')
    sup.open_url(link)
    time.sleep(1)
    # images_links = []

    image_slider = sup.driver.find_elements(By.CLASS_NAME, 'aeg-product-image-thumbnail-gallery-image')

    j = 1
    print(f'Found {len(image_slider)} images for number: {num}')

    for im in image_slider:
        img = im.find_element(By.TAG_NAME, 'img').get_attribute('src')
        # images_links.append(img)
        print(f'Downloading images for number: {num}, from link: {img}')
        if j == 1:
            img_name = str(num)
        else:
            img_name = str(num) + '_altpic' + str(j-1)
        ext = img.split('?')[0].split('.')[-1]

        subprocess.run(f'wget -O ./scraped_data/images/aeg/{img_name}.{ext} {link} -q --show-progress', shell=True)
        j+=1
    i+=1
