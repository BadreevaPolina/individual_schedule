$(function(){
setTimeout(oneSecondFunction, 500);
});

var buttons = document.querySelectorAll('.btn.btn-outline-dark.stretched-link');
var c_teacher = Number(document.getElementById("count_teacher").value);
var ids = "";

function oneSecondFunction() {
if (document.querySelectorAll('.btn.btn-outline-dark.stretched-link').length != 1){
var buttons = document.querySelectorAll('.btn.btn-outline-dark.stretched-link');
var c_teacher = Number(document.getElementById("count_teacher").value);
for (var i=0; i<buttons.length; i++) {
  buttons[i].addEventListener('click', displayGreeting)
}
}
}

function displayGreeting(event) {
  if (c_teacher>0){
    const id = event.target.querySelector(".id").value + ", ";
  if(event.target.style.backgroundColor != "rgb(33, 37, 41)"){
    console.log(event.target.style.backgroundColor = "#212529");
    console.log(event.target.style.color = "#fff");
    ids = ids + id;
    c_teacher=c_teacher-1;
    }
   else {
    console.log(event.target.style.backgroundColor = "#fff");
    console.log(event.target.style.color = "#212529");
    ids = ids.replace(id, "");
    c_teacher=c_teacher+1;
   }
  }
}

function setAction(form) {
    if (c_teacher == 0){
    form.action = "/time";
    event.target.querySelector(".index_teachers").value = ids
    return true;
    }
    return false;
}