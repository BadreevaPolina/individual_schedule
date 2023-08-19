function find() {
    let student = $('input[name="student"]').val();
    let teacher = $('input[name="teacher"]').val();
    let flag_place = $('input[name="flag_place"]').val();
    if (flag_place === undefined)
    {
        flag_place = "False";
    }
    $.ajax({
        url: '/individual-schedule/find',
        type: 'POST',
        data: { student: student, teacher: teacher, flag_place: flag_place },
        dataType: 'json',
        success: function(response) {
            let currentPage = location.href;
            if ('redirect' in response) {
                window.location.href = response.redirect;
            }
            else {
                $('input[name="count_teacher"]').val(response.count_teacher);
                $('input[name="json_teachers"]').val(response.json_teachers);
                $('input[name="words_error"]').val(response.words_error);
                $('[id="words_error"]').text(response.words_error);

                if (currentPage.indexOf("/individual-schedule/timetable") !== -1) {
                    $('[id="incorrect_data"]').text("None");
                    $('input[name="incorrect_data"]').val("None");
                    $('input[id="answer_json"]').val("[]");
                    $('input[id="timetable_unchanged_json"]').val("[]");

                    $.ajax({
                        url: 'static/js/info_teacher.js',
                        cache: true,
                        dataType: 'script'
                    })
                    $.ajax({
                        url: 'static/js/clicked_buttons.js',
                        cache: true,
                        dataType: 'script'
                    })
                    $.ajax({
                        url: 'static/js/table.js',
                        cache: true,
                        dataType: 'script'
                    })
                    $.ajax({
                        url: 'static/js/visible_elements.js',
                        cache: true,
                        dataType: 'script'
                    })
                }
                else{
                    $.ajax({
                        url: 'static/js/info_teacher.js',
                        cache: true,
                        dataType: 'script'
                    })
                    $.ajax({
                        url: 'static/js/clicked_buttons.js',
                        cache: true,
                        dataType: 'script'
                    })
                }

                const submitButton = $('button[type="submit"]');
                submitButton.prop('disabled', false);
                submitButton.find('.spinner-border').addClass('d-none');
            }
        },
        error: function(jqXHR, textStatus, errorThrown) {
            if (jqXHR.status === 500) {
                message = jqXHR.responseJSON.message;
                window.location.href = '/individual-schedule/error?error=' + message;
            }
            else{
                window.location.href = '/individual-schedule/error';
            }
        }
    });
}