
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# @author  Michael Cotterell
# @see     LICENSE (MIT style license file).
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from ipykernel.kernelbase import Kernel
from .templates import *
from math import ceil

import os
import pexpect
import re

SCALATION_KERNEL_VERSION = '1.1.x'
SCALATION_KERNEL_AUTHORS = 'Michael E. Cotterell, John A. Miller'
SCALATION_KERNEL_LICENSE = 'MIT'

SCALATION_VERSION = '1.4'
SCALATION_JARS    = os.environ['SCALATION_JARS']

SCALA_EXEC        = 'scala'                  # scala executable
SCALA_PROMPT_MAIN = 'scala> '                # main prompt
SCALA_PROMPT_CONT = '     \| '               # continue prompt
SCALA_PROMPT      = [SCALA_PROMPT_MAIN,
                     SCALA_PROMPT_CONT]
SCALA_OPTIONS     = ['-Dscala.color',        # disable color
                     '-cp', SCALATION_JARS]  # add jars

HTML_PREFIX = '<scalation_kernel>:html:'
JSON_PREFIX = '<scalation_kernel>:json:'
TEXT_PREFIX = '<scalation_kernel>:text:'
IMAG_PREFIX = '<scalation_kernel>:imag:'  # images

CMD_PLOTV   = '::plotv'
CMD_PLOTM   = '::plotm'
CMD_PLOTF   = '::plotf'
CMD_PLOT3D  = '::plot3d'
CMD_DEBUG   = '::debug'
CMD_PRETTYR = '::relation'

