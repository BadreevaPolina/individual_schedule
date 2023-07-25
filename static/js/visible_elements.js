function initialize() {
    checkInputFieldWarning();
    checkJson();
}

function checkInputFieldWarning() {
    const hiddenElementWarning = document.querySelector('.warning');
    const inputFieldWarning = document.querySelector('#incorrect_data');
    if (inputFieldWarning.value === ' ' || inputFieldWarning.value === '' ||  inputFieldWarning.value === 'None') {
        hiddenElementWarning.style.display = 'none';
    } else {
        hiddenElementWarning.style.display = 'block';
    }
}


function checkJson() {
    const json = document.getElementById("json_teachers").value;
    const hiddenElementTable = document.querySelector('#calendar');
    const hiddenElementTableUnchanged = document.querySelector('#calendar_unchanged');
    const hiddenElementAnswer = document.querySelector('#answer').value;
    const showDivCheckbox = document.querySelector('#showDiv');

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
}

function showDivCheckboxChange(event) {
    const hiddenElementTable = document.querySelector('#calendar');
    const hiddenElementTableUnchanged = document.querySelector('#calendar_unchanged');
    const hiddenElementAnswer = document.querySelector('#answer').value;
    if(hiddenElementAnswer!== "None") {
        if (event.target.checked) {
            hiddenElementTableUnchanged.style.visibility = "visible";
            hiddenElementTable.style.visibility = "hidden";
        } else {
            hiddenElementTableUnchanged.style.visibility = "hidden";
            hiddenElementTable.style.visibility = "visible";
        }
    }
}

initialize();
const showDivCheckbox = document.querySelector('#showDiv');
showDivCheckbox.addEventListener('change', showDivCheckboxChange);
