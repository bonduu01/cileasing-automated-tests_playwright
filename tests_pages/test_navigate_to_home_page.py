from pages.home_page import HomePage
from utils.constants import BASE_URL


def test_go_to_home_page_with_pom(page) -> None:
    home_page = HomePage(page, BASE_URL)
    home_page.go_to_home_page()
    home_page.verify_home_page_loads()



