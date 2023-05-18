import sys

def test():
    from webdriver_manager.chrome import ChromeDriverManager

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as chrome_service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options

    #install and set driver
    chrome_driver_path=ChromeDriverManager().install()
    chrome_driver_service=chrome_service(chrome_driver_path)

    #set options to headless
    chrome_options=Options()
    chrome_options.add_argument("--headless")

    #init client
    chrome_client=webdriver.Chrome(service=chrome_driver_service, options=chrome_options)

    #get scores from page
    ####chrome_client.get("http://127.0.0.1:8777")
    chrome_client.get("https://api.ipify.org")

    value= chrome_client.find_element(By.XPATH, "/html/body/pre").text

    return value.isdigit() and (1<=int(value)<=1000)

result=test()

if not result:
    sys.exit(1)