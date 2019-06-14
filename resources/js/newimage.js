var file = null

function updatePhoto(event)
{
    var reader = new FileReader();
    reader.onload = function(event)
    {
        //Criar uma imagem
        var img = new Image();
        img.src = event.target.result;
    }

    //Obter o ficheiro
    reader.readAsDataURL(event.target.files[0]);
    file = event.target.files[0];
}

function sendFile() 
{
    if(file == null)
    {
        alert("Please choose a file first")
    }
    else
    {
        var data = new FormData();
        var image = document.getElementById('image')
        data.append("image", file);
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "put");
        xhr.upload.addEventListener("progress", updateProgress, false);
        xhr.send(data);
    }
}

function updateProgress(evt){
    if(evt.loaded == evt.total)
    alert("Image was upload successfuly!");
}