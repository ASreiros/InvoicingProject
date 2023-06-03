document.querySelector('#register-btn').addEventListener('click', ()=>{
    document.querySelector('#register-form').classList.remove('noshow')
    document.querySelector('.modal').classList.remove('noshow')
})

document.querySelector('#join-btn').addEventListener('click', ()=>{
    document.querySelector('#join-form').classList.remove('noshow')
    document.querySelector('.modal').classList.remove('noshow')
})


document.querySelector('.modal').addEventListener('click', ()=>{
    document.querySelectorAll('.hidden-form').forEach(form => {
        form.classList.add('noshow')
    });
    document.querySelector('.modal').classList.add('noshow')
})

document.querySelectorAll('.hidden-form span').forEach(span => {
    span.addEventListener('click', ()=>{
        document.querySelector('.signin').classList.toggle('noshow')
        document.querySelector('.register').classList.toggle('noshow')
    })
});

// Cookie consent

const cookie_consent = document.querySelector('#cookie-consent')
if (cookie_consent){
    cookie_consent.addEventListener('click', ()=>{
        document.cookie = "cookie_consent=true";
        document.querySelector('.cookie-consent-container').classList.add('noshow')
    
    })
}
