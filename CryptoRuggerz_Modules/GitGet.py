try:
    import requests
    import sherlock
    from bs4 import BeautifulSoup
    import pandas as pd
    import re
    import os
    from subprocess import call
    import colorama
    from colorama import Fore
except Exception as e:
    print("Some Modules are missing {}".format(e))

print(Fore.LIGHTGREEN_EX + "\n============ STARTING PROJECT BACKGROUND CHECK ============\n" + Fore.RESET)

while True:
    base_url = "https://github.com/"
    giturl = input(Fore.LIGHTGREEN_EX + "Enter Project to perform background check on: \n" + Fore.RESET)
    giturlin = "https://github.com/orgs/" + giturl + "/people?page="
    r = requests.get(giturlin)
    soup = BeautifulSoup(r.text, 'html.parser')
    li = soup.findAll('a', class_='f4 d-block')

    Name = []
    RepoNickname = []
    RepoURL = []

    # class CallPy(object):
    #     def __init__(self, path='Users\hidan\PycharmProjects\GitGet\sherlock.py'):
    #         self.path=path
    #     def call_python_file(self):
    #         call(["python", "{}".format(self.path),"/ ",user])

    for _, i in enumerate(li):
        # for a in i.findAll('a', href=True):
        usernick = i["href"]
        userUrl = base_url + i["href"]
        # print(_, i.text.strip(), userUrl)
        Name.append(i.text.strip())
        RepoNickname.append(i["href"])
        RepoURL.append(userUrl)
    tem = list(zip(Name, RepoNickname, RepoURL))
    df = pd.DataFrame(data=tem, columns = ["Name", "RepoNickname", "UserUrl"])
    print(df)

    choice = input(Fore.LIGHTGREEN_EX + "\nEnter choice:\n(1)for user information\n(2)for the projects he is doing\nYour Choice: " + Fore.RESET)
    if choice == "1":
        user = input("Enter the user code to see his information: ")
        print("==============This process will take awhile==============")
        print("Press \"Ctrl + c\" if you are tired of waiting!" )
        cmd =  "python3 sherlock/ "+ str(user)
        os.chdir('../sherlock/')
        os.system(cmd)
        # c = CallPy()
        # c.call_python_file()
        option = input("Enter choice:\n1)See his Github projects\n2)Search another coin\n3)Exit the program.\nYour Choice:")
        if option == "1":
            # url = input("Enter the user to see his repository:\n")
            urlin = "https://github.com/" + user + "?tab=repositories"
            r = requests.get(urlin)
            soup = BeautifulSoup(r.text, 'html.parser')
            # gets information from the html class <d-inline-block mb-1>
            li = soup.findAll('div', class_='d-inline-block mb-1')

            # list to store the values to be later displayed by pandas as df
            no = []
            Repo = []
            url = []

            # _ will print the number due to the enumerate
            for _, i in enumerate(li):

                for a in i.findAll('a'):
                    newUrl = base_url + a["href"]
                no.append(_)
                Repo.append(i.text.strip())
                url.append(newUrl)
                # prints without pandas
                # print(_, i.text.strip(), newUrl)
            tem = list(zip(no, Repo, url))
            df = pd.DataFrame(data=tem, columns=["No", "Repo", "Url"])
            print(df)
            option2 = input("Select your choice:\n1)Enter another coin?\n2)Exit program\nYour choice: ")
            if option2 == "1":
                print("--------------------------------------------------------------------------")
            elif option2 == "2":
                print("Exiting...")
                break
            else:
                while (option2 != "1" or option2 !="2"):
                    print("Invalid input")
                    option2 = input("Select your choice:\n1)Enter another coin?\n2)Exit program\nYour choice: ")
                    if option2 == "1":
                        print("--------------------------------------------------------------------------")
                    elif option2 == "2":
                        print("Exiting...")
                        break
        elif option == "2":
            print("--------------------------------------------------------------------------")
        elif option == "3":
            print("Exiting...")
            break

    elif choice == "2":
        url = input("Enter the user to see his repository:\n")
        userurl = url
        urlin = "https://github.com/"+url+"?tab=repositories"
        r = requests.get(urlin)
        soup = BeautifulSoup(r.text, 'html.parser')
        #gets information from the html class <d-inline-block mb-1>
        li = soup.findAll('div', class_='d-inline-block mb-1')
        #list to store the values to be later displayed by pandas as df
        no = []
        Repo = []
        url = []

        # _ will print the number due to the enumerate
        for _, i in enumerate(li):

            for a in i.findAll('a'):
                newUrl = base_url + a["href"]
            no.append(_)
            Repo.append(i.text.strip())
            url.append(newUrl)
            # prints without pandas
            # print(_, i.text.strip(), newUrl)
        tem = list(zip(no, Repo, url))
        df = pd.DataFrame(data=tem, columns = ["No", "Repo", "Url"])
        print(df)
        option = input("Enter choice:\n1)Find more information about user\n2)Search another coin\n3)Exit the program.\nYour Choice: ")
        if option == "1":
            print("============== This process will take awhile ==============")
            cmd = "python sherlock/ " + str(userurl)
            os.chdir('/Users/hidan/OneDrive/Desktop/sherlock-master')
            os.system(cmd)
            # c = CallPy()
            # c.call_python_file()
        elif option == "2":
            print("--------------------------------------------------------------------------")
        elif option == "3":
            print("Exiting...")
            break
        else:
            print("Wrong input, please try again.")
            break
    else:
        print("Wrong input. Closing....")
        break




