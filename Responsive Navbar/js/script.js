let x = document.getElementById('logo');
let flag = 1;
function showMenu(){
    if(flag==1){
        document.getElementById('menu').style.display="none";
        flag=0;
    }
    else{
        document.getElementById('menu').style.display="block";
        flag=1;
    }
}

// const hamburger = document.querySelector(".hamburger");
// const navMenu = document.querySelector(".nav-menu");

// hamburger.addEventListener("click",() => {
//     hamburger.classList.toggle("active");
//     navMenu.classList.toggle("active");

// })