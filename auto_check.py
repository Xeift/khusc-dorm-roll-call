import smtplib
import email.message
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import schedule


_acc = str(input('請輸入學號：'))
_pwd = str(input('請輸入校務系統密碼：'))
_email = str(input('請輸入email：'))

def job():
    chromedriver_autoinstaller.install()
    print('自動點名系統啟動中')

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    driver.get('http://db.kh.usc.edu.tw/dormRollCall/login.php')
    driver.find_element('xpath','/html/body/form/center/table/tbody/tr[1]/td[2]/input').send_keys(_acc)# enter acc
    driver.find_element('xpath','/html/body/form/center/table/tbody/tr[2]/td[2]/input').send_keys(_pwd)# enter pwd
    driver.find_element('xpath','/html/body/form/center/table/tbody/tr[3]/td/input').click()# click login
    driver.find_element('xpath','/html/body/form/input[2]').click()# roll call
    alert = driver.switch_to.alert
    alert_text = alert.text
    alert.accept()

    if '非校內宿舍IP' in alert_text:
        print('點名失敗，請連接宿舍網路')

        msg=email.message.EmailMessage()

        msg['From']='lamerk0218@gmail.com'
        msg['To']=_email
        msg['Subject']='點名失敗，請手動點名'

        msg.add_alternative('<h1>點名失敗，請手動點名</h1>', subtype='html')

        server=smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('lamerk0218', 'PWD_HERE')
        server.send_message(msg)
        server.close()

    else:
        print('點名成功')

    driver.close()

schedule.every().day.at('21:35').do(job)

while True:
    schedule.run_pending()