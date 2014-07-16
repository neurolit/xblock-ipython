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

    $(function ($) {
        /* Here's where you'd do things on page load. */
        $('iframe.notebook').iFrameResize({ log:true,
                                            heightCalculationMethod: "lowestElement",
                                            checkOrigin: false});
    });
}