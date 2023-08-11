import json
from abc import ABC,abstractmethod
import requests


def user_requirements():
    choose_site = input("Введите название сайта для парсинга: ").lower()
    name_vacancy = input("Введите название вакансии: ").lower()
    town = input("Введите город для поиска (1-Москва 2-Санкт-Петербург): ")
    quantity_vacancy = int(input("Введите число отображаемых вакансий: "))
    if town == '2' or town == 2:
        town = 113

    return (choose_site, name_vacancy, town,quantity_vacancy)

choose_site, name_vacancy, town, quantity_vacancy = user_requirements()

#print(choose_site,name_vacancy,town,quantity_vacancy)

class Parsing(ABC):

    @abstractmethod
    def get_requests(self):
        pass


class HeadHunterParsing(Parsing):

    def get_requests(self):
        payload = {'text': name_vacancy, 'area': int(town), 'page': 1, 'per_page': quantity_vacancy}
        api = requests.get('https://api.hh.ru/vacancies', params=payload)

        dict_with_info = api.json()
        return dict_with_info


class SuperJobParsing(Parsing):

    def get_requests(self):
        # choose_town_list = [{
        #
        #         'count': int(quantity_vacancy),
        #
        #         'keyword': name_vacancy, 'town': {
        #             "id": 14,
        #             "title": "Санкт-Петербург",
        #             "declension": "в Санкт-Петербурге",
        #             "genitive": "Санкт-Петербурга"
        #         }}, {
        #
        #         'count': int(quantity_vacancy),
        #
        #         'keyword': name_vacancy, 'town': {
        #             "id": 4,
        #             "title": "Москва",
        #             "declension": "в Москве",
        #             "genitive": "Москвы"
        #         }}]
        # params = choose_town_list[1]
        # print(choose_town_list[1])
        # if town == 113:
        #     params = {
        #
        #         'count': int(quantity_vacancy),
        #
        #         'keyword': name_vacancy, 'town': {
        #             "id": 14,
        #             "title": "Санкт-Петербург",
        #             "declension": "в Санкт-Петербурге",
        #             "genitive": "Санкт-Петербурга"
        #         }}
        # elif town == 1:
        #     params = {
        #
        #         'count': int(quantity_vacancy),
        #
        #         'keyword': name_vacancy, 'town': {
        #             "id": 4,
        #             "title": "Москва",
        #             "declension": "в Москве",
        #             "genitive": "Москвы"
        #         }}
        #     print("MOSCOW")

        params = {

            'count': int(quantity_vacancy),

            'keyword': name_vacancy,
             }

        headers = {
            'X-Api-App-Id': 'v3.r.137723472.32eaa9a552c69e968965b080a6a5da31937fed7c.79dec64b99800a1cdfd2559db1a7677cc61ee2f0'}

        url = 'https://api.superjob.ru/2.0/vacancies'

        req = requests.get(url, params, headers=headers)
        dict_with_info = req.json()
        return dict_with_info



hh_1 = HeadHunterParsing()
sj_1 = SuperJobParsing()

# print(hh_1.get_requests())
# print(sj_1.get_requests())



class Vacancy:
    def __init__(self, name, salary, experience, id, day):
        self.name = name
        self.salary = salary
        self.experience = experience
        self.id = id
        self.day = day

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.salary}, {self.experience}, {self.id}, {self.day})"





class AddVacancy(ABC):

    @abstractmethod
    def add_vacancy(self, quantity_vacancy):
        pass

    # @abstractmethod
    # def show_highest_salary(self):
    #     pass
    #
    # @abstractmethod
    # def sort_by_salary(self):
    #     pass
    #
    # @abstractmethod
    # def show_day_status(self):
    #     pass



