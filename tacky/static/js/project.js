/* Project specific Javascript goes here. */
$(function() {

$("td").click(function() {
  var row_index = $(this).parent().index();
  var col_index = $(this).index();
  var new_index = Number(row_index * 3 + col_index);
  $("#id_move").val(new_index);
  $(this).addClass( "player");

  $(".updateform").submit();
});
});



