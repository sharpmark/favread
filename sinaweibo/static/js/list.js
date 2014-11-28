var selectedid = -1;

$(document).ready(function() {

    $('#status-panel').perfectScrollbar({wheelSpeed: 30, suppressScrollX: true});

    $('.status-item').click(function() {
        nowid = $(this).attr('sid');
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

            $('#status-detail').perfectScrollbar({wheelSpeed: 50, suppressScrollX: true});
        }
    });

    $(window).resize(function() {
        $('#status-detail').perfectScrollbar('update');
        $('#status-panel').perfectScrollbar('update');
    });

});

function favorites(id, action, csrf) {
    post_data = {};
    post_data['status_id'] = id;
    post_data['action_type'] = action;
    post_data['csrfmiddlewaretoken'] = csrf;
    $.ajax({
        type: 'POST',
        url: '/favorites/',
        data: post_data,
        dataType: 'json'
    });

    if (id == selectedid) {
        $('#status-detail').hide();
    }

    // 不需要，因为整个status会被删除。
    // if ('destroy'==action) { switch_opt(id); }

    event.stopPropagation();
    $("#item-" + id).remove();
};

function switch_opt(id) {
    $('#'+id+'-del').toggle();
    $('#'+id+'-opt').toggle();
    event.stopPropagation();
};

function edit_tag(id) {
    //$('#tag-editor').toggle();
}
