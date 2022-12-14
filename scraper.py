import requests
from bs4 import BeautifulSoup

response = requests.get("https://stadion.uz/")
soup = BeautifulSoup(response.text, "html.parser")

global liga

games = soup.find_all("div", id="online_tablo")

info = []

no_info = []


def scrape_data():
    global data_list
    info = []
    no_info = []

    if games != []:
        for g in games[0].ul.find_all("li"):
            data_list = []
            data = {}
            try:
                if g.div.get("id", "") == "online_tablo_title":
                    match_list = []
                    liga = g.div.b.text
                    # print("\n\nLiga: ", liga)
                    matches = g.ul.find_all("ul", id="online_tablo_game")

                    for i in matches:
                        match = {}
                        text = ""
                        for k in i.text.split("\n"):
                            text += " " + k.strip()
                        splited_data = text.split()
                        time = splited_data[0] + " " + splited_data[1]
                        team = ' '.join(splited_data[2:])

                        # print(f"Time: {time}")
                        # print(f"Team: {team}")

                        match.update({'time': f'{time}'})
                        match.update({'team': f'{team}'})
                        # print('Match:', match)

                        match_list.append(match)
                    # print('\n\nMatch list:', match_list)

                    data.update({'name': f'{liga}'})
                    data.update({'matches': match_list})
                    data_list.append(data)
                    # print('\n\nData list:', data_list)

                info.append(data_list)
                # print('Info:', info)
            except:
                pass
        return info
    else:
        match = {}
        data_list = []
        match_list = []
        data = {}

        match.update({'time': ''})
        match.update({'team': ''})

        match_list.append(match)

        data.update({'name': 'no data'})
        data.update({'matches': match_list})

        data_list.append(data)

        no_info.append(data_list)

        return no_info


scrape_data()


