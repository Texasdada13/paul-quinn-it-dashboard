from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def main():
    os.makedirs("screenshots", exist_ok=True)
    
    # Configure Chrome options for better screenshots
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1920, 1080)
    
    try:
        print("Navigating to dashboard...")
        driver.get("http://localhost:8503")
        
        # Wait for Streamlit to fully load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stSelectbox']"))
        )
        time.sleep(10)  # Longer wait for full content load
        
        personas = [
            "CFO - Financial Steward",
            "CIO - Strategic Partner", 
            "CTO - Technology Operator",
            "Project Manager View",
            "HBCU Institutional View"
        ]
        
        for i, persona in enumerate(personas):
            print(f"\nCapturing {persona}...")
            
            try:
                # Scroll to top before taking any screenshots
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)
                
                if i > 0:  # Skip for first persona as it's already selected
                    # Click on the Streamlit selectbox
                    selectbox = driver.find_element(By.CSS_SELECTOR, "[data-testid='stSelectbox'] > div")
                    driver.execute_script("arguments[0].scrollIntoView(true);", selectbox)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", selectbox)
                    time.sleep(3)
                    
                    # Find and click the option
                    options_elements = driver.find_elements(By.CSS_SELECTOR, "[data-baseweb='menu'] [role='option']")
                    for option in options_elements:
                        if persona in option.text:
                            driver.execute_script("arguments[0].click();", option)
                            break
                    
                    time.sleep(8)  # Wait for content to load
                
                # Scroll back to top and wait
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(3)
                
                # Take full page screenshot
                persona_clean = persona.replace(' - ', '_').replace(' ', '_')
                filename = f"screenshots/{persona_clean}_main_overview.png"
                
                # Get full page height and take full page screenshot
                total_height = driver.execute_script("return document.body.scrollHeight")
                driver.set_window_size(1920, total_height)
                time.sleep(2)
                
                driver.save_screenshot(filename)
                print(f"  Main view saved: {filename}")
                
                # Reset window size
                driver.set_window_size(1920, 1080)
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(2)
                
                # Now capture each tab
                try:
                    # Look for tabs - try multiple selectors
                    tab_selectors = [
                        "[data-baseweb='tab']",
                        ".stTabs [data-baseweb='tab']",
                        "[data-testid='stTabs'] button"
                    ]
                    
                    tabs = []
                    for selector in tab_selectors:
                        tabs = driver.find_elements(By.CSS_SELECTOR, selector)
                        if tabs:
                            break
                    
                    print(f"  Found {len(tabs)} tabs")
                    
                    for tab_index, tab in enumerate(tabs):
                        try:
                            # Scroll tab into view
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab)
                            time.sleep(2)
                            
                            # Get tab text for filename
                            tab_text = tab.text.strip()
                            if not tab_text:
                                tab_text = f"Tab_{tab_index}"
                            
                            print(f"  Clicking tab: {tab_text}")
                            
                            # Click the tab
                            driver.execute_script("arguments[0].click();", tab)
                            time.sleep(5)  # Wait for tab content to load
                            
                            # Scroll to top
                            driver.execute_script("window.scrollTo(0, 0);")
                            time.sleep(2)
                            
                            # Take full page screenshot of this tab
                            tab_clean = tab_text.replace(' ', '_').replace('&', 'and').replace('/', '_').replace('📊', '').replace('📃', '').replace('🏛️', '').replace('📈', '').replace('📋', '').strip('_')
                            tab_filename = f"screenshots/{persona_clean}_tab_{tab_index}_{tab_clean}.png"
                            
                            # Get full page height for tab
                            total_height = driver.execute_script("return document.body.scrollHeight")
                            driver.set_window_size(1920, total_height)
                            time.sleep(2)
                            
                            driver.save_screenshot(tab_filename)
                            print(f"    Tab screenshot saved: {tab_filename}")
                            
                            # Reset window size
                            driver.set_window_size(1920, 1080)
                            
                        except Exception as tab_error:
                            print(f"    Error with tab {tab_index}: {tab_error}")
                            
                except Exception as tabs_error:
                    print(f"  No tabs found or error accessing tabs: {tabs_error}")
                
            except Exception as persona_error:
                print(f"  Error with persona {persona}: {persona_error}")
                
        print("\nScreenshots completed! Check the 'screenshots' folder.")
        
    except Exception as e:
        print(f"Main error: {e}")
        driver.save_screenshot("screenshots/debug_main_error.png")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()