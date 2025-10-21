from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os

# URLs and config
speed_test = "https://fast.com/"
twitter_home = "https://x.com/home"
SPEED_THRESHOLD = 30  # complain if below this

# Setup Chrome with some anti-detection stuff I found online
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

# Save login session so we don't have to login every time
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)

# This hides the webdriver property
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})

def is_logged_in():
    """Check if we're already logged into Twitter"""
    try:
        driver.get(twitter_home)
        time.sleep(5)
        
        # Look for stuff that's only there when logged in
        try:
            driver.find_element(By.CSS_SELECTOR, '[data-testid="SideNav_NewTweet_Button"]')
            return True
        except:
            try:
                driver.find_element(By.CSS_SELECTOR, '[aria-label="Post"]')
                return True
            except:
                return False
    except:
        return False

def wait_for_manual_login():
    """Let user login manually then wait for them to finish"""
    print("\n" + "="*60)
    print("🔐 MANUAL LOGIN REQUIRED")
    print("="*60)
    print("\nYour internet speed is too low!")
    print("Please log in to Twitter manually to post complaint.\n")
    print("Steps:")
    print("1. Log in using your credentials in the browser")
    print("2. Complete any verification (2FA, email, etc.)")
    print("3. Wait until you see your Twitter home feed")
    print("4. Script will auto-detect and continue")
    print("\nOpening Twitter login page...")
    print("-"*60)
    
    driver.get("https://x.com/i/flow/login")
    time.sleep(3)
    
    print("\n⏳ Waiting for you to log in...")
    
    # Give them up to 5 minutes
    max_attempts = 60
    attempts = 0
    
    while attempts < max_attempts:
        try:
            # If we can find the home button, they're logged in
            driver.find_element(By.CSS_SELECTOR, '[data-testid="AppTabBar_Home_Link"]')
            print("\n✅ Login detected! Proceeding with tweet...")
            time.sleep(3)
            return True
        except:
            current_url = driver.current_url
            if "home" in current_url:
                print("\n✅ Login successful! Proceeding...")
                time.sleep(3)
                return True
            
            attempts += 1
            time.sleep(5)
    
    print("\n⚠️ Login timeout. Please try again.")
    return False

def compose_and_post_tweet(message):
    """Write and post the tweet"""
    try:
        print("\n📝 Composing tweet...")
        
        # Go to home first
        driver.get(twitter_home)
        time.sleep(5)
        
        # Click the tweet button - sometimes it's hard to find
        try:
            tweet_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="SideNav_NewTweet_Button"]'))
            )
            tweet_button.click()
        except:
            # Try the floating one instead
            try:
                tweet_button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Post"]')
                tweet_button.click()
            except:
                print("❌ Could not find tweet button. Please click 'Post' button manually.")
                input("Press Enter after clicking the Post/Tweet button...")
        
        time.sleep(3)
        
        # Find the text box where we type
        try:
            tweet_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]'))
            )
        except:
            tweet_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[role="textbox"][data-testid*="tweet"]'))
            )
        
        tweet_box.click()
        time.sleep(1)
        
        # Type slowly so it looks natural
        for char in message:
            tweet_box.send_keys(char)
            time.sleep(0.05)
        
        time.sleep(2)
        
        print(f"✓ Tweet composed: {message}")
        
        print("\n" + "="*60)
        print("✅ TWEET READY TO POST")
        print("="*60)
        print("\nYour complaint tweet:")
        print("-"*60)
        print(message)
        print("-"*60)
        print("\nThe tweet is ready but NOT posted yet.")
        print("\nOptions:")
        print("1. Press Enter to POST the tweet")
        print("2. Or press Ctrl+C to cancel and post manually")
        print("-"*60)
        
        input("\nPress Enter to POST tweet: ")

        posted = False

        try:
            print("Trying exact XPath...")
            post_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[2]/div[2]/div/div/div/button[2]'))
            )
            time.sleep(2)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", post_button)
            time.sleep(2)
            posted = True
            print("✓ Posted using exact XPath!")
        except Exception as e:
            print(f"Exact XPath failed: {str(e)[:100]}")
        
        # If not worked, ask user to do it manually
        if not posted:
            print("\n⚠️ Could not click Post button automatically.")
            print("The tweet is composed and ready in the browser.")
            print("\n👉 Please click the 'Post' button manually (it should be blue)")
            input("Press Enter after you've clicked Post...")
            posted = True
        
        if posted:
            print("\n✅ Tweet posted successfully!")
        
        time.sleep(3)
        return posted
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tweet cancelled. You can post it manually from the browser.")
        return False
    except Exception as e:
        print(f"\n❌ Error posting tweet: {e}")
        print("You can still post manually in the browser window")
        import traceback
        traceback.print_exc()
        return False

