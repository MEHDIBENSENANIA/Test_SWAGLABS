from playwright.sync_api import Page, TimeoutError


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.inventory_header = '//*[@id="inventory_filter_container"]/div'

    def is_on_inventory_page(self):
        try:

            self.page.wait_for_selector(self.inventory_header, timeout=5000)


            header_text = self.page.text_content(self.inventory_header).strip()
            print(f"Header text: {header_text}")


            return "Products" in header_text
        except TimeoutError:
            print("Timed out waiting for inventory page header.")
            return False