class HeadHunterAddVacancy(AddVacancy):

    def add_vacancy(self,quantity_vacancy):
        all_vacancy = []

        for i in range(0, quantity_vacancy):

            if hh_1.get_requests()['items'][i]['salary'] == None:
                salary = "Зарплата скрыта работодателем"
            elif hh_1.get_requests()['items'][i]['salary']['from'] == None:
                salary = "Зарплата скрыта работодателем"
            else:
                salary = hh_1.get_requests()['items'][i]['salary']['from']

            all_vacancy.append(
                Vacancy(hh_1.get_requests()['items'][i]['name'], salary,
                        hh_1.get_requests()['items'][i]['experience']['name'], hh_1.get_requests()['items'][i]['id'],
                        hh_1.get_requests()['items'][i]['employment']['name']))
            # all_vacancy.append(json.dumps({"name":hh_1.get_requests()['items'][i]['name'], "salary":salary,
            #                     "experience":hh_1.get_requests()['items'][i]['experience']['name'],
            #                     "id": hh_1.get_requests()['items'][i]['id'], "day":hh_1.get_requests()['items'][i]['employment']['name']}))


        while True:
            print("Для сравнения и сортировки вакансий их необходимо добавить в базу.")
            print("Для выхода введите - 0")
            user_quest = int(input("Введите id вакансии, которую хотите добавить в базу: "))

            for s in all_vacancy:
                dict_with_data = {"name": s.name, "salary": s.salary, "experience": s.experience, "id": s.id, "day": s.day}
                if int(s.id) == user_quest:

                    with open('data.json', 'a') as file:
                        file.write(json.dumps(dict_with_data,ensure_ascii=False) + "\n")

            if user_quest == 0:
                break


    # def show_highest_salary(self):
    #     with open('data.json', 'rt') as file:
    #         content = file.readlines()
    #         maximum_salary = 0
    #         for i in content:
    #             sal = json.loads(i)['salary']
    #             if str(sal).isdigit() and sal>maximum_salary:
    #                 maximum_salary = sal
    #
    #     with open('data.json', 'rt') as file:
    #         content = file.readlines()
    #         for i in content:
    #             sal = json.loads(i)['salary']
    #             if sal == maximum_salary:
    #                 print(f"{json.loads(i)['name']}, Зп: {json.loads(i)['salary']},"
    #                       f" Опыт: {json.loads(i)['experience']}, ID: {json.loads(i)['id']}, Занятость: {json.loads(i)['day']}")
    #
    #
    #
    #
    #
    # def sort_by_salary(self):
    #     list_for_sort = []
    #
    #     def compare_by_salary(list_for_sort):
    #         return list_for_sort['salary']
    #
    #     with open('data.json', 'rt') as file:
    #         content = file.readlines()
    #         for i in content:
    #             list_for_sort.append(json.loads(i))
    #     for i in list_for_sort:
    #         if i['salary'] == "Зарплата скрыта работодателем":
    #             i['salary'] = 0
    #     new_list = sorted(list_for_sort, key=compare_by_salary, reverse=True)
    #     for i in range(len(new_list)):
    #         print(f"{new_list[i]['name']}, Зп: {new_list[i]['salary']},"
    #               f" Опыт: {new_list[i]['experience']}, ID: {new_list[i]['id']}, Занятость: {new_list[i]['day']}")
    #
    #
    #
    #
    # def show_day_status(self):
    #     list_for_sort = []
    #
    #     with open('data.json', 'rt') as file:
    #         content = file.readlines()
    #         for i in content:
    #             list_for_sort.append(json.loads(i))
    #     for i in list_for_sort:
    #         if i['day'] == "Полная занятость":
    #             print(f"{i['name']}, Зп: {i['salary']},"
    #                   f" Опыт: {i['experience']}, ID: {i['id']}, Занятость: {i['day']}")
    #
    #


class SuperJobAddVacancy(AddVacancy):

    def add_vacancy(self, quantity_vacancy):

        all_vacancy = []

        for i in range(0, quantity_vacancy):

            if sj_1.get_requests()['objects'][i]['payment_from'] == None:
                salary = "Зарплата скрыта работодателем"
            elif sj_1.get_requests()['objects'][i]['payment_from'] == None:
                salary = "Зарплата скрыта работодателем"
            else:
                salary = sj_1.get_requests()['objects'][i]['payment_from']

            all_vacancy.append(
                Vacancy(sj_1.get_requests()['objects'][i]['profession'], salary,
                        sj_1.get_requests()['objects'][i]['experience']['title'], sj_1.get_requests()['objects'][i]['id'],
                        sj_1.get_requests()['objects'][i]['type_of_work']['title']))
            # all_vacancy.append(json.dumps({"name":hh_1.get_requests()['items'][i]['name'], "salary":salary,
            #                     "experience":hh_1.get_requests()['items'][i]['experience']['name'],
            #                     "id": hh_1.get_requests()['items'][i]['id'], "day":hh_1.get_requests()['items'][i]['employment']['name']}))

        while True:
            print("Для сравнения и сортировки вакансий их необходимо добавить в базу.")
            print("Для выхода введите - 0")
            user_quest = int(input("Введите id вакансии, которую хотите добавить в базу: "))

            for s in all_vacancy:
                dict_with_data = {"name": s.name, "salary": s.salary, "experience": s.experience, "id": s.id,
                                  "day": s.day}
                if int(s.id) == user_quest:
                    with open('data.json', 'a') as file:
                        file.write(json.dumps(dict_with_data, ensure_ascii=False) + "\n")

            if user_quest == 0:
                break


    # def show_highest_salary(self):
    #     pass
    #
    #
    # def sort_by_salary(self):
    #     pass
    #
    #
    # def show_day_status(self):
    #     pass





