import csv
from selenium import webdriver
import time
from parsel import Selector
from selenium.webdriver.common.keys import Keys


file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]
writer = csv.writer(open('testing.csv', 'w'))
writer.writerow(['Name', 'Designation', 'Location', 'Mail', ])

driver = webdriver.Firefox()

driver.get('https://www.linkedin.com/')

driver.find_element_by_xpath('//a[text()="Sign in"]').click()

username_input = driver.find_element_by_name('session_key')
username_input.send_keys(username)

password_input = driver.find_element_by_name('session_password')
password_input.send_keys(password)


driver.find_element_by_xpath('//button[text()="Sign in"]').click()


driver.get('https://www.google.com')

search_query = driver.find_element_by_name('q')
linkedin_base = 'site:linkedin.com/in/'
google_base=input('Enter Your Criteria')
search_query.send_keys(linkedin_base+ " AND " + google_base)
search_query.send_keys(Keys.RETURN)
time.sleep(3)

linkedin_urls = driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
linkedin_urls = [profile.get_attribute('href') for profile in linkedin_urls]
time.sleep(0.5)

print(linkedin_urls)

for linkedin_url in linkedin_urls:
    try:
        driver.get(linkedin_url)
        time.sleep(5)
        sel = Selector(text=driver.page_source)

        name = sel.xpath('//title/text()').extract_first().split(' | ')[0]

        if name:
            name = name.strip()

        Designation = sel.xpath('//h2/text()').extract_first().strip()

        if Designation:
            job_title = Designation.strip()

        company = ' , '.join(sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract())

        if company:
            company = company.strip()



        location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()

        if location:
            location = location.strip()

        linkedin_url = driver.current_url
        writer.writerow([name.encode('utf-8'),
                         Designation.encode('utf-8'),
                         company.encode('utf-8'),
                         location.encode('utf-8'),
                         linkedin_url.encode('utf-8')])

    except:
        print('error')

driver.quit()