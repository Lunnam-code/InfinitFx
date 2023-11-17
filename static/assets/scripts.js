// menu toggle 
let menu = document.querySelector('.menu');
let menuItem = document.querySelector('.main-menu-item ul');

menu.onclick = () =>{
  menuItem.classList.toggle('active');
}

window.onscroll = () =>{
  menuItem.classList.remove('active');
}

const header = document.querySelector("header");
window.addEventListener("scroll",function(){
  header.classList.toggle("sticky", window.scrollY > 50);
})
const topBar = document.querySelector(".top-bar");
window.addEventListener("scroll",function(){
  topBar.classList.toggle("sticky", window.scrollY > 50);
})


// home slider 
var sliderIndex = 1;
showSlides(sliderIndex);

function plusSlides(n){
  showSlides(sliderIndex += n);
}


function showSlides(n){
  var i;
  var slides = document.getElementsByClassName('mySlides');
  if (n > slides.length){ sliderIndex = 1}
  if (n < 1){sliderIndex = slides.length}
  for (i = 0; i < slides.length; i++){
    slides[i].style.display = 'none';
  }
 
  slides[sliderIndex - 1].style.display = "block";

}

// premium slider 





const carousel = document.querySelector(".carousel");
const arrowBtns = document.querySelectorAll(".wrapper div");
const firstCardWidth = carousel.querySelector(".card").offsetWidth;
const carouselChildrens = [...carousel.children];

let isDragging = false, startX, startScrollLeft, timeoutId;
const intervalDuration = 3000; 
let intervalId; 


//Let's work on the infinte or loop scrolling effect

//get the number of card that can fit in the carousel at once
let cardPerview = Math.round(carousel.offsetWidth / firstCardWidth);

// Insert copies of the last few cards to beginningof the carousel for infinit e scrolling 
carouselChildrens.slice(-cardPerview).reverse().forEach(card => {
  carousel.insertAdjacentHTML("afterbegin", card.outerHTML)
});

// Insert copies of the first few cards to end of the carousel for infinite scrolling 
carouselChildrens.slice(0, cardPerview).forEach(card => {
  carousel.insertAdjacentHTML("beforeend", card.outerHTML)
});



const infiniteScroll = () =>{
  //if the carousel is at the begging, scrol to the end
  if(carousel.scrollLeft === 0){
    carousel.classList.add("no-transition");
    carousel.scrollLeft = carousel.scrollWidth - ( 2 * carousel.offsetWidth);
    carousel.classList.remove("no-transition");
  } 
  //if the carousel is at the end, scroll beginning
  else if(Math.ceil(carousel.scrollLeft) === carousel.scrollWidth - carousel.offsetWidth){
    carousel.classList.add("no-transition");
    carousel.scrollLeft = carousel.offsetWidth;
    carousel.classList.remove("no-transition");
  }

}

// for mousemovement 


const dragStart = (e) => {
  isDragging = true;
  carousel.classList.add("dragging")
  //records the initial cursor and scroll possition of the carousel
  startX = e.pageX;
  startScrollLeft = carousel.scrollLeft;
}

const dragging = (e) =>{
  if (!isDragging) return // if isdragging is full from here
  // Updates the scroll position of the carousel based on the cursor movement
  carousel.scrollLeft = startScrollLeft - (e.pageX - startX);
}

const dragStop = () => {
  isDragging = false;
  carousel.classList.remove("dragging");
}

// Add event listeners for the arrow buttons to scroll the carousel left and right
arrowBtns.forEach(btn => {
  btn.addEventListener("click", () =>{
    //if clicked button is left, then substract first card width from the carousel scrollLeft else add to it
    carousel.scrollLeft += btn.id ===  "left" ? -firstCardWidth : firstCardWidth;
  })
});

// Function to move the carousel to the right
const moveRight = () => {
  carousel.scrollLeft += firstCardWidth;
  restartAutoplay(); // Restart autoplay after manual navigation
};

// Function to start the autoplay
const startAutoplay = () => {
  intervalId = setInterval(moveRight, intervalDuration);
};

// Function to restart the autoplay
const restartAutoplay = () => {
  clearInterval(intervalId);
  startAutoplay();
};

// Add event listeners for drag start and scroll to restart autoplay
carousel.addEventListener('mousedown', () => {
  clearInterval(intervalId); // Clear existing interval when dragging starts
});

carousel.addEventListener('scroll', () => {
  restartAutoplay(); // Restart autoplay after scroll
});

