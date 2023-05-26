  var hiddenElementWarning = document.querySelector('.warning');
var inputFieldWarning = document.querySelector('#incorrect_data');
if (inputFieldWarning.value === ' ' || inputFieldWarning.value === '' ||  inputFieldWarning.value === 'None') {
    hiddenElementWarning.style.display = 'none';
  } else {
    hiddenElementWarning.style.display = 'block';
  }
var json = document.getElementById("json_teachers").value;
var hiddenElementError = document.querySelector('#calendar');

if (json !== "None"){
    hiddenElementError.style.display = 'none';
} else {
    hiddenElementError.style.display = 'block';
  }