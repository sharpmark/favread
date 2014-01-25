var selectedid = -1;

$(document).ready(function() {
    $(".feed").click(function() {
        nowid = $(this).attr("id");
        if (selectedid == nowid) {
            $("#extra").toggle();
        }
        else {
            if (! $("#extra").is(":visible")) {
                $("#extra").show();
            }

            $("#extra").html($.ajax({url:"/status/"+nowid+"/", async:false}).responseText);

            selectedid = nowid;
        }
    });
    $(window).resize(function() {
        $("#extra").perfectScrollbar('update');
        $("#left").perfectScrollbar('update');
    });
});

$(function () {
    $('#extra').perfectScrollbar();
    $('#left').perfectScrollbar();
})


