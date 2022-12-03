$(function() {
  $(".card:first").hide()
  $.ajax({
    url: "/static/json/info_teacher.json",
    success: function(result) {
      $.each(result, function(index, item) {
      for (i = 0; i < 2; i++){
        var cards = $(".card:first").clone()
        var full_name = item[i].full_name;
        var post = item[i].post;
        var department = item[i].department;
        var indexs = item[i].index;
        $(cards).find(".card-title").html(full_name + "   " + indexs + "  " );
        $(cards).find(".card-text").html(post + ", " + department);
        $(cards).show()
        $(cards).appendTo($(".info_teacher"))
        }
      });
    }
  });
});