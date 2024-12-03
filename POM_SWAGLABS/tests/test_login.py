from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
import time


def test_login_scenarios():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport=None)
        page = context.new_page()
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        login_page.navigate()
        users = [
            {"username": "standard_user", "password": "secret_sauce", "expected_url": "inventory.html",
             "should_succeed": True},
            {"username": "locked_out_user", "password": "secret_sauce",
             "expected_error": "Sorry, this user has been locked out.", "should_succeed": False},
            {"username": "problem_user", "password": "secret_sauce", "expected_url": "inventory.html",
             "should_succeed": True},
            {"username": "performance_glitch_user", "password": "secret_sauce", "expected_url": "inventory.html",
             "should_succeed": True},
        ]

        for user in users:
            print(f"Testing user: {user['username']}")

            # Login
            login_page.login(user["username"], user["password"])
            time.sleep(5)
            if user["should_succeed"]:
                print(f"Current URL after login: {page.url}")
                assert "inventory.html" in page.url, "User was not redirected to the inventory page."
                assert inventory_page.is_on_inventory_page(), f"Test failed for {user['username']}"
                print(f" Login successful for {user['username']}")
            else:
                error_message = login_page.get_error_message()
                assert user[
                           "expected_error"] in error_message, f"Expected error message not found for {user['username']}. Got: {error_message}"
                print(f" Error displayed as expected for {user['username']}")

            login_page.navigate()
            time.sleep(2)

        browser.close()



if __name__ == "__main__":
    test_login_scenarios()
