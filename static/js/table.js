
  document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'timeGridWeek',
      headerToolbar: {
        left: 'prev',
        center: 'title',
        right: 'next'
      },
      height: 'auto',
      editable: false,
      selectable: false,
      selectMirror: true,
      nowIndicator: true,
      eventSources: [
    {
      url: 'static/json/answer.json'
    }]
    });
    calendar.render();
  });

  document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar_unchanged');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'timeGridWeek',
      headerToolbar: {
        left: 'prev',
        center: 'title',
        right: 'next'
      },
      height: 'auto',
      editable: false,
      selectable: false,
      selectMirror: true,
      nowIndicator: true,
      eventSources: [
    {
      url: 'static/json/timetable_unchanged.json'
    }]
    });
    calendar.render();
  });