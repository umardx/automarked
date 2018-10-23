$(function () {
    $('.list-device').DataTable({
        responsive: true,
    });

    $('status').each(function(i, e) {
        var status = $(e).attr('status');

        if(status==="True") {
            $(e).html('<span class="badge bg-green">' + 'Reachable' + '</span>');
        } else {
            $(e).html('<span class="badge bg-grey">' + 'Unreachable' + '</span>');
        }
    });

    var now = moment();

    $('checked_time').each(function(i, e) {
        var time = moment.utc($(e).attr('datetime'));

        if(now.diff(time, 'hours') <= 1) {
            $(e).html('<span class="badge bg-cyan">' + time.from(now) + '</span>');
        } else
        if(now.diff(time, 'days') <= 1) {
            $(e).html('<span class="badge bg-light-blue">' + time.from(now) + '</span>');
        } else {
            $(e).html('<span class="badge bg-grey">' + time.from(now) + '</span>');
        }
    });
});