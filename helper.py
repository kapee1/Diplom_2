from faker import Faker


def generate_user_data():
    fake = Faker('ru_RU')
    user_data = {'email': fake.email() + '10062024',
                 'password': fake.password(length=8),
                 'name': fake.user_name()}
    return user_data



