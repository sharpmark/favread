var selectedid = -1;

$(document).ready(function() {

    $('#status-panel').perfectScrollbar({suppressScrollX: true});

    $('.status-item').click(function() {
        nowid = $(this).attr('id');
        if (selectedid == nowid) {
            $('#status-detail').toggle();
        }
        else {

            $('#status-detail').perfectScrollbar('destroy');

            $('#status-detail').html($.ajax({url:'/status/'+nowid+'/', async:false}).responseText);
            selectedid = nowid;

            if (! $('#status-detail').is(':visible')) {
                $('#status-detail').show();
            }

            $('#status-detail').perfectScrollbar({suppressScrollX: true});
        }
    });

    $(window).resize(function() {
        $('#status-detail').perfectScrollbar('update');
        $('#status-panel').perfectScrollbar('update');
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
