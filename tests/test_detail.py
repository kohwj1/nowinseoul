import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select


class DetailTestCase(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(30)
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.driver.get('https://nowinseoul.makemyproject.net/ko/detail/POI054')

    def test_01_site_access(self):
        self.assertEqual(self.driver.title, '혜화역 :: Now in Seoul')

    def test_02_crowd_density(self):
        self.assertIn(self.driver.find_element(By.XPATH, '//*[@id="crowd-tag"]').text, ['여유', '보통', '약간 붐빔', '붐빔'])

        density_bar_data = self.driver.find_element(By.XPATH, '//*[@id="crowd-density-bar"]').get_attribute('style')
        density_bar_data = density_bar_data.replace('background: linear-gradient(to right, rgb', '').split('rgb')
        self.assertEqual(len(density_bar_data), 13)

    def test_03_traffic(self):
        self.assertIn(self.driver.find_element(By.XPATH, '//*[@id="road-traffic-tag"]').text, ['원활', '서행', '정체'])

    def test_04_weather(self):
        self.assertRegex(self.driver.find_element(By.XPATH, '/html/body/div[2]/section/div[1]/div/div[2]/div/div[1]/span[1]').text, r'^\d{2}:\d{2}$')
        current_temperature = int(self.driver.find_element(By.XPATH, '/html/body/div[2]/section/div[1]/div/div[2]/div/div[1]/span[2]').text.replace('°C',''))
        expected_farenheit_temperature = int(current_temperature * 1.8 + 32)
        
        self.driver.find_element(By.XPATH, '/html/body/div[2]/section/div[1]/div/div[1]/div/div/button[2]').click()
        self.assertEqual(self.driver.find_element(By.XPATH, '/html/body/div[2]/section/div[1]/div/div[2]/div/div[1]/span[2]/span').text, '°F')
        current_farenheit_temperature = int(self.driver.find_element(By.XPATH, '/html/body/div[2]/section/div[1]/div/div[2]/div/div[1]/span[2]').text.replace('°F',''))
        self.assertEqual(expected_farenheit_temperature, current_farenheit_temperature)

    def test_05_public_bike(self):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/section/div[2]/div/ul/li[1]')))

        self.assertRegex(self.driver.find_element(By.XPATH, '//*[@id="total-bikes"]').text, r'^공공자전거 \d{1,2}대 사용 가능$')
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'leaflet-marker-icon').is_displayed())
        self.assertRegex(self.driver.find_element(By.XPATH, '/html/body/div[2]/section/div[2]/div/ul/li[1]/span[1]').text, r'^\d{1,2}$')

    def test_06_localized(self):        
        Select(self.driver.find_element(By.XPATH, '//*[@id="lang-select"]')).select_by_value('ja')      
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.current_url, 'https://nowinseoul.makemyproject.net/ja/detail/POI054')
        
        self.driver.get(self.driver.current_url)
        self.assertEqual(self.driver.title, '恵化駅 (ヘファ駅) :: Now in Seoul')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/section/div[2]/div/ul/li[1]')))
        
        self.assertEqual(self.driver.find_element(By.XPATH, '/html/body/div[2]/section/section[1]/div/div[1]/div[2]').text, '混雑度')
        self.assertRegex(self.driver.find_element(By.XPATH, '//*[@id="total-bikes"]').text, r'^公共自転車\d{1,2}台使用可能$')

        Select(self.driver.find_element(By.XPATH, '//*[@id="lang-select"]')).select_by_value('en')      
        self.driver.implicitly_wait(5)
        self.assertEqual(self.driver.current_url, 'https://nowinseoul.makemyproject.net/en/detail/POI054')
        
        self.driver.get(self.driver.current_url)
        self.assertEqual(self.driver.title, 'Hyehwa station :: Now in Seoul')
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/section/div[2]/div/ul/li[1]')))
        
        self.assertEqual(self.driver.find_element(By.XPATH, '/html/body/div[2]/section/section[1]/div/div[1]/div[2]').text, 'Crowd Density')
        self.assertRegex(self.driver.find_element(By.XPATH, '//*[@id="total-bikes"]').text, r'^\d{1,2} Public bike\(s\) available$')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=3)