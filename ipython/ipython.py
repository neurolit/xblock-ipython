"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

from django.utils.translation import ugettext as _
from django.template import Context, Template

from .utils import render_template

import logging
log = logging.getLogger(__name__)

class IPythonNotebookXBlock(XBlock):
    """
    XBlock displaying an iPython Notebook link
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # URL format :
    # https://connect.inria.fr/ipythonExercice/CourseID/NotebookID.ipynb/UserID

    ipython_server_url = String(
        help=_("The URL IPython server"),
        display_name=_("IPython server URL"),
        default="https://connect.inria.fr",
        scope=Scope.settings
    )

    notebook_id = String(
        help=_("The ID of the IPython notebook"),
        display_name=_("Notebook ID"),
        default="",
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

        try:
            student_id = self.runtime.anonymous_student_id
        except AttributeError:
            # This a displayed in the studio
            student_id = "AnonymousStudentID"

        course_id = self.location.course

        context = {
            'self': self,
            'notebook_url': self.ipython_server_url + "/ipythonExercice/" + course_id + "/" + self.notebook_id + ".ipynb/" + student_id
        }

        frag = Fragment()
        frag.add_content(render_template('/templates/html/ipython.html', context))
        frag.add_css(self.resource_string("static/css/ipython.css"))
        frag.add_javascript(self.resource_string("static/js/src/ipython.js"))
        frag.initialize_js('IPythonNotebookXBlock')
        return frag

    def studio_view(self, context=None):
        """
        The studio view of the IPythonNotebookXBlock, with form
        """
        context = {
            'self': self
        }

        frag = Fragment()
        frag.add_content(render_template('/templates/html/ipython-studio.html', context))
        frag.add_css(self.resource_string("static/css/ipython.css"))
        frag.add_javascript(self.resource_string("static/js/src/ipython.js"))
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