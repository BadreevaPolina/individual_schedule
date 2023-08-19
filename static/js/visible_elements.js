function initialize() {
    checkInputFieldWarning();
    checkJson();
    const showDivCheckbox = document.querySelector('#showDiv');
    showDivCheckbox.addEventListener('change', showDivCheckboxChange);
}

function checkInputFieldWarning() {
    const hiddenElementWarning = document.querySelector('.warning');
    const inputFieldWarning = document.querySelector('input[name="incorrect_data"]').value;
    const json = document.getElementById("json_teachers").value;
    if (json != "None" || inputFieldWarning === ' ' || inputFieldWarning === '' ||  inputFieldWarning === 'None') {
        hiddenElementWarning.style.display = 'none';
    } else {
        hiddenElementWarning.style.display = 'block';
    }
}


function checkJson() {
    const json = document.getElementById("json_teachers").value;
    const hiddenElementTable = document.querySelector('#calendar');
    const hiddenElementTableUnchanged = document.querySelector('#calendar_unchanged');
    const hiddenElementAnswer = document.querySelector('#answer_json').value;
    const showDivCheckbox = document.querySelector('#showDiv');
    if (json !== "None"){
        hiddenElementTableUnchanged.style.display = 'none';
        hiddenElementTable.style.display = 'none';
        showDivCheckbox.style.display = 'none';
    } else {
        if(hiddenElementAnswer !== "[]"){
            showDivCheckbox.style.display = 'block';
            hiddenElementTable.style.display = 'block';
            hiddenElementTable.style.visibility = "hidden";
            hiddenElementTableUnchanged.style.display = 'block';
            hiddenElementTableUnchanged.style.visibility = "visible";
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
    const hiddenElementAnswer = document.querySelector('#answer_json').value;
    if(hiddenElementAnswer !== "[]") {
        if (event.target.checked) {
            hiddenElementTableUnchanged.style.visibility = "hidden";
            hiddenElementTable.style.visibility = "visible";
        } else {
            hiddenElementTableUnchanged.style.visibility = "visible";
            hiddenElementTable.style.visibility = "hidden";
        }
    }
}

initialize();
