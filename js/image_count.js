 
$.getJSON( "/image_count", function( json ) {
    console.log( "JSON Data: " + json["count"] );
    $( "#image_count" ).text(json["count"])
});