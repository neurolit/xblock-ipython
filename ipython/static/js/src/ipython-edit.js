 /* Javascript for IPythonNotebookXBlock. */
function IPythonNotebookXBlock(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
    
    $('.save-button', element).bind('click', function() {
        var data = {
            'ipython_server_url': $('#ipython_server_url').val(),
            'notebook_id': $('#notebook_id').val(),
            'course_id': $('#course_id').val()
        };

        $.post(handlerUrl, JSON.stringify(data)).complete(function() {
            window.location.reload(false);
        });
    });

    $('.cancel-button', element).bind('click', function() {
        runtime.notify('cancel', {});
    });

    var update_url = function() {
        var url = $('input[id=ipython_server_url]').val() + '/' +
                  $('input[id=course_id]').val() + '/' +
                  $('input[id=notebook_id]').val() + '.ipynb/student';
        $('a#notebook_url').html(url).attr('href', url);
    }

    $('#settings-tab input').on('input', function(){
        update_url();
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
        update_url();
    });

}