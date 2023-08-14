document.addEventListener('DOMContentLoaded', function() {
    const calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
        initialView: 'timeGridWeek',
        headerToolbar: {
            left: 'prev',
            center: 'title',
            right: 'next'
        },
        customButtons: {
            prev: {
                text: ' < ',
                click: function() {
                    calendar.prev();
                    calendarUnchanged.prev();
                }
            },
            next: {
                text: ' > ',
                click: function() {
                    calendar.next();
                    calendarUnchanged.next();
                }
            }
        },
        height: 'auto',
        editable: false,
        selectable: false,
        selectMirror: true,
        nowIndicator: true,
        events: JSON.parse(document.getElementById("answer_json").value)
    });
    const calendarUnchanged = new FullCalendar.Calendar(document.getElementById('calendar_unchanged'), {
        initialView: 'timeGridWeek',
        headerToolbar: {
            left: 'prev',
            center: 'title',
            right: 'next'
        },
        customButtons: {
            prev: {
                text: ' < ',
                click: function() {
                    calendar.prev();
                    calendarUnchanged.prev();
                }
            },
            next: {
                text: ' > ',
                click: function() {
                    calendar.next();
                    calendarUnchanged.next();
                }
            }
        },
        height: 'auto',
        editable: false,
        selectable: false,
        selectMirror: true,
        nowIndicator: true,
        eventMouseEnter: function(info) {
            let resultTittle = info.event.title.replace(/(.*?,.*?,).*$/, '$1');
            if (resultTittle.charAt(resultTittle.length - 1) === ',') {
                resultTittle = resultTittle.slice(0, -1);
            }
            info.el.title = info.event.extendedProps.subject + ", \n" +
            info.event.extendedProps.place + ", \n" + resultTittle;},
        events: JSON.parse(document.getElementById("timetable_unchanged_json").value)
    });

    calendar.render();
    calendarUnchanged.render();
});