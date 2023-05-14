var json = document.getElementById("json_teachers").value;
var obj = JSON.parse(json)
value = obj.teacher[0];
const full_name = [];
const post = [];
const department = [];
const index = [];
var i = 0;

JSON.parse(json, function(key, value) {
  if (key == 'full_name') full_name[i] = value;
  if (key == 'post') post[i] = value;
  if (key == 'department') department[i] = value;
  if (key == 'index') {
  index[i] = value;
  i = i + 1;
  }
});

$(function() {
  $(".card:first").hide()
   for (i = 0; i < index.length; i++){
    var elms = document.querySelectorAll("[id='id']");
        if (i === 0) {
            elms[0].value = index[index.length-1];
        }
        if (i !== 0) {
            elms[i].value = index[i-1];
        }
        var cards = $(".card:first").clone()
        $(cards).find(".full_name").html(full_name[i]);
        $(cards).find(".post_department").html(department[i] + ", " + post[i]);
        $(cards).show()
        $(cards).appendTo($(".info_teacher"))
        }
    $(".card").style.display = "block";
    });

setTimeout(myFunction, 10)
function myFunction() {
    const element = document.querySelector(".info_teacher");
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
        inline: 'nearest'
    });
}
