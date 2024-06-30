import requests
import urls
import allure
import data


class TestOrderCreation:
    @allure.title('Создание нового заказа без авторизация пользователя')  # не соответствует документации
    def test_create_new_order_without_auth_success(self):
        response = requests.post(urls.BASE_URL + urls.CREATE_ORDER, data=data.burger_ingredients)

        assert response.status_code == 200
        assert response.json()['success'] is True and 'number' in response.json()['order']

    @allure.title('Создание нового заказа для авторизованного пользователя')
    def test_create_new_order_with_auth_success(self, create_and_delete_new_user):
        token, user = create_and_delete_new_user
        response = requests.post(urls.BASE_URL + urls.CREATE_ORDER, data=data.burger_ingredients,
                                 headers={'Authorization': token})

        assert response.status_code == 200
        assert response.json()['success'] is True and 'number' in response.json()['order']

    @allure.title('Невозможно создать заказ без ингредиентов')
    def test_create_order_without_ingredients_failed(self):
        response = requests.post(urls.BASE_URL + urls.CREATE_ORDER)

        assert response.status_code == 400
        assert response.json()['success'] is False and response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Невозможно создать заказ с неверным хэшем ингредиентов')
    def test_create_new_order_with_wrong_ingredients_hash_failed(self):
        ingredients = {"ingredients": ["2314dfd32"]}  # несуществующие ингредиенты
        response = requests.post(urls.BASE_URL + urls.CREATE_ORDER, data=ingredients)

        assert response.status_code == 500


class TestGetUserOrders:
    @allure.title('Получение списка заказов для авторизованного пользователя')
    def test_get_auth_user_orders_success(self, create_and_delete_new_user):
        token, user = create_and_delete_new_user
        order_response = requests.post(urls.BASE_URL + urls.CREATE_ORDER, data=data.burger_ingredients,
                                       headers={'Authorization': token})  # создание заказа
        order_number = order_response.json()['order']['number']
        response = requests.get(urls.BASE_URL + urls.GET_USER_ORDERS,
                                headers={'Authorization': token})  # получение заказов пользователя

        assert response.status_code == 200
        assert len(response.json()['orders']) == 1 and response.json()['orders'][0]['number'] == order_number

    @allure.title('Невозможно получить список заказов без авторизации')
    def test_get_orders_without_auth_failed(self):
        response = requests.get(urls.BASE_URL + urls.GET_USER_ORDERS)

        assert response.status_code == 401
        assert response.json()['success'] is False and response.json()['message'] == 'You should be authorised'
