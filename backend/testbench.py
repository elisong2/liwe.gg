from lib.utils import utils 
from lib.consts import *
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import requests
from lib.supaUser import SupaUser

def test1():
    print(utils.get_puuid("OPMAGEMASTER", "NA1", API_KEY))
    print(API_KEY)

def test2(epoch):
    utils.unix_converter(epoch)

def test3():
    data = [1, 2, 3]
    utils.write_csv(data, "output.csv")                                                                                       

def get_all_games(): # retrieves ids for all old games available, up to 1000 count 
    onek = []
    index = 0
    for i in range(10):
        print(index) 
        matches = utils.get_match_ids_all_q_types(OPMAGE_PUUID, API_KEY, index, 100)
        index += 100
        
    # print(matches)
    # print(len(matches))

def find_ranked():
    return 0

def get_some_games(player, file):
    with open('output.csv', 'w') as file:
        pass

    matches = utils.get_match_ids_all_q_types(player, API_KEY, count=20)
    utils.write_csv(matches)


def poop(): # find first game of that ranked grind
    balls = utils.get_match_ids_by_q_type(OPMAGE_PUUID, API_KEY, RANKED, start_idx=0, count=50)
    # balls = utils.get_match_ids_all_q_types(OPMAGE_PUUID, API_KEY, count=20)
    with open('output.csv', 'w') as file:
        pass
    utils.write_csv(balls)

def fart():
    balls = utils.get_match_data("NA1_4849818099", API_KEY)
    peen = utils.get_player_data(balls, OPMAGE_PUUID)

    # print(balls['info']['gameCreation'])
    print(peen)


def bbb():
    print(utils.unix_converter(1701739762015))
# fart()
# fart()

def nut():
    row = 3
    col = 0
    print((row // 3) * 3 + (col // 3))

def hi():
    # x = utils.get_match_ids_all_q_types(OPMAGE_PUUID, count=1, start_idx=10)
    y = utils.get_match_data('NA1_5331861807')
    z = utils.get_player_data(y, OPMAGE_PUUID)
    print(y['info']['queueId'])


def bye():
    return 1, 2, 3

# print("Unix_Time =>",unix_time)
# displaying date and time in a regular 
# string format
# print("Date & Time =>" ,
#       date_time.strftime('%Y-%m-%d %H:%M:%S'))

# import datetime

# Unix epoch timestamp (e.g., 1696857600)
# timestamp = 1729322547223
# Convert the Unix timestamp to a datetime object
# dt_object = datetime.datetime.fromtimestamp(timestamp)
# print(timestamp//1000)
# Print the result
#print(dt_object)



"""
#1: some games from the request are already on record, need to be able to start appending
at the correct index

#2: request no go far enough back, need to be able to tell that it hasn't got 
everything and increase the starting index

function():
                check #1 here
    while some timestamp is greater than the last recorded timestamp in player class
        
        request
        use datetime.datetime.now() to choose appropriate 'count'
        use iterative method to check first index that is greater than lastrecord
            *** count value spans 20-100 *** figure out a mod operation?
            if the diff b/w curr date and lastrecord <= 2 days: count = 20
            1 day = 86400 seconds = 8.64e7 milliseconds


        set some condition for the next iteration to check
        option 1: if the entire request list was appended to csv
                  then use unix time of final appended game to determine 'index'

"""


   

        
def dickballs():
    counter = 0
    while 1:
        counter += 1
        if counter == 4:
            break
    
    print("dickballs", counter)

def season15start():
    start = datetime(2025, 1, 9, 0, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    print(int(start.timestamp()))






# bigdick()

def fml():
    print("first 5")
    print(utils.get_match_ids_all_q_types(OPMAGE_PUUID, API_KEY, start_idx=0, count=5))
    print("next 5")
    print(utils.get_match_ids_all_q_types(OPMAGE_PUUID, API_KEY, start_idx=5, count=5))
    print("\n")
    print("all 10")
    print(utils.get_match_ids_all_q_types(OPMAGE_PUUID, API_KEY, start_idx=0, count=10))

# print(fml())

def pus(listy):
    for i in range(len(listy) - 1):
        if listy[i] == 2 and listy[i+1] == 2:
            print("True")
    
    print("False")

def getJSON():
    my_url = "https://ddragon.leagueoflegends.com/cdn/15.9.1/data/en_US/summoner.json"
    api_resp = requests.get(my_url)
    print(api_resp.json())

# getJSON()


def decoding_match_data():
    data = utils.get_match_data("NA1_5347838860", API_KEY)
    my_data = utils.get_player_data(data, OPMAGE_PUUID)
    # print(my_data)
    print(my_data["timePlayed"])
    # print(my_data["win"])
    # print(my_data["spell1Casts"])


# decoding_match_data()

# x = utils.unix_converter(1746825492)
# print(x)


def season16start():
    start = datetime(2025, 1, 8, 0, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    print(int(start.timestamp()))

def bigdick():
    print(utils.get_match_ids_all_q_types(OPMAGE_PUUID, API_KEY, count=100))

def newDecodeMatch(matchid):
    data = utils.get_match_data(matchid, API_KEY)
    my_data = utils.get_player_data(data, OPMAGE_PUUID)
    print(my_data)

# bigdick()
# newDecodeMatch('NA1_5433541005')

def supatest():
    fart = SupaUser("mingoose9", "#NA1")
    fart.data_update()
    fart.data_view()

def augment_test():
    url = "https://raw.communitydragon.org/latest/cdragon/arena/en_us.json"
    augment_data = requests.get(url).json()
    print(augment_data["augments"][0]["name"])
    
    
    
    augment_map = {
       int(augment["id"]): augment["name"]
        for augment in augment_data["augments"]
    }
    print(augment_map)

def get_champ_roles(champ):
    url = "https://ddragon.leagueoflegends.com/cdn/16.6.1/data/en_US/champion.json"
    champ_data = requests.get(url).json()
    print(champ_data["data"][champ]["tags"][0])
    print(champ_data["data"][champ]["name"])
    # return champ_data["data"][champ]["tags"][0]

def get_champ_names():
    url = "https://ddragon.leagueoflegends.com/cdn/16.6.1/data/en_US/champion.json"
    champ_data = requests.get(url).json()
    
    formatted_names = {}
    for champ, values in champ_data["data"].items():
        formatted_names[champ] = values["name"]
        
    return formatted_names

def convert_seconds_to_minutes(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    if remaining_seconds < 10:
        remaining_seconds = f"0{remaining_seconds}"
    print(f"{minutes}:{remaining_seconds}")

supatest()