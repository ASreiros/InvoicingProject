
document.querySelector('.basic-info>.doc-name>img').addEventListener('click',function(){
    dokName = document.querySelector('.basic-info>.doc-name>h2')
    current = dokName.innerHTML
    switch (current) {
        case 'pvm sąskaita-faktūra':
            dokName.innerHTML = "sąskaita-faktūra"            
            break;
        case 'sąskaita-faktūra':
            dokName.innerHTML = "invoice"            
            break;
        case 'invoice':
            dokName.innerHTML = "pvm sąskaita-faktūra"            
            break;                      
        default:
            dokName.innerHTML = "pvm sąskaita-faktūra" 
            break;
    }
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
    console.log("click");
    control = document.querySelector('#add-line-holder')
    block = document.querySelector('.inv-lines')
    line = document.createElement("div");
    line.classList.add('invoice-line');
    line.innerHTML = `
    <button class="remove-line">-</button>
    <input class="product" maxlength="50" type="text">
    <input class="vnt" type="number" min="0" value="1">
    <input type="text" maxlength="5" value="vnt">
    <input class="price" type="number" min="0" value="1">
    <input class="total" type="number" readonly value="1">
    `
    block.insertBefore(line, control);
    remove_button_usability()

})

function remove_button_usability(){
    remove_buttons = document.querySelectorAll('.remove-line')
    remove_button = remove_buttons[remove_buttons.length-1]
    .addEventListener('click',(e)=>{
        console.log("click -");
        if (window.confirm("Ar norite ištrinti visa eilutė?")){
            e.target.parentElement.remove()
        }
    })
}

remove_button_usability()

