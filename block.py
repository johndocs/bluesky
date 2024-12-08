from atproto import Client, models
from credentials import HANDLE, PASSWORD
from search import act_on_users, USERS_PATH

client = Client()
profile = client.login(HANDLE, PASSWORD)


def block_actor(handle):
    "block bluesky actor by handle"
    data = client.get_profile(actor=handle)
    blocked_user_did = data.did
    display_name = data.display_name
    block = client.app.bsky.graph.block

    block_record = models.AppBskyGraphBlock.Record(
        subject=blocked_user_did,
        created_at=client.get_current_time_iso()
    )
    uri = client.app.bsky.graph.block.create(client.me.did, block_record).uri
    print(f"Blocked {display_name} ({blocked_user_did}) with uri={uri}")

def block_user(user):
    "block bluesky for `user` dict from act_on_users"
    handle = user["handle"]
    block_actor(handle)

if __name__ == "__main__":
    with open(USERS_PATH, "r") as f:
        act_on_users(f, block_user)
