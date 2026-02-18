import os
from fastapi import FastAPI, Query
from livekit import api

app = FastAPI()

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "secret")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/token")
def token(room: str = Query(...), identity: str = Query(...), name: str | None = Query(None)):
    grants = api.VideoGrants(room_join=True, room=room)
    jwt = (
        api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(identity)
        .with_name(name or identity)
        .with_grants(grants)
        .to_jwt()
    )
    return {"token": jwt, "url": "ws://localhost:7880"}
