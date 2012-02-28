#!/usr/bin/env python
# coding=UTF-8

import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import unittest


class BasicWebUiTest(unittest.TestCase):
    test_uri = "http://www.mnot.net/"
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(redbot_uri)
        self.uri = self.browser.find_element_by_id("uri")
        self.uri.send_keys(self.test_uri + Keys.RETURN)
        time.sleep(1.0)
        self.check_complete()
        
    def test_multi(self):
        check = self.browser.find_element_by_xpath("//a[@accesskey='a']")
        check.click()
        time.sleep(0.5)
    
    def check_complete(self):
        try:
            self.browser.find_element_by_xpath("//div[@class='footer']")
        except NoSuchElementException:
            raise Exception, "Page not complete."
    
    def tearDown(self):
        self.check_complete()
        self.browser.close()

class CnnWebUiTest(BasicWebUiTest):
    test_uri = 'http://edition.cnn.com/'


if __name__ == "__main__":
    redbot_uri = os.environ.get("REDBOT_URI", None)
    if redbot_uri:
      unittest.main()
    else:
      import sys
      sys.path.insert(0, "deploy")
      import webui
      import thor
      def cb():
        suite = unittest.TestLoader()
        suite.loadTestsFromTestCase(BasicWebUiTest)
        suite.loadTestsFromTestCase(CnnWebUiTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
        thor.loop.stop()
      webui.standalone_main(8080, "deploy/static", cb)
      redbot_uri = "http://localhost:8080/"
    