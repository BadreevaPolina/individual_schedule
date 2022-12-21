$(function() {
  $(".card:first").hide()
  $.ajax({
    url: "/static/json/info_teacher.json",
    success: function(result) {
      $.each(result, function(index, item) {
      for (i = 0; i < item.length; i++){
        var cards = $(".card:first").clone()
        var full_name = item[i].full_name;
        var post = item[i].post;
        var department = item[i].department;
        var id = item[i].index;
        var elms = document.querySelectorAll("[id='id']");

        if (i === item.length - 1) {
            elms[i].value = item[0].index;
        } else {
            elms[i].value = item[i+1].index;
            }
        $(cards).find(".card-title").html(full_name);
        $(cards).find(".card-text").html(department + ", " + post);
        $(cards).show()
        $(cards).appendTo($(".info_teacher"))
        }
      });
    }
  });
});