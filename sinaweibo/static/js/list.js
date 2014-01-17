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
            // $("#extra").html(nowid);
            selectedid = nowid;
        }
    });
});

$(function () {
    $('#extra').perfectScrollbar();
    $('#left').perfectScrollbar();
})


