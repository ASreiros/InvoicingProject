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

