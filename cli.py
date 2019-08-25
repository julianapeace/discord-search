import pdb
import click
import os
import pandas as pd
import requests
import json
import random

with open("keys.json", "r") as f:
    key = json.load(f)
api_key = key["api"]

@click.command()
@click.argument('keyword')

def cli(keyword):
    """Globally search your discord chats."""

    search_url = "https://api.yuuvis.io/dms/objects/search"

    payload = payload = "{\r\n  \"query\": {\r\n    \"statement\": \"SELECT * FROM singleMessage WHERE CONTAINS ('" + keyword + "')\",\r\n    \"skipCount\": 0,\r\n    \"maxItems\": 50\r\n  }\r\n}"
    headers = {
        'Content-Type': "application/json",
        'Ocp-Apim-Subscription-Key': api_key,
        'Host': "api.yuuvis.io",
        }

    response = requests.request("POST", search_url, data=payload, headers=headers)
    obj = json.loads(response.text)

    representation_dict = {
            "Keyword": keyword,
            "Timestamp": [],
            "Channel_Name": [],
            "User": [],
            "Message": [],
            "Object_ID": [],
        }

    for x in obj['objects']:
        representation_dict['Object_ID'].append(x['properties']['enaio:objectId']['value'])
        representation_dict['Channel_Name'].append(x['properties']['ten5d613e03f761b924fc5e2cf8:m']['value'])
        representation_dict['User'].append(x['properties']['ten5d613e03f761b924fc5e2cf8:u']['value'])
        representation_dict['Timestamp'].append(x['properties']['ten5d613e03f761b924fc5e2cf8:t']['value'])

    if len(representation_dict['Object_ID']) > 0:
        for obj_id in representation_dict['Object_ID']:
            obj_id
            url = "https://api.yuuvis.io/dms/objects/" + obj_id + "/contents/file"
            response = requests.request("GET", url, headers={
                'Ocp-Apim-Subscription-Key': api_key,
                })
            representation_dict['Message'].append(response.text)

    # test = obj['objects']
    # print("test ", json.dumps(test[4], indent=2))
    # num_of_results = obj["totalNumItems"]
    ascii_art = ["""\
           .       .                   .       .      .     .      .
          .    .         .    .            .     ______
      .           .             .               ////////
                .    .   ________   .  .      /////////     .    .
           .            |.____.  /\        ./////////    .
    .                 .//      \/  |\     /////////
       .       .    .//          \ |  \ /////////       .     .   .
                    ||.    .    .| |  ///////// .     .
     .    .         ||           | |//`,/////                .
             .       \\        ./ //  /  \/   .
  .                    \\.___./ //\` '   ,_\     .     .
          .           .     \ //////\ , /   \                 .    .
                       .    ///////// \|  '  |    .
      .        .          ///////// .   \ _ /          .
                        /////////                              .
                 .   ./////////     .     .
         .           --------   .                  ..             .
  .               .        .         .                       .
                        ________________________
____________------------                        -------------_________
    """,
    """
                    ___                                          ___
 __________________/  /                       __________________/  /
| _    _______    /  /                       | _    _______    /  /
|(_) .d########b. //)| _____________________ |(_) .d########b. //)|
|  .d############//  ||        _____        ||  .d############//  |
| .d######""####//b. ||() || [DISCORD] || ()|| .d######""####//b. |
| 9######(  )#_//##P ||()|__|  | = |  |__|()|| 9######(  )#_//##P |
| 'b######++#/_/##d' ||() ||   | = |   || ()|| 'b######++#/_/##d' |
|  "9############P"  ||   ||   |___|   ||   ||  "9############P"  |
|  _"9a#######aP"    ||  _   _____..__   _  ||  _"9a#######aP"    |
| |_|  `""""''       || (_) |_____||__| (_) || |_|  `""""''       |
|  ___..___________  ||_____________________||  ___..___________  |
| |___||___________| |                       | |___||___________| |
|____________________|Global Search 4 DISCORD|____________________|
    """,
    """
                      ___..............._
             __.. ' _'.""""""\\""""""""- .`-._
 ______.-'         (_) |      \\           ` \\`-. _
/_       --------------'-------\\---....______\\__`.`  -..___
| T      _.----._           Xxx|x...           |          _.._`--. _
| |    .' ..--.. `.         XXX|XXXXXXXXXxx==  |       .'.---..`.     -._
\_j   /  /  __  \  \        XXX|XXXXXXXXXXX==  |      / /  __  \ \        `-.
 _|  |  |  /  \  |  |       XXX|""'            |     / |  /  \  | |          |
|__\_j  |  \__/  |  L__________|_______________|_____j |  \__/  | L__________J
     `'\ \      / ./__________________________________\ \      / /___________
        `.`----'.'                                     `.`----'.'
        `""""'                                         `""""'
    """,
"""
                                         ^^
    ^^      ..                                       ..
            []                                       []
          .:[]:_          ^^                       ,:[]:.
        .: :[]: :-.                             ,-: :[]: :.
      .: : :[]: : :`._                       ,.': : :[]: : :.
    .: : : :[]: : : : :-._               _,-: : : : :[]: : : :.
_..: : : : :[]: : : : : : :-._________.-: : : : : : :[]: : : : :-._
_:_:_:_:_:_:[]:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:[]:_:_:_:_:_:_
!!!!!!!!!!!![]!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![]!!!!!!!!!!!!!
^^^^^^^^^^^^[]^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[]^^^^^^^^^^^^^
            []                                       []
            []                                       []
            []                                       []
 ~~^-~^_~^~/  \~^-~^~_~^-~_^~-^~_^~~-^~_~^~-~_~-^~_^/  \~^-~_~^-~~-
~ _~~- ~^-^~-^~~- ^~_^-^~~_ -~^_ -~_-~~^- _~~_~-^_ ~^-^~~-_^-~ ~^
   ~ ^- _~~_-  ~~ _ ~  ^~  - ~~^ _ -  ^~-  ~ _  ~~^  - ~_   - ~^_~
     ~-  ^_  ~^ -  ^~ _ - ~^~ _   _~^~-  _ ~~^ - _ ~ - _ ~~^ -
        ~^ -_ ~^^ -_ ~ _ - _ ~^~-  _~ -_   ~- _ ~^ _ -  ~ ^-
            ~^~ - _ ^ - ~~~ _ - _ ~-^ ~ __- ~_ - ~  ~^_-
                ~ ~- ^~ -  ~^ -  ~ ^~ - ~~  ^~ - ~
""",
"""
                       .,,uod8B8bou,,.
              ..,uod8BBBBBBBBBBBBBBBBRPFT?l!i:.
         ,=m8BBBBBBBBBBBBBBBRPFT?!||||||||||||||
         !...:!TVBBBRPFT||||||||||!!^^""'   ||||
         !.......:!?|||||!!^^""'            ||||
         !.........||||                     ||||
         !.........||||  ##                 ||||
         !.........||||                     ||||
         !.........||||                     ||||
         !.........||||                     ||||
         !.........||||                     ||||
         `.........||||                    ,||||
          .;.......||||               _.-!!|||||
   .,uodWBBBBb.....||||       _.-!!|||||||||!:'
!YBBBBBBBBBBBBBBb..!|||:..-!!|||||||!iof68BBBBBb....
!..YBBBBBBBBBBBBBBb!!||||||||!iof68BBBBBBRPFT?!::   `.
!....YBBBBBBBBBBBBBBbaaitf68BBBBBBRPFT?!:::::::::     `.
!......YBBBBBBBBBBBBBBBBBBBRPFT?!::::::;:!^"`;:::       `.
!........YBBBBBBBBBBRPFT?!::::::::::^''...::::::;         iBBbo.
`..........YBRPFT?!::::::::::::::::::::::::;iof68bo.      WBBBBbo.
  `..........:::::::::::::::::::::::;iof688888888888b.     `YBBBP^'
    `........::::::::::::::::;iof688888888888888888888b.     `
      `......:::::::::;iof688888888888888888888888888888b.
        `....:::;iof688888888888888888888888888888888899fT!
          `..::!8888888888888888888888888888888899fT|!^"'
            `' !!988888888888888888888888899fT|!^"'
                `!!8888888888888888899fT|!^"'
                  `!988888888899fT|!^"'
                    `!9899fT|!^"'
                      `!^"'
"""
    ]
    print(random.choice(ascii_art))

    if len(representation_dict['Object_ID']) > 0:
        print("""\

        ███████╗██╗   ██╗ ██████╗ ██████╗███████╗███████╗███████╗
        ██╔════╝██║   ██║██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝
        ███████╗██║   ██║██║     ██║     █████╗  ███████╗███████╗
        ╚════██║██║   ██║██║     ██║     ██╔══╝  ╚════██║╚════██║
        ███████║╚██████╔╝╚██████╗╚██████╗███████╗███████║███████║
        ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝╚══════╝╚══════╝╚══════╝

        """)
    else:
        print("""\
                    ███████╗       ██████╗██╗  ██╗
                    ██╔════╝▄ ██╗▄██╔════╝██║ ██╔╝
                    █████╗   ████╗██║     █████╔╝
                    ██╔══╝  ▀╚██╔▀██║     ██╔═██╗
                    ██║       ╚═╝ ╚██████╗██║  ██╗
                    ╚═╝            ╚═════╝╚═╝  ╚═╝

        """)
        # print("""\
        #                  ██████╗         ██╗
        #                 ██╔═████╗    ██╗██╔╝
        #                 ██║██╔██║    ╚═╝██║
        #                 ████╔╝██║    ██╗██║
        #                 ╚██████╔╝    ╚═╝╚██╗
        #                  ╚═════╝         ╚═╝
        #
        # """)
    df = pd.DataFrame.from_dict(representation_dict,
                                # columns=[
                                #     "Input1",
                                #     "Input2",
                                #     "(Input1 + Input2)",
                                #     "Enc(Input1)",
                                #     "Enc(Input2)",
                                #     "HE Sum (Pailler)"]
                                )
    df = df.drop(['Object_ID'], axis=1)
    print(repr(df))
    return
    # pdb.set_trace() // debugger

if __name__ == '__main__':
    cli()
