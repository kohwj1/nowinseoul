import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select


class IndexTestCase(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(30)
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.driver.get('https://nowinseoul.makemyproject.net')

    def test_01_site_access(self):
        self.assertEqual(self.driver.current_url, 'https://nowinseoul.makemyproject.net/ko/')
        self.assertEqual(self.driver.title, 'Now in Seoul')

    def test_02_featured_attractions(self):
        self.assertEqual(self.driver.find_element(By.XPATH, '//*[@id="attractions-container"]/div[1]/a/div[2]').text, '강남 MICE 관광특구')
        self.assertEqual(self.driver.find_element(By.XPATH, '//*[@id="attractions-container"]/div[1]/a/div[1]/img').get_attribute('src'), 'https://nowinseoul.makemyproject.net/static/images/attraction/600/POI001.webp')

        self.driver.find_element(By.XPATH, '/html/body/form/div[1]/label[4]').click()

        self.assertEqual(self.driver.find_element(By.XPATH, '//*[@id="attractions-container"]/div[2]/a/div[2]').text, '남산공원')
        self.assertEqual(self.driver.find_element(By.XPATH, '//*[@id="attractions-container"]/div[2]/a/div[1]/img').get_attribute('src'), 'https://nowinseoul.makemyproject.net/static/images/attraction/600/POI091.webp')

    def test_03_gotomap(self):
        self.driver.find_element(By.XPATH, '/html/body/form/div[2]').click()
        
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div')))
        self.assertEqual(self.driver.current_url, 'https://nowinseoul.makemyproject.net/ko/map')

    def test_04_localized(self):        
        Select(self.driver.find_element(By.XPATH, '//*[@id="lang-select"]')).select_by_value('ja')      
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.current_url, 'https://nowinseoul.makemyproject.net/ja/')
        self.driver.get(self.driver.current_url)
        self.assertEqual(self.driver.find_element(By.XPATH, '//*[@id="attractions-container"]/div[1]/a/div[2]').text, '江南MICE観光特区')
        self.assertEqual(self.driver.find_element(By.XPATH, '/html/body/form/div[2]/a').text, 'マップで探す')

        Select(self.driver.find_element(By.XPATH, '//*[@id="lang-select"]')).select_by_value('en')
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.current_url, 'https://nowinseoul.makemyproject.net/en/')
        self.driver.get(self.driver.current_url)
        self.assertEqual(self.driver.find_element(By.XPATH, '//*[@id="attractions-container"]/div[1]/a/div[2]').text, 'Gangnam MICE Special Tourist Zone')
        self.assertEqual(self.driver.find_element(By.XPATH, '/html/body/form/div[2]/a').text, 'Browse on Map')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=3)