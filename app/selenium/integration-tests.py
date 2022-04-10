import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# This works woohoo

#----------- Basic Functions -------

def login(self, u, p):
    self.driver.get("http://web:8000/login/")
    username = self.driver.find_element_by_name('username')
    password = self.driver.find_element_by_name('password')
    submit = self.driver.find_element_by_name('submit')
    username.send_keys(u)
    password.send_keys(p)
    submit.click()


def create_listing(self, h, s, sd, p, d):
    wait = WebDriverWait(self.driver, 10)
    self.driver.get("http://web:8000")
    nav = self.driver.find_element_by_name('create-listing')
    nav.click()
    wait.until(lambda driver: self.driver.current_url == "http://web:8000/create-listing/")

    header = self.driver.find_element_by_name('header')
    skill = self.driver.find_element_by_name('skill')
    skill_description = self.driver.find_element_by_name('skill_description')
    price = self.driver.find_element_by_name('price')
    description = self.driver.find_element_by_name('description')
    submit = self.driver.find_element_by_name('submit')
    header.send_keys(h)
    skill.send_keys(s)
    skill_description.send_keys(sd)
    price.send_keys(p)
    description.send_keys(d)
    submit.click()

    wait = WebDriverWait(self.driver, 10)

#---------- Test Log in ------------

class LogIn(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
           desired_capabilities=DesiredCapabilities.CHROME
        )
        #self.driver.get("http://web:8000/login/")

    def test_login_valid_fields(self):
        username = "user"
        password = "password"
        login(self, username, password)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: self.driver.current_url != "http://web:8000/login/")
        assert "Welcome" in self.driver.page_source


    def tearDown(self):
        self.driver.quit()

#---------- Test Sign Up ------------
class SignUp(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
           desired_capabilities=DesiredCapabilities.CHROME
        )
        self.driver.get("http://web:8000/signup/")

    def test_signup_valid_fields(self):
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        email = self.driver.find_element_by_name('email')
        submit = self.driver.find_element_by_name('submit')
        username.send_keys("user102343204")
        password.send_keys("password")
        email.send_keys("test@email.com")
        submit.click()
        self.driver.implicitly_wait(20)
        assert "A user with that" in self.driver.page_source

    def tearDown(self):
        self.driver.quit()

#---------- Test Create Listing ------------
class CreateListing(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
           desired_capabilities=DesiredCapabilities.CHROME
        )
        login(self, "user", "password")



    def test_createlisting_valid_fields(self):
        create_listing(self, "Cooking", "Cooking", "Making food", 10, "Learn how to cook")
        assert "You did it" in self.driver.page_source

    def tearDown(self):
        self.driver.quit()

class Search(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
           desired_capabilities=DesiredCapabilities.CHROME
        )
        # log in
        login(self, "user", "password")
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: self.driver.current_url != "http://web:8000/login/")
        # create listing
        create_listing(self, "Cooking", "Cooking", "Making food", 10, "Learn how to cook")

    def test_search_valid_fields(self):
        self.driver.get('http://web:8000')
        searchbar = self.driver.find_element_by_name('search_terms')
        searchbar.send_keys("Cooking")
        searchbar.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: self.driver.current_url != "http://web:8000")
        assert "Cooking" in self.driver.page_source

    def tearDown(self):
        self.driver.quit()

class LogOut(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
           desired_capabilities=DesiredCapabilities.CHROME
        )
        # log in
        login(self, "user", "password")
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: self.driver.current_url != "http://web:8000/login/")

    def test_logout_valid_fields(self):
        self.driver.get('http://web:8000')
        logout = self.driver.find_element_by_name('logout')
        logout.click()
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: self.driver.current_url == "http://web:8000/login/")
        assert "Log In" in self.driver.page_source

    def tearDown(self):
        self.driver.quit()

class ItemDetail(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
           desired_capabilities=DesiredCapabilities.CHROME
        )
        # log in
        login(self, "user", "password")
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: self.driver.current_url != "http://web:8000/login/")
        # create listing
        create_listing(self, "Cooking", "Cooking", "Making food", 10, "Learn how to cook")

    def test_itemdetail_valid_fields(self):
        self.driver.get('http://web:8000')
        searchbar = self.driver.find_element_by_name('search_terms')
        searchbar.send_keys("Cooking")
        searchbar.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: self.driver.current_url != "http://web:8000")
        item = self.driver.find_element_by_class_name('detail-link')
        self.driver.execute_script("arguments[0].click()", item)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: self.driver.current_url != "http://web:8000/search/" )
        assert "Cooking" in self.driver.page_source

    def tearDown(self):
        self.driver.quit()



if __name__ == "__main__":
    unittest.main()
