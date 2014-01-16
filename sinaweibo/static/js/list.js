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
            $("#extra").html(nowid);
            selectedid = nowid;
        }
    });
});

$(function () {
    $('#right').bind('mousewheel', function(event) {
        event.preventDefault();
        var scrollTop = this.scrollTop;
        this.scrollTop = (scrollTop + ((event.deltaY * event.deltaFactor) * -1));
        console.log(event.deltaY);
    });
});
