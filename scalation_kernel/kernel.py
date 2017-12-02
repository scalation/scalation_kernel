
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# @author  Michael Cotterell
# @version 1.0.1
# @see     LICENSE (MIT style license file).
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from ipykernel.kernelbase import Kernel
from .templates import *
from math import ceil

import os
import pexpect
import re

SCALATION_KERNEL_VERSION = '1.0.1'
SCALATION_KERNEL_AUTHORS = 'Michael E. Cotterell, John A. Miller'
SCALATION_KERNEL_LICENSE = 'MIT'

SCALATION_VERSION = '1.3'
SCALATION_JARS    = ':'.join([os.environ['SCALATION_MATHSTAT_JAR'],
                              os.environ['SCALATION_MODELING_JAR']])

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

CMD_CHARTS  = ':charts'
CMD_PLOTV   = ':plotv'
CMD_PLOTM   = ':plotv'
CMD_PLOTF   = ':plotv'

class ScalaTionKernel(Kernel):
    """A Scala+ScalaTion kernel for Jupyter. It uses the system or container's 
    Scala installation for the underlying REPL. This implementation uses 
    ipykernel and pexpect to allow the kernel to easily interact with the REPL.
    """

    implementation = 'scalation'
    implementation_version = '1.0.1'
    language = 'scala'
    language_info = {
        'name': 'scala',
        'mimetype': 'text/x-scala-source',
        'file_extension': '.scala',
    }

    @property
    def language_version(self):
        return '2.12.4'
#        code = 'println(util.Properties.versionString.replaceFirst("version ", ""))'
#        self.child.sendline(code)
#        self.child.expect(SCALA_PROMPT)
#        child_output = self.child.before
#        lines = child_output.splitlines()
#        return lines[1]

    @property
    def banner(self):
        banner_str  = 'ScalaTion Kernel {}\nAuthors: {}\nLicense: {}'
        return banner_str.format(SCALATION_KERNEL_VERSION,
                                 SCALATION_KERNEL_AUTHORS,
                                 SCALATION_KERNEL_LICENSE)

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.child = pexpect.spawnu(SCALA_EXEC, SCALA_OPTIONS) # start 
        self.child.expect(SCALA_PROMPT)

    def render_template(self, template_name, template_dict):
        """Render a template using the given dictionary."""
        return template_name.render(**template_dict)

    def send_chart_setup_response(self):
        from matplotlib import pyplot
        from io import BytesIO
        import base64

        figfile = BytesIO()
        pyplot.plot([1, 2, 3, 4])
        pyplot.plot([1, 4, 9, 16])
        pyplot.savefig(figfile, format='png')
        figfile.seek(0)        
        figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8')
        self.send_image_response("data:image/png;base64,{}".format(figdata_png))
        
#        html_content = '\n'.join(['<script src="//cdnjs.cloudflare.com/ajax/libs/require.js/2.3.5/require.min.js"></script>',
#                                  '<script src="//cdn.plot.ly/plotly-latest.min.js" charset="utf-8"></script>'])
#        self.send_html_response(html_content)

    def send_plotv_response(self, plot_args):

        from matplotlib import pyplot
        from io import BytesIO
        import argparse, ast, base64, shlex
        
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('vectors', metavar='V', nargs='+')
        parser.add_argument('--title')
        parser.add_argument('--xlabel')
        parser.add_argument('--ylabel')
        parser.add_argument('--style')
#        args    = parser.parse_args(plot_args.split())
        args    = parser.parse_args(shlex.split(plot_args))
        figfile = BytesIO()

        if args.title != None:
            pyplot.title(args.title)

        if args.xlabel != None:
            pyplot.xlabel(args.xlabel)

        if args.ylabel != None:
            pyplot.ylabel(args.ylabel)

        for v in args.vectors:
            code_line = 'println({}().mkString("[", ",", "]"))'.format(v)
            self.child.sendline(code_line)            # send the line
            nrows  = ceil(len(code_line) / 80)        # how many times is the input split by pexpect?
            prompt = self.child.expect(SCALA_PROMPT)  # check for prompt
            output = self.child.before                # get entire output
            lines  = output.splitlines()              # breakup into lines
            lines  = lines[nrows:-1]                  # ignore input lines and last line
            if len(lines) > 0:                        # more than one line in output?
                lines = '\n'.join(lines) + '\n'       # rejoin lines
                vec   = ast.literal_eval(lines)
                pyplot.plot(vec)

        pyplot.savefig(figfile, format='png')
        pyplot.clf()
        figfile.seek(0)        
        figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8')
        self.send_image_response("data:image/png;base64,{}".format(figdata_png))

    def send_html_response(self, html_content):
        """Send an HTML response."""
        html = {
            'data': {
                'text/html': '{}'.format(html_content)
            },
            'metadata': {}
        }
        self.send_response(self.iopub_socket, 'display_data', html)

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
        self.send_html_response("<p><strong>SCALATION_KERNEL_DEBUG:</strong></p><pre><code>{}</code></pre>".format(debug_message))

    def send_template_response(self, template_name, template_dict):
        """Send an HTML response using the given template and dictionary."""
        rendered = self.render_template(template_name, template_dict)
        self.send_html_response(rendered)

    def send_pretty_response(self, line):
        """Send a pretty response for supported REPL outputs."""
        # TODO finish

        regex   = r"^(.*)(?:\:\s)(.*)(?:\s=\s*)([\s\S]*)"
        matches = re.findall(regex, line)

        if len(matches) == 1:
            var_name, var_type, var_value = matches[0]
            info_dict = {'name': var_name,
                         'type': var_type,
                         'value': var_value}

            if var_type.startswith('scalation.linalgebra.Vec'):
                vector_regex = regex = r"(\d+\.\d+)(?:,?)"
                vector_elems = re.findall(vector_regex, var_value)
                vector_dict  = {'name': var_name,
                                'elems': vector_elems}
                self.send_template_response(vector_template, vector_dict)
            else:
                self.send_template_response(info_template, info_dict)
                
    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):

        if not silent:
            for code_line in code.splitlines():

#                self.send_debug_response("sendline --> {}\n".format(code_line))

                # enabling charts?
                if code_line.startswith(CMD_CHARTS):
                    self.send_debug_response("trying to enable charts!")
                    self.send_chart_setup_response()

                elif code_line.startswith(CMD_PLOTV):
                    self.send_debug_response("trying to send a plotv!")
                    self.send_plotv_response(code_line[len(CMD_PLOTV):])

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
                                
#                lines = lines[1:len(lines)]         # ignore first two and last lines
#                lines = '\n'.join(lines)             # rejoin the lines
#                stream_content = {'name': 'stdout', 'text': '{}'.format(lines)}
            #    self.send_response(self.iopub_socket, 'stream', stream_content)

#                if lines.startswith('scalation_kernel_html>'):
#                    lines = lines[len('scalation_kernel_html'):]
#                    self.send_html_response(lines)
#                if lines.startswith('res'):          # scala result
#                    self.send_pretty_response(lines) # pretty print result
#                elif not lines.startswith('import'): # echo back unless import
#                    self.send_html_response('<pre style="font-size: small; display: flex; white-space: normal; word-break: break-word;"><code>{}</code></pre>'.format(lines))

#                    self.send_response(self.iopub_socket, 'stream', stream_content)
#                    regex   = r"^(.*)(?:\:\s)(.*)"
#                    matches = re.findall(regex, lines)
#                    if len(matches) == 0:
#                        self.send_response(self.iopub_socket, 'stream', stream_content)
        
        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }

    
