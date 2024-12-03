from playwright.sync_api import Page
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = "input[id='user-name']"
        self.password_input = "input[id='password']"
        self.login_button = "input[id='login-button']"
        self.error_message_xpath = "//*[@id='login_button_container']/div/form/h3"  # Simplified XPath for error message

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/v1/")

    def login(self, username: str, password: str):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

    def get_error_message(self):

        self.page.wait_for_selector(self.error_message_xpath, timeout=5000)  # Wait for 5 seconds

        try:
            error_message = self.page.text_content(self.error_message_xpath).strip()
            return error_message
        except Exception as e:
            print(f"Error while extracting message: {e}")
            return ""
