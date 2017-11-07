
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# @author  Michael Cotterell
# @version 1.0
# @see     LICENSE (MIT style license file).
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from ipykernel.kernelbase import Kernel
from .templates import *

import os
import pexpect
import re

SCALATION_KERNEL_VERSION = '1.0'
SCALATION_KERNEL_AUTHORS = 'Michael E. Cotterell, John A. Miller'
SCALATION_KERNEL_LICENSE = 'MIT'

SCALATION_VERSION = '1.3'
SCALATION_JARS    = ':'.join([os.environ['SCALATION_MATHSTAT_JAR'],
                              os.environ['SCALATION_MODELING_JAR']])

SCALA_PROMPT  = 'scala> '
SCALA_OPTIONS = ['-Dscala.color',
                 '-cp', SCALATION_JARS]

class ScalaTionKernel(Kernel):
    """A Scala+ScalaTion kernel for Jupyter. It uses the system or container's 
    Scala installation for the underlying REPL. This implementation uses 
    ipykernel and pexpect to allow the kernel to easily interact with the REPL.
    """

    implementation = 'scalation'
    implementation_version = '1.0'
    language = 'scala'
    language_info = {
        'name': 'scala',
        'mimetype': 'text/x-scala-source',
        'file_extension': '.scala',
    }

    @property
    def language_version(self):
        code = 'println(util.Properties.versionString.replaceFirst("version ", ""))'
        self.child.sendline(code)
        self.child.expect(SCALA_PROMPT)
        child_output = self.child.before
        lines = child_output.splitlines()
        return lines[1]

    @property
    def banner(self):
        banner_str  = 'ScalaTion Kernel {} (Scala {} + ScalaTion {})\nAuthors: {}\nLicense: {}'
        return banner_str.format(SCALATION_KERNEL_VERSION,
                                 self.language_version,
                                 SCALATION_VERSION,
                                 SCALATION_KERNEL_AUTHORS,
                                 SCALATION_KERNEL_LICENSE)

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.child = pexpect.spawnu('scala', SCALA_OPTIONS)
        self.child.expect(SCALA_PROMPT)

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
                self.child.sendline(code_line)
                self.child.expect(SCALA_PROMPT)
                child_output = self.child.before     # entire output
                lines = child_output.splitlines()    # breakup into lines
                lines = lines[1:len(lines)]          # ignore first two and last lines
                lines = '\n'.join(lines)             # rejoin the lines
                stream_content = {'name': 'stdout', 'text': '{}\n'.format(lines)}
 #               self.send_response(self.iopub_socket, 'stream', stream_content)
                if lines.startswith('res'):          # scala result
                    self.send_pretty_response(lines) # pretty print result
                elif not lines.startswith('import'): # echo back unless import
                    self.send_html_response('<pre style="font-size: small; display: flex; white-space: normal; word-break: break-word;"><code>{}</code></pre>'.format(lines))
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
