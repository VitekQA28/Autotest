from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import io


class CardPr:

    @allure.title("Открытие браузера")
    def __init__(self, browser):
        """
        Эта функция открывает браузер

        затем переходит на страницу по URL

        и открывает окно браузера на весь экран

        добавляет куки
        """
        
        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cookie = {
            "name" : "cookieControl",
            "value" : "true"
        }
        self.__driver = browser
        self.__driver.get('https://prostayaeda.s2.citruspro.ru/')
        self.__driver.implicitly_wait(10)
        self.__driver.maximize_window()
        #self.__driver.add_cookie(cookie)
        #self.__driver.refresh()

    @allure.step("Принимаем cookie")
    def get_cookie(self):
        self.__driver.find_element(By.XPATH, "//*[@id='gdpr-cookie-accept']").click()

    @allure.step("Нажать на кнопку МЕНЮ")
    def open_menu(self):
        self.__driver.find_element(By.XPATH, "//*[@id='header']/div[1]/div/div[1]/div[2]/nav/nav/ul/li[1]/a").click()

    @allure.step("Открываем карточку товара c доступным остатком")
    def open_available_card(self):
        self.__driver.find_element(By.XPATH, "//*[@id='bx_10163737_2065_c8abe16af0bc770650f5cb4ee614c4c3']/a/div[2]/div").click()
        with allure.step("Нажимаем на + для увеличения кол-ва товара"):
            self.__driver.find_element(By.XPATH, "//*[@id='bx_117848907_2065']/div[2]/div[2]/div[2]/div[2]/div[1]/a[2]").click()
        with allure.step("Нажимаем на кнопку В корзину и открываем корзину с товаром"):
            button = self.__driver.find_element(By.XPATH, "//*[@id='bx_117848907_2065']/div[2]/div[2]/div[2]/div[2]/div[2]/a/span[2]")
            for i in range(2):
                button.click()
                time.sleep(1)

    @allure.step("Открываем карточку товара с 0 остатком")
    def open_no_stock_card(self):
        self.__driver.find_element(By.XPATH, "//*[@id='bx_10163737_2465_4f877ed29f8ae72b74be00bb9098a65a']/a/div[2]/div/div[2]").click()
        with allure.step("Нажимаем на + для увеличения кол-ва товара"):
            self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/a[2]").click()
        with allure.step("Нажимаем на кнопку В корзину и открываем корзину с товаром"):
            button = self.__driver.find_element(By.XPATH, "//*[@id='bx_117848907_2465']/div[2]/div[2]/div[2]/div[2]/div[2]/a")
            button.click()
            WebDriverWait(self.__driver, 10).until(EC.visibility_of_any_elements_located((By.XPATH, "/html/body/div[2]/div/div[1]/div")))
            time.sleep(0.5)
            res = self.__driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div/div[1]/div")
            res.click()
            time.sleep(1)
            self.__driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/div/div[1]/div/ul/li[2]").click()
            time.sleep(0.5)
            button = self.__driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div/div/button")
            for i in range(2):
                button.click()
                time.sleep(1)
            self.__driver.find_element(By.XPATH, "//*[@id='bx_117848907_2465']/div[2]/div[2]/div[2]/div[2]/div[2]/a").click()

    @allure.step("Заполняем информацию о доставки на ближайшее время")
    def adress(self)->str:
        try:
            WebDriverWait(self.__driver, 2).until(EC.visibility_of_any_elements_located((By.XPATH, "//*[@id='STREET_PRESET_TYPE']")))
        except:
            self.__driver.refresh()
        WebDriverWait(self.__driver, 10).until(EC.visibility_of_any_elements_located((By.XPATH, "//*[@id='STREET_PRESET_TYPE']")))
        with allure.step("Вводим населеный пункт"):
            sity = self.__driver.find_element(By.XPATH, "//*[@id='STREET_PRESET_TYPE']")
            sity.send_keys("Йошкар-Ола", Keys.RETURN)
        with allure.step("Вводим название улицы"):
            time.sleep(0.5)
            street = self.__driver.find_element(By.XPATH, "//*[@id='vue-app__order']/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[2]/span")
            street.click()
            self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/form/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[1]/input").send_keys("Советская улица")
            time.sleep(0.5)
            self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/form/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[1]/input").send_keys(Keys.RETURN)
        with allure.step("Вводим номер дома"):
            house = self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/form/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[2]/input")
            time.sleep(0.5)
            house.send_keys(int(10))
            self.__driver.find_element(By.XPATH, "//*[@id='16']").click()
        with allure.step("Выбираем время доставки"):
            self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/form/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div[1]/input").send_keys("В ближайшее время", Keys.RETURN)
        with allure.step("Нажимаем кнопку Далее"):
            self.__driver.find_element(By.XPATH, "//*[@id='vue-app__order']/div[1]/div[1]/div[1]/div[3]/div[3]/a").click()   
            
    @allure.step("Заполняем информацию о доставке на другую дату ")
    def adress_any(self)->str:
        try:
            WebDriverWait(self.__driver, 2).until(EC.visibility_of_any_elements_located((By.XPATH, "//*[@id='STREET_PRESET_TYPE']")))
        except:
            self.__driver.refresh()
        WebDriverWait(self.__driver, 10).until(EC.visibility_of_any_elements_located((By.XPATH, "//*[@id='STREET_PRESET_TYPE']")))
        with allure.step("Вводим населеный пункт"):
            sity = self.__driver.find_element(By.XPATH, "//*[@id='STREET_PRESET_TYPE']")
            sity.send_keys("Йошкар-Ола", Keys.RETURN)
        with allure.step("Вводим название улицы"):
            time.sleep(0.5)
            street = self.__driver.find_element(By.XPATH, "//*[@id='vue-app__order']/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[2]/span")
            street.click()
            self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/form/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[1]/input").send_keys("Советская улица")
            time.sleep(0.5)
            self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/form/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div/div/div[1]/input").send_keys(Keys.RETURN)
        with allure.step("Вводим номер дома"):
            house = self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/form/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div/div[2]/div[2]/input")
            time.sleep(0.5)
            house.send_keys(int(10))
            self.__driver.find_element(By.XPATH, "//*[@id='16']").click()
        with allure.step("Нажимаем кнопку Далее"):
            self.__driver.find_element(By.XPATH, "//*[@id='vue-app__order']/div[1]/div[1]/div[1]/div[3]/div[3]/a").click()   

    @allure.step("Заполняем информацию - персональные данные клиента")
    def personal_info(self)->str:
        WebDriverWait(self.__driver, 10).until(EC.visibility_of_any_elements_located((By.XPATH, "//*[@id='vue-app__order']/div[1]/div[1]/div[2]/div[3]/div[1]/h5[1]")))
        with allure.step("Вводим Имя"):
            self.__driver.find_element(By.XPATH, "//*[@id='1']").send_keys("Тест", Keys.RETURN)
        with allure.step("Вводим номер телефона"):
            self.__driver.find_element(By.XPATH, "//*[@id='4']").send_keys("+79024657539", Keys.RETURN)
        with allure.step("Вводим Email"):
            self.__driver.find_element(By.XPATH, "//*[@id='2']").send_keys("test@mail.ru", Keys.RETURN)
        with allure.step("Выбираем оплату"):
            self.__driver.find_element(By.XPATH, "//*[@id='payment-systems-block']/div/div/div/div/div[1]").click()
        with allure.step("Нажимаем на кнопку Сделать заказ"):
            time.sleep(1)
            self.__driver.find_element(By.XPATH, "//*[@id='vue-app__order']/div[1]/div[2]/div[4]/button").click()

    @allure.step("Проверяем, что страница с информцией о заказе открылась")
    def title_info(self)->str:
        WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/div")))
        title = self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div/h1").text
        return title

    @allure.step("Проверяем, что сформировался номер заказа")
    def order_info(self)->str:
        WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/div")))
        order = self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div/h2").text
        return order
    
    @allure.step("Проверяем, что имя заказчика совпадает")
    def contact_info(self)->str:
        WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/div")))
        name = self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div/div[2]/div/div[1]/span").text
        return name
    
    @allure.step("Проверяем, что кнопка “Оплатить” активна")
    def pay_button(self):
        self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div/a").click()
        WebDriverWait(self.__driver, 10)
        curent_url = self.__driver.current_url
        return curent_url
    
    @allure.step("Проверяем, что дата доставки больше текущей даты на ... часов")
    def data_info(self)->str:
        WebDriverWait(self.__driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/div")))
        data = self.__driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div/div[1]/div[2]/div[2]").text
        return data
    
    @allure.step("Закрываем браузер")
    def close_browser(self):
        self.__driver.quit
    