# Main execution
try:
    print("="*60)
    print("TWITTER INTERNET SPEED COMPLAINT BOT")
    print("="*60)
    
    # First, check the speed
    print("\n[STEP 1/3] Testing Internet Speed...")
    print("-"*60)
    driver.get(speed_test)
    time.sleep(3)
    
    print("⏳ Measuring speed (please wait at least 30 seconds)...")
    print("Please wait...\n")
    
    # Wait a bit for it to measure
    print("   Waiting for initial measurement...")
    time.sleep(30)
    
    # Try to read the speed
    internet_speed = None
    speed_unit = "Mbps"
    max_wait = 30
    elapsed = 0
    
    while elapsed < max_wait and internet_speed is None:
        try:
            speed_element = driver.find_element(By.ID, "speed-value")
            speed_text = speed_element.text.strip()
            if speed_text and speed_text != "—":
                internet_speed = float(speed_text)
                
                # Get the unit
                try:
                    unit_element = driver.find_element(By.ID, "speed-units")
                    speed_unit = unit_element.text.strip()
                    print(f"   Detected unit: {speed_unit}")
                except:
                    try:
                        page_text = driver.find_element(By.TAG_NAME, "body").text
                        if "Kbps" in page_text or "kbps" in page_text:
                            speed_unit = "Kbps"
                            print(f"   Detected unit from page: Kbps")
                        else:
                            speed_unit = "Mbps"
                            print(f"   Assuming unit: Mbps (default)")
                    except:
                        speed_unit = "Mbps"
                        print(f"   Assuming unit: Mbps (default)")
                
                break
        except:
            pass
        
        if elapsed % 5 == 0:
            remaining = max_wait - elapsed
            print(f"   {remaining} seconds remaining...")
        
        time.sleep(1)
        elapsed += 1
    
    # If we couldn't read it automatically, ask the user
    if internet_speed is None:
        print("\n⚠️ Could not automatically read speed")
        speed_input = input("Please enter your internet speed (e.g., '5.2 Mbps' or '512 Kbps'): ")
        
        speed_input = speed_input.strip().upper()
        if 'KBPS' in speed_input or 'KB/S' in speed_input:
            speed_value = float(''.join(c for c in speed_input if c.isdigit() or c == '.'))
            internet_speed = speed_value / 1000
            speed_unit = "Kbps (converted)"
            print(f"📊 Converted: {speed_value} Kbps = {internet_speed} Mbps")
        else:
            internet_speed = float(''.join(c for c in speed_input if c.isdigit() or c == '.'))
            speed_unit = "Mbps"
    else:
        # Convert Kbps to Mbps if needed
        if 'KBPS' in speed_unit.upper() or 'KB/S' in speed_unit.upper():
            original_speed = internet_speed
            internet_speed = internet_speed / 1000
            print(f"\n✓ Speed test complete!")
            print(f"📊 Your internet speed: {original_speed} Kbps = {internet_speed} Mbps")
        else:
            print(f"\n✓ Speed test complete!")
            print(f"📊 Your current internet speed: {internet_speed} Mbps")
            
        # Double check if it seems too high
        if internet_speed > 100 and speed_unit == "Mbps":
            print(f"\n⚠️ Wait, that seems unusually high...")
            confirm = input(f"Is your speed really {internet_speed} Mbps? If it's {internet_speed} Kbps, type 'k': ").strip().lower()
            if confirm == 'k' or confirm == 'kbps':
                print(f"Converting {internet_speed} Kbps to Mbps...")
                internet_speed = internet_speed / 1000
                speed_unit = "Kbps (corrected)"
                print(f"📊 Corrected speed: {internet_speed} Mbps")
    
    print("-"*60)
    
    # Check if speed is too slow
    print(f"\n[STEP 2/3] Analyzing Speed...")
    print(f"Threshold: {SPEED_THRESHOLD} Mbps")
    print(f"Your speed: {internet_speed} Mbps")
    
    if internet_speed < SPEED_THRESHOLD:
        print(f"\n❌ SPEED IS TOO LOW!")
        print(f"Your speed ({internet_speed} Mbps) is below {SPEED_THRESHOLD} Mbps")
        print("Time to complain on Twitter! 😤\n")
        
        # Now login to Twitter
        print("[STEP 3/3] Logging into Twitter...")
        print("-"*60)
        
        if not is_logged_in():
            print("❌ Not logged in")
            if not wait_for_manual_login():
                print("❌ Login failed. Exiting...")
                driver.quit()
                exit()
        else:
            print("✅ Already logged in!")
            driver.get(twitter_home)
            time.sleep(3)
        
        # Format speed nicely for the tweet
        if 'converted' in speed_unit.lower() or internet_speed < 1:
            speed_display = f"{internet_speed * 1000} Kbps"
        else:
            speed_display = f"{internet_speed} Mbps"
        
        complaint = f"Hi @JioCare, I'm on the ₹349/month plan but my internet speed is only {speed_display} instead of the expected {SPEED_THRESHOLD}+ Mbps. Kindly look into this issue and resolve it soon. Thank you. #Jio #InternetIssue"
        
        compose_and_post_tweet(complaint)
        
        print("\n" + "="*60)
        print("✅ COMPLAINT SUBMITTED!")
        print("="*60)
        print("\nYour internet provider has been notified (publicly)! 📢")
        print("Check your Twitter profile to see the tweet.")
        
    else:
        print(f"\n✅ SPEED IS ACCEPTABLE!")
        print(f"Your speed ({internet_speed} Mbps) is above {SPEED_THRESHOLD} Mbps")
        print("No need to complain. Enjoy your internet! 🎉")
        print("\nClosing browser in 5 seconds...")
        time.sleep(5)
        driver.quit()
        exit()
    
    print("\n" + "="*60)
    print("SCRIPT COMPLETED")
    print("="*60)
    
    if internet_speed < SPEED_THRESHOLD:
        print("\nBrowser will remain open.")
        print("Press Enter to close...")
        input()

except KeyboardInterrupt:
    print("\n\n⚠️ Script cancelled by user")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    print("\nBrowser will stay open for inspection")
    input("Press Enter to close...")
finally:
    try:
        driver.quit()
    except:

        pass