// Start autoplay when the page loads
startAutoplay();



carousel.addEventListener('mousedown', dragStart);
carousel.addEventListener('mousemove', dragging);
document.addEventListener('mouseup', dragStop);//stop dragging when mouse is released
carousel.addEventListener('scroll', infiniteScroll);



// Testimonial Slider 

const testCarousel = document.querySelector(".test-carousel");
const testArrowBtns = document.querySelectorAll(".test-wrapper div");
const testFirstCardWidth = testCarousel.querySelector(".test-card").offsetWidth;
const testCarouselChildrens = [...testCarousel.children];

let testIsDragging = false, testStartX, testStartScrollLeft, testTimeoutId;
const testIntervalDuration = 3000; 
let testIntervalId; 


//Let's work on the infinte or loop scrolling effect

//get the number of card that can fit in the testCarousel at once
let testCardPerview = Math.round(testCarousel.offsetWidth / testFirstCardWidth);

// Insert copies of the last few cards to beginningof the testCarousel for infinit e scrolling 
testCarouselChildrens.slice(-testCardPerview).reverse().forEach(card => {
  testCarousel.insertAdjacentHTML("afterbegin", card.outerHTML)
});

// Insert copies of the first few cards to end of the testCarousel for infinite scrolling 
testCarouselChildrens.slice(0, testCardPerview).forEach(card => {
  testCarousel.insertAdjacentHTML("beforeend", card.outerHTML)
});



const testInfiniteScroll = () =>{
  //if the testCarousel is at the begging, scrol to the end
  if(testCarousel.scrollLeft === 0){
    testCarousel.classList.add("no-transition");
    testCarousel.scrollLeft = testCarousel.scrollWidth - ( 2 * testCarousel.offsetWidth);
    testCarousel.classList.remove("no-transition");
  } 
  //if the testCarousel is at the end, scroll beginning
  else if(Math.ceil(testCarousel.scrollLeft) === testCarousel.scrollWidth - testCarousel.offsetWidth){
    testCarousel.classList.add("no-transition");
    testCarousel.scrollLeft = testCarousel.offsetWidth;
    testCarousel.classList.remove("no-transition");
  }

}

// for mousemovement 


const testDragStart = (e) => {
  testIsDragging = true;
  testCarousel.classList.add("dragging")
  //records the initial cursor and scroll possition of the testCarousel
  testStartX = e.pageX;
  testStartScrollLeft = testCarousel.scrollLeft;
}

const testDragging = (e) =>{
  if (!testIsDragging) return // if testIsDragging is full from here
  // Updates the scroll position of the testCarousel based on the cursor movement
  testCarousel.scrollLeft = testStartScrollLeft - (e.pageX - testStartX);
}

const testDragStop = () => {
  testIsDragging = false;
  testCarousel.classList.remove("dragging");
}

// Add event listeners for the arrow buttons to scroll the testCarousel left and right
testArrowBtns.forEach(btn => {
  btn.addEventListener("click", () =>{
    //if clicked button is left, then substract first card width from the testCarousel scrollLeft else add to it
    testCarousel.scrollLeft += btn.id ===  "left" ? -testFirstCardWidth : testFirstCardWidth;
  })
});

// Function to move the testCarousel to the right
const testMoveRight = () => {
  testCarousel.scrollLeft += testFirstCardWidth;
  testRestartAutoplay(); // Restart autoplay after manual navigation
};

// Function to start the autoplay
const testStartAutoplay = () => {
  testIntervalId = setInterval(moveRight, testIntervalDuration);
};

// Function to restart the autoplay
const testRestartAutoplay = () => {
  clearInterval(testIntervalId);
  testStartAutoplay();
};

// Add event listeners for drag start and scroll to restart autoplay
testCarousel.addEventListener('mousedown', () => {
  clearInterval(testIntervalId); // Clear existing interval when dragging starts
});

testCarousel.addEventListener('scroll', () => {
  testRestartAutoplay(); // Restart autoplay after scroll
});

// Start autoplay when the page loads
testStartAutoplay();



testCarousel.addEventListener('mousedown', testDragStart);
testCarousel.addEventListener('mousemove', testDragging);
document.addEventListener('mouseup', testDragStop);//stop testDragging when mouse is released
testCarousel.addEventListener('scroll', testInfiniteScroll);




// logo slider , partners

var copy = document.querySelector(".logos-slide").cloneNode(true);
document.querySelector('.logos').appendChild(copy);


// FAQ 








