import time
import math
from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import JavascriptException
from PIL import Image
from utils import filex, jsonx


from covid19_icta._utils import log

URL = 'https://vaccine.covid19.gov.lk/sign-in'
HEIGHT = 1350
ASPECT_RATIO = 8 / 9
WIDTH = HEIGHT * ASPECT_RATIO
WEBSITE_LOAD_WAIT_TIME = 2


def _run():
    return True


def scrape():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(URL)
    browser.set_window_size(WIDTH, HEIGHT)

    image_file = '/tmp/covid19_icta.latest.png'
    browser.save_screenshot(image_file)
    log.info('Saved screenshot to %s', image_file)

    try:
        browser.execute_script(
            "document.getElementsByClassName('jss22')[0].style.maxHeight = '100000px';"
        )
        time.sleep(WEBSITE_LOAD_WAIT_TIME)

        table_centers = browser.find_element_by_class_name('jss22')
        table_image_file = '/tmp/covid19_icta.latest.table.png'
        table_centers.screenshot(table_image_file)

        # reshape image
        im = Image.open(table_image_file)
        (width, height) = im.size
        k = math.floor(math.sqrt(ASPECT_RATIO * height / width))
        PADDING_RATIO = 1.01
        new_width = (int)(PADDING_RATIO * width * k)
        new_height = (int)(PADDING_RATIO * height / k)
        im2 = Image.new(im.mode, (new_width, new_height), 0)
        for i in range(0, k):
            left, right = 0, width
            upper = (int)(i * height / k)
            lower = (int)((i + 1) * height / k)
            im_sub = im.crop((left, upper, right, lower))
            im2.paste(im_sub, ((int)(i * width * PADDING_RATIO), 0))
        im2.save(table_image_file)

        log.info('Saved table screenshot to %s', table_image_file)

    except JavascriptException as e:
        table_image_file = None
        log.error(e)

    html = browser.page_source
    browser.quit()

    html_file = '/tmp/covid19_icta.latest.html'
    filex.write(html_file, html)
    log.info('Saved page source to %s', html_file)


    return html, image_file, table_image_file


def parse_center_list(html):
    soup = BeautifulSoup(html, 'html.parser')
    div_message = soup.find('div', class_='jss23')
    message = div_message.text.strip()
    log.info('message = %s', message)

    tr_list = soup.find_all('tr', class_='MuiTableRow-root')
    center_list = []
    for tr in tr_list:
        td_list = tr.find_all('td', class_='MuiTableCell-body')
        if not td_list:
            continue
        [date, center, dose, age] = [td.text for td in td_list]
        moh_area, __, center_name = center.partition(' | ')
        date = str(parse(date))[:10]

        center = dict(
            date=date,
            center=center,
            moh_area=moh_area,
            center_name=center_name,
            dose=dose,
            age=age,
        )
        center_list.append(center)

    data = dict(
        center_list=center_list,
    )
    data_file = '/tmp/covid19_icta.latest.json'
    jsonx.write(data_file, data)
    log.info('Saved data for %d centers to %s', len(center_list), data_file)

    return center_list
