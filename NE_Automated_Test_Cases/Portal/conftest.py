import pytest
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from pytest_html import extras
import os


@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("detach", True)
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        driver.implicitly_wait(10)
        yield driver
    finally:
        driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        driver = item.funcargs.get("browser", None)
        if driver:
            screenshot = driver.get_screenshot_as_base64()
            # html = f'<div><img src="data:image/png;base64,{screenshot}" alt="screenshot" style="width:600px;height:auto;"></div>'
            html = f'<div style="display: flex; justify-content: center; align-items: center; margin-top: 10px;">\
                <img src="data:image/png;base64,{screenshot}" alt="screenshot" style="max-width:100%; height:auto; border: 1px solid #ccc; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">\
            </div>'
            report.extras = [extras.html(html)]


def pytest_html_report_title(report):
    report.title = "NerdEssay Portal - Place Order Test Cases"


def pytest_configure(config):
    config.option.html = "report.html"
    config.option.self_contained_html = True


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    yield
    if platform.system() == 'Windows':
        os.system('start report.html')
    elif platform.system() == 'Darwin':  # macOS
        os.system('open report.html')
    else:  # Linux
        os.system('xdg-open report.html')
