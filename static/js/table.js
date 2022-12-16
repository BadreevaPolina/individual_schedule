
  document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialDate: '2022-12-14',
      initialView: 'timeGridWeek',
      headerToolbar: {
        left: '',
        center: 'title',
        right: ''
      },
      height: 'auto',
      editable: true,
      selectable: false,
      selectMirror: true,
      nowIndicator: true,
        eventSources: [
    {
      url: 'static/json/answer.json'
    }
  ]
    });

    calendar.render();
  });

