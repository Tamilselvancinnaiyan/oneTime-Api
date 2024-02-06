from selenium import webdriver


# Specify the path to the Chrome WebDriver
 

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(executable_path= "Users/tamil/eclipse-workspace/chromedriver_mac64/chromedriver")
print("log 1")
# Open Google homepage
driver.get('https://www.google.com')

