// toggle icon navbar 
document.addEventListener('DOMContentLoaded', function() {
  let menuIcon = document.querySelector(".dashboard-icon-menu");
  let sideMenuSpans = document.querySelectorAll(".side-menu-span");
  let sideMenu = document.querySelector(".side-menu");
  let profileMenu = document.querySelector(".profile-image")
  let profileLink = document.querySelector('.profile-item')
  let bodyContainer = document.querySelector(".container-item");
  let standardElement = document.querySelector(".btn1");
  let businessElement = document.querySelector(".btn2");
  let professionalElement = document.querySelector(".btn3");
  let enterpriseElement = document.querySelector(".btn4");
  let button = document.querySelectorAll('.btn-set-range')
  let inputField = document.querySelector('.input-field');
  let investBtn = document.querySelector('.invest-btn')

  menuIcon.onclick = () => {
    sideMenuSpans.forEach(span => {
      span.classList.toggle("hidden");
    });
    sideMenuSpans.forEach(span => {
      span.classList.toggle("open");
    });

    sideMenu.classList.toggle("collapsed");
    bodyContainer.classList.toggle("bodycollapsed");
  }

  profileMenu.onclick = ()=>{
    profileLink.classList.toggle('profile-open');
  }

  window.onload = ()=>{
    standardElement.classList.add("btn-active");
    let min = parseInt(standardElement.getAttribute("data-min"));
    inputField.value = min;
    standardElement.onclick = () => {
      standardElement.classList.add("btn-active");
      businessElement.classList.remove("btn-active");
      professionalElement.classList.remove("btn-active");
      enterpriseElement.classList.remove("btn-active");
    };
    businessElement.onclick = () => {
      businessElement.classList.add("btn-active");
      standardElement.classList.remove("btn-active");
      professionalElement.classList.remove("btn-active");
      enterpriseElement.classList.remove("btn-active");
    };
    professionalElement.onclick = () => {
      professionalElement.classList.add("btn-active");
      businessElement.classList.remove("btn-active");
      standardElement.classList.remove("btn-active");
      enterpriseElement.classList.remove("btn-active");
    };
    enterpriseElement.onclick = () => {
      enterpriseElement.classList.add("btn-active");
      businessElement.classList.remove("btn-active");
      standardElement.classList.remove("btn-active");
      professionalElement.classList.remove("btn-active");
    };
  }

  button.forEach(function(button) {
    button.addEventListener('click', function() {
      let min = this.getAttribute('data-min');
      let max = this.getAttribute('data-max');
      inputField.value = min;
      inputField.min = min;
      inputField.max = max;
    });
  });
  
  investBtn.onclick = () =>{
    investBtn.innerHTML = 'Loading..'
  }


});

