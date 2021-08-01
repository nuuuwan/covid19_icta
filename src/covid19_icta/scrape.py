import time

from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import filex, jsonx

from covid19_icta._utils import log

URL = 'https://vaccine.covid19.gov.lk/sign-in'
HEIGHT = 1440
WIDTH = HEIGHT * 16 / 9
WEBSITE_LOAD_WAIT_TIME = 2


def _run():
    return True


def scrape():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(URL)
    browser.set_window_size(WIDTH, HEIGHT)
    time.sleep(WEBSITE_LOAD_WAIT_TIME)

    image_file = '/tmp/covid19_icta.latest.png'
    browser.save_screenshot(image_file)
    log.info('Saved screenshot to %s', image_file)

    html = browser.page_source
    browser.quit()

    html_file = '/tmp/covid19_icta.latest.html'
    filex.write(html_file, html)
    log.info('Saved page course to %s', html_file)

    return html, image_file


def parse_and_tweet(html, image_file):
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
        date = str(parse(date))[:10]

        center = dict(
            date=date,
            center=center,
            dose=dose,
            age=age,
        )
        center_list.append(center)

    data = dict(
        message=message,
        center_list=center_list,
    )
    data_file = '/tmp/covid19_icta.latest.json'
    jsonx.write(data_file, data)
    log.info('Saved data for %d centers to %s', len(center_list), data_file)

    return message, center_list
