import requests
import time
import sys
from mcstatus import JavaServer
players = []  # List of players online, starts empty!
MC_URL = ""
DISCORD_WEBHOOK = ""
BOT_NAME = None

def update_players(server: JavaServer):
    global players
    try:
        curr_players_sample = server.status().players.sample
    except:
        print("Error in server connection ...", flush=True)
        return
    curr_players_sample = curr_players_sample if curr_players_sample is not None else []  # sample can be None
    for p in curr_players_sample:
        if p in players:  # nothing happens, they are still online
            players.remove(p)
        else:  # player p joined!
            msg = f"{p.name} joined"
            msg_server(msg)
            print(msg, flush=True)
    # what's left in players, left!
    for p in players:
        msg = f"{p.name} left"
        msg_server(msg)
        print(msg, flush=True)
    # swap players to be new_players
    players = curr_players_sample


def msg_server(msg):
    data = {}
    data["content"] = msg
    if BOT_NAME is not None:
        data["username"] = BOT_NAME
    requests.post(DISCORD_WEBHOOK, data)


def run():
    server = JavaServer.lookup(MC_URL)
    print("Server is Running...", flush=True)
    while True:
        update_players(server)
        time.sleep(5)


def main():
    if not (3 <= len(sys.argv) <= 4):
        print("Must run in format ServerBot.py MINECRAFT_URL DISCORD_WEBHOOK", flush=True)
        return
    global MC_URL
    global DISCORD_WEBHOOK
    global BOT_NAME
    MC_URL = sys.argv[1]
    DISCORD_WEBHOOK = sys.argv[2]
    if len(sys.argv) == 4:
        BOT_NAME = sys.argv[3]
    run()


main()
