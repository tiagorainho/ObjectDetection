function renderObjectsTable()
{
    $.getJSON('/list?type=names', 
        function(data) 
        {
            let table = document.getElementById("objs_table")
            let tbody = table.children[1]
            let classes = []
            let counter = 0
            if(data.length == 0)
            {
                let thead = table.children[0]
                thead.innerHTML = ""
                tbody.innerHTML += `<td><p id="slide-right">No images found on database, please upload an image first.</p></td>`
            }
            else
            {
                for(let i = 0; i < data.length; i++) 
                {
                    counter = 0;
                    for(let k = 0; k < data.length; k++)
                    {
                        if(data[k]["class"] == data[i]["class"]) counter++
                    }
                    if(!classes.includes(data[i]["class"]))
                    {
                        tbody.innerHTML += `
                            <tr id="slide-right">
                                <th scope="row">
                                `+ data[i]["class"] +`
                                </th>
                                <td>
                                ` + (counter) + `
                                </td>

                                <td>
                                </td>
                            </tr>
                        `
                        classes.push(data[i]["class"])
                    }
                }
            }
        })
}
function delete_objects(id)
{
    $.getJSON('/delete_object?id=' + id,
        function(data)
        {
            location.reload();
            if(data == "success") alert("All objects deleted")
            else alert("Database already empty")
        }
    )
}

renderObjectsTable()