import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# 
from datetime import datetime, timedelta
from calendar import monthrange, month_name

# webdriver setup
chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('log-level=2')
driver_exe = 'chromedriver'
driver = webdriver.Chrome(driver_exe,options=chrome_options)

# clockwise urls
main_url = 'https://secure.clockwise.info/clockwise/sharevalue/'
hour_registration_url = 'https://secure.clockwise.info/clockwise/sharevalue/urenregistratie/matrix.php'
# login
username = '###'
password = '###'
# for row select use name field u_{month_number-1}{row_number-1} 
# so when selecting day 15 in the 3th row u_142.
# the month is 2 digits, 2th is 01 

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'    

def login():
    print(f'{style.YELLOW}--> Start ClockWise session')
    # get the login page
    driver.get(main_url)
    # find username field and fill it in
    print('--> Fill in user credentials')
    driver.find_element_by_name('naam').send_keys(username)
    # find the password field
    password_element = driver.find_element_by_name('wwoord')
    # fill in the password field
    password_element.send_keys(password)
    # hit enter to submit
    password_element.send_keys(Keys.ENTER)
    print('->> Logging in')

def get_work_days():
    days = []
    excluded =(6,7)
    current_date = datetime.today()
    start_day = current_date.replace(day=1)
    last_day = datetime(current_date.year,current_date.month,monthrange(datetime.today().year, datetime.today().month)[1]) 

    while start_day.date() <= last_day.date():
        if start_day.isoweekday() not in excluded:
            days.append(start_day.day)
        start_day += timedelta(days=1)
    return days


def fill_hours_and_save(row, hours=8):
    print(f'--> Getting the working days of:{month_name[datetime.today().month]}')
    working_days = get_work_days()
    # get the hour registration url
    print('--> Navigate to the hours registration')
    driver.get(hour_registration_url)
    print('--> Fill in the hours')
    for day in working_days:
        # stupid thing of clockwise is that the selection of the cells is not based on the current day value but day-1
        clockwise_cell = day-1
        element_name = f'u_0{clockwise_cell}{row}' if clockwise_cell < 10 else f'u_{clockwise_cell}{row}' 
        # to be save first clear the cell
        driver.find_element_by_name(element_name).clear()
        # fill in the hours
        driver.find_element_by_name(element_name).send_keys(hours)
    print(f'--> Saving the hours{style.RESET}')
    driver.find_element_by_name('verwerken').click()
    time.sleep(1)

login()
fill_hours_and_save(2,8)

driver.close()