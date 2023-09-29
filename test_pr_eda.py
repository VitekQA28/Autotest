from page.CatalogPr import CatalogPr
from page.CardPr import CardPr
import allure
import pytest
import time
from datetime import datetime

#@pytest.mark.skip
@allure.severity("critical")
@allure.epic("Оформление заказа из карточки товара")
@allure.title("Заказ товара с доступным остатком из детальной карточки")
def test_product_available_in_stock():
    card_page = CardPr('browser')
    card_page.get_cookie()
    card_page.open_menu()
    card_page.open_available_card()
    card_page.adress()
    card_page.personal_info()

    assert card_page.title_info() == "СПАСИБО, ВАШ ЗАКАЗ ПРИНЯТ"
    order_text = card_page.order_info()
    assert order_text.startswith("Заказ №") and len(order_text) > len("Заказ №"), "Номер заказа отсутствует"
    assert card_page.contact_info() == "Тест"
    assert card_page.pay_button().startswith("https://securecardpayment.ru/payment/merchants/sbersafe_sberid/payment_ru"), "Страница с оплатой не открылась"
    card_page.close_browser()
    
@allure.severity("critical")
@allure.epic("Оформление заказа из карточки товара")
@allure.title("Заказ товара с нулевым остатком из детальной карточки")
def test_product_is_out_of_stock():
    card_page = CardPr('browser')
    card_page.get_cookie()
    card_page.open_menu()
    card_page.open_no_stock_card()
    card_page.adress_any()
    card_page.personal_info()

    assert card_page.title_info() == "СПАСИБО, ВАШ ЗАКАЗ ПРИНЯТ"
    order_text = card_page.order_info()
    assert order_text.startswith("Заказ №") and len(order_text) > len("Заказ №"), "Номер заказа отсутствует"
    assert card_page.contact_info() == "Тест"
    assert card_page.pay_button().startswith("https://securecardpayment.ru/payment/merchants/sbersafe_sberid/payment_ru"), "Страница с оплатой не открылась"
    card_page.close_browser()