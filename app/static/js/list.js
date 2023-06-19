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