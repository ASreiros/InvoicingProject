
const documentType = document.querySelector('#inv-type').innerHTML
if (documentType == 'sąskaita-faktūra'){
    document.querySelector('#VAT-settings').classList.add("noshow")
    document.querySelector('#total-sum-holder-vat').classList.add("noshow")
    console.log("no show added");
} else{
    console.log(documentType);
}

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
    <button type="button" class="remove-line">-</button>
    <input class="product" name="product-name" required maxlength="50" type="text">
    <input class="vnt user-input" name="product-vnt" required step="0.01" type="number" value="1">
    <input class ='vnt-name' name="vnt-name" type="text" required maxlength="5" value="vnt">
    <input class="price user-input" name="price" step="0.01" required type="number" value="0">
    <input class="total" name="line-total" type="number" readonly value="0">
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

const form = document.querySelector(".invoice")
form.addEventListener('submit', (event) => {
    event.preventDefault();
    lines = []
    document.querySelectorAll('.invoice-line').forEach(line=>{
        line_info = {
            'product': line.querySelector('.product').value,
            'quantity': line.querySelector('.vnt').value,
            'unit': line.querySelector('.vnt-name').value,
            'price': line.querySelector('.price').value,
            'total': line.querySelector('.total').value,
        }
        
        lines.push(line_info)
    })


    data = {
        "type": document.querySelector('#inv-type').innerHTML,
        "date": document.querySelector('#date').value,
        "series": document.querySelector('#inv-series').value,
        "number": document.querySelector('#inv-number').value,
        "buyer-name": document.querySelector('#b-name').value, 
        "buyer-tax": document.querySelector('#b-tax').value, 
        "buyer-vat-tax": document.querySelector('#b-vat').value, 
        "buyer-address": document.querySelector('#b-address').value, 
        "beforeVat": document.querySelector('#beforeVAT').value,
        "vat": document.querySelector('#VAT').value,
        "vatTypas": document.querySelector('#pvm-tipas').value,
        "afterVat": document.querySelector('#afterVAT').value, 
        "lines": lines
    }


    fetch(`${window.origin}/save-invoice`,{
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
        });
    });
})        

