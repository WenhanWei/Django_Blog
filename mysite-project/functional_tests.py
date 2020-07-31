from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def test_first_time_enter_in_my_website(self):
        # Emma has heard about a cool new online blog. She goes
        # to check out its homepage
        self.browser.get('http://127.0.0.1:8000')

        # She notices the page title, ico and my personal details
        self.assertIn('WenhanWei\'s Blog', self.browser.title)

        # She will click the navigation bar to see the other part of my website (Blog or My portfolio)
        home_button = self.browser.find_element_by_id('home')
        home_button.click()
        portfolio_button = self.browser.find_element_by_id('portfolio')
        portfolio_button.click()

        # After She browsed my portfolio, she enter in the blog page to see my articles
        blog_button = self.browser.find_element_by_id('blog')
        blog_button.click()

        # She read the most recent post's abstract and think it is good to read the full page.
        abstract = self.browser.find_element_by_class_name('read-more').find_element_by_css_selector('p').text
        print(abstract)
        # She can click the title or the read more button
        blog_post_title = self.browser.find_element_by_class_name('entry-title')
        blog_post_title.click()
        self.browser.back()
        blog_read_more = self.browser.find_element_by_class_name('read-more')
        blog_read_more.click()
        self.browser.forward()

        # After she read my post, she wants to comment my post.
        comment_form = self.browser.find_element_by_class_name('comment-form')

        inputs = comment_form.find_elements_by_css_selector('div>div')

        name = inputs[0].find_element_by_id('id_name')
        email = inputs[1].find_element_by_id('id_email')
        text = comment_form.find_element_by_css_selector('div>div>textarea')
        submit = comment_form.find_element_by_css_selector('div>div>button')

        name.send_keys('emma')
        email.send_keys('emma@email.com')
        text.send_keys('Nice Post!')
        submit.click()

        # She also see the side bar about my posts,
        # she can easily access my posts by different tags or categories and time line.
        # if the post have markdown, there will be a directory at the top aside bar

        widget_title = self.browser.find_elements_by_class_name('widget')

        if widget_title[0].find_element_by_css_selector('h3').text == 'Article Directories':

            article_directories = widget_title[0].find_element_by_css_selector('ul>li>a')
            print(article_directories.text)
            article_directories.click()
            self.browser.back()

            widget_title = self.browser.find_elements_by_class_name('widget')
            archives = widget_title[1].find_element_by_css_selector('ul>li>a')
            print(archives.text)
            archives.click()
            self.browser.back()

            widget_title = self.browser.find_elements_by_class_name('widget')
            categories = widget_title[2].find_element_by_css_selector('ul>li>a')
            print(categories.text)
            categories.click()
            self.browser.back()

            widget_title = self.browser.find_elements_by_class_name('widget')
            recent_post = widget_title[3].find_element_by_css_selector('ul>li>a')
            print(recent_post.text)
            recent_post.click()
            self.browser.back()

            widget_title = self.browser.find_elements_by_class_name('widget')
            tags = widget_title[4].find_element_by_css_selector('ul>li>a')
            print(tags.text)
            tags.click()
            self.browser.back()
        else:
            archives = widget_title[0].find_element_by_css_selector('ul>li>a')
            print(archives.text)
            archives.click()
            self.browser.back()

            widget_title = self.browser.find_elements_by_class_name('widget')
            categories = widget_title[1].find_element_by_css_selector('ul>li>a')
            print(categories.text)
            categories.click()
            self.browser.back()

            widget_title = self.browser.find_elements_by_class_name('widget')
            recent_post = widget_title[2].find_element_by_css_selector('ul>li>a')
            print(recent_post.text)
            recent_post.click()
            self.browser.back()

            widget_title = self.browser.find_elements_by_class_name('widget')
            tags = widget_title[3].find_element_by_css_selector('ul>li>a')
            print(tags.text)
            tags.click()
            self.browser.back()

        # She notice a search input shows up at the nav bar and test it.
        search = self.browser.find_element_by_tag_name('form').find_element_by_tag_name('input')
        search.send_keys('test')
        search.send_keys(Keys.ENTER)

        # Finally she wants to visit my github page
        footer = self.browser.find_element_by_tag_name('footer')
        github = footer.find_element_by_css_selector("div>div>div>ul>li>a")
        github.click()

    def tearDown(self):
        self.browser.quit()


if __name__ == '__main__':
    unittest.main(warnings='ignore')
