from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    from_email = "SENDER E-MAIL"  
    from_password = "GOOGLE APPS PASSWORD"  
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)

        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()


def advance_search():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2&q=python%20AND%20%28django,%20OR%20javascript,%20OR%20react,%20OR%20html,%20OR%20css%29&sort=recency&page=1&per_page=50")
    wait = WebDriverWait(driver, 20)

    h2_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "h5.mb-0.mr-2.job-tile-title")))
    p_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mb-0.text-body-sm")))
    ul_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job-tile-info-list.text-base-sm.mb-4")))
    job_times = driver.find_elements(By.CSS_SELECTOR, ".job-tile-header .job-tile-header-line-height")
    
    for h2_element , p_element , ul_element, job_time in zip(h2_elements, p_elements, ul_elements, job_times):
        title= h2_element.text
        p_text = p_element.text
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        a_element = h2_element.find_element(By.TAG_NAME, "a")
        href_value = a_element.get_attribute("href")
        post_time = job_time.find_element(By.CSS_SELECTOR, "small[data-test='job-pubilshed-date'] span:nth-child(2)").text

        match = re.search(r'(\d+)\s*hour', post_time)  
        if match:
            hours_posted = int(match.group(1))
            if hours_posted > 3:  
                print("Stopped job due to time condition.")
                break
        elif "yesterday" in post_time.lower():
            print("Stopped job due to time condition.")
            break
        email_subject = f"New Job Post: {title}"
        email_body = f"""
        Job Title: {title}
        Post Time: {post_time}
        Description: {p_text}
        Skills Required: 
        """
        for li in li_elements:
            email_body += f"{li.text}\n"
        
        email_body += f"\nJob Link: {href_value}"
        to_email = "SEND E-MAIL"
        send_email(email_subject, email_body, to_email)

    driver.quit()


if __name__ == "__main__":
    advance_search() 