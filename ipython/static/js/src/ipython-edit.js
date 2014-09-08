 /* Javascript for IPythonNotebookXBlock. */
function IPythonNotebookXBlock(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
    
    $('.save-button', element).bind('click', function() {
        var data = {
            'ipython_server_url': $('#ipython_server_url').val(),
            'notebook_id': $('#notebook_id').val(),
            'course_id': $('#course_id').val(),
            'is_notebook_static': $('#is_notebook_static').is(':checked')
        };

        $.post(handlerUrl, JSON.stringify(data)).complete(function() {
            window.location.reload(false);
        });
    });

    $('.cancel-button', element).bind('click', function() {
        runtime.notify('cancel', {});
    });

    var update_url = function() {
        var url ;
        if ($('input[id=is_notebook_static]').is(":checked")) {
            url = $('input[id=ipython_server_url]').val() + '/ipythonStaticNotebook/' +
                  $('input[id=course_id]').val() + '/' +
                  $('input[id=notebook_id]').val() + '.ipynb';
        } else {
            url = $('input[id=ipython_server_url]').val() + '/ipythonExercice/' +
                  $('input[id=course_id]').val() + '/' +
                  $('input[id=notebook_id]').val() + '.ipynb/student';
        }
        $('a#notebook_url').html(url).attr('href', url);
    }

    $('#settings-tab input').on('input', function(){
        update_url();
    });
    $('#settings-tab input#is_notebook_static').on('change', function(){
        update_url();
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
        update_url();
    });

}