class ScalaTionKernel(Kernel):
    """A Scala+ScalaTion kernel for Jupyter. It uses the system or container's 
    Scala installation for the underlying REPL. This implementation uses 
    ipykernel and pexpect to allow the kernel to easily interact with the REPL.
    """

    debug_mode = False
    implementation = 'scalation_kernel'
    implementation_version = '1.1.x'
    language = 'scala'
    language_info = {
        'name': 'scala',
        'mimetype': 'text/x-scala-source',
        'file_extension': '.scala'
    }

    @property
    def language_version(self):
        """Return the Scala version that the kernel is interacting with."""
        version_code = 'println(util.Properties.versionString.replaceFirst("version ", ""))'
        version = do_quick(version_code)
        return str(version)

    @property
    def banner(self):
        """Return the banner message."""
        banner_dict = { 'version': SCALATION_KERNEL_VERSION,
                        'authors': SCALATION_KERNEL_AUTHORS,
                        'license': SCALATION_KERNEL_LICENSE }
        banner_str  = self.render_template(banner_template, banner_dict)
        return banner_str

    def __init__(self, **kwargs):
        """Construct the kernel."""
        Kernel.__init__(self, **kwargs)
        self.child = pexpect.spawnu(SCALA_EXEC, SCALA_OPTIONS) # start scala
        self.child.expect(SCALA_PROMPT)                        # wait for prompt

    def render_template(self, template_name, template_dict):
        """Render a template using the given dictionary."""
        return template_name.render(**template_dict)

    def send_html_response(self, html_content):
        """Send an HTML response."""
        html = {
            'data': {
                'text/html': '{}'.format(html_content)
            },
            'metadata': {}
        }
        self.send_response(self.iopub_socket, 'display_data', html)

    def send_template_response(self, template_name, template_dict):
        """Send an HTML response using the given template and dictionary."""
        rendered = self.render_template(template_name, template_dict)
        self.send_html_response(rendered)
        
    def toggle_debug_mode(self):
        """Toggle whether or not the kernel sends additional debug responses."""
        self.debug_mode = not self.debug_mode
        toggle_debug_mode_dict = {'debug_mode': self.debug_mode }
        self.send_template_response(toggle_debug_mode_template, toggle_debug_mode_dict)

    def do_quick(self, code_line, evaluate = False):
        """Quickly execute a line using the underlying REPL and, if needed, 
           evaluate it as Python code.
        """
        self.send_debug_response("<code>do_quick</code> with <code>{}</code>".format(code_line))
        if isinstance(code_line, list):           # handle code list
            for line in code_line:                # handle each line in list
                self.child.sendline(line)         # send each line
                self.child.expect(SCALA_PROMPT)   # check for prompt
        else:                                     # handle single line
            self.child.sendline(code_line)        # send the line
            self.child.expect(SCALA_PROMPT)       # check for prompt
        nrows  = ceil(len(code_line) / 80)        # how many times is the input split by pexpect?
        output = self.child.before                # get entire output
        lines  = output.splitlines()              # breakup into lines
        lines  = lines[nrows:-1]                  # ignore input lines and last line
        lines = '\n'.join(lines)                  # rejoin lines
        if evaluate:
            return self.do_ast_eval(lines)
        else:
            return lines
        
    def send_prettyr_response(self, relation):
        """Send a response with a prettier version of a ``Relation``."""
        self.send_debug_response("building a prettier relation for <code>{}</code>".format(relation))
        prettyr_dict = { 'name':     self.do_quick('println({}.name)'.format(relation)),
                         'colNames': self.do_quick('println({}.colName.mkString("[\'", "\',\'", "\']"))'.format(relation), True),
                         'data':     self.do_quick(['println((0 until {0}.rows).map({0}.row(_)'.format(relation), 
                                                    '.mkString("[\'", "\',\'", "\']"))',
                                                    '.mkString("[", ",", "]"))'.format(relation)], True) }
        self.send_template_response(prettyr_template, prettyr_dict)

    def do_ast_eval(self, expression):
        """Evaluate an expression as Python code."""
        import ast
        try:
            return ast.literal_eval(expression)
        except Exception as e:
            debug_message = "problem calling <code>ast.literal_eval</code> with <code>{}</code>. {}".format(expression, str(e))
            self.send_debug_response(debug_message)
            return None

    def send_plot3d_response(self, plot_args):

        self.send_debug_response("building a plot3d (matrix plot)")

        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import pyplot
        pyplot.switch_backend('agg')
        
        from io import BytesIO
        import argparse, ast, base64, shlex
        import numpy as np
        
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('x')
        parser.add_argument('y')
        parser.add_argument('z')
        parser.add_argument('--title')
        parser.add_argument('//')
        parser.add_argument('/*')
        parser.add_argument('*/')
        
        args    = parser.parse_args(shlex.split(plot_args))
        figfile = BytesIO()

        if args.title != None:
            pyplot.title(args.title)

        x = self.do_quick('println({}().mkString("[", ",", "]"))'.format(args.x), True)
