# timetable_bot

  this bot allows you to receive the schedule of couples of the University of RTU MIREA in personal messages in the telegram messenger in the form of cute pictures.
<br><br>
  (The schedule for the next day on weekdays at 0:45, the schedule for the whole week is on weekends)


## Setup
Install the requremets and configure the CRON table: <br>
  `cd <path_to_file>` <br>
  `make setup`

to test the script in action enter:<br>
  `make start`
  
to disable script:<br>
  `make stop`
  
## Setting configuration
  to make the bot work properly replace the following lines in `config.json` file:<br>
  * "TELEGRAM_GROUPS" : {<br>
        `<YOUR TELEGRAM ID>` : ["`<YOUR STUDY GROUP>`"]<br>

  * edit `FONT_PATH`, `SCRIPT_PATH` to the <b>propper path</b>
  
  to insert telegram bot key:
  * make file `telegram_bot_key.txt` and put your bot tocken into this file
  
## Example of program execution
![изображение](https://user-images.githubusercontent.com/16050682/161161953-d8489159-f5a6-4939-98d0-bbd9985afba6.png)
<br>
![изображение](https://user-images.githubusercontent.com/16050682/161161972-2775ee78-b66c-4804-aae2-c743a1a1bbbb.png)
<br>
![изображение](https://user-images.githubusercontent.com/16050682/161161996-7db13667-68be-4753-bc80-01161ee3bc13.png)

## COPYRIGHTS

the attached font is distributed under Apache License Version 2.0, January 2004

