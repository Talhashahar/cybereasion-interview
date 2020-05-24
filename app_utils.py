import pymongo
import docker
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def get_collection():
    """
        create reference to mongodb collection
    :return:
        reference to mongodb collection
    """
    myclient = pymongo.MongoClient(
        host=f"{config['mongo']['hostname']}:{config['mongo']['port']}",
        username=config['mongo']['username'],
        password=config['mongo']['password'],
    )
    return myclient["cr-db"]["users"]


def load_data():
    """
        parse data.txt file and load the data to mongoDB (via pymongo package)
    :return:
    """
    col = get_collection()
    list_to_insert = list()
    with open("data_files/data.txt") as f:
        lines = [line.rstrip() for line in f]
    for line in lines:
        obj = {i.split(': ')[0]: i.split(': ')[1] for i in line.split(', ')}
        list_to_insert.append(obj)
    res = col.insert_many(list_to_insert)


def get_manipulate_docs():
    """
        Manipulate the data from mongoDB
    :return:
        list of users with the manipulate (task required)
    """
    col = get_collection()
    cursor = col.find({})
    ret_list = list()
    for document in cursor:
        temp_dict = dict()
        try:
            temp_dict['firstname'] = document['firstname'].capitalize()
            temp_dict['lastname'] = document['lastname'].capitalize()
            temp_dict['password'] = len(document['password']) * "*"
            temp_dict['username'] = document['username']
            ret_list.append(temp_dict)
        except Exception as e:
            print(e)
    sorted_list = sorted(ret_list, key=lambda i: i['firstname'])
    return sorted_list


def run_mongo_docker():
    """
        Check if mongo container is ready, if not Deploy and insert data if container (from my dockerhub account)
    :return:
        None
    """
    client = docker.from_env()

    containers = client.containers.list()
    container_running = False
    for container in containers:
        if config['docker']['image_name'] in container.image.tags:
            container_running = True
            break
    if not container_running:
        client.containers.run(config['docker']['image_name'],
                              environment=[f"MONGO_INITDB_ROOT_USERNAME={config['mongo']['username']}",
                                           f"MONGO_INITDB_ROOT_PASSWORD={config['mongo']['password']}"],
                              ports={config['mongo']['port']: config['mongo']['port']}, detach=True)
        load_data()
