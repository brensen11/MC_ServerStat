import requests
import time
import sys
from mcstatus import JavaServer
players = []  # List of players online, starts empty!
MC_URL = ""
DISCORD_WEBHOOK = ""

def update_players(server: JavaServer):
    global players
    curr_players_sample = server.status().players.sample
    curr_players_sample = curr_players_sample if curr_players_sample is not None else []  # sample can be None
    for p in curr_players_sample:
        if p in players:  # nothing happens, they are still online
            players.remove(p)
        else:  # player p joined!
            msg = f"{p.name} joined"
            msg_server(msg)
            print(msg)
    # what's left in players, left!
    for p in players:
        msg = f"{p.name} left"
        msg_server(msg)
        print(msg)
    # swap players to be new_players
    players = curr_players_sample


def msg_server(msg):
    requests.post(DISCORD_WEBHOOK, {"content": msg})


def run():
    server = JavaServer.lookup(MC_URL)
    print("Server is Running...")
    while True:
        update_players(server)
        time.sleep(5)


def main():
    if len(sys.argv) != 3:
        print("Must run in format ServerBot.py MINECRAFT_URL DISCORD_WEBHOOK")
        return
    global MC_URL
    global DISCORD_WEBHOOK
    MC_URL = sys.argv[1]
    DISCORD_WEBHOOK = sys.argv[2]
    run()


main()