#        x = [x] * len(x)
        x = np.array(x)
        
        y = self.do_quick('println({}().mkString("[", ",", "]"))'.format(args.y), True)
 #       y = [y] * len(y)
        y = np.array(y)

        x, y = np.meshgrid(x, y)
        
        z = self.do_quick('println({}().map(_.mkString("[", ",", "]")).mkString("[", ",", "]"))'.format(args.z), True)
        z = np.array(z)

        fig  = pyplot.figure()
        ax   = fig.gca(projection='3d')
        surf = ax.plot_surface(x, y, z)

        pyplot.savefig(figfile, format='png')
        pyplot.clf()
        figfile.seek(0)        
        figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8')
        self.send_image_response("data:image/png;base64,{}".format(figdata_png))
        
    def send_plotm_response(self, plot_args):
        """Generate a plot with ``matplotlib`` using-specified ScalaTion matrices
           and options, converts it to PNG format, and sends it back to the
           notebook as a templated response.
        """

        self.send_debug_response("building a plotm (matrix plot)")

        from matplotlib import pyplot
        pyplot.switch_backend('agg')
        
        from io import BytesIO
        import argparse, ast, base64, shlex
        
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('matrices', metavar='M', nargs='+')
        parser.add_argument('--title')
        parser.add_argument('--xlabel')
        parser.add_argument('--ylabel')
        parser.add_argument('--axis')
        parser.add_argument('--//')
        parser.add_argument('--/*')
        parser.add_argument('--*/')
        
        args    = parser.parse_args(shlex.split(plot_args))
        figfile = BytesIO()

        if args.title != None:
            pyplot.title(args.title)

        if args.xlabel != None:
            pyplot.xlabel(args.xlabel)

        if args.ylabel != None:
            pyplot.ylabel(args.ylabel)

        if args.axis != None:            
            pyplot.axis(args.axis)
            
        for mat in args.matrices:
            self.send_debug_response("building a plotm for <code>{}</code>".format(mat))
            dim2 = self.do_quick('println({}.dim2)'.format(mat), True)
            for col in range(0, dim2):
                self.send_debug_response("building column <code>{}</code> for <code>{}</code>".format(col, mat))
                col_data = self.do_quick('println({}.col({})().mkString("[", ",", "]"))'.format(mat, col), True)
                pyplot.plot(col_data)

        pyplot.savefig(figfile, format='png')
        pyplot.clf()
        figfile.seek(0)        
        figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8')
        self.send_image_response("data:image/png;base64,{}".format(figdata_png))
        
    def send_plotv_response(self, plot_args):
        """Generate a plot with ``matplotlib`` using-specified ScalaTion vectors
           and options, converts it to PNG format, and sends it back to the
           notebook as a templated response.

        NOTE:
            With the current implementation, an ``argparse`` exception may cause
            the kernel to restart. If this happens, the user must re-evaluate
            past cells in the notebook. A solution is being considered for the
            next major release.

        TODO:
            Current support is minimal. Ideally, we would like to support all or
            most plot types provided by ``matplotlib``.
        """

        self.send_debug_response("building a plotv (vector plot)")

        from matplotlib import pyplot
        pyplot.switch_backend('agg')
        
        from io import BytesIO
        import argparse, ast, base64, shlex
        import numpy as np        
        
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('vectors', metavar='VectorD', nargs='+', help='a ScalaTion vector')
        parser.add_argument('--title', help='plot title')
        parser.add_argument('--xlabel', help='x-axis label')
        parser.add_argument('--ylabel', help='y-axis label')
        parser.add_argument('--axis')
        parser.add_argument('--bar', action='store_false', default=None)
        parser.add_argument('--xkcd', action='store_false', default=None)
        parser.add_argument('--scatter', action='store_false', default=None)
        
        args    = parser.parse_args(shlex.split(plot_args))
        figfile = BytesIO()

        if args.title != None:
            pyplot.title(args.title)

        if args.xlabel != None:
            pyplot.xlabel(args.xlabel)

        if args.ylabel != None:
            pyplot.ylabel(args.ylabel)

        if args.axis != None:
            
            pyplot.axis(args.axis)
            
        for v in args.vectors:
            y = self.do_quick('println({}().mkString("[", ",", "]"))'.format(v), True)
            x = np.arange(len(y))
            vec = self.do_quick('println({}().mkString("[", ",", "]"))'.format(v), True)
        
        if args.xkcd != None:
            with pyplot.xkcd():
                fig1 = pyplot.figure()
                pyplot.plot(vec)

        if (args.xkcd != None) & (args.scatter != None):
            with pyplot.xkcd():
                fig1 = pyplot.figure()
                pyplot.scatter(x,y)

        if (args.xkcd != None) & (args.bar != None):
            with pyplot.xkcd():
                fig2 = pyplot.figure()
                pyplot.bar(x,y)

        if args.scatter != None:
            pyplot.scatter(x,y)
        if args.bar != None:
            pyplot.bar(x,y)
        else:
            pyplot.plot(vec)

        pyplot.savefig(figfile, format='png')
        pyplot.clf()
        figfile.seek(0)        
        figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8')
        self.send_image_response("data:image/png;base64,{}".format(figdata_png))

    def send_json_response(self, json_content):
        """Send a JSON response."""
        html = {
            'data': {
                'text/json': '{}'.format(json_content)
            },
            'metadata': {}
        }
        self.send_response(self.iopub_socket, 'display_data', html)
        
    def send_image_response(self, image_content):
        """Send an image response."""
        self.send_html_response('<img src="{}"/>'.format(image_content))

    def send_debug_response(self, debug_message):
        """If ``debug_mode`` is enabled, send a debug response."""
        if self.debug_mode:
            import datetime, time, inspect, uuid
            debug_stack = inspect.stack()[1:]
            debug_dict  = { 'timestamp': str(datetime.datetime.utcnow()),
                            'stack': debug_stack,
                            'message': debug_message,
                            'uuid': uuid.uuid4() }
            self.send_template_response(debug_template, debug_dict)
                
    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        """Execute user ``code``, one line at a time.

           If a line begins with a kernel-specific command (e.g., ```::plotv```,
           ```::debug_mode```, etc.), then it is executed immediately; 
           otherwise, the kefrnel assumes that the line contains Scala code and 
           sends it to the Scala REPL via the kernel's ``pexepct.spawnu`` 
           instance. As output is returned, the kernel searches for 
           kernel-specific output prefixes, and if found, parses the output 
           appropriately using corresponding templates before sending the 
           response; otherwise, all of the output it returned as is.

           TODO:
               Currently, the ``silent`` parameter does not function as
               described by ``ipykernel.kernelbase.Kernel``. We intend to fix
               this in the next minor release (which is 1.2).
        """

        if not silent:
            for code_line in code.splitlines():

                self.send_debug_response("executing line: <code>{}</code>".format(code_line))

                if code_line.startswith(CMD_DEBUG):
                    self.toggle_debug_mode()

                elif code_line.startswith(CMD_PRETTYR):
                    self.send_prettyr_response(code_line[len(CMD_PRETTYR):].strip())
                    
                elif code_line.startswith(CMD_PLOTV):
                    self.send_plotv_response(code_line[len(CMD_PLOTV):])

                elif code_line.startswith(CMD_PLOTM):
                    self.send_plotm_response(code_line[len(CMD_PLOTM):])

                elif code_line.startswith(CMD_PLOT3D):
                    self.send_plot3d_response(code_line[len(CMD_PLOT3D):])

                else:
                
                    self.child.sendline(code_line)                # send the line
                    nrows  = ceil(len(code_line) / 80)            # how many times is the input split by pexpect?
                    prompt = self.child.expect(SCALA_PROMPT)      # check for prompt
                    if SCALA_PROMPT[prompt] == SCALA_PROMPT_MAIN: # back to the main prompt?
                        output = self.child.before                # get entire output
                        lines  = output.splitlines()              # breakup into lines
                        lines  = lines[nrows:-1]                  # ignore input lines and last line
                        if len(lines) > 0:                        # more than one line in output?
                            if lines[0].startswith(IMAG_PREFIX):
                                lines = '\n'.join(lines) + '\n'   # rejoin lines
                                lines = lines[len(IMAG_PREFIX):]  # strip prefix
                                self.send_image_response(lines)
                            elif lines[0].startswith(HTML_PREFIX):  
                                lines = '\n'.join(lines) + '\n'   # rejoin lines
                                lines = lines[len(HTML_PREFIX):]  # strip prefix
                                self.send_html_response(lines)
                            elif lines[0].startswith(JSON_PREFIX):                            
                                lines = '\n'.join(lines) + '\n'   # rejoin lines
                                lines = lines[len(JSON_PREFIX):]  # strip prefix
                                self.send_json_response(lines)
                            else:
                                lines = '\n'.join(lines) + '\n'   # rejoin lines
                                stream_content = {'name': 'stdout', 'text': '{}'.format(lines)}
                                self.send_response(self.iopub_socket, 'stream', stream_content)
                                        
        return { 'status': 'ok',
                 'execution_count': self.execution_count,
                 'payload': [],
                 'user_expressions': {} }

    
