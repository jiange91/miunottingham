var slideIndex = 0;
var intervalId = 0;

const prevBtn = document.querySelector('.prev')
prevBtn.addEventListener('click', () => updateSlideIndex(slideIndex-1))
prevBtn.addEventListener('touchstart', () => updateSlideIndex(slideIndex-1))
const nextBtn = document.querySelector('.next')
nextBtn.addEventListener('click', () => updateSlideIndex(slideIndex+1))
nextBtn.addEventListener('touchstart', () => updateSlideIndex(slideIndex+1))
const dotBtn = document.querySelectorAll('.dot')
dotBtn.forEach((dot,i) => {
  dot.addEventListener('click', () => updateSlideIndex(i))
  dot.addEventListener('touchstart', () => updateSlideIndex(i))
})

showSlides()
function updateSlideIndex(i) {
  clearInterval(intervalId)
  slideIndex = i
  showSlides()
}

function showSlides() {
    var slides = document.querySelectorAll(".mySlides");
    slides.forEach(i => {i.style.display = 'none'; dotBtn.forEach(i => i.classList.remove('active'))})
    if (slideIndex > slides.length - 1) {slideIndex = 0} 
    if (slideIndex < 0) {slideIndex = slides.length - 1}
    slides[slideIndex].style.display = "block"; 
    dotBtn[slideIndex].classList.add('active')
    // change every 5 seconds 
    // ! do not comment out 
    intervalId = setTimeout(() => updateSlideIndex(slideIndex+1), 5000)
}