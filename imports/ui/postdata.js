import {Template} from 'meteor/templating';
import {Data} from '../api/data.js'
import './postdata.html'

Template.postdata.helpers({
	data() {
		return Data.find({})
	}
})
Template.postdata.events({
	'click .postdata'() {
		console.log("clicked")
        var formData = new FormData();
        var metadataBlob = new Blob([$('input[type=file]')[0].files[0]],{type:"application/json"});
        var contentBlob = new Blob([$('input[type=file]')[1].files[0]],{type:"text/plain"});
        formData.append('data', metadataBlob, "metadata");
        formData.append('myDocument', contentBlob, "contentdata");

        $.ajax({
            url: "http://localhost:8000/dms/objects",
            processData: false,
            contentType: false,
            cache: false,
            beforeSend: function(xhrObj){
                // Request headers
                xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key", 'fd023b66c32847ab8a55a342be4c7c47');
            },
            type: "POST",

            data: formData
        })
        .done(function(data) {

        	var contentStream = data.objects[0].contentStreams[0]
        	var properties = data.objects[0].properties
          console.log("contentStream", contentStream)
          console.log("properties", properties)
          return Data.insert({
          	text: "sample"
          })
        })
        .fail(function() {
            alert("error");
        });
	}
})
