#!/usr/bin/env python3
from googleapiclient.discovery import build
from discord_webhook import DiscordWebhook

WEBHOOK_URL = "YOUR DISCORD WEBHOOK URL HERE"
DEVELOPER_KEY = "YOUR API KEY HERE"
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

'''These are the three channels I used.  This script WILL run with ANY YouTube
 channel ID given a small refactor with and is semi-scalable due to the cases dict.'''
ID_WENDIGOON = "UCuX9VrqRC3-EUq1eZ0NBbQg" #Wendigoon Channel ID
ID_WENDIGANG = "UC3cpN6gcJQqcCM6mxRUo_dA" #Wendigang Channel ID
ID_CREEPCAST = "UC8Gwis8sr3O-IVA7BGDxh9g" #CreepCast Channel ID



def main() -> None:
    '''Checks for new videos from the 3 channels specified, 
    compares them to storage files, and outputs to Discord 
    if new content is found.'''

    with open("goon_storage.txt", "r") as goon_read:
        with open("gang_storage.txt", "r") as gang_read:
            with open("cast_storage.txt", "r") as cast_read:
                
                try:
                    stored_goon = goon_read.readlines()
                    stored_gang = gang_read.readlines()
                    stored_cast = cast_read.readlines()
                except IndexError:
                    stored_goon = ""
                    stored_gang = ""
                    stored_cast = ""

                #print(stored_goon, stored_gang, stored_cast) Testing statement

                cases = {
                    (True, False, False): lambda: (store_titles(goon_vid, False, False), message_discord(goon_vid, False, False)),
                    (False, True, False): lambda: (store_titles(False, gang_vid, False), message_discord(False, gang_vid, False)),
                    (False, False, True): lambda: (store_titles(False, False, cast_vid), message_discord(False, False, cast_vid)),
                    (True, True, False): lambda: (store_titles(goon_vid, gang_vid, False), message_discord(goon_vid, gang_vid, False)),
                    (True, False, True): lambda: (store_titles(goon_vid, False, cast_vid), message_discord(goon_vid, False, cast_vid)),         
                    (False, True, True): lambda: (store_titles(False, gang_vid, cast_vid), message_discord(False, gang_vid, cast_vid)),
                    (True, True, True): lambda: (store_titles(goon_vid, gang_vid, cast_vid), message_discord(goon_vid, gang_vid, cast_vid))
                }

                goon_bool = False
                gang_bool = False
                cast_bool = False

                goon_vid = get_vids(ID_WENDIGOON)
                if goon_vid not in stored_goon:
                    goon_bool = True
                #print(goon_vid in stored_goon) Testing statement
                
                gang_vid = get_vids(ID_WENDIGANG)
                if gang_vid not in stored_gang:
                    gang_bool = True
                #print(gang_vid in stored_gang) Testing statement

                cast_vid = get_vids(ID_CREEPCAST)
                if cast_vid not in stored_cast:
                    cast_bool = True
                #print(cast_vid in stored_cast) Testing statement

                all_bool = (goon_bool, gang_bool, cast_bool)
                if any(all_bool):
                    cases[all_bool]()
                #print(all_bool) Testing statement


def get_vids(id) -> str:
    '''Fetches the latest video title and link from a given YouTube channel ID.'''

    yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    vid = yt.search().list(
        part="snippet",
        channelId=id,
        maxResults=1,
        order="date"
    ).execute()

    items = vid.get("items", [])
    if items:
        snippet = items[0].get("snippet", {})
        title = snippet.get("title", "NO TITLE FOUND")
        link = f" | https://www.youtube.com/watch?v={items[0]['id']['videoId']}"
    return title + link


def store_titles(goon, gang, cast) -> None:
    '''Stores the latest video titles and links into their respective storage files.'''

    print(goon, gang, cast)
    if goon:
        with open("goon_storage.txt", "w") as goon_write:
            goon_write.write(goon)
            print("***NEW WENDIGOON TITLE + LINK STORED***")
    if gang:
        with open("gang_storage.txt", "w") as gang_write:
            gang_write.write(gang)
            print("***NEW WENDIGANG TITLE + LINK STORED***")
    if cast:
        with open("cast_storage.txt", "w") as cast_write:
            cast_write.write(cast)
            print("***NEW CREEPCAST TITLE + LINK STORED***")


def message_discord(goon, gang, cast) -> None:
    '''Sends a message to a Discord webhook with the new video information.'''

    if any([goon, gang, cast]):
        content = "***{ Begin Transmission of New Wendigoon/CreepCast Content }***\n" 
    if goon:
        content += f"\n\tNEW WENDIGOON EPISODE RELEASED:{goon}\n"
    if gang:
        content += f"\n\tNEW WENDIGANG EPISODE RELEASED:{gang}\n"
    if cast:
        content += f"\n\tNEW CREEPCAST EPISODE RELEASED:{cast}\n\n"
    if any([goon, gang, cast]):
        content += "\tIf you have any questions, bugs to report, or would like a new YT channel added to this updater, let the bot creator know.\n\n"
        content += "***{ End Transmission }***"

    webhook = DiscordWebhook(url=WEBHOOK_URL, content=content)
    response = webhook.execute()


if __name__ == "__main__":
    main()
    '''Thank you for checking out my code! If you have any questions, feel free to reach out.'''