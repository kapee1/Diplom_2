from faker import Faker


def generate_user_data():
    fake = Faker('ru_RU')
    user_data = {'email': fake.email() + '10062024',
                 'password': fake.password(length=8),
                 'name': fake.user_name()}
    return user_data


def get_burger_ingredients():
    ingredients = {"ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]}
    return ingredients
