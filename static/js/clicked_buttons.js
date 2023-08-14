$(function(){
    setTimeout(listenButtons, 500);
});

let countTeachers = Number(document.getElementById("count_teacher").value);
let ids = "", names = "";

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
        let mas = teachers.split(", ");
        mas = mas.filter(function(item) {
            return !error.includes(item);
        });
        for (let i = 0; i < mas.length; i++) {
            mas[i] = mas[i].split(" ")[0];
        }
        let c = 0, j = 0;
        if(buttons.length != mas.length + 1){
            for (let i = 1; i < buttons.length; i++) {
                let surname = button[i].querySelector('h5.full_name').textContent.substring(0, mas[j].length);
                if(surname.toLowerCase() !== mas[j].toLowerCase()){
                    if(c === 1){
                        buttons[i-1].style.backgroundColor = "#212529";
                        buttons[i-1].style.color = "#fff";
                        let id = button[i-1].querySelector(".id").value + ", ";
                        let name = button[i-1].querySelector(".full_name").textContent + ", ";
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
                        let id = button[i].querySelector(".id").value + ", ";
                        let name = button[i].querySelector(".full_name").textContent + ", ";
                        ids += id;
                        names += name;
                        countTeachers--;
                        if (countTeachers == 0){
                            button[i].click();
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