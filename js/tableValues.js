
$.getJSON( "/all_objects", function( json ) {
    var tb="";
    for(var i=0;i<json.length;i++){
        tb+='<tr><td>' + json[i][1] + '</td><td>' + json[i][2] + '</td><td>'+ json[i][0] + '</td></tr>'
    }
    $('#ObjectTable').append(tb);
});