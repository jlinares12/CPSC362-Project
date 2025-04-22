hamburger = document.querySelector(".hamburger");

hamburger.onclick = function() {
  navBar = document.querySelector(".nav-box");
  navBar.classList.toggle("active")
  console.log("click works");
}
