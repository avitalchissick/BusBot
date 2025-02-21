This project utilises a Telegram bot to display data from GTFS (General Transit Feed Specification) in Israel.
The data is downloaded to a local Data folder.
When the bot starts it checks the remote server for new data, and downloads the latst version.

The data is loaded internally and used as needed per user requests.

The bot allows the user to following requests:

1 - Display a list of buses that are planned to go through a specific 
    stop/station using the code written on the stop sign. (/stop command)

2 - Display a list of stops/stations in close range 
    to the location provided by the user. (/location command)

