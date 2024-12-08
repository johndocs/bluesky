import requests
import jsonlines

def search_bluesky_actors(query, limit=10, cursor=None):
    # URL for searching actors
    url = "https://public.api.bsky.app/xrpc/app.bsky.actor.searchActors"

    params = {
        "q": query,
        "limit": limit
    }

    if cursor:
        params["cursor"] = cursor

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()  # Return the JSON response if successful
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def get_actor_profile(actor_handle):
    url = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile"
    params = {
        "actor": actor_handle
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def search_everyone(SEARCH_KEYWORD, fp, max_users=5):
    cursor = None
    n = 0

    writer = jsonlines.Writer(fp)
    while True:
        results = search_bluesky_actors(SEARCH_KEYWORD, cursor=cursor)
        for actor in results["actors"]:
            handle = actor["handle"]
            display_name = actor["displayName"]
            profile = get_actor_profile(handle)
            bio = profile.get("description", "")
            bio = bio.replace("\n", " ")
            followers = profile.get("followersCount", 0)

            user = {
                "handle": handle,
                "followers": followers,
                "display_name": actor["displayName"],
                "bio": bio,
            }
            writer.write(user)

            n += 1
            if n >= max_users:
                return

        cursor = results.get("cursor")
        if not cursor:
            break

def act_on_users(f, action):
    "act_on_users(f, action) calls action(user) for each user in f"
    reader = jsonlines.Reader(f)
    for user in reader:
        action(user)

def print_user(user):
    followers = user["followers"]
    handle = user["handle"]
    display_name = user["display_name"]
    bio = user["bio"]
    print(f"{followers:4} {handle:20} {display_name:20} '{bio[:100]}'")

USERS_PATH = "agile_users.jsonl"
SEARCH_KEYWORD = "Agile AND Software"

USERS_PATH = "gig_work.jsonl"
SEARCH_KEYWORD = "gig AND work"

USERS_PATH = "gig_work2.jsonl"
SEARCH_KEYWORD = "gig work"

USERS_PATH = "pdf_dev.jsonl"
SEARCH_KEYWORD = "pdf"

USERS_PATH = "anime.jsonl"
SEARCH_KEYWORD = "anime"


if __name__ == "__main__":
    if True:
        with open(USERS_PATH, "w") as f:
            search_everyone(SEARCH_KEYWORD, f, max_users=10_000)
    else:
        with open(USERS_PATH, "r") as f:
            act_on_users(f, print_user)
