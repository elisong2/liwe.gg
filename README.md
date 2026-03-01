Hello! This is liwe.gg, a full stack League of Legends stats platform built using Riot Games' API.

Years ago, the game client used to give fun statistics such as number of spellcasts, damage dealt, champs played, etc, at the end of each season. The goal is to not only bring that back, but also on a service that can be checked throughout the year. This is an ongoing project, so more features are to come!

Demo:

- visit liwegg.vercel.app
- search 'OPMAGEMASTER#NA1' or your own account!

Frontend:

- Typescript, Next.js, React, Tailwind, Vercel

Backend:

- Python, FastAPI, Supabase/Postgres, Railway
  Other:
- Riot Games Developer API

Notes:

- Initially used local file storage for simplicity but migrated to Supabase for scalability on deployment

Limitations:

- Performance is largely bottlenecked by Riot's fetch rate limit for personal dev keys
- Performance is further limited by how data is retrieved. Data is fetched through a player's match history and indexing through each game. Retrieving a batch of games requires a fetch, and retrieving each game's data requires its own fetch as well. Since fetching each game's data is unavoidable, I've optimized the number of fetches needed on the batches of games themselves to find a balance between not making too individually small batch requests, and fewer large batches that may pull games already recorded.
- I've added sleep timers to ensure the system can continue functioning without long interruptions

Tradeoffs:

- Each match is stored as a 'match_id,' and I'm currently storing all match_ids of the season for each player in the event of a major feature addition to allow for data retrofits. However, this would require competing against the rate limit.
- The tradeoff is to either do this and have a cleaner storage on the backend, or to avoid fetching match data more than once by storing the entire match data on the first ever request of a match. However each match data JSON is massive, and with often hundreds to thousands of games per season, the storage system would quickly become messy.

Future improvements:

- adding features to allow for accounts to be more easily compared to friends' list
