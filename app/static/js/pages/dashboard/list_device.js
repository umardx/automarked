$(function () {
    $('.list-device').DataTable({
        responsive: true,
    });

    let timer = setInterval(function () {
        let now = moment();

        $('checked_time').each(function(i, e) {
            let time = moment.utc($(e).attr('datetime'));

            if(now.diff(time, 'hours') <= 1) {
                $(e).html('<span class="badge bg-light-green" title="' + time.local().format('lll') + '">' + time.from(now) + '</span>');
            } else
            if(now.diff(time, 'days') <= 1) {
                $(e).html('<span class="badge bg-cyan" title="' + time.local().format('lll') + '">' + time.from(now) + '</span>');
            } else {
                $(e).html('<span class="badge bg-grey" title="' + time.local().format('lll') + '">' + time.from(now) + '</span>');
            }
        });

        $('status').each(function(i, e) {
            let status = $(e).attr('status');
    
            if(status==="True") {
                $(e).html('<span class="badge bg-green">' + 'Reachable' + '</span>');
            } else {
                $(e).html('<span class="badge bg-grey">' + 'Unreachable' + '</span>');
            }
        });
    }, 200);
});
