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

if (json !== "None"){
    hiddenElementTableUnchanged.style.display = 'none';
    hiddenElementTable.style.display = 'none';
} else {
       if(hiddenElementAnswer !== "None"){
    hiddenElementTable.style.display = 'block';
    } else{
    hiddenElementTable.style.display = 'none';
    }
    hiddenElementTableUnchanged.style.display = 'block';
}

