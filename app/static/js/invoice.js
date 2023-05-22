
document.querySelector('.basic-info>.doc-name>img').addEventListener('click',function(){
    dokName = document.querySelector('.basic-info>.doc-name>h2')
    current = dokName.innerHTML
    switch (current) {
        case 'pvm sąskaita-faktūra':
            dokName.innerHTML = "sąskaita-faktūra"
            document.querySelector('#VAT-settings').style.display = 'none'
            document.querySelector('#total-sum-holder-vat').style.display = 'none'             
            break;
        case 'sąskaita-faktūra':
            dokName.innerHTML = "invoice"
            document.querySelector('#VAT-settings').style.display = 'flex' 
            document.querySelector('#total-sum-holder-vat').style.display = 'flex'            
            break;
        case 'invoice':
            dokName.innerHTML = "pvm sąskaita-faktūra"
            document.querySelector('#VAT-settings').style.display = 'flex'            
            document.querySelector('#total-sum-holder-vat').style.display = 'flex' 
            break;                      
        default:
            dokName.innerHTML = "pvm sąskaita-faktūra"
            document.querySelector('#VAT-settings').style.display = 'flex'
            document.querySelector('#total-sum-holder-vat').style.display = 'flex' 
            break;
    }
    input_entered()
})

document.querySelector(".date-input>p").addEventListener("click", () => {
    document.querySelector(".date-input>input").showPicker();
  });
document.querySelector(".date-input>input").addEventListener('change', () => {
    console.log('some change');
    console.log(document.querySelector(".date-input>input").value);
    document.querySelector(".date-input>p").innerHTML = document.querySelector(".date-input>input").value
});

document.querySelector('#add-line').addEventListener('click', ()=>{
    control = document.querySelector('#add-line-holder')
    block = document.querySelector('.inv-lines')
    line = document.createElement("div");
    line.classList.add('invoice-line');
    line.innerHTML = `
    <button class="remove-line">-</button>
    <input class="product" maxlength="50" type="text">
    <input class="vnt user-input" type="number" value="1">
    <input class="vnt-name" type="text" maxlength="5" value="vnt">
    <input class="price user-input" type="number"  value="0">
    <input class="total" type="number" readonly value="0">
    `
    block.insertBefore(line, control);
    add_usability_to_new_line()
    input_entered()

})

document.querySelector('#pvm-tipas').addEventListener("change", input_entered)

function add_usability_to_new_line(){
    remove_buttons = document.querySelectorAll('.remove-line')
    remove_button = remove_buttons[remove_buttons.length-1]
    .addEventListener('click',(e)=>{
        if (window.confirm("Ar norite ištrinti visa eilutė?")){
            e.target.parentElement.remove()
            input_entered()
        }
    })


    document.querySelectorAll('.user-input').forEach(inp=>{
        inp.addEventListener("input", input_entered)
    })

}

add_usability_to_new_line()


function input_entered(){
    lines = document.querySelectorAll('.invoice-line')
    lines_data = []
    lines.forEach(lin=>{
        let line = {}
        line["vnt"] = lin.querySelector(".vnt").value
        line["price"] = lin.querySelector(".price").value
        if (line["vnt"] == ""){
            line["vnt"] = 0 
        } 
        if (line["price"] == ""){
            line["price"] = 0 
        } 
        
        lines_data.push(line)
    })
    data = {
        'inv-type': document.querySelector('#inv-type').innerHTML,
        'lines': lines_data,
        'vat-type':document.querySelector('#pvm-tipas').value,
    }
    console.log("data before fetch",data);

    fetch(`${window.origin}/calculate_lines`,{
        method: "POST",
        credentials: "include",
        body:JSON.stringify(data),
        cache:"no-cache",
        headers: new Headers({
            "content-type":"application/json"
        })
    })
    .then(function(response){
        if (response.status != 200){
            console.log("Response status is not 200:  ", response.status, response.statusText);
            return
        }

        response.json().then(function(info){
            console.log("info after fetch:",info);
            const data = info[0]['data']
            console.log(data);
            document.querySelector('#beforeVAT').value = data['total_before_VAT']
            document.querySelector('#VAT').value = data['VAT']
            document.querySelector('#afterVAT').value = data['total_after_VAT']
            totals = document.querySelectorAll('.invoice-line>.total')
            lines = data['lines']
            for (let i = 0; i < totals.length; i++) {
                totals[i].value = lines[i]['total']
                
            }
        })


    })}

