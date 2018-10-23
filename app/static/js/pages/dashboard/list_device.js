$(function () {
    $('.list-device').DataTable({
        responsive: true,
    });

    var now = moment();

$('time').each(function(i, e) {
    var time = moment($(e).attr('datetime'));

    if(now.diff(time, 'days') <= 1) {
        $(e).html('<span>' + time.from(now) + '</span>');
    }
});
});