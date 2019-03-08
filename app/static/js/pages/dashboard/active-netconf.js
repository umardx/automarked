// create the editor at container1 and container2
let req_container = document.getElementById("request");
let res_container = document.getElementById("response");
let options = {
    mode: 'tree'
};

let req_editor = new JSONEditor(req_container, options);
let res_editor = new JSONEditor(res_container, options);

let req_data = {};

let res_data = {};

function update_req_editor(req_data) {
    return req_editor.set(req_data);
}

function update_res_editor(res_data) {
    return res_editor.set(res_data);
}

function get_req_editor() {
    return req_editor.get();
}

$(function () {
    $(document).ready(function () {
        // Active netconf menu
        $("#netconf").addClass("active");

        let req_process;

        update_req_editor(req_data);
        update_res_editor(res_data);

        // initialize network configuration socket_io
        var nc_io = io.connect(document.location.protocol+'//'+document.location.host+'/nc');

        nc_io.on('receive', function(val) {
            console.info(JSON.stringify(val, null, 1));
        });

        nc_io.on('disconnect', function(){ });

        nc_io.on('render_req', function (val) {
            update_req_editor(val);
        });

        nc_io.on('render_res', function (val) {
            update_res_editor(val.data);
            console.info(JSON.stringify(val, null, 1));
            if (val.error) {
                toastr["error"](val.error.split('Error:').pop(), 'Operation failed!')
            } else {
                toastr["success"]('Operation success!')
            }
            $('#btnRequest').prop('disabled', false);
            if(!$("#progress").hasClass('hidden')) {
                $("#progress").addClass('hidden');
            }
        });

        $('#btnRequest').click(function () {
            let emit_data = {
                'device_id': $('#selectHost').val(),
                'operation': $('#selectOperation').val(),
                'model': $('#selectModel').val(),
                'data': get_req_editor()
            };
            nc_io.emit('render_res', emit_data);
            $('#btnRequest').prop('disabled', true);
            $("#progress").removeClass('hidden');
            clearTimeout(req_process).then(function () {
                req_process = setTimeout(function () {
                    $('#btnRequest').prop('disabled', false);
                    if(!$("#progress").hasClass('hidden')) {
                        toastr["error"]('Operation timout!')
                        $("#progress").addClass('hidden');
                    }
                }, 10000)
            });
        });

        $('#selectHost, #selectOperation, #selectModel').on('change', function () {
            if (
                $("#selectHost, #selectOperation, #selectModel")
                    .filter(function() { return $(this).val(); }).length > 2
            ) {
                $('#btnRequest').prop('disabled', false);
            } else {
                $('#btnRequest').prop('disabled', true);
            }

            if (
                $("#selectOperation, #selectModel")
                    .filter(function() { return $(this).val(); }).length > 1
            ) {
                let emit_data = {
                    'operation': $('#selectOperation').val(),
                    'model': $('#selectModel').val()
                };
                nc_io.emit('render_req', emit_data);
            }
        });

    });
});

