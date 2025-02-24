This project utilises a Telegram bot to display data from GTFS (General Transit Feed Specification) in Israel - https://www.gov.il/he/pages/gtfs_general_transit_feed_specifications

The data is downloaded to a local Data folder.
When the bot starts it checks the remote server for new data, and downloads the latst version.

The data is loaded internally and used as needed per user requests.

The bot allows the user to following requests:

1 - Display a list of buses that are planned to go through a specific 
    stop/station using the code written on the stop sign. (/stop command)

2 - Display a list of stops/stations in close range 
    to the location provided by the user. (/location command)

Main files in the code:
RunBot.py - handles all bot functionality
Utils\DataUtils.py - handles everything to do with loading data from GTFS files and the files from the remote server
Utils\BusUtils.py - handles getting requested information per user parameters

Future ideas:
1 - Improve bot GUI by using telegram API - done
2 - Add usage of real-time information (available via API as described in https://www.gov.il/he/pages/real_time_information_siri)
