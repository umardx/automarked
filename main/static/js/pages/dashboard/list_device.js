function setIntervalAndExecute(fn, t) {
    fn();
    return(setInterval(fn, t));
}


$(function () {
    $('.list-device').DataTable({
        responsive: true,
    });

    setIntervalAndExecute(function () {
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
    }, 10000);
});

function getId(_device_id){
    document.device_id = _device_id;
}

$(document).on('opening', '.remodal', function () {
    var modal = $(this);
    let device_id = document.device_id;
    fetch('/dashboard/device/' + device_id).then(function (response) {
        response.json().then(function (data) {
            document.getElementById('id').value = device_id;
            document.getElementById('host').value = data.host;
            document.getElementById('host').focus();
            document.getElementById('port').value = data.port;
            document.getElementById('port').focus();
            document.getElementById('username').value = data.username;
            document.getElementById('username').focus();
            document.getElementById('password').value = data.password;
            document.getElementById('password').focus();
        })
    })
});
