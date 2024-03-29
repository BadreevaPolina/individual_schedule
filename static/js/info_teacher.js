function initialize() {
    cookieNotify();
    checkboxPlace();
    disableSubmitButton();
    checkInputFieldError();
    parseJson();
    scrollToTeacherInfo();
}

function cookieNotify() {
    $(document).ready(function(){
        let isRead = localStorage.getItem("cookie_read");
        if (isRead === null) {
            $(".cookie").show();
        }

        $(".accept").click(function(){
            localStorage.setItem("cookie_read", "true");
            $(".cookie").hide();
        });
    });
}

function disableSubmitButton() {
    $('form').submit(function() {
        const submitButton = $(this).find('button[type="submit"]:focus');
        submitButton.prop('disabled', true);
        submitButton.find('.spinner-border').removeClass('d-none');
    });
}

function checkboxPlace() {
    const checkbox = document.getElementById("flexCheck");
    if(checkbox !== null){
        checkbox.addEventListener('click', function() {
            if (checkbox.checked) {
                checkbox.value = "True";
            } else {
                checkbox.value = "False";
            }
        });
    }
}

function checkInputFieldError() {
    const hiddenElementError = document.querySelector('.error');
    const inputFieldError = document.querySelector('input[name="words_error"]').value;
    if (inputFieldError === ' ' || inputFieldError === '' || inputFieldError === 'None') {
        hiddenElementError.style.display = 'none';
    } else {
        hiddenElementError.style.display = 'block';
    }
}

function parseJson() {
    const json = document.getElementById("json_teachers").value;
    if (json !== "None") {
        const obj = JSON.parse(json);
        const fullName = [], post = [], department = [], index = [];
        let i = 0;
        JSON.parse(json, function(key, value) {
            if (key == 'full_name') fullName[i] = value;
            if (key == 'post') post[i] = value;
            if (key == 'department') department[i] = value;
            if (key == 'index') {
                index[i] = value;
                i++;
            }
        });
        displayTeacherCards(fullName, post, department, index);
    }
}

function displayTeacherCards(full_name, post, department, index) {
    $('.card').slice(1).remove();
    $(".card:first").hide();
    for (let i = 0; i < index.length; i++) {
        const elms = document.querySelectorAll("[id='id']");
        if (i === 0) {
            elms[0].value = index[index.length - 1];
        }
        if (i !== 0) {
            elms[i].value = index[i - 1];
        }
        const cards = $(".card:first").clone();
        $(cards).find(".full_name").html(full_name[i]);
        $(cards).find(".post_department").html(department[i] + ", " + post[i]);
        $(cards).show();
        $(cards).appendTo($(".info_teacher"));
    }
    $(".card").slice(1).css("display", "block");
}

function scrollToTeacherInfo() {
    setTimeout(function() {
        const element = document.querySelector(".info_teacher");
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
            inline: 'nearest'
        });
    }, 10);
}

initialize();