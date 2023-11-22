import requests
import time
from mcstatus import JavaServer
players = []  # List of players online, starts empty!
JAKES_URL = "play.jacobknowlton.com:25565"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1176359011285737513/LVjlY30UW4MSWUWgSFgGJUQBfHkMjQB9Tyt6njUuxKJMpMn_EivMF7Z5s4urZ2xp_lvi"  # test server


def update_players(server: JavaServer):
    global players
    curr_players_sample = server.status().players.sample
    curr_players_sample = curr_players_sample if curr_players_sample is not None else []  # sample can be None
    print(f"Poll Results: {curr_players_sample}")
    for p in curr_players_sample:
        if p in players:  # nothing happens, they are still online
            players.remove(p)
        else:  # player p joined!
            msg_server(f"{p.name} joined")
    # what's left in players, left!
    for p in players:
        msg_server(f"{p.name} left")
    # swap players to be new_players
    players = curr_players_sample


def msg_server(msg):
    requests.post(DISCORD_WEBHOOK, {"content": msg})


def run():
    server = JavaServer.lookup(JAKES_URL)
    # update_players(server)
    while True:
        update_players(server)
        time.sleep(5)


run()
