import pytest
import requests

import data
import urls
import helper
import allure


class TestUserCreation:
    @allure.title('Создание нового пользователя')
    def test_create_new_user_success(self):
        user = helper.generate_user_data()
        response = requests.post(urls.BASE_URL + urls.CREATE_USER, data=user)
        token = response.json()['accessToken']
        requests.delete(urls.BASE_URL + urls.DELETE_USER, headers={'Authorization': token})

        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Невозможно создать пользователя если данные уже используются')
    def test_create_already_existed_user_failed(self, create_and_delete_new_user):
        token, user = create_and_delete_new_user
        false_response = requests.post(urls.BASE_URL + urls.CREATE_USER, data=user)

        assert false_response.status_code == 403
        assert false_response.json()['success'] is False
        assert false_response.json()['message'] == data.user_already_exists_response_message

    @allure.title('Невозможно создать пользователя без заполнения любого из обязательных полей')
    @pytest.mark.parametrize('field', ('email', 'password', 'name'))
    def test_create_user_without_required_field_failed(self, field):
        user = helper.generate_user_data()
        del user[field]
        response = requests.post(urls.BASE_URL + urls.CREATE_USER, data=user)

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == data.reg_without_required_fields_response_message


class TestUserLogin:
    @allure.title('Успешная авторизация зарегистрированного пользователя')
    def test_user_login_successful(self, create_and_delete_new_user):
        token, user = create_and_delete_new_user
        response = requests.post(urls.BASE_URL + urls.LOGIN_USER, data=user)

        assert response.status_code is 200
        assert response.json()['success'] is True and 'accessToken' in response.json()

    @allure.title('Невозможно авторизовать пользователя, если хотя бы одно из полей неверно')
    @pytest.mark.parametrize('field', ('email', 'password'))
    def test_user_login_with_wrong_data_failed(self, field, create_and_delete_new_user):
        token, user = create_and_delete_new_user
        user[field] = 'wrong_data'
        response = requests.post(urls.BASE_URL + urls.LOGIN_USER, data=user)

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == data.incorrect_email_or_password_response_message


class TestChangeUserData:
    @allure.title('Изменение данных для авторизованного пользователя')
    @pytest.mark.parametrize('field', ('name', 'email'))
    def test_change_user_data_with_auth_success(self, field, create_and_delete_new_user):
        token, user = create_and_delete_new_user
        new_field_value = 'wakanda'
        user[field] = new_field_value
        response = requests.patch(urls.BASE_URL + urls.CHANGE_USER_DATA, data=user, headers={'Authorization': token})

        assert response.status_code == 200
        assert response.json()['success'] is True and new_field_value in response.json()['user'][field]

    @allure.title('Невозможно изменить пользовательские данные без авторизации')
    @pytest.mark.parametrize('field', ('name', 'email'))
    def test_change_user_data_without_auth_failed(self, field, create_and_delete_new_user):
        token, user = create_and_delete_new_user
        new_field_value = 'wakanda'
        user[field] = new_field_value
        response = requests.patch(urls.BASE_URL + urls.CHANGE_USER_DATA, data=user)

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == data.no_auth_response_message
