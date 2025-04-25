import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

# Step 1: Set up Selenium WebDriver
driver = webdriver.Safari()  # Use SafariDriver; replace with ChromeDriver if using Chrome
url = "https://iimlibrariesconsortium.in/faculty.html"  #
driver.get(url)

# Step 2: Click "Show More" until it no longer exists
while True:
    try:
        # Wait for the "Show More" button to be clickable
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show More')]"))
        )
        show_more_button.click()
        time.sleep(2)  # Wait for more content to load
    except Exception as e:
        print("No more 'Show More' button found or all content is loaded.")
        break

# Step 3: Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Step 4: Extract faculty information
faculty_data = []

# Extract the faculty name (inside <font> tag within <h3>)
faculty_names = soup.find_all("h3", class_="h4 g-mb-15")

for faculty_name in faculty_names:
    # Extract name from the <font> tag within <h3>
    name_tag = faculty_name.find("font")
    if name_tag:
        name = name_tag.text.strip()
    
    # Extract email from the <b>Email:</b> section
    email_tag = faculty_name.find_next("b", text="Email:")
    if email_tag:
        # Locate the sibling containing the email
        sibling = email_tag.find_next_sibling(text=True)
        if sibling:
            email = sibling.strip().replace("&nbsp;", "")
            faculty_data.append((name, email))

# Step 5: Save to a CSV file on the Desktop
desktop_path = os.path.expanduser("~/Desktop/IIM_Faculty_Emails.csv")
df = pd.DataFrame(faculty_data, columns=["Name", "Email"])
df.to_csv(desktop_path, index=False)

print(f"Data saved to {desktop_path}")

