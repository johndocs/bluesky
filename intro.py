from atproto import Client
from credentials import HANDLE, PASSWORD

client = Client()
profile = client.login(HANDLE, PASSWORD)
print(f"profile={profile}")


client.actor.searchActors("agile")

resp = None
while True:
    resp = client.actor.searchActors("agile", cursor=resp.cursor if resp else None)
    for actor in resp.actors:
        print(f"actor={actor}")
    if not resp.cursor: break
