"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment

from django.utils.translation import ugettext as _
from django.template import Context, Template

from .utils import render_template, xblock_field_list

import logging
log = logging.getLogger(__name__)

class IPythonNotebookXBlock(XBlock):
    """
    XBlock displaying an iPython Notebook link
    """

    # Fields are defined on the class. You can access them in your code as
    # self.<fieldname>.

    # URL format :
    # https://connect.inria.fr/ipythonExercice/CourseID/NotebookID.ipynb/UserID

    display_name = String(
        help=_("The name students see. This name appears in the course ribbon and as a header for the video."),
        display_name=_("Component Display Name"),
        default=_("New ipython notebook"),
        scope=Scope.settings
    )

    ipython_server_url = String(
        display_name=_("Server URL"),
        help=_("The URL of the IPython server. Don't forget the leading protocol (http:// or https://) and the path, without a trailing slash. https://yourserver.com is correct, for example."),
        default="https://connect.inria.fr",
        scope=Scope.settings
    )

    course_id = String(
        display_name=_("Course ID"),
        help=_("The ID of the course in IPython"),
        default="",
        scope=Scope.settings
    )

    notebook_id = String(
        display_name=_("Notebook ID"),
        help=_("The ID of the IPython notebook, without the trailing .ipynb"),
        default="",
        scope=Scope.settings
    )

    is_notebook_static = Boolean(
        help=_("A static notebook won't be edited by students."),
        display_name=_("Static notebook"),
        default=False,
        scope=Scope.settings
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        The primary view of the IPythonNotebookXBlock, shown to students
        when viewing courses.
        """

        student_id = self.xmodule_runtime.anonymous_student_id
        # student_id will be "student" if called from the Studio

        if self.is_notebook_static:
            notebook_url = "{0}/ipythonStaticNotebook/{1}/{2}.ipynb".format(self.ipython_server_url,
                                                                            self.course_id,
                                                                            self.notebook_id)
        else:
            notebook_url = "{0}/ipythonExercice/{1}/{2}.ipynb/{3}".format(self.ipython_server_url,
                                                                          self.course_id,
                                                                          self.notebook_id,
                                                                          student_id)

        context = {
            'self': self,
            'notebook_url': notebook_url,
            'is_in_studio': student_id == 'student'
        }

        frag = Fragment()
        frag.add_content(render_template('/templates/html/ipython.html', context))
        frag.add_css(self.resource_string("static/css/ipython.css"))
        frag.add_javascript(self.resource_string("static/js/src/ipython.js"))
        frag.add_javascript(self.resource_string("static/js/src/iframeResizer.min.js"))
        frag.initialize_js('IPythonNotebookXBlock')
        return frag

    def studio_view(self, context=None):
        """
        The studio view of the IPythonNotebookXBlock, with form
        """

        if self.course_id == "":
            self.course_id = self.location.course

        context = {
            'self': self,
            'fields': xblock_field_list(self, [ "ipython_server_url", "course_id", "notebook_id", "is_notebook_static" ])
        }

        frag = Fragment()
        frag.add_content(render_template('/templates/html/ipython-edit.html', context))
        frag.add_javascript(self.resource_string("static/js/src/ipython-edit.js"))
        frag.initialize_js('IPythonNotebookXBlock')
        return frag

    @XBlock.json_handler
    def studio_submit(self, submissions, suffix=''):
        if submissions['notebook_id']== "":
            response = {
                'result': 'error',
                'message': 'You should give a notebook ID'
            }
        elif submissions['ipython_server_url']== "":
            response = {
                'result': 'error',
                'message': 'You should give a server URL'
            }
        else:
            log.info(u'Received submissions: {}'.format(submissions))
            self.notebook_id = submissions['notebook_id']
            self.ipython_server_url = submissions['ipython_server_url']
            self.is_notebook_static = submissions['is_notebook_static']
            if submissions['course_id'] == '':
                self.course_id = self.location.course
            else:
                self.course_id = submissions['course_id']
            response = {
                'result': 'success',
            }
        return response

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("IPythonNotebookXBlock",
             """<vertical_demo>
                <ipython>
                </ipython>
                </vertical_demo>
             """),
        ]