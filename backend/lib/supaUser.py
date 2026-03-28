import os
from urllib import response

import supabase
from lib.utils import utils 
from lib.consts import *
from datetime import datetime, timezone
from supabase import create_client, Client

class SupaUser:
    def __init__(self, ign, tag):
        self.ign = ign
        self.tag = tag
        self.summoner = ign+tag
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

        temp = utils.get_puuid(self.ign, self.tag[1:], API_KEY, region="americas")
        if temp[0] == "ERROR":
                print("THERE WAS AN ERROR: ", temp)
                
                raise Exception(f"PUUID lookup failed: {temp}")
              
        else:
            self.puuid = temp

        print(self.puuid)
        
        new_user_response = self.supabase.table("profiles").upsert(
            {
             "summoner": self.summoner,
             "puuid": temp,
             "last_updated": s16_start_na,
             "total_games_played": 0,
             "arena_games_played": 0,
             "updated": False
             },
             on_conflict="puuid",
             ignore_duplicates=True
        ).execute()

        
        
        profile_retrieve = self.supabase.table("profiles").select("*").eq("puuid", temp).execute()
        
        if profile_retrieve.data[0]["summoner"] != self.summoner:
            update_summoner_name_response = self.supabase.table("profiles").update(
                {
                    "summoner": self.summoner
                }
            ).eq("puuid", self.puuid
        ).execute()
        

        print("response:", response)
        print(f"Welcome {self.summoner}!")
        print(self.puuid)

        self.last_updated= int(profile_retrieve.data[0]["last_updated"])
        self.total_games_played = int(profile_retrieve.data[0]["total_games_played"])
        self.arena_games_played = int(profile_retrieve.data[0]["arena_games_played"])

        utils.load_augments()
        
    def data_view(self):
        response_data = {}
        
        profiles_response = (
            self.supabase.table("profiles")
            .select("*")
            .eq("puuid", self.puuid)
            .execute()
        ).data

        champs_overall_response = (
            self.supabase.table("per_champ_overall")
            .select("*")
            .eq("profile_puuid", self.puuid)
            .order("champion", desc=False)
            .execute()
        ).data
        
        champs_sr_response = (
            self.supabase.table("per_champ_sr")
            .select("*")
            .eq("profile_puuid", self.puuid)
            .order("champion", desc=False)
            .execute()
        ).data 
        
        champs_urf_response = (
            self.supabase.table("per_champ_urf")
            .select("*")
            .eq("profile_puuid", self.puuid)
            .order("champion", desc=False)
            .execute()
        ).data

        champs_arena_response = (
            self.supabase.table("per_champ_arena")
            .select("*")
            .eq("profile_puuid", self.puuid)
            .order("champion", desc=False)
            .execute()
        ).data

        arena_augments_response = (
            self.supabase.table("arena_augments_selected")
            .select("*")
            .eq("profile_puuid", self.puuid)
            .order("augment", desc=False)
            .execute()
        ).data

        roles_played_response = (
            self.supabase.table("roles_played")
            .select("*")
            .eq("profile_puuid", self.puuid)
            .execute()
        ).data

        longest_sr_response = (
            self.supabase.table("longest_sr_games")
            .select("*")
            .eq("profile_puuid", self.puuid)
            .execute()
        ).data

        shortest_sr_response = (
            self.supabase.table("shortest_sr_games")
            .select("*")
            .eq("profile_puuid", self.puuid)
            .execute()
        ).data

        summs_response = (
            self.supabase.table("summs_total")
            .select("*")
            .eq("profile_puuid", self.puuid)
            .execute()
        ).data

        response_data["prof"] = profiles_response
        response_data["champs_overall"] = champs_overall_response
        response_data["champs_sr"] = champs_sr_response
        response_data["champs_urf"] = champs_urf_response
        response_data["champs_arena"] = champs_arena_response
        response_data["arena_augments"] = arena_augments_response
        response_data["roles_played"] = roles_played_response
        response_data["longest_sr"] = longest_sr_response
        response_data["shortest_sr"] = shortest_sr_response
        response_data["summs"] = summs_response

        return response_data         

    def data_update(self):
        formatted_champ_names = utils.get_champ_names()
        match_list = []
        recent_flag = False
        counter = 0
        total_counter = 0
        start_idx = 0
        count = 20 
        last_updated_temp = self.last_updated
        arena_game_counter = 0
        max_game_length_time = 0
        min_game_length_time = 0

        while 1:
            matches = utils.get_match_ids_all_q_types(self.puuid, API_KEY, start_idx=start_idx, count=count)
            print(matches)
            
            if matches[0] == "ERROR":
                print(matches)
                print("Try again later!")
                return
            # go through the matches we have just pulled
            for i in range(len(matches)):
                # if the time of the match is greater than what was last recorded then you append + adding second clause to ensure only season 15 games for now
                curr_match = utils.get_match_data(matches[i], API_KEY)
                gameMode = curr_match["info"]["gameMode"]
                mapId = int(curr_match["info"]["mapId"])
                queueId = int(curr_match["info"]["queueId"])
                gameType = curr_match["info"]["gameType"]
                print("gameMode:",curr_match["info"]["gameMode"]) # should be CLASSIC
                print("mapId:",curr_match["info"]["mapId"]) # should be 11
                print("queueId:",curr_match["info"]["queueId"]) # should be 400
                print("gameType:",curr_match["info"]["gameType"]) # should be MATCHED_GAME
                
                max_game_length_time = max(max_game_length_time, int(curr_match["info"]["gameDuration"]))
                min_game_length_time = min(min_game_length_time, int(curr_match["info"]["gameDuration"])) if min_game_length_time > 0 else int(curr_match["info"]["gameDuration"])

                if "ERROR" in curr_match:
                    print(curr_match)
                    print("Try again later!")
                    return
                time = int(curr_match["info"]["gameStartTimestamp"]) // 1000 # gameCreation is loading screen
                version = int(curr_match["info"]["gameVersion"][:2])
                # if time > last_updated: print("this is a recent game")
                # print(version)
                if time <= self.last_updated:
                    break
                elif time > self.last_updated and version == season_16:
                    counter += 1
                    total_counter += 1
                    if recent_flag == False:
                        last_updated_temp = time
                        recent_flag = True
                        print("LAST UPDATED TEMP:", last_updated_temp)
                    # create sublist starting from oldest match that meets this requirement ^^^ and onward

                    match_list.append(matches[i])
                    
                    my_game_data = utils.get_player_data(curr_match, self.puuid)
                    stuff = self.format_game_data(my_game_data, formatted_champ_names)
                    # print(my_game_data)
                    # return

                    # updating database happens here
                    self.update_per_champ_overall(stuff)

                    self.supabase.rpc("update_roles_played", {
                        "p_profile_puuid": self.puuid,
                        "p_role": utils.get_champ_role(my_game_data["championName"]),
                        "p_wins": stuff["win"],
                        "p_losses": stuff["loss"]
                    }).execute()

                    self.update_summs(my_game_data)
                    if (
                        gameMode in ["CLASSIC", "SWIFTPLAY"] and 
                        gameType == "MATCHED_GAME" and
                        mapId in [1, 2, 11] and
                        queueId in [400, 420, 430, 440, 480, 490, 700, 870, 880, 890]
                    ):
                        self.update_per_champ_sr(stuff)
                        self.supabase.rpc("update_game_extremes_full", {
                            "p_profile_puuid": self.puuid,
                            "p_champion": stuff["champion"],
                            "p_gameduration": curr_match["info"]["gameDuration"],
                            "p_kills": stuff["k"],
                            "p_deaths": stuff["d"],
                            "p_assists": stuff["a"]
                        }).execute()
                    
                    elif queueId in [1700, 1710]: 
                        self.update_per_champ_arena(stuff, my_game_data)

                        arena_game_counter += 1
                    
                    elif gameMode == "URF" and queueId in [900, 1900, 1010]:
                        self.update_per_champ_urf(stuff)
                    
                
            # append the correct set of matches
        
            if len(matches) == counter:
                start_idx += count
                counter = 0
            else: 
                print("\nUpdate completed for " + self.summoner + "!")
                
                update_result = self.supabase.table("profiles").update(
                    {
                    "last_updated": last_updated_temp, 
                    "total_games_played": self.total_games_played + total_counter,
                    "arena_games_played": self.arena_games_played + arena_game_counter,
                    }).eq("puuid", self.puuid).execute()
                
                print("puuid being used:", self.puuid)
                print("update result:", update_result)
                # self.supabase.table("match_ids").upsert(
                #     {
                #     "summoner": self.summoner,
                #     "puuid": temp,
                #     "last_updated": s16_start,
                #     "total_games_played": 0,
                #     "arena_games_played": 0,
                #     "updated": False
                #     },
                #     on_conflict="puuid"
                #     ).execute()
    
                # update summoner name in database if changed
                # record match ids
                # make default values 0
            
                print(total_counter, "new games recorded :D")
                return
    
        

    def update_per_champ_overall(self, stuff):
        self.supabase.rpc("update_per_champ_overall", {
            "p_profile_puuid": self.puuid,
            "p_champion": stuff["champion"],
            "p_wins": stuff["win"],
            "p_losses": stuff["loss"],
            "p_q": stuff["q"],
            "p_w": stuff["w"],
            "p_e": stuff["e"],
            "p_r": stuff["r"],
            "p_k": stuff["k"],
            "p_d": stuff["d"],
            "p_a": stuff["a"],
            "p_dk": stuff["dk"],
            "p_tk": stuff["tk"],
            "p_qk": stuff["qk"],
            "p_pk": stuff["pk"],
            "p_largestkillingspree": stuff["largestKillingSpree"],
            "p_longesttimespentliving": stuff["longestTimeSpentLiving"],
            "p_firstbloodkill": stuff["firstBloodKill"],
            "p_firsttowerkill": stuff["firstTowerKill"],
            "p_goldearned": stuff["goldEarned"],
            "p_cs": stuff["cs"],
            "p_totaldamagedealttochampions": stuff["totalDamageDealtToChampions"],
            "p_totaldamagetaken": stuff["totalDamageTaken"],
            "p_totaldamageshieldedonteammates": stuff["totalDamageShieldedOnTeammates"],
            "p_damageselfmitigated": stuff["damageSelfMitigated"],
            "p_totalhealsonteammates": stuff["totalHealsOnTeammates"],
            "p_timeccingothers": stuff["timeCCingOthers"],
            "p_damagedealttobuildings": stuff["damageDealtToBuildings"],
            "p_damagedealttoobjectives": stuff["damageDealtToObjectives"],
            "p_damagedealttoturrets": stuff["damageDealtToTurrets"],
            "p_missingpings": stuff["missingPings"],
            "p_visionscore": stuff["visionScore"],
            "p_wardskilled": stuff["wardsKilled"],
            "p_wardsplaced": stuff["wardsPlaced"]
        }).execute()
    def update_per_champ_sr(self, stuff):
        self.supabase.rpc("update_per_champ_sr", {
            "p_profile_puuid": self.puuid,
            "p_champion": stuff["champion"],
            "p_wins": stuff["win"],
            "p_losses": stuff["loss"],
            "p_q": stuff["q"],
            "p_w": stuff["w"],
            "p_e": stuff["e"],
            "p_r": stuff["r"],
            "p_k": stuff["k"],
            "p_d": stuff["d"],
            "p_a": stuff["a"],
            "p_dk": stuff["dk"],
            "p_tk": stuff["tk"],
            "p_qk": stuff["qk"],
            "p_pk": stuff["pk"],
            "p_largestkillingspree": stuff["largestKillingSpree"],
            "p_longesttimespentliving": stuff["longestTimeSpentLiving"],
            "p_firstbloodkill": stuff["firstBloodKill"],
            "p_firsttowerkill": stuff["firstTowerKill"],
            "p_goldearned": stuff["goldEarned"],
            "p_cs": stuff["cs"],
            "p_totaldamagedealttochampions": stuff["totalDamageDealtToChampions"],
            "p_totaldamagetaken": stuff["totalDamageTaken"],
            "p_totaldamageshieldedonteammates": stuff["totalDamageShieldedOnTeammates"],
            "p_damageselfmitigated": stuff["damageSelfMitigated"],
            "p_totalhealsonteammates": stuff["totalHealsOnTeammates"],
            "p_timeccingothers": stuff["timeCCingOthers"],
            "p_damagedealttobuildings": stuff["damageDealtToBuildings"],
            "p_damagedealttoobjectives": stuff["damageDealtToObjectives"],
            "p_damagedealttoturrets": stuff["damageDealtToTurrets"],
            "p_missingpings": stuff["missingPings"],
            "p_visionscore": stuff["visionScore"],
            "p_wardskilled": stuff["wardsKilled"],
            "p_wardsplaced": stuff["wardsPlaced"]
        }).execute()
    def update_per_champ_arena(self, stuff, my_game_data):
        self.supabase.rpc("update_per_champ_arena", {
            "p_profile_puuid": self.puuid,
            "p_champion": stuff["champion"],
            "p_wins": stuff["win"],
            "p_losses": stuff["loss"],
            "p_q": stuff["q"],
            "p_w": stuff["w"],
            "p_e": stuff["e"],
            "p_r": stuff["r"],
            "p_k": stuff["k"],
            "p_d": stuff["d"],
            "p_a": stuff["a"],
            "p_largestkillingspree": stuff["largestKillingSpree"],
            "p_longesttimespentliving": stuff["longestTimeSpentLiving"],
            "p_goldearned": stuff["goldEarned"],
            "p_totaldamagedealttochampions": stuff["totalDamageDealtToChampions"],
            "p_totaldamagetaken": stuff["totalDamageTaken"],
            "p_totaldamageshieldedonteammates": stuff["totalDamageShieldedOnTeammates"],
            "p_damageselfmitigated": stuff["damageSelfMitigated"],
            "p_totalhealsonteammates": stuff["totalHealsOnTeammates"],
            "p_timeccingothers": stuff["timeCCingOthers"],
            "p_missingpings": stuff["missingPings"],
        }).execute()


        augment_ids = [
            my_game_data["playerAugment1"],
            my_game_data["playerAugment2"],
            my_game_data["playerAugment3"],
            my_game_data["playerAugment4"],
            my_game_data["playerAugment5"],
            my_game_data["playerAugment6"],
        ]
        augment_map = utils.load_augments()
        augment_names = [augment_map.get(aug_id, "Unknown Augment") for aug_id in augment_ids if aug_id > 0]

        p_data = [
            {"augment": aug, "times_selected": 1}
            for aug in augment_names
            if aug != "Unknown Augment"
        ]
        self.supabase.rpc("bulk_update_arena_augments", {
            "p_profile_puuid": self.puuid,
            "p_augment_data" : p_data
        }).execute()



    def update_per_champ_urf(self, stuff):
        self.supabase.rpc("update_per_champ_urf", {
            "p_profile_puuid": self.puuid,
            "p_champion": stuff["champion"],
            "p_wins": stuff["win"],
            "p_losses": stuff["loss"],
            "p_q": stuff["q"],
            "p_w": stuff["w"],
            "p_e": stuff["e"],
            "p_r": stuff["r"],
            "p_k": stuff["k"],
            "p_d": stuff["d"],
            "p_a": stuff["a"],
            "p_dk": stuff["dk"],
            "p_tk": stuff["tk"],
            "p_qk": stuff["qk"],
            "p_pk": stuff["pk"],
            "p_largestkillingspree": stuff["largestKillingSpree"],
            "p_longesttimespentliving": stuff["longestTimeSpentLiving"],
            "p_firstbloodkill": stuff["firstBloodKill"],
            "p_firsttowerkill": stuff["firstTowerKill"],
            "p_goldearned": stuff["goldEarned"],
            "p_cs": stuff["cs"],
            "p_totaldamagedealttochampions": stuff["totalDamageDealtToChampions"],
            "p_totaldamagetaken": stuff["totalDamageTaken"],
            "p_totaldamageshieldedonteammates": stuff["totalDamageShieldedOnTeammates"],
            "p_damageselfmitigated": stuff["damageSelfMitigated"],
            "p_totalhealsonteammates": stuff["totalHealsOnTeammates"],
            "p_timeccingothers": stuff["timeCCingOthers"],
            "p_damagedealttobuildings": stuff["damageDealtToBuildings"],
            "p_damagedealttoobjectives": stuff["damageDealtToObjectives"],
            "p_damagedealttoturrets": stuff["damageDealtToTurrets"],
            "p_missingpings": stuff["missingPings"],
            "p_visionscore": stuff["visionScore"],
            "p_wardskilled": stuff["wardsKilled"],
            "p_wardsplaced": stuff["wardsPlaced"]
        }).execute()

    def update_summs(self, my_game_data):
        ss1_name = ss_picker(my_game_data["summoner1Id"])
        ss1_casts = int(my_game_data["summoner1Casts"])
        ss2_name = ss_picker(my_game_data["summoner2Id"])
        ss2_casts = int(my_game_data["summoner2Casts"])

        # self.supabase.rpc("update_summs_used", {
        #     "p_profile_puuid": self.puuid,
        #     "p_spell": ss1_name,
        #     "p_casts": ss1_casts
        # }).execute()

        # self.supabase.rpc("update_summs_used", {
        #     "p_profile_puuid": self.puuid,
        #     "p_spell": ss2_name,
        #     "p_casts": ss2_casts
        # }).execute()

        self.supabase.rpc("bulk_update_summs", {
            "p_profile_puuid": self.puuid,
            "p_summs_data": [
                {"spell": ss1_name, "casts": ss1_casts},
                {"spell": ss2_name, "casts": ss2_casts}
            ]
        }).execute()

        print("Summs updated for " + self.summoner)

    
    def format_game_data(self, my_game_data, formatted_champ_names):
        
        stuff = {}

        if my_game_data["championName"] == "FiddleSticks":
             stuff["champion"] = "Fiddlesticks"
        else:
            stuff["champion"] = formatted_champ_names[my_game_data["championName"]]

        stuff["win"] = 1 if my_game_data["win"] else 0
        stuff["loss"] = 0 if my_game_data["win"] else 1
        stuff["q"] = int(my_game_data["spell1Casts"])
        stuff["w"] = int(my_game_data["spell2Casts"])
        stuff["e"] = int(my_game_data["spell3Casts"])
        stuff["r"] = int(my_game_data["spell4Casts"])
        stuff["k"] = int(my_game_data["kills"])
        stuff["d"] = int(my_game_data["deaths"])
        stuff["a"] = int(my_game_data["assists"])
        stuff["dk"] = int(my_game_data["doubleKills"])
        stuff["tk"] = int(my_game_data["tripleKills"])
        stuff["qk"] = int(my_game_data["quadraKills"])
        stuff["pk"] = int(my_game_data["pentaKills"])
        stuff["largestKillingSpree"] = int(my_game_data["largestKillingSpree"])
        stuff["longestTimeSpentLiving"] = int(my_game_data["longestTimeSpentLiving"])
        stuff["firstBloodKill"] = 1 if my_game_data["firstBloodKill"] else 0
        stuff["firstTowerKill"] = 1 if my_game_data["firstTowerKill"] else 0
        stuff["goldEarned"] = int(my_game_data["goldEarned"])
        stuff["cs"] = int(my_game_data["neutralMinionsKilled"]) + int(my_game_data["totalMinionsKilled"])
        # largestMultiKill = int(my_game_data["largestMultiKill"])
        stuff["totalDamageDealtToChampions"] = int(my_game_data["totalDamageDealtToChampions"])
        stuff["totalDamageTaken"] = int(my_game_data["totalDamageTaken"])
        stuff["totalDamageShieldedOnTeammates"] = int(my_game_data["totalDamageShieldedOnTeammates"])
        stuff["damageSelfMitigated"] = int(my_game_data["damageSelfMitigated"])
        stuff["totalHealsOnTeammates"] = int(my_game_data["totalHealsOnTeammates"])
        stuff["timeCCingOthers"] = int(my_game_data["timeCCingOthers"])
        stuff["damageDealtToBuildings"] = int(my_game_data["damageDealtToBuildings"])
        stuff["damageDealtToObjectives"] = int(my_game_data["damageDealtToObjectives"])
        stuff["damageDealtToTurrets"] = int(my_game_data["damageDealtToTurrets"])
        stuff["missingPings"] = int(my_game_data["enemyMissingPings"])
        # stuff["teamPosition"] = my_game_data["teamPosition"]
        stuff["visionScore"] = int(my_game_data["visionScore"])
        stuff["wardsKilled"] = int(my_game_data["wardsKilled"])
        stuff["wardsPlaced"] = int(my_game_data["wardsPlaced"])

        return stuff
        
