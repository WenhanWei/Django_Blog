from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_enter_in_the_homepage(self):
        # Emma has heard about a cool new online blog. She goes
        # to check out its homepage
        self.browser.get('http://127.0.0.1:8000')

        # She notices the page title, ico and my personal details
        self.assertIn('WenhanWei', self.browser.title)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
