import datetime
import smtplib, os, time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from apscheduler import jobstores
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from server import variably
from config import email_key, pupil_id, pupil_pass, email_pass, git_pass, git_user, my_email, botty_email

sched = BlockingScheduler(timezone='EST', standalone=True)

chrome_exec_shim = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
opts = webdriver.ChromeOptions()
opts.binary_location = chrome_exec_shim
opts.add_argument('--disable-gpu')
hw = 'HW#{}'
driver = webdriver.Chrome(ChromeDriverManager().install())


# WRITE TO FAILSAFE
def github_write(name):
    driver.get('https://gist.github.com/Botty-Account/e1a117c4891b6f93a3b2cf243d836527/edit')
    driver.find_element_by_id('login_field').send_keys(git_user)
    driver.find_element_by_id('password').send_keys(git_pass)
    driver.find_element(By.XPATH, '//input[@type="submit"]').click()
    name_box = driver.find_element(By.XPATH,
                                   '//input[@class="form-control filename js-gist-filename js-blob-filename"]')
    for i in range(5):
        name_box.send_keys(Keys.BACK_SPACE)
    name_box.send_keys(name)
    driver.find_element(By.XPATH, '//button[@class="btn btn-primary"]').click()


# GITHUB READING TO DETERMINE IF FAILSAFE TURNED ON
def github_read():
    driver.get('https://gist.github.com/Botty-Account/e1a117c4891b6f93a3b2cf243d836527/edit')
    driver.find_element_by_id('login_field').send_keys(git_user)
    driver.find_element_by_id('password').send_keys(git_pass)
    driver.find_element(By.XPATH, '//input[@type="submit"]').click()
    name_box = driver.find_element(By.XPATH,
                                   '//input[@class="form-control filename js-gist-filename js-blob-filename"]')
    if 'True' in driver.page_source:
        bool_val = True
    else:
        bool_val = False

    return bool_val


# EMAIL TIME
def email_time(recipient, subject, content):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(email_key, email_pass)
    smtpObj.sendmail(botty_email, recipient,
                     'Subject:' + subject + ' \n' + content)


# PUPILPATH LOGIN
def pupillog():
    driver.get('https://google.com')
    driver.get('https://pupilpath.skedula.com/')
    time.sleep(.400)
    if 'Sign In' in driver.page_source:
        driver.find_element_by_id('sign_in').click()
        driver.find_element_by_class_name('form-input').send_keys(pupil_id)
        time.sleep(.400)
        driver.find_element_by_id('sign_in').click()
        time.sleep(.400)
        driver.find_element_by_id('user_password').send_keys(pupil_pass)
        time.sleep(.400)
        driver.find_element_by_id('sign_in').click()
        time.sleep(.400)
    driver.find_element_by_class_name('ui-button-text').click()
    time.sleep(.250)
    try:
        driver.find_element(By.XPATH, '//a[@title="Recent Assignments"]').click()
        time.sleep(.400)
    except NoSuchElementException:
        print('recent Assignment skip')
    try:
        driver.find_element_by_link_text('All Assignments').click()
        time.sleep(.400)
    except NoSuchElementException:
        print('Assignment ski[')
    try:
        driver.find_element(By.XPATH, '//tr[@data-codesec="MPS21-38"]').click()
    except NoSuchElementException:
        print('xpath skip')


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def recent():
    number = 1
    while hw.format(number) in driver.page_source:
        number += 1
    return number - 1


# MORNING PUPILPATH COMMAND
# @sched.scheduled_job('cron', id='pupil_morn', day_of_week='mon-fri', hour=8)
def pupil_morn():
    print('pupil_morn start')
    driver.refresh()
    time.sleep(2)
    global number
    driver.get('https://www.google.com/')
    time.sleep(1)
    pupillog()
    time.sleep(3)
    number = recent()
    if number == 0:
        driver.refresh()
        driver.get('https://www.google.com/')
        time.sleep(.650)
        pupillog()
        number = recent()
    email_time(my_email, 'Successful check!', f'There are currently {number} homeworks up my dude. I ' +
               'will update you on future changes')
    print(number)
    print('pupil_morn complete')


# AFTERNOON PUPILPATH COMMAND
# @sched.scheduled_job('cron', id='pupil_noon', day_of_week='mon-fri', hour=15, minute=40)
def pupil_noon():
    print('pupil_noon start')
    driver.refresh()
    time.sleep(3)
    driver.get('https://www.google.com/')
    time.sleep(.500)
    pupillog()
    time.sleep(.500)
    nnew_num = recent()
    time.sleep(3)
    if nnew_num == number:
        email_time(my_email, 'failure to upload',
                   f'homework {nnew_num} not uploaded boi. extra credit time!!!!!!!!!')
    else:
        email_time(my_email, 'homework successfully uploaded', 'we will get him next time tho')
    print('pupil_noon complete')


sched.add_job(pupil_morn, 'cron', id='pupil_morn', day_of_week='mon-fri', hour=7)
print('sched set')
sched.add_job(pupil_noon, 'cron', id='pupil_noon', day_of_week='mon-fri', hour=14, minute=40)
print('sched set')


sched.print_jobs()

sched.start()
