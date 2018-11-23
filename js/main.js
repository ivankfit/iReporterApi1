let menu=document.querySelector('#menu');
let menulink=document.querySelector('#menushow');

menulink.addEventListener('click',(e)=>{
    console.log('clicked');
    menu.classList.toggle('showing');
e.preventDefault();
});