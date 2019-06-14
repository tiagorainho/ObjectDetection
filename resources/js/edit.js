function renderObjects()
{
    let url_string = window.location.href
    let url = new URL(url_string);
    let id = url.searchParams.get("id");
    $.getJSON('/get?id='+id, 
        function(data) 
        {
            let image_html = document.getElementById("img")
            let inputs = document.getElementById("inputs_edit")
            if(data == "not found"){
                image_html.innerHTML = `<h6 class="text-center"><img width="45px" src = "/icons/not_Found.png"></h6>`
                inputs.innerHTML =
                `<h4>Image not Found</h4>
                `
            }
            else{
                image_html.innerHTML = `<h6 class="text-center"><img class="rounded" width="200px" src = "/images/objs/` + data[0]['name'] + `"></h6>`
                inputs.innerHTML =
                `<div class="col-md-8 offset-md-2">
                    <input class="form-control-sm form-control mb-3" id="text" type="text" value=` + data[0]['class'] + `>
                    <input type="range" onchange="updateConfidence()" min="1" max="100" value="`+ data[0]['confidence'] +`" class="slider" id="confidenceSlider" width="100px">
                    <small>Confidence: <span id="confidenceValueHtml">` + data[0]['confidence'] + `</span></small>
                    <h5 class="text-center mt-3"><button class="btn btn-primary btn-sm" onclick="save()" type="button">Save</button></h5>
                </div>
                ` 
            }
        })
}
function updateConfidence()
{
    let confidence_slider = document.getElementById('confidenceSlider')
    let confidenceValueHtml = document.getElementById('confidenceValueHtml')
    confidenceValueHtml.innerHTML = confidence_slider.value
}
function save()
{
    let url_string = window.location.href
    let url = new URL(url_string);
    let id = url.searchParams.get("id");

    let confidence = document.getElementById('confidenceSlider').value

    let text = document.getElementById('text').value
    $.getJSON('/edit_object?id=' + id + `&obj=` + text +`&confidence=` + confidence,
        function(data) 
        {
            renderObjects()
            alert(data)
        })
}

renderObjects()