def do_choose_site():
    if choose_site in ['hh','HH','headhunter', 'HeadHunter', 'Hh']:
        for i in range(0, quantity_vacancy):
            if hh_1.get_requests()['items'][i]['salary'] == None:
                salary = "Зарплата скрыта работодателем"
            elif hh_1.get_requests()['items'][i]['salary']['from'] == None:
                salary = "Зарплата скрыта работодателем"
            else:
                salary = hh_1.get_requests()['items'][i]['salary']['from']

            print(hh_1.get_requests()['items'][i]['name'], salary,
                  hh_1.get_requests()['items'][i]['experience']['name'],
                  hh_1.get_requests()['items'][i]['id'], hh_1.get_requests()['items'][i]['employment']['name'])
            print()
        hh_2 = HeadHunterAddVacancy()
        hh_2.add_vacancy(quantity_vacancy)
    else:
        for i in range(0, quantity_vacancy):
            print()
            print(sj_1.get_requests()['objects'][i]['profession'], sj_1.get_requests()['objects'][i]['experience']['title'], sj_1.get_requests()['objects'][i]['payment_from'],
                  sj_1.get_requests()['objects'][i]['id'], sj_1.get_requests()['objects'][i]['type_of_work']['title'])
        sj_2 = SuperJobAddVacancy()
        sj_2.add_vacancy(quantity_vacancy)


do_choose_site()



class Manipulation:

    def show_highest_salary(self):
        with open('data.json', 'rt') as file:
            content = file.readlines()
            maximum_salary = 0
            for i in content:
                sal = json.loads(i)['salary']
                if str(sal).isdigit() and sal>maximum_salary:
                    maximum_salary = sal

        with open('data.json', 'rt') as file:
            content = file.readlines()
            for i in content:
                sal = json.loads(i)['salary']
                if sal == maximum_salary:
                    print(f"{json.loads(i)['name']}, Зп: {json.loads(i)['salary']},"
                          f" Опыт: {json.loads(i)['experience']}, ID: {json.loads(i)['id']}, Занятость: {json.loads(i)['day']}")





    def sort_by_salary(self):
        list_for_sort = []

        def compare_by_salary(list_for_sort):
            return list_for_sort['salary']

        with open('data.json', 'rt') as file:
            content = file.readlines()
            for i in content:
                list_for_sort.append(json.loads(i))
        for i in list_for_sort:
            if i['salary'] == "Зарплата скрыта работодателем":
                i['salary'] = 0
        new_list = sorted(list_for_sort, key=compare_by_salary, reverse=True)
        for i in range(len(new_list)):
            print(f"{new_list[i]['name']}, Зп: {new_list[i]['salary']},"
                  f" Опыт: {new_list[i]['experience']}, ID: {new_list[i]['id']}, Занятость: {new_list[i]['day']}")




    def show_day_status(self):
        list_for_sort = []

        with open('data.json', 'rt') as file:
            content = file.readlines()
            for i in content:
                list_for_sort.append(json.loads(i))
        for i in list_for_sort:
            if i['day'] == "Полная занятость" or i['day'] == "Полный рабочий день":
                print(f"{i['name']}, Зп: {i['salary']},"
                      f" Опыт: {i['experience']}, ID: {i['id']}, Занятость: {i['day']}")




manipulation = Manipulation()

def last_user_requirements():
    while True:
        print()
        print("У приложения есть следующие возможности. ")
        print("Вывести вакансию с наибольшей зарплатой - 3")
        print("Отсортировать вакансии по зарплате - 4")
        print("Вывести вакансии с полной занятостью - 5")
        print("Для выхода введите - 0")
        print("Для реализации введите число:")
        action = int(input())
        if action == 3:
            manipulation.show_highest_salary()
        elif action == 4:
            manipulation.sort_by_salary()
        elif action == 5:
            manipulation.show_day_status()
        elif action == 0:
            break
        else:
            print("Некорректный ввод")


# hh_2 = HeadHunterManipulation()
# hh_2.add_vacancy(quantity_vacancy)

# sj_2 = SuperJobAddVacancy()
# sj_2.add_vacancy(quantity_vacancy)



# manipulation.sort_by_salary()
last_user_requirements()


#hh_2.show_highest_salary()
#hh_2.sort_by_salary()
# hh_2.show_day_status()






































