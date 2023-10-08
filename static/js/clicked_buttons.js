$(function(){
    setTimeout(listenButtons, 500);
});

if (window.countTeachers === undefined) {
    let countTeachers, ids, names;
}
countTeachers = Number(document.getElementById("count_teacher").value);
ids = "", names = "";


function listenButtons() {
    const buttons = document.querySelectorAll('.btn.btn-outline-dark.stretched-link');
    if (buttons.length !== 1){
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].addEventListener('click', changeColor)
        }
        defineButtons()
    }
}

function defineButtons() {
    const buttons = document.querySelectorAll('.btn.btn-outline-dark.stretched-link');
    if (buttons.length !== 1){
        const teachers = document.querySelector('input[name="teacher"]').value;
        const errorElement = document.getElementById("error");
        const error = errorElement.querySelector("h4").textContent.split(", ");
        let list = teachers.split(",");
        list = list.map(function(item) {
            let trimmedItem = item.trim();
            if (!error.includes(trimmedItem)) {
                return trimmedItem;
            }
        });
        list = list.filter(function(item) {
            return item !== '';
        });
        for (let i = 0; i < list.length; i++) {
            list[i] = list[i].split(" ")[0];
        }
        let c = 0, j = 0;
        if(buttons.length != list.length + 1){
            for (let i = 1; i < buttons.length; i++) {
                let surname = buttons[i].querySelector('h5.full_name').textContent.substring(0, list[j].length);
                if(surname.toLowerCase() !== list[j].toLowerCase()){
                    if(c === 1){
                        buttons[i-1].style.backgroundColor = "#212529";
                        buttons[i-1].style.color = "#fff";
                        let id = buttons[i-1].querySelector(".id").value + ", ";
                        let name = buttons[i-1].querySelector(".full_name").textContent + ", ";
                        ids += id;
                        names += name;
                        countTeachers--;
                        if (countTeachers == 0){
                            button[i-1].click();
                        }
                    }
                    if(i === buttons.length - 1){
                        buttons[i].style.backgroundColor = "#212529";
                        buttons[i].style.color = "#fff";
                        let id = buttons[i].querySelector(".id").value + ", ";
                        let name = buttons[i].querySelector(".full_name").textContent + ", ";
                        ids += id;
                        names += name;
                        countTeachers--;
                        if (countTeachers == 0){
                            buttons[i].click();
                        }
                    }
                    c = 1;
                    j++;
                }
                else{
                    c++;
                }
            }
        }
    }
}

function changeColor(event) {
    if (countTeachers > 0){
        const id = event.target.querySelector(".id").value + ", ";
        const name = event.target.querySelector(".full_name").textContent + ", ";
        if(event.target.style.backgroundColor != "rgb(33, 37, 41)"){
            event.target.style.backgroundColor = "#212529";
            event.target.style.color = "#fff";
            ids += id;
            names += name;
            countTeachers--;
        }
        else {
            event.target.style.backgroundColor = "#fff";
            event.target.style.color = "#212529";
            ids = ids.replace(id, "");
            names = names.replace(name, "");
            countTeachers++;
        }
    }
}

function setAction(form) {
    if (countTeachers == 0){
        form.action = "/individual-schedule/timetable";
        form.querySelector(".index_teachers").value = ids;
        form.querySelector(".teachers").value = names;
        return true;
    }
    return false;
}


function getData(form) {
    let focusedButton = $('button[type="submit"]:focus');
    let buttonName = focusedButton.attr('class');

    if (buttonName == "button-standard") {
        find();
        return false;
    }
    if (buttonName == "button-4-months") {
        timetable_4_month();
        return false;
    }
    else{
        let submitButton = $('button[type="submit"].button-standard');
        submitButton.prop('disabled', true);
        submitButton.find('.spinner-border').removeClass('d-none');
        find();
        return false;
    }
}

function getDataMain(form){
    find();
    return false;
}