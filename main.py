import os 
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

TUTOR_EMAIL = os.getenv("TUTOR_EMAIL")
TUTOR_PASSWORD = os.getenv("TUTOR_PASSWORD")

LOGIN_URL = "https://www.tutor.com/providers/schedule"

def main():
    print("Email loaded:", TUTOR_EMAIL is not None)
    print("Password loaded:", TUTOR_PASSWORD is not None)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,slow_mo=300)
        page = browser.new_page()
        
        # Go to site
        page.goto(LOGIN_URL)
        page.locator("#ctl00_ctl00_phContentMain_phContentMain_tbxUser").click()
        page.locator("#ctl00_ctl00_phContentMain_phContentMain_tbxUser").fill(TUTOR_EMAIL)
        page.locator("#ctl00_ctl00_phContentMain_phContentMain_tbxUser").press("Tab")
        page.locator("#ctl00_ctl00_phContentMain_phContentMain_tbxPass").fill(TUTOR_PASSWORD)
        page.locator("#ctl00_ctl00_phContentMain_phContentMain_tbxPass").press("Enter")
       # page.get_by_role("button", name="Login").click()
        with page.expect_popup() as page1_info:
            page.get_by_role("link", name="Open the Schedule Manager").click()
        page1 = page1_info.value
        page1.locator("#txtUserName").click()
        page1.locator("#txtUserName").fill(TUTOR_EMAIL)
        page1.locator("#txtUserName").press("Tab")
        page1.locator("#txtPassword").fill(TUTOR_PASSWORD)
        page1.locator("#txtPassword").press("Enter")
        page1.get_by_role("button", name="Sign In").click()

        # Highlight the hours
        page1.locator("#cell150").click()
        page1.locator("#cell150").click(modifiers=["ControlOrMeta"])
        page1.locator("#cell150").click(modifiers=["ControlOrMeta"])
        page1.locator("#cell157").click(modifiers=["ControlOrMeta"])
        page1.locator("#cell164").click(modifiers=["ControlOrMeta"])
        page1.locator("#cell158").click(modifiers=["ControlOrMeta"])
        page1.locator("#cell165").click(modifiers=["ControlOrMeta"])
        page1.locator("#cell5").click(modifiers=["ControlOrMeta"])

        #Schedule the hours
        page1.get_by_role("button", name="Schedule_Selected").click()
    
        # Close the browser
        browser.close()
        print("~~~|Broser has been closed!~~~")

if __name__ == "__main__":
    main()