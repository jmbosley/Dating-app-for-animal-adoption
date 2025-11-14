'use strict';

window.addEventListener('load', function () {

  console.log("Hello World!");

});

// https://stackoverflow.com/a/20306103
function confirmAnimalDeletion() {
  return confirm("Are you sure you want to permanently delete this animal?");
}

// https://www.w3schools.com/howto/howto_js_slideshow.asp
function plusSlides(n) {
  	showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
  	dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
	}