function find() {
    const student = $('input[name="student"]').val();
    const teacher = $('input[name="teacher"]').val();
    const flag_place = $('input[name="flag_place"]').val() || "False";

    $.ajax({
        url: '/individual-schedule/find',
        type: 'POST',
        data: { student, teacher, flag_place },
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        success: function(response) {
            const currentPage = location.href;
            if ('redirect' in response) {
                window.location.href = response.redirect;
            } else {
                $('input[name="count_teacher"]').val(response.count_teacher);
                $('input[name="json_teachers"]').val(response.json_teachers);
                $('input[name="words_error"]').val(response.words_error);
                $('[id="words_error"]').text(response.words_error);

                if (currentPage.indexOf("/individual-schedule/timetable") !== -1) {
                    $('[id="incorrect_data"]').text("None");
                    $('input[name="incorrect_data"]').val("None");
                    $('input[id="answer_json"]').val("[]");
                    $('input[id="timetable_unchanged_json"]').val("[]");

                    let scripts = [
                        'info_teacher.js',
                        'clicked_buttons.js',
                        'table.js',
                        'visible_elements.js'
                    ];

                    scripts.forEach(script => {
                        $.ajax({
                            url: `static/js/${script}`,
                            cache: true,
                            dataType: 'script'
                        });
                    });
                } else {
                    let scripts = [
                        'info_teacher.js',
                        'clicked_buttons.js'
                    ];

                    scripts.forEach(script => {
                        $.ajax({
                            url: `static/js/${script}`,
                            cache: true,
                            dataType: 'script'
                        });
                    });
                }

                const submitButton = $('button[type="submit"]');
                submitButton.prop('disabled', false);
                submitButton.find('.spinner-border').addClass('d-none');
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            const errorMessage = (jqXHR.status === 500) ? jqXHR.responseJSON.message : "Ошибка. Попробуйте снова.";
            window.location.href = `/individual-schedule/error?error=${errorMessage}`;
        }
    });
}

function timetable_4_month() {
    $.ajax({
        url: '/individual-schedule/timetable_4_month',
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        success: function(response) {
            window.location.href = response.redirect;
        },
        error: function(jqXHR, textStatus, errorThrown) {
            const errorMessage = (jqXHR.status === 500) ? jqXHR.responseJSON.message : "Ошибка. Попробуйте снова.";
            window.location.href = `/individual-schedule/error?error=${errorMessage}`;
        }
    });
}