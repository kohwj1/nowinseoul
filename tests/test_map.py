import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select


class MapTestCase(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(30)
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.driver.get('https://nowinseoul.makemyproject.net/ko/map')

    def test_01_page_access(self):
        self.assertEqual(self.driver.title, 'Map :: Now in Seoul')

    def test_02_marker_init(self):
        self.assertEqual(len(self.driver.find_elements(By.CLASS_NAME, 'leaflet-marker-icon')), 80)

    def test_03_search_by_placename_and_reset(self):
        input_field = self.driver.find_element(By.XPATH, '//*[@id="mapSearch"]')
        btn_search = self.driver.find_element(By.XPATH, '//*[@id="btnSearch"]')
        input_field.clear()
        input_field.send_keys('남산공원')
        btn_search.click()
        
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'leaflet-popup')))
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'leaflet-popup').is_displayed())
        
        self.driver.find_element(By.XPATH, '//*[@id="btnReset"]').click()
        self.assertEqual(len(self.driver.find_elements(By.CLASS_NAME, 'leaflet-marker-icon')), 80)

    def test_04_map_filter(self):
        filter_food = self.driver.find_element(By.XPATH, '//*[@id="filterForm"]/div[2]/div/label[1]')
        filter_freeflow = self.driver.find_element(By.XPATH, '//*[@id="filterForm"]/div[3]/div/label[2]')

        filter_food.click()
        self.assertEqual(len(self.driver.find_elements(By.CLASS_NAME, 'leaflet-marker-icon')), 22)

        filter_food.click()
        self.assertEqual(len(self.driver.find_elements(By.CLASS_NAME, 'leaflet-marker-icon')), 80)
        
        filter_freeflow.click()
        self.assertEqual(self.driver.find_element(By.CLASS_NAME, 'leaflet-marker-icon').get_attribute('src'), 'https://nowinseoul.makemyproject.net/static/images/ui/marker_0.png')

    def test_05_localized(self):        
        Select(self.driver.find_element(By.XPATH, '//*[@id="lang-select"]')).select_by_value('ja')      
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.current_url, 'https://nowinseoul.makemyproject.net/ja/map')
        self.driver.get(self.driver.current_url)
        self.assertEqual(self.driver.find_element(By.XPATH, '//*[@id="filterForm"]/div[1]/p').text, '場所名で検索')
        self.assertEqual(self.driver.find_element(By.XPATH, '//*[@id="filterForm"]/div[3]/div/label[1]').text, '全て')

        Select(self.driver.find_element(By.XPATH, '//*[@id="lang-select"]')).select_by_value('en')
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.current_url, 'https://nowinseoul.makemyproject.net/en/map')
        self.driver.get(self.driver.current_url)
        self.assertEqual(self.driver.find_element(By.XPATH, '//*[@id="filterForm"]/div[1]/p').text, 'Search by place name')
        self.assertEqual(self.driver.find_element(By.XPATH, '//*[@id="filterForm"]/div[3]/div/label[1]').text, 'All')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=3)