/* Javascript for IPythonNotebookXBlock. */
function IPythonNotebookXBlock(runtime, element) {
    $('iframe.notebook').iFrameResize({ log: false,
                                        heightCalculationMethod: "lowestElement",
                                        checkOrigin: false });
    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}