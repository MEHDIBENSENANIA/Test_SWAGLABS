from playwright.sync_api import sync_playwright
import time


def test_sauce_demo_logins():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport=None)
        page = context.new_page()

        # Ouvrir le site
        page.goto("https://www.saucedemo.com/v1/")
        time.sleep(2)
        users = [
            {"username": "standard_user", "expected_url": "inventory.html",
             "message": "Connexion réussie pour standard_user"},
            {"username": "locked_out_user", "expected_error": "Sorry, this user has been locked out.",
             "message": "Utilisateur verrouillé détecté"},
            {"username": "problem_user", "expected_url": "inventory.html",
             "message": "Connexion réussie pour problem_user"},
            {"username": "performance_glitch_user", "expected_url": "inventory.html",
             "message": "Connexion réussie pour performance_glitch_user"},
        ]

        for user in users:
            print(f"Test de l'utilisateur : {user['username']}")
            page.fill('input[placeholder="Username"]', user['username'])
            page.fill('input[placeholder="Password"]', 'secret_sauce')
            page.click('input[type="submit"]')
            time.sleep(2)  # Pause pour permettre le chargement

            # Vérification des résultats
            if "expected_url" in user:
                if user["expected_url"] in page.url:
                    print(f" {user['message']}")
                else:
                    print(f" Erreur : L'utilisateur {user['username']} n'a pas atteint l'URL attendue.")

            if "expected_error" in user:
                # Vérifier si le message d'erreur s'affiche
                error_message = page.text_content('//*[@id="login_button_container"]/div/form/h3')
                if user["expected_error"] in error_message:
                    print(f" {user['message']}")
                else:
                    print(f"Erreur : Le message attendu pour {user['username']} n'a pas été trouvé.")

            page.goto("https://www.saucedemo.com/v1/")
            time.sleep(2)

        # Fermez le navigateur
        browser.close()


if __name__ == "__main__":
    test_sauce_demo_logins()
