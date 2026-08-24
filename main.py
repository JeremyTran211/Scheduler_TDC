import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

load_dotenv()

TUTOR_EMAIL = os.getenv("TUTOR_EMAIL")
TUTOR_PASSWORD = os.getenv("TUTOR_PASSWORD")

LOGIN_URL = "https://www.tutor.com/providers/schedule"

# Each day increments by 7 to the next hour, starting at 12am EST
# Sunday: 0, Monday: 1, Tuesday: 2...
# Sunday: 7, Monday: 8, Tuesday: 9...

# Regular hours: Wednesay 6-9pm, Thursday 7-9pm
DESIRED_CELLS = [
    "#cell150",
    "#cell157",
    "#cell164",
    "#cell158",
    "#cell165",
]

# Sunday 11am - 4pm 
SUNDAY_CELLS = [
    "#cell98", 
    "#cell105", 
    "#cell112",
    "#cell119",
    "#cell126",
]

def main():
    print("Email loaded:", TUTOR_EMAIL is not None)
    print("Password loaded:", TUTOR_PASSWORD is not None)

    if not TUTOR_EMAIL or not TUTOR_PASSWORD:
        print("Missing TUTOR_EMAIL or TUTOR_PASSWORD in .env")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        page = browser.new_page()

        try:
            # Go to Tutor.com provider schedule page
            page.goto(LOGIN_URL)

            # Main Tutor.com login
            page.locator("#ctl00_ctl00_phContentMain_phContentMain_tbxUser").fill(TUTOR_EMAIL)
            page.locator("#ctl00_ctl00_phContentMain_phContentMain_tbxPass").fill(TUTOR_PASSWORD)
            page.get_by_role("button", name="Login").click()

            print("Logged into Tutor.com main page.")

            # Open Schedule Manager popup
            with page.expect_popup() as page1_info:
                page.get_by_role("link", name="Open the Schedule Manager").click()

            page1 = page1_info.value

            # Schedule Manager login
            page1.locator("#txtUserName").fill(TUTOR_EMAIL)
            page1.locator("#txtPassword").fill(TUTOR_PASSWORD)
            page1.get_by_role("button", name="Sign In").click()

            print("Logged into Schedule Manager.")

            # Give Schedule Manager time to load
            page1.wait_for_load_state("networkidle")

            # Go one week ahead
            page1.locator("#weekAhead").click()
            print("Clicked week ahead.")

            # Highlight desired cells
            selected_count = 0

            for selector in DESIRED_CELLS:
                try:
                    cell = page1.locator(selector)
                    cell.wait_for(state="visible", timeout=3000)
                    cell.click(modifiers=["ControlOrMeta"])
                    selected_count += 1
                    print(f"Selected {selector}")
                    page1.screenshot(path=f"screenshot/scheduled{selector}.png")
                except Exception as e:
                    print(f"Could not select {selector}: {e}")

            print(f"Selected {selected_count} cells.")

            # Wait briefly so the page can update the Schedule Selected button
            page1.wait_for_timeout(1000)

            # Find Schedule Selected button
            schedule_button = page1.get_by_role("button", name="Schedule Selected")
            schedule_button.wait_for(state="visible", timeout=5000)

            print("Schedule button visible:", schedule_button.is_visible())
            print("Schedule button enabled:", schedule_button.is_enabled())
            
            if schedule_button.is_enabled():
                schedule_button.click()
                print("Clicked Schedule Selected.")
                page1.screenshot(path="screenshot/schedule_submitted.png")

                # --- Verification step ---
                # Give the server a moment to process the submission
                page1.wait_for_timeout(2000)
                page1.wait_for_load_state("networkidle")

                # Reload to get a fresh, authoritative view of the schedule
                page1.reload()
                page1.wait_for_load_state("networkidle")
                page1.locator("#weekAhead").click()   # re-navigate to the same week (reload resets it)
                page1.wait_for_timeout(1000)

                scheduled_cells = []
                missing_cells = []

                for selector in DESIRED_CELLS:
                    cell = page1.locator(selector)
                    cell_text = cell.inner_text().strip()
                    cell_class = cell.get_attribute("class") or ""

                    if "FILLED" in cell_class or cell_text == "Scheduled!":
                        scheduled_cells.append(selector)
                    else:
                        missing_cells.append(f"{selector} (state: {cell_text or cell_class})")

                print(f"Verified scheduled: {scheduled_cells}")
                print(f"Missing: {missing_cells}")

                if missing_cells:
                    print(f"WARNING: {len(missing_cells)} of {len(DESIRED_CELLS)} cells were NOT scheduled.")
                    page1.screenshot(path="screenshot/verification_mismatch.png")
                else:
                    print("All desired cells confirmed scheduled.")

            else:
                print("Schedule button is disabled/grayed out. Not clicking.")
                page1.screenshot(path="screenshot/schedule_button_disabled.png")
            
        except PlaywrightTimeoutError as e:
            print("Timeout error:", e)
            page.screenshot(path="screenshot/timeout_error.png")

        except Exception as e:
            print("Bot failed:", e)
            page.screenshot(path="screenshot/bot_failed.png")

        finally:
            input("Press Enter to close the browser...")
            browser.close()
            print("Browser has been closed! ~~~")


if __name__ == "__main__":
    main()
