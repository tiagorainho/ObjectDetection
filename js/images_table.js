$.getJSON( "/search_objects_by_name", function( json ) {
    var tb=""
    /*if(json.length>0){
        //console.log("json[0]")
        //for(var i=0;i<json.length;i++){
            
        //}
        //tb+=""
    }
    else{
        
    }
    */
    console.log("json[0]")
    tb+="<p>ola</p>"
    $('#image_table').append(tb);
});