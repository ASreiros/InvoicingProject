document.querySelector("#btn-user-settings").addEventListener("click", ()=>{
    document.querySelector("#user-form").classList.remove("noshow")
    document.querySelector(".modal").classList.remove("noshow")
})

document.querySelector("#btn-password").addEventListener("click", ()=>{
    document.querySelector("#password-form").classList.remove("noshow")
    document.querySelector(".modal").classList.remove("noshow")
})

document.querySelector(".modal").addEventListener("click", ()=>{
    document.querySelector("#user-form").classList.add("noshow")
    document.querySelector("#password-form").classList.add("noshow")
    document.querySelector(".modal").classList.add("noshow")
})


document.querySelectorAll('.delete-line').forEach(delBtn=>{
    delBtn.addEventListener('click', ()=>{
        line = delBtn.parentElement.parentElement
        inv = line.querySelector('.number').innerText
        if(confirm(`Ar tikrai norite ištrinti sąskaita "${inv}"?`)){
            data = {
                "invoice_id": line.querySelector('.id').value
            }
            fetch(`${window.origin}/delete-invoice`,{
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
                    if (info[0]['result']){
                        location.reload();
                    } else{
                        document.querySelector('.error-info').classList.remove("noshow")
                        document.querySelector('.error-info>p').innerText = "Ištrinti sąskaita nepavyko. \n"
                    }
                })
        
        
            })




        }
    })
})

document.querySelectorAll('.print-line').forEach(delBtn=>{
    delBtn.addEventListener('click', ()=>{
        line = delBtn.parentElement.parentElement
        invoice_id = line.querySelector('.id').value
        const file_link = `/get-pdf/${invoice_id}`
        const fElement = document.createElement('a');
        fElement.href = file_link;
        fElement.setAttribute('target', '_blank');
        fElement.click();
        fElement.remove();    
    })
})            