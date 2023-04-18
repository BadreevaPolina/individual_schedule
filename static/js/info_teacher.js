$(function() {
  $(".card:first").hide()
  $.ajax({
    url: "/individual-schedule/static/json/info_teacher.json",
    success: function(result) {
      $.each(result, function(index, item) {
      for (i = 0; i < item.length; i++){
        var cards = $(".card:first").clone()
        var full_name = item[i].full_name;
        var post = item[i].post;
        var department = item[i].department;
        var id = item[i].index;
        var elms = document.querySelectorAll("[id='id']");

        if (i === 0) {
            elms[0].value = item[item.length-1].index;
        }
        if (i !== 0) {
            elms[i].value = item[i-1].index;
        }
        $(cards).find(".full_name").html(full_name);
        $(cards).find(".post_department").html(department + ", " + post);
        $(cards).show()
        $(cards).appendTo($(".info_teacher"))
        }
      });
    }
  });
});