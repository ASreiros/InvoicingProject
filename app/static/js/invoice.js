
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