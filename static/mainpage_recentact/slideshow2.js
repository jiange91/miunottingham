var slideIndex = 0;
var intervalId = 0;

const prevBtn = document.querySelector('.prev')
prevBtn.addEventListener('click', () => updateSlideIndex(slideIndex-1))
// ! for mobile 'touchstart'
prevBtn.addEventListener('touchstart', () => updateSlideIndex(slideIndex-1))
const nextBtn = document.querySelector('.next')
nextBtn.addEventListener('click', () => updateSlideIndex(slideIndex+1))
nextBtn.addEventListener('touchstart', () => {updateSlideIndex(slideIndex+1); console.log('touch start clicked')})
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
    intervalId = setTimeout(() => updateSlideIndex(slideIndex+1), 7000)
}


// todo: listen to swipe [mobile device]
function swipedetect(el, callback){
  
  var touchsurface = el,
  swipedir,
  startX,
  startY,
  distX,
  distY,
  threshold = 150, //required min distance traveled to be considered swipe
  restraint = 100, // maximum distance allowed at the same time in perpendicular direction
  allowedTime = 300, // maximum time allowed to travel that distance
  elapsedTime,
  startTime,
  handleswipe = callback || function(swipedir){}

  touchsurface.addEventListener('touchstart', function(e){
      var touchobj = e.changedTouches[0]
      swipedir = 'none'
      dist = 0
      startX = touchobj.pageX
      startY = touchobj.pageY
      startTime = new Date().getTime() // record time when finger first makes contact with surface
      e.preventDefault()
  }, false)

  touchsurface.addEventListener('touchmove', function(e){
      e.preventDefault() // prevent scrolling when inside DIV
  }, false)

  touchsurface.addEventListener('touchend', function(e){
      var touchobj = e.changedTouches[0]
      console.log(touchobj)
      distX = touchobj.pageX - startX // get horizontal dist traveled by finger while in contact with surface
      distY = touchobj.pageY - startY // get vertical dist traveled by finger while in contact with surface
      elapsedTime = new Date().getTime() - startTime // get time elapsed
      if (elapsedTime <= allowedTime){ // first condition for awipe met
          if (Math.abs(distX) >= threshold && Math.abs(distY) <= restraint){ // 2nd condition for horizontal swipe met
              swipedir = (distX < 0)? 'left' : 'right' // if dist traveled is negative, it indicates left swipe
          }
      }
      handleswipe(swipedir)
      e.preventDefault()
  }, false)
}

//USAGE:

var el = document.querySelector('.swipezone');
swipedetect(el, function(swipedir){
  // swipedir contains either "none", "left", "right", "top", or "down"
  console.log(swipedir)
  if (swipedir === 'right') {
    updateSlideIndex(slideIndex-1)
  }
  if (swipedir === 'left') {
    updateSlideIndex(slideIndex+1)

  }
//  if (swipedir)
});
