 
$.getJSON( "/object_count", function( json ) {
    console.log( "JSON Data: " + json["count"] );
    $( "#object_count" ).text(json["count"])
});