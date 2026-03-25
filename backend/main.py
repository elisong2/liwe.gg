from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from lib.liwe import liwe

from lib.user import user
from lib.supaUser import SupaUser
from typing import List, Dict
import traceback

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000" ,       # local dev frontend origin
        "https://liwegg.vercel.app" ,    # deployed frontend origin
        "https://liwegg-production.up.railway.app"
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StatsResponse(BaseModel):
    prof:               List[Dict]
    champs_overall:     List[Dict]
    champs_sr:          List[Dict]
    champs_urf:         List[Dict]
    champs_arena:       List[Dict]
    arena_augments:     List[Dict]
    roles_played:       List[Dict]
    longest_sr:         List[Dict]
    shortest_sr:        List[Dict]
    summs:              List[Dict]
    

@app.get("/")  
def root():
    return {"Thanks for using liwe.gg!"}

# view
@app.get("/player/{ign}-{tag}", response_model=StatsResponse)
def view(ign: str, tag: str) :
    try:
        me = SupaUser(ign, "#"+tag)
        yee = me.data_view()
        
        return {
            'prof': yee["prof"],
            'champs_overall': yee["champs_overall"],
            'champs_sr': yee["champs_sr"],
            'champs_urf': yee["champs_urf"],
            'champs_arena': yee["champs_arena"],
            'arena_augments': yee["arena_augments"],
            'roles_played': yee["roles_played"],
            'longest_sr': yee["longest_sr"],
            'shortest_sr': yee["shortest_sr"],
            'summs': yee["summs"]
        }

    except Exception as e:
        print(traceback.format_exc())  # log error server-side
        raise HTTPException(status_code=500, detail=str(e))

# # new player
@app.post("/player/{ign}-{tag}", response_model=StatsResponse)
def create(ign: str, tag: str):
    try:
        me = SupaUser(ign, "#"+tag)
        me.data_update()
        yee = me.data_view()
        

        return {
            'prof': yee["prof"],
            'champs_overall': yee["champs_overall"],
            'champs_sr': yee["champs_sr"],
            'champs_urf': yee["champs_urf"],
            'champs_arena': yee["champs_arena"],
            'arena_augments': yee["arena_augments"],
            'roles_played': yee["roles_played"],
            'longest_sr': yee["longest_sr"],
            'shortest_sr': yee["shortest_sr"],
            'summs': yee["summs"]
        }

    except Exception as e:
        print(traceback.format_exc())  # log error server-side
        raise HTTPException(status_code=500, detail=str(e))

# # updating player
@app.patch("/player/{ign}-{tag}", response_model=StatsResponse)
def update(ign: str, tag: str):
    try:
        me = SupaUser(ign, "#"+tag)
        me.data_update()
        yee = me.data_view()
        

        return {
            'prof': yee["prof"],
            'champs_overall': yee["champs_overall"],
            'champs_sr': yee["champs_sr"],
            'champs_urf': yee["champs_urf"],
            'champs_arena': yee["champs_arena"],
            'arena_augments': yee["arena_augments"],
            'roles_played': yee["roles_played"],
            'longest_sr': yee["longest_sr"],
            'shortest_sr': yee["shortest_sr"],
            'summs': yee["summs"]
        }

    except Exception as e:
        print(traceback.format_exc())  # log error server-side
        raise HTTPException(status_code=500, detail=str(e))
    



'''
Alright one more time to get the chain of command down lol. 

User hits update -> 
frontend sends http patch -> 
backend runs liwe script (gets info from riot api, updates dataframes if needed) -> 
sends a response in the form of basemodel back to frontend, either with new info or to say there is nothing to update -> 
frontend handles it accordingly 
'''
