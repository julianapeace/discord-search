var fs = require('fs');
var json = require('./kpatch.json');
// var writeFile = require('./file_write_tools.js');
var keys = require('./keys.json');
var { promisify } = require('util')
// var request = promisify(require("request"));
var fetch = require("node-fetch");
var writeFile = promisify(fs.writeFile)
var readFile = promisify(fs.readFile);
var FormData = require('form-data');

var meta =  json.meta
var data = json.data

var channel_id = Object.keys(meta.channels)[0]
var channel_name = meta.channels[channel_id].name
var users = json.meta.users
var users_index_array = Object.keys(users)
var users_obj = {}
for (i = 0; i < Object.keys(users).length; i++) {
  users_obj[users_index_array[i]] = users[users_index_array[i]].name
}
var usernames = Object.values(users_obj)

var convo = data[channel_id]








/* ALL THE MAGIC HAPPENS BELOW */
var forLoop = async _ => {
  for (var i = 0; i < Object.values(convo).length; i++) {
    var messages = Object.values(convo)
    var singleMessage = messages[i]

    var username = usernames[singleMessage.u]
    var timestamp = singleMessage.t
    var message = singleMessage.m

    var metaData = {
      "objects": [{
        "properties": {
          "enaio:objectTypeId": {
            "value": "singleMessage"
          },
          "u": {
            "value": username
          },
          "t": {
            "value": timestamp
          },
          "m": {
            "value": channel_name
          }
        },
        "contentStreams": [{
          "cid": "julieDiscordChats"
        }]
      }]
    }


    try {
      var metaton = await writeFile('metaData.json', JSON.stringify(metaData))
      var singleton = await writeFile('singleMessage.txt', JSON.stringify(message))

      var content = await readFile('singleMessage.txt', 'utf-8')
      console.log('1: ', content);

      var formData = new FormData();
      formData.append('data', fs.createReadStream('./metaData.json'));
      formData.append('julieDiscordChats', fs.createReadStream('./singleMessage.txt'));

      var settings = {
        method: 'POST',
        body: formData,
        headers: {
          'Ocp-Apim-Subscription-Key': keys['api']
          // 'Content-Type': 'multipart/form-data'
        }
      };

      var fetchResponse = await fetch(`https://api.yuuvis.io/dms/objects`, settings);
      var data = await fetchResponse.json();




      // request.post({
      //   url: 'https://api.yuuvis.io/dms/objects',
      //   formData: {
      //     data: fs.createReadStream('./metaData.json'),
      //     julieDiscordChats: fs.createReadStream('./singleMessage.txt'),
      //   },
      //   headers: {
      //       'Ocp-Apim-Subscription-Key': keys['api'],
      //       'Content-Type': 'multipart/form-data'
      //     }
      // })

    } catch (e) {
      return e;
    }

  }
}

forLoop()
