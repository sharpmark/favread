var selectedid = -1;

$(document).ready(function() {
    $(".status-item").click(function() {
        nowid = $(this).attr("id");
        if (selectedid == nowid) {
            $("#status-detail").toggle();
        }
        else {
            if (! $("#status-detail").is(":visible")) {
                $("#status-detail").show();
            }

            $("#status-detail").html($.ajax({url:"/status/"+nowid+"/", async:false}).responseText);

            selectedid = nowid;
        }
    });
});

function favorites(id, action) {
    post_data = {};
    post_data['status_id'] = id;
    post_data['action_type'] = action;
    $.ajax({
        type: 'POST',
        url: '/favorites/',
        data: post_data,
        dataType: 'json'
    });
    event.stopPropagation()
    $("#" + id).hide();
}


