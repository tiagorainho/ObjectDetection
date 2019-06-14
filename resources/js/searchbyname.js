let confidence = 50;
let name = "all"

function renderObjects(name)
{
    if(name == "all")
    {
        $.getJSON('/list?type=detected', 
        function(data) 
        {
            results_num = 0
            let row = document.getElementById("images_row")
            row.innerHTML = ""
            for(let i = 0; i < data.length; i++) 
            {
                if(data[i]['confidence'] >= confidence)
                {
                    row.innerHTML += `
                    <div class="col-md-3 mb-4">
                        <h1 id="slide-right" class="text-center"><a href="/edit?id=`+ data[i]['image']+`"><img class="rounded" src="/images/objs/`+ data[i]['name'] +`" width= "80px"></a></h1>
                        <p id="slide-right-delay" class="text-center">`+ data[i]['class'] +` <img id="pointer" src="/icons/delete-icon.png" width="25px" onclick="delete_object(`+data[i]['id']+`)" ></p>
                    </div>
                    `
                    results_num += 1
                }
            }
            let results_num_html = document.getElementById('results_num')
            results_num_html.innerHTML = results_num
        }
    )}
    else
    {
        $.getJSON('/list?type=detected&name=' + name, 
        function(data) 
        {
            results_num = 0
            let row = document.getElementById("images_row")
            row.innerHTML = ""
            for(let i = 0; i < data.length; i++)
            {
                if(data[i]['confidence'] >= confidence)
                {
                    row.innerHTML += `
                    <div class="col-md-3 mb-4">
                        <h1 id="slide-right" class="text-center"><a href="/edit?id=`+ data[i]['image']+`"><img class="rounded" src="/images/objs/`+ data[i]['name'] +`" width= "80px"></a></h1>
                        <p id="slide-right-delay" class="text-center">`+ data[i]['class'] +` <img id="pointer" src="/icons/delete-icon.png" width="25px" onclick="delete_object(`+data[i]['id']+`)" ></p>
                    </div>
                    `
                    results_num += 1
                }
            }
            let results_num_html = document.getElementById('results_num')
            results_num_html.innerHTML = results_num        
        }
    )}
}

function updateConfidence()
{
    let confidence_slider = document.getElementById('confidenceSlider')
    let confidenceValueHtml = document.getElementById('confidenceValueHtml')
    let results_num_html = document.getElementById('results_num')
    results_num_html.innerHTML = results_num
    confidenceValueHtml.innerHTML = confidence_slider.value
    confidence = confidence_slider.value

    searchByType()
}

function searchByType()
{
    name = document.getElementById('name').value
    if(name == "") name = "all"
    renderObjects(name)
}

function delete_object(id)
{
    $.getJSON('/delete_object?id=' + id,
        function(data)
        {
            renderObjects(name)
            if(data == "success") alert("Object was deleted from database")
        }
    )}


renderObjects("all")