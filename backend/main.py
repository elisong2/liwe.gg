from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from lib.liwe import liwe

from lib.user import user
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
    prof:          List[Dict]
    champ_agg:     List[Dict]
    summs:         List[Dict]
    match_history: List[Dict]
    overall_agg:   List[Dict]

@app.get("/")  
def root():
    return {"Thanks for using liwe.gg!"}

# view
@app.get("/player/{ign}-{tag}", response_model=StatsResponse)
def view(ign: str, tag: str) :
    try:
        me = user(ign, "#"+tag)
        prof_df, champ_df, ss_df, gen_df, overall_df = me.get_dataframes()

        prof_df = prof_df.drop(columns=["Unnamed: 0"], errors="ignore")
        champ_df = champ_df.drop(columns=["Unnamed: 0"], errors="ignore")
        ss_df = ss_df.drop(columns=["Unnamed: 0"], errors="ignore")
        gen_df = gen_df.drop(columns=["Unnamed: 0"], errors="ignore")
        overall_df = overall_df.drop(columns=["Unnamed: 0"], errors="ignore")

        return {
            'prof': prof_df.to_dict(orient="records"),
            'champ_agg': champ_df.to_dict(orient="records"),
            'summs': ss_df.to_dict(orient="records"),
            'match_history': gen_df.to_dict(orient="records"),
            'overall_agg': overall_df.to_dict(orient="records")
        }

    except Exception as e:
        print(traceback.format_exc())  # log error server-side
        raise HTTPException(status_code=500, detail=str(e))

# # new player
@app.post("/player/{ign}-{tag}", response_model=StatsResponse)
def create(ign: str, tag: str):
    try:
        me = user(ign, "#"+tag)
        me.update()
        prof_df, champ_df, ss_df, gen_df, overall_df = me.get_dataframes()
        

        prof_df = prof_df.drop(columns=["Unnamed: 0"], errors="ignore")
        champ_df = champ_df.drop(columns=["Unnamed: 0"], errors="ignore")
        ss_df = ss_df.drop(columns=["Unnamed: 0"], errors="ignore")
        gen_df = gen_df.drop(columns=["Unnamed: 0"], errors="ignore")
        overall_df = overall_df.drop(columns=["Unnamed: 0"], errors="ignore")

        return {
            'prof': prof_df.to_dict(orient="records"),
            'champ_agg': champ_df.to_dict(orient="records"),
            'summs': ss_df.to_dict(orient="records"),
            'match_history': gen_df.to_dict(orient="records"),
            'overall_agg': overall_df.to_dict(orient="records")
        }

    except Exception as e:
        print(traceback.format_exc())  # log error server-side
        raise HTTPException(status_code=500, detail=str(e))

# # updating player
@app.patch("/player/{ign}-{tag}", response_model=StatsResponse)
def update(ign: str, tag: str):
    try:
        me = user(ign, "#"+tag)
        me.update()
        prof_df, champ_df, ss_df, gen_df, overall_df = me.get_dataframes()
        

        prof_df = prof_df.drop(columns=["Unnamed: 0"], errors="ignore")
        champ_df = champ_df.drop(columns=["Unnamed: 0"], errors="ignore")
        ss_df = ss_df.drop(columns=["Unnamed: 0"], errors="ignore")
        gen_df = gen_df.drop(columns=["Unnamed: 0"], errors="ignore")
        overall_df = overall_df.drop(columns=["Unnamed: 0"], errors="ignore")

        return {
            'prof': prof_df.to_dict(orient="records"),
            'champ_agg': champ_df.to_dict(orient="records"),
            'summs': ss_df.to_dict(orient="records"),
            'match_history': gen_df.to_dict(orient="records"),
            'overall_agg': overall_df.to_dict(orient="records")
        }

    except Exception as e:
        print(traceback.format_exc())  # log error server-side
        raise HTTPException(status_code=500, detail=str(e))
    
# def build_response(me):
#     prof_df, champ_df, ss_df, gen_df, overall_df = me.get_dataframes()
#     return {
#             'prof': prof_df.to_dict(orient="records"),
#             'champ_agg': champ_df.to_dict(orient="records"),
#             'summs': ss_df.to_dict(orient="records"),
#             'match_history': gen_df.to_dict(orient="records"),
#             'overall_agg': overall_df.to_dict(orient="records")
#         }


'''
Alright one more time to get the chain of command down lol. 

User hits update -> 
frontend sends http patch -> 
backend runs liwe script (gets info from riot api, updates dataframes if needed) -> 
sends a response in the form of basemodel back to frontend, either with new info or to say there is nothing to update -> 
frontend handles it accordingly 
'''
