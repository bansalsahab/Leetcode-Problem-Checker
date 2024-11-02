import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Path to your CSV file and ChromeDriver
csv_file = "Microsoft.csv"
chrome_driver_path = 'C:\\Users\\Parth bansal\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe'

def setup_driver():
    options = Options()
    
    # Add arguments to handle WebGL errors
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    options.add_argument('--enable-unsafe-swiftshader')
    
    # Add window size
    options.add_argument('--window-size=1920,1080')
    
    # Add user agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Disable logging
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    service = ChromeService(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def wait_for_manual_login(driver, wait):
    """Wait for manual login to complete"""
    print("\nPlease login manually in the browser window.")
    print("The script will continue once login is detected...")
    
    max_wait_time = 300  # 5 minutes maximum wait time
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        try:
            # Check for elements that indicate successful login
            for selector in [
                (By.CLASS_NAME, "nav-user-icon"),
                (By.CSS_SELECTOR, "[data-cy='nav-user-icon']"),
                (By.XPATH, "//div[contains(@class, 'user-avatar')]")
            ]:
                try:
                    element = wait.until(EC.presence_of_element_located(selector))
                    if element:
                        print("\nLogin detected! Continuing with automation...")
                        return True
                except:
                    continue
            
            # Check if still on login page
            if "login" not in driver.current_url.lower():
                print("\nDetected navigation away from login page. Assuming successful login...")
                return True
                
            time.sleep(2)  # Check every 2 seconds
            
        except Exception as e:
            print(f"Error while waiting for login: {str(e)}")
            continue
    
    print("\nTimeout waiting for manual login. Please try again.")
    return False

def check_problem_status(driver, wait, problem_link):
    """Check if a problem is solved"""
    try:
        print(f"\nChecking problem: {problem_link}")
        driver.get(problem_link)
        time.sleep(3)  # Wait for page load
        
        # Different possible selectors for solved status
        solved_indicators = [
            (By.CSS_SELECTOR, "[data-difficulty='solved']"),
            (By.CSS_SELECTOR, ".text-success"),  # Green success text
            (By.XPATH, "//div[contains(@class, 'text-success')]"),
            (By.XPATH, "//div[contains(text(), 'Solved')]"),
            (By.CSS_SELECTOR, "[data-accepted='true']")
        ]
        
        for selector_type, selector in solved_indicators:
            try:
                element = wait.until(EC.presence_of_element_located((selector_type, selector)))
                if element:
                    print("Problem is solved!")
                    return "Yes"
            except:
                continue
        
        print("Problem is not solved")
        return "No"
        
    except Exception as e:
        print(f"Error checking problem status: {str(e)}")
        return "Error"

def update_csv():
    driver = None
    try:
        print("Setting up Chrome driver...")
        driver = setup_driver()
        wait = WebDriverWait(driver, 1)  # Reduced wait time to 10 seconds for faster response

        print("Loading CSV file...")
        df = pd.read_csv(csv_file)
        
        # Check if 'problem_link' column exists
        if 'problem_link' not in df.columns:
            print("Error: CSV file must contain a 'problem_link' column")
            return
            
        # Create or reset SOLVED column
        df['SOLVED'] = ''

        # Navigate to login page
        print("Opening LeetCode login page...")
        driver.get("https://leetcode.com/accounts/login")
        time.sleep(3)  # Wait for initial page load
        
        # Wait for manual login
        if not wait_for_manual_login(driver, wait):
            print("Manual login failed or timed out. Exiting...")
            return

        print("\nChecking problem statuses...")

        # Check each problem
        for index, row in df.iterrows():
            problem_link = row['problem_link']
            if pd.isna(problem_link) or not isinstance(problem_link, str):
                print(f"Skipping invalid link at row {index + 1}")
                df.at[index, 'SOLVED'] = 'Invalid Link'
                continue
                
            # Reducing delay between loading pages
            try:
                driver.get(problem_link)
                status = check_problem_status(driver, wait, problem_link)
                df.at[index, 'SOLVED'] = status
            except TimeoutException:
                print(f"Timeout on loading problem at row {index + 1}. Skipping.")
                df.at[index, 'SOLVED'] = 'Timeout'

            # Save progress after each check
            df.to_csv(csv_file, index=False)
            print(f"Progress saved - {index + 1}/{len(df)} problems checked")

        print("\nAll problems checked! CSV file has been updated.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
    finally:
        if driver:
            print("\nClosing browser...")
            driver.quit()


if __name__ == "__main__":
    update_csv()