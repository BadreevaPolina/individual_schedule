  var hiddenElementWarning = document.querySelector('.warning');
var inputFieldWarning = document.querySelector('#incorrect_data');
if (inputFieldWarning.value === ' ' || inputFieldWarning.value === '' ||  inputFieldWarning.value === 'None') {
    hiddenElementWarning.style.display = 'none';
  } else {
    hiddenElementWarning.style.display = 'block';
  }

var json = document.getElementById("json_teachers").value;
var hiddenElementTable = document.querySelector('#calendar');
var hiddenElementTableUnchanged = document.querySelector('#calendar_unchanged');
var hiddenElementAnswer = document.querySelector('#answer').value;
var showDivCheckbox = document.querySelector('#showDiv');


if (json !== "None"){
    hiddenElementTableUnchanged.style.display = 'none';
    hiddenElementTable.style.display = 'none';
    showDivCheckbox.style.display = 'none';
} else {
       if(hiddenElementAnswer !== "None"){
    hiddenElementTable.style.display = 'block';
    hiddenElementTable.style.visibility = "visible";
    hiddenElementTableUnchanged.style.display = 'block';
    hiddenElementTableUnchanged.style.visibility = "hidden";
    } else{
    hiddenElementTable.style.display = 'none';
    showDivCheckbox.style.display = 'none';
    hiddenElementTableUnchanged.style.display = 'block';
    hiddenElementTableUnchanged.style.visibility = "visible";
    }
}


  showDivCheckbox.addEventListener('change', function() {
  if(hiddenElementAnswer !== "None") {
    if (this.checked) {
      hiddenElementTable.style.visibility = "hidden";
      hiddenElementTableUnchanged.style.visibility = "visible";
    } else {
      hiddenElementTable.style.visibility = "visible";
      hiddenElementTableUnchanged.style.visibility = "hidden";
    }
  }});

