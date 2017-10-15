
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# @author  Michael Cotterell
# @version 1.0
# @see     LICENSE (MIT style license file).
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from ipykernel.kernelbase import Kernel

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
        return lines[2]

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
    
    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):

        if not silent:
            for code_line in code.splitlines():
                self.child.sendline(code_line)
                self.child.expect(SCALA_PROMPT)
                child_output = self.child.before   # entire output
                lines = child_output.splitlines()  # breakup into lines
                for line in lines[2:len(lines)-1]: # ignore first two and last lines
                    stream_content = {'name': 'stdout', 'text': '{}\n'.format(line)}
                    self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
