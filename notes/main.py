from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()
    def check_for_row_in_list_table(self,row_text):
        table=self.browser.find_element(By.ID,'id_list_table')
        rows=table.find_elements(By.TAG_NAME,'tr')
        self.assertIn(row_text,[row.text for row in rows])
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 新访客访问网站的首页
        # 他听说这是一个很酷的待办事项应用
        self.browser.get('http://localhost:8000')

        # 他注意到网页的标题和头部都包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # 应用邀请他输入一个待办事项
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # 他在文本框中输入了“Buy flowers"
        inputbox.send_keys('Buy flowers')

        # 他按下回车键后页面更新了
        # 待办事项表格中显示了“1: Buy flowers"
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1:Buy flowers')

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1:Buy flowers')
        self.check_for_row_in_list_table('2:Give a gift to Lisi')

        # 页面中又显示了一个文本框，可以输入其他的事项
        # 他输入了“Use peacock feathers to make a fly"
        # 做事清单很有趣
        self.fail('Finish the test!')

        # 页面更新了，现在的清单中显示了这两个待办事项



if __name__ == '__main__':
    unittest.main()
