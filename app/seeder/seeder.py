import requests
import random
import json
import datetime

url_order = "http://127.0.0.1:5000/order/"
url_ingredient = "http://127.0.0.1:5000/ingredient/"
url_beverage = "http://127.0.0.1:5000/beverage/"
url_size = "http://127.0.0.1:5000/size/"

with open("app/seeder/info/clients.json", "r") as file:
    data_client = json.load(file)

client_list = [(item["name"], item["ndi"]) for item in data_client]

def load_and_transform_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    list_result = [(item['name'], item['price']) for item in data]
    return list_result

beverages_list = load_and_transform_data('app/seeder/info/beverages.json')
ingredients_list = load_and_transform_data('app/seeder/info/ingredients.json')
sizes_list = load_and_transform_data('app/seeder/info/sizes.json')




ingredient_options = [1, 2, 3, 4, 5, 6,7,8,9,10]
beverage_options = [1, 2, 3, 4, 5, 6,7,8,9,10]
def create_orders():
    for i in range(100):
        client = random.choice(client_list)
        client_name = client[0]
        client_dni = client[1]
        client_address = "Dirección {}".format(i)
        client_phone = "09631605{:03d}".format(i)
        size_id = random.randint(1, 5)
        ingredients = random.sample(range(1, len(ingredients_list)+1), random.randint(1, len(ingredients_list)))
        beverages = random.sample(range(1, len(beverages_list)+1), random.randint(1, len(beverages_list)))

        body = {
            "client_name": client_name,
            "client_dni": client_dni,
            "client_address": client_address,
            "client_phone": client_phone,
            "size_id": size_id,
            "ingredients": ingredients,
            "beverages": beverages
        }

        requests.post(url_order, json=body)


def create_elements(url, elements_list):
    for i in range (len(elements_list)):
        element = elements_list[i]
        name = element[0]
        price = element[1]

        body = {
            "name": name,
            "price": price,
        }

        requests.post(url, json=body)


def run_seeder():
    try :
        create_elements(url_ingredient, ingredients_list)
        print ("ingredients created")
        create_elements(url_beverage, beverages_list)
        print ("beverages created")
        create_elements(url_size, sizes_list)
        print ("sizes created")
        create_orders()
        print ("orders created")
    except Exception as e:
        print (e)


if __name__ == "__main__":
    run_seeder()


