import os
from lib.utils import utils 
from lib.consts import *
from datetime import datetime, timezone
import pandas as pd
import csv

class user:
    def __init__(self, ign, tag):
        self.ign = ign
        self.tag = tag

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = os.path.join(script_dir, "user_data")

        self.user_dir = os.path.join(self.base_dir, ign + tag)  
        if not os.path.exists(self.user_dir):
            # os.makedirs(self.user_dir)
            self.create_dataframe()
            print("Welcome " + ign + "!")
        else: print("Welcome back " + ign + "!")
        
            
    def create_dataframe(self):
        temp = utils.get_puuid(self.ign, self.tag[1:], API_KEY, region="americas")
        if temp[0] == "ERROR":
                print(temp)
                print("Try again later!")
                return
        #
        os.makedirs(self.user_dir)
        prof_data = {
            "Summoner": [self.ign + self.tag],     # To store event or action timestamps
            "PUUID": [temp],
            "Last updated": [s16_start],
            "Games Played": [0],
            "Updated": [False]           
        }
        self.prof_df = pd.DataFrame(prof_data)
        
        #
        # gen_stats = {
        #     "S15 KDA": [],
        #     "S15 W/L": [],

        #     "Norms KDA": [],
        #     "Norms W/L": [],

        #     "ARAM KDA": [],
        #     "ARAM W/L": [],

        #     "Arena KDA": [],
        #     "Arena W/L": []
        # }
        # self.gen_df = pd.DataFrame(gen_stats)

        # This will be match history for now
        self.gen_df = pd.DataFrame()
        
        #
        self.ss_df = pd.DataFrame(columns=["Spell", "Uses"])
       
        #
        self.champ_df = pd.DataFrame()

        self.overall_df = pd.DataFrame()

        # Save the newly created DataFrame
        self.prof_df.to_csv(os.path.join(self.user_dir, self.ign + self.tag + '_prof.csv'), index=False)
        self.gen_df.to_csv(os.path.join(self.user_dir, self.ign + self.tag + 'genStats.csv'))
        self.ss_df.to_csv(os.path.join(self.user_dir, self.ign + self.tag + 'ssCasts.csv'))
        self.champ_df.to_csv(os.path.join(self.user_dir, self.ign + self.tag + 'champStats.csv'))
        self.overall_df.to_csv(os.path.join(self.user_dir, self.ign + self.tag + 'overallStats.csv'))

        with open(os.path.join(self.user_dir, self.ign + self.tag + ".csv"), mode="w") as file:
            pass 

        print(f"New dataframes created and saved")

    def get_dataframes(self):
        prof_filepath = os.path.join(self.user_dir, self.ign + self.tag + '_prof.csv')  
        prof_df = pd.read_csv(prof_filepath)

        champ_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'champStats.csv') 
        champ_df = pd.read_csv(champ_df_filepath)

        ss_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'ssCasts.csv')
        ss_df = pd.read_csv(ss_df_filepath)
        
        gen_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'genStats.csv')
        gen_df = pd.read_csv(gen_df_filepath)

        overall_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'overallStats.csv')
        overall_df = pd.read_csv(overall_df_filepath)

        return prof_df, champ_df, ss_df, gen_df, overall_df
    

    def update(self):
        start_idx = 0
        count = 20 

        # fetching a copy of the profile
        prof_filepath = os.path.join(self.user_dir, self.ign + self.tag + '_prof.csv')  
        profile = pd.read_csv(prof_filepath)
        puuid = profile["PUUID"].iloc[0]
        last_updated = int(profile["Last updated"].iloc[0])
        last_updated_temp = last_updated
        
        match_list = []
        recent_flag = False
        counter = 0
        total_counter = 0
        gen_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'genStats.csv') 
        champ_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'champStats.csv') 
        ss_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'ssCasts.csv')
        overall_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'overallStats.csv')

        champ_df = pd.read_csv(champ_df_filepath)
        ss_df = pd.read_csv(ss_df_filepath)
        overall_df = pd.read_csv(overall_df_filepath)
        gen_df = pd.read_csv(gen_df_filepath)

        while 1:
            # get all the matches
            matches = utils.get_match_ids_all_q_types(puuid, API_KEY, start_idx=start_idx, count=count)
            if matches[0] == "ERROR":
                print(matches)
                print("Try again later!")
                return
            # go through the matches we have just pulled
            for i in range(len(matches)):
                # if the time of the match is greater than what was last recorded then you append + adding second clause to ensure only season 15 games for now
                curr_match = utils.get_match_data(matches[i], API_KEY)
                if "ERROR" in curr_match:
                    print(curr_match)
                    print("Try again later!")
                    return
                time = int(curr_match["info"]["gameStartTimestamp"]) // 1000 #gameCreation is loading screen
                version = int(curr_match["info"]["gameVersion"][:2])
                # if time > last_updated: print("this is a recent game")
                # print(version)
                if time <= last_updated:
                    
                    break
                elif time > last_updated and version == season_16:
                    counter += 1
                    total_counter += 1
                    if recent_flag == False:
                        last_updated_temp = time
                        recent_flag = True
                    # create sublist starting from oldest match that meets this requirement ^^^ and onward
                    match_list.append(matches[i])
                    
                    my_game_data = utils.get_player_data(curr_match, puuid)
                    gen_df = self.update_gen_stats_df(gen_df, my_game_data)
                    champ_df = self.update_champ_df(champ_df, my_game_data)  
                    ss_df = self.update_ss_df(ss_df, my_game_data) 
                    overall_df = self.update_overall(overall_df, my_game_data)
                
            # append the correct set of matches
           

            if len(matches) == counter:
                start_idx += count
                counter = 0
            else: 
                package = (profile, champ_df, ss_df)
                print("\nUpdate completed for " + profile["Summoner"].iloc[0])
                profile.at[0, "Last updated"] = last_updated_temp 
                profile.at[0, "Games Played"] += total_counter
                
                profile.to_csv(prof_filepath, index=False)

                gen_df.to_csv(gen_df_filepath, index=False)
                champ_df.to_csv(champ_df_filepath, index=False)
                ss_df.to_csv(ss_df_filepath, index=False)
                overall_df.to_csv(overall_df_filepath, index=False)

                match_id_filepath = os.path.join(self.user_dir, self.ign + self.tag + '.csv')
                utils.write_csv(match_list, match_id_filepath)


                print(total_counter, "new games recorded :D")
                return package
            
        
    def update_champ_df(self, df, my_game_data): # per champ aggregation
        champ_name = my_game_data["championName"]
        
        win = my_game_data["win"]
        q = int(my_game_data["spell1Casts"])
        w = int(my_game_data["spell2Casts"])
        e = int(my_game_data["spell3Casts"])
        r = int(my_game_data["spell4Casts"])
        k = int(my_game_data["kills"])
        d = int(my_game_data["deaths"])
        a = int(my_game_data["assists"])
        dk = int(my_game_data["doubleKills"])
        tk = int(my_game_data["tripleKills"])
        qk = int(my_game_data["quadraKills"])
        pk = int(my_game_data["pentaKills"])
        goldEarned = int(my_game_data["goldEarned"])
        largestKillingSpree = int(my_game_data["largestKillingSpree"])
        largestMultiKill = int(my_game_data["largestMultiKill"])
        totalDamageDealtToChampions = int(my_game_data["totalDamageDealtToChampions"])
        totalDamageShieldedOnTeammates = int(my_game_data["totalDamageShieldedOnTeammates"])
        totalHealsOnTeammates = int(my_game_data["totalHealsOnTeammates"])
        totalDamageTaken = int(my_game_data["totalDamageTaken"])
        cs = int(my_game_data["neutralMinionsKilled"]) + int(my_game_data["totalMinionsKilled"])
        # cspm = cs / (int(my_game_data["timePlayed"]) / 60)  # FIXED
        # cspm = round(cspm, 1)

        if "Champion" in df.columns and champ_name in df["Champion"].values:
            df.loc[df["Champion"] == champ_name, "Q"] += q
            df.loc[df["Champion"] == champ_name, "W"] += w
            df.loc[df["Champion"] == champ_name, "E"] += e
            df.loc[df["Champion"] == champ_name, "R"] += r

            df.loc[df["Champion"] == champ_name, "Kills"] += k
            df.loc[df["Champion"] == champ_name, "Deaths"] += d
            df.loc[df["Champion"] == champ_name, "Assists"] += a

            df.loc[df["Champion"] == champ_name, "Double Kills"] += dk
            df.loc[df["Champion"] == champ_name, "Triple Kills"] += tk
            df.loc[df["Champion"] == champ_name, "Quadra Kills"] += qk
            df.loc[df["Champion"] == champ_name, "Pentakills"] += pk

            df.loc[df["Champion"] == champ_name, "Gold Earned"] += goldEarned

            curr_val = df.loc[df["Champion"] == champ_name, "Largest Killing Spree"].iloc[0]
            new_val = max(curr_val, largestKillingSpree)
            df.loc[df["Champion"] == champ_name, "Largest Killing Spree"] = new_val

            curr_val = df.loc[df["Champion"] == champ_name, "Largest Multikill"].iloc[0]
            new_val = max(curr_val, largestMultiKill)
            df.loc[df["Champion"] == champ_name, "Largest Multikill"] = new_val

            df.loc[df["Champion"] == champ_name, "Total Damage Dealt to Champions"] += totalDamageDealtToChampions
            df.loc[df["Champion"] == champ_name, "Total Damage Shielded on Teammates"] += totalDamageShieldedOnTeammates
            df.loc[df["Champion"] == champ_name, "Total Heals on Teammates"] += totalHealsOnTeammates
            df.loc[df["Champion"] == champ_name, "Total Damage Taken"] += totalDamageTaken
            df.loc[df["Champion"] == champ_name, "CS"] += cs
            
            # curr_val = df.loc[df["Champion"] == champ_name, "CS/M"].iloc[0]
            # new_val = max(curr_val, cspm)
            # df.loc[df["Champion"] == champ_name, "CS/M"] = new_val
            
            if win:
                df.loc[df["Champion"] == champ_name, "Wins"] += 1
            else:
                df.loc[df["Champion"] == champ_name, "Losses"] += 1

        else:
            new_row = pd.DataFrame([{
                "Champion": champ_name,
                "Q": q,
                "W": w,
                "E": e,
                "R": r,

                "Kills": k,
                "Deaths": d,
                "Assists": a,

                "Double Kills": dk,
                "Triple Kills": tk,
                "Quadra Kills": qk,
                "Pentakills": pk,

                "Gold Earned": goldEarned,
                "Largest Killing Spree": largestKillingSpree,
                "Largest Multikill": largestMultiKill,
                "Total Damage Dealt to Champions": totalDamageDealtToChampions,
                "Total Damage Shielded on Teammates": totalDamageShieldedOnTeammates,
                "Total Heals on Teammates": totalHealsOnTeammates,
                "Total Damage Taken": totalDamageTaken,
                "CS": cs,
                # "CS/M": cspm,

                "Wins": 1 if win else 0,
                "Losses": 0 if win else 1
            }])
            
            # df = new_row
            df = pd.concat([df, new_row], ignore_index=True)
            df = df.convert_dtypes()
        
        df = df.sort_values(by='Champion')
        
        return df
        

    def update_gen_stats_df(self, df, my_game_data): # match history
        champ_name = my_game_data["championName"]
        win = my_game_data["win"]  # should already be boolean
        q = int(my_game_data["spell1Casts"])
        w = int(my_game_data["spell2Casts"])
        e = int(my_game_data["spell3Casts"])
        r = int(my_game_data["spell4Casts"])
        k = int(my_game_data["kills"])
        d = int(my_game_data["deaths"])
        a = int(my_game_data["assists"])
        dk = int(my_game_data["doubleKills"])
        tk = int(my_game_data["tripleKills"])
        qk = int(my_game_data["quadraKills"])
        pk = int(my_game_data["pentaKills"])
        goldEarned = int(my_game_data["goldEarned"])
        largestKillingSpree = int(my_game_data["largestKillingSpree"])
        largestMultiKill = int(my_game_data["largestMultiKill"])
        totalDamageDealtToChampions = int(my_game_data["totalDamageDealtToChampions"])
        totalDamageShieldedOnTeammates = int(my_game_data["totalDamageShieldedOnTeammates"])
        totalHealsOnTeammates = int(my_game_data["totalHealsOnTeammates"])
        totalDamageTaken = int(my_game_data["totalDamageTaken"])
        cs = int(my_game_data["neutralMinionsKilled"]) + int(my_game_data["totalMinionsKilled"])
        # cspm = cs / (int(my_game_data["timePlayed"]) / 60)  # FIXED
        # cspm = round(cspm, 1)

        ss1_name = ss_picker(my_game_data["summoner1Id"])
        ss1_casts = int(my_game_data["summoner1Casts"])
        ss2_name = ss_picker(my_game_data["summoner2Id"])
        ss2_casts = int(my_game_data["summoner2Casts"])

        new_row = pd.DataFrame([{
            "Champion": champ_name,
            "Q": q,
            "W": w,
            "E": e,
            "R": r,

            "Kills": k,
            "Deaths": d,
            "Assists": a,

            "Double Kills": dk,
            "Triple Kills": tk,
            "Quadra Kills": qk,
            "Pentakills": pk,

            "Gold Earned": goldEarned,
            "Largest Killing Spree": largestKillingSpree,
            "Largest Multikill": largestMultiKill,
            "Total Damage Dealt to Champions": totalDamageDealtToChampions,
            "Total Damage Shielded on Teammates": totalDamageShieldedOnTeammates,
            "Total Heals on Teammates": totalHealsOnTeammates,
            "Total Damage Taken": totalDamageTaken,
            "CS": cs,
            # "CS/M": cspm,

            "Win": "Yes" if win else "No",
            


            ss1_name: ss1_casts,
            ss2_name: ss2_casts,
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df = df.convert_dtypes()
        # df = new_row

        return df


    def update_overall(self, df, my_game_data): # aggregation
        win = my_game_data["win"]
        q = int(my_game_data["spell1Casts"])
        w = int(my_game_data["spell2Casts"])
        e = int(my_game_data["spell3Casts"])
        r = int(my_game_data["spell4Casts"])
        k = int(my_game_data["kills"])
        d = int(my_game_data["deaths"])
        a = int(my_game_data["assists"])
        dk = int(my_game_data["doubleKills"])
        tk = int(my_game_data["tripleKills"])
        qk = int(my_game_data["quadraKills"])
        pk = int(my_game_data["pentaKills"])
        goldEarned = int(my_game_data["goldEarned"])
        largestKillingSpree = int(my_game_data["largestKillingSpree"])
        largestMultiKill = int(my_game_data["largestMultiKill"])
        totalDamageDealtToChampions = int(my_game_data["totalDamageDealtToChampions"])
        totalDamageShieldedOnTeammates = int(my_game_data["totalDamageShieldedOnTeammates"])
        totalHealsOnTeammates = int(my_game_data["totalHealsOnTeammates"])
        totalDamageTaken = int(my_game_data["totalDamageTaken"])
        cs = int(my_game_data["neutralMinionsKilled"]) + int(my_game_data["totalMinionsKilled"])
        # cspm = cs / (int(my_game_data["timePlayed"]) / 60)  # FIXED
        # cspm = round(cspm, 2)

        if not df.empty:
            df.loc[0, "Q"] += q
            df.loc[0, "W"] += w
            df.loc[0, "E"] += e
            df.loc[0, "R"] += r

            df.loc[0, "Kills"] += k
            df.loc[0, "Deaths"] += d
            df.loc[0, "Assists"] += a

            df.loc[0, "Double Kills"] += dk
            df.loc[0, "Triple Kills"] += tk
            df.loc[0, "Quadra Kills"] += qk
            df.loc[0, "Pentakills"] += pk

            df.loc[0, "Gold Earned"] += goldEarned
            df.loc[0, "Largest Killing Spree"] = max(df.loc[0, "Largest Killing Spree"], largestKillingSpree)
            df.loc[0, "Largest Multikill"] = max(df.loc[0, "Largest Multikill"], largestMultiKill)
            df.loc[0, "Total Damage Dealt to Champions"] += totalDamageDealtToChampions
            df.loc[0, "Total Damage Shielded on Teammates"] += totalDamageShieldedOnTeammates
            df.loc[0, "Total Heals on Teammates"] += totalHealsOnTeammates
            df.loc[0, "Total Damage Taken"] += totalDamageTaken
            df.loc[0, "CS"] += cs
            # df.loc[0, "CS/M"] += max(df.loc[0, "CS/M"], cspm)

            if win:
                df.loc[0, "Wins"] += 1
            else:
                df.loc[0, "Losses"] += 1

        else:
            new_row = pd.DataFrame([{
                "Q": q, "W": w, "E": e, "R": r,
                "Kills": k, "Deaths": d, "Assists": a,
                "Double Kills": dk, "Triple Kills": tk, "Quadra Kills": qk, "Pentakills": pk,
                "Gold Earned": goldEarned,
                "Largest Killing Spree": largestKillingSpree,
                "Largest Multikill": largestMultiKill,
                "Total Damage Dealt to Champions": totalDamageDealtToChampions,
                "Total Damage Shielded on Teammates": totalDamageShieldedOnTeammates,
                "Total Heals on Teammates": totalHealsOnTeammates,
                "Total Damage Taken": totalDamageTaken,
                "CS": cs, 
                # "CS/M": cspm,
                "Wins": 1 if win else 0,
                "Losses": 0 if win else 1
            }])
            # df = pd.concat([df, new_row], ignore_index=True)
            df = new_row
        return df
        


    def update_ss_df(self, df, my_game_data):
        ss1_name = ss_picker(my_game_data["summoner1Id"])
        ss1_casts = int(my_game_data["summoner1Casts"])
        ss2_name = ss_picker(my_game_data["summoner2Id"])
        ss2_casts = int(my_game_data["summoner2Casts"])
        
        
        if ss1_name in df["Spell"].values:
            df.loc[df["Spell"] == ss1_name, "Uses"] += ss1_casts
        else:
            new_row = pd.DataFrame([{"Spell": ss1_name, "Uses": ss1_casts}])
            df = pd.concat([df, new_row], ignore_index=True)
        
        if ss2_name in df["Spell"].values:
            df.loc[df["Spell"] == ss2_name, "Uses"] += ss2_casts
        else:
            new_row = pd.DataFrame([{"Spell": ss2_name, "Uses": ss2_casts}])
            df = pd.concat([df, new_row], ignore_index=True)
        print(df)
        return df
     
            
  
    def reshape(self):
        return
        # fetching a copy of the profile
        prof_filepath = os.path.join(self.user_dir, self.ign + self.tag + '_prof.csv')  
        profile = pd.read_csv(prof_filepath)
        puuid = profile["PUUID"].iloc[0]
        
        total_counter = 0
        gen_stats_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'genStats.csv') 
        champ_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'champStats.csv') 
        ss_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'ssCasts.csv')

        gen_stats_df = pd.read_csv(gen_stats_filepath)
        champ_df = pd.read_csv(champ_df_filepath)
        ss_df = pd.read_csv(ss_df_filepath)

   
        # get all the matches
        with open(self.user_dir, self.ign + self.tag + '.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                print(lines)
                curr_match = utils.get_match_data(str(lines), API_KEY)
                if "ERROR" in curr_match:
                    print(curr_match)
                    print("Try again later!")
                    return
                total_counter += 1
                my_game_data = utils.get_player_data(curr_match, puuid)
                gen_stats_df = self.update_gen_stats_df(gen_stats_df, my_game_data)
                champ_df = self.update_champ_df(champ_df, my_game_data)  
                ss_df = self.update_ss_df(ss_df, my_game_data) 

        
            print("\nReshape completed for " + profile["Summoner"].iloc[0])
            gen_stats_df.to_csv(gen_stats_filepath, index=False)
            champ_df.to_csv(champ_df_filepath, index=False)
            ss_df.to_csv(ss_df_filepath, index=False)

            


            print(total_counter, "new games recorded :D")
            return
        


    def manual_update(self, start_idx, count=25):

        idx = start_idx
        
        prof_filepath = os.path.join(self.user_dir, self.ign + self.tag + '_prof.csv')  
        profile = pd.read_csv(prof_filepath)
        puuid = profile["PUUID"].iloc[0]
        last_updated = int(profile["Last updated"].iloc[0])
        last_updated_temp = last_updated
        
        match_list = []
        recent_flag = False
        counter = 0
        total_counter = 0
        # gen_stats_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'genStats.csv') 
        champ_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'champStats.csv') 
        ss_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'ssCasts.csv')

        # gen_stats_df = pd.read_csv(gen_stats_filepath)
        champ_df = pd.read_csv(champ_df_filepath)
        ss_df = pd.read_csv(ss_df_filepath)

        
        # get all the matches
        matches = utils.get_match_ids_all_q_types(puuid, API_KEY, start_idx=idx, count=count)
        if matches[0] == "ERROR":
            print(matches)
            print("Try again later!")
            return
        # go through the matches we have just pulled
        for i in range(len(matches)):
            # if the time of the match is greater than what was last recorded then you append + adding second clause to ensure only season 15 games for now
            curr_match = utils.get_match_data(matches[i], API_KEY)
            if "ERROR" in curr_match:
                print(curr_match)
                print("Try again later!")
                return
            time = int(curr_match["info"]["gameStartTimestamp"]) // 1000 #gameCreation is loading screen
            version = int(curr_match["info"]["gameVersion"][:2])
            # if time > last_updated: print("this is a recent game")
            # print(version)
            if time <= last_updated:
                break
            elif time > last_updated and version == curr_season:
                counter += 1
                total_counter += 1
                if recent_flag == False:
                    last_updated_temp = time
                    recent_flag = True
                # create sublist starting from oldest match that meets this requirement ^^^ and onward
                match_list.append(matches[i])
                
                my_game_data = utils.get_player_data(curr_match, puuid)
                # gen_stats_df = self.update_gen_stats_df(gen_stats_df, my_game_data)
                champ_df = self.update_champ_df(champ_df, my_game_data)  
                ss_df = self.update_ss_df(ss_df, my_game_data) 
                
            # append the correct set of matches
           

           
        print("\nUpdate completed for " + profile["Summoner"].iloc[0])
        profile.at[0, "Last updated"] = last_updated_temp 
        profile.to_csv(prof_filepath, index=False)

        # gen_stats_df.to_csv(gen_stats_filepath, index=False)
        champ_df.to_csv(champ_df_filepath, index=False)
        ss_df.to_csv(ss_df_filepath, index=False)

        match_id_filepath = os.path.join(self.user_dir, self.ign + self.tag + '.csv')
        utils.write_csv(match_list, match_id_filepath)


        print(total_counter, "new games recorded :D")
        return

    


    def test_update(self):
        return
        prof_filepath = os.path.join(self.user_dir, self.ign + self.tag + '_prof.csv')  
        profile = pd.read_csv(prof_filepath)
        puuid = profile["PUUID"].iloc[0]
        last_updated = int(profile["Last updated"].iloc[0])
        last_updated_temp = last_updated

        champ_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'champStats.csv') 
        ss_df_filepath = os.path.join(self.user_dir, self.ign + self.tag + 'ssCasts.csv')
        champ_df = pd.read_csv(champ_df_filepath)
        ss_df = pd.read_csv(ss_df_filepath)

        match_list = []

        total_counter = 0

        recent_flag = False

        matches = utils.get_match_ids_all_q_types(puuid, API_KEY, start_idx=0, count=20)
        if matches[0] == "ERROR":
            print(matches)
            print("Try again later!")
            return
        # go through the matches we have just pulled
        for i in range(len(matches)):
            # if the time of the match is greater than what was last recorded then you append + adding second clause to ensure only season 15 games for now
            curr_match = utils.get_match_data(matches[i], API_KEY)
            if "ERROR" in curr_match:
                print(curr_match)
                print("Try again later!")
                return
            time = int(curr_match["info"]["gameStartTimestamp"]) // 1000 #gameCreation is loading screen
            version = int(curr_match["info"]["gameVersion"][:2])
            # if time > last_updated: print("this is a recent game")
            # print(version)
            if time <= last_updated:
                break
            elif time > last_updated and version == curr_season:
               
                total_counter += 1
                if recent_flag == False:
                    last_updated_temp = time
                    recent_flag = True
                # create sublist starting from oldest match that meets this requirement ^^^ and onward
                match_list.append(matches[i])
                
                my_game_data = utils.get_player_data(curr_match, puuid)
                champ_df = self.update_champ_df(champ_df, my_game_data)  
                ss_df = self.update_ss_df(ss_df, my_game_data)

        print("\nUpdate completed for " + profile["Summoner"].iloc[0])
        profile.at[0, "Last updated"] = last_updated_temp 
        profile.to_csv(prof_filepath, index=False)

        
        champ_df.to_csv(champ_df_filepath, index=False)
        ss_df.to_csv(ss_df_filepath, index=False)

        match_id_filepath = os.path.join(self.user_dir, self.ign + self.tag + '.csv')
        utils.write_csv(match_list, match_id_filepath)


        print(total_counter, "new games recorded :D")
        return