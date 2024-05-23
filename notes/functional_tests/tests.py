from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
Max_wait=10
class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()
    def wait_for_row_in_list_table(self,row_text):
        start_time=time.time()
        while True:
            try:
                table=self.browser.find_element(By.ID,'id_list_table')
                rows=table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except(AssertionError,WebDriverException) as e:
                if time.time()-start_time>Max_wait:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 新访客访问网站的首页
        # 他听说这是一个很酷的待办事项应用
        self.browser.get(self.live_server_url)

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
        self.wait_for_row_in_list_table('1:Buy flowers')

        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.wait_for_row_in_list_table('1:Buy flowers')
        self.wait_for_row_in_list_table('2:Give a gift to Lisi')

        # 页面中又显示了一个文本框，可以输入其他的事项
        # 他输入了“Use peacock feathers to make a fly"
        # 做事清单很有趣
        #self.fail('Finish the test!')

        # 页面更新了，现在的清单中显示了这两个待办事项


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 新用户访问首页
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy flowers')
        # 他注意到清单有一个唯一的URL
        zhangsan_list_url=self.browser.current_url
        self.assertRegex(zhangsan_list_url,'/lists/.+')
        # 现在另一个新用户访问了网站
        self.browser.quit()
        self.browser=webdriver.Chrome()
        # 新用户访问首页
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertNotIn('Give a gift to Lisi',page_text)

        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:Buy milk')
        # 新用户获得了一个唯一的URL
        wangwu_list_url=self.browser.current_url
        self.assertRegex(wangwu_list_url,'/lists/.+')
        self.assertNotEqual(zhangsan_list_url,wangwu_list_url)
        # 页面中没有用户1的清单
        page_text=self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertIn('Buy milk',page_text)
        # 两个用户都很满意

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1:testing')
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
        )
