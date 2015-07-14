#
# Copyright 2015 tero.saarni@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#
# Known problems:
#
#   - stderr is left open by master process
#
#     for further information, see
#     https://lists.mindrot.org/pipermail/openssh-unix-dev/2014-January/031975.html
#     https://code.google.com/p/parallel-ssh/issues/detail?id=67
#     https://bugzilla.mindrot.org/show_bug.cgi?id=1988
#

from __future__ import print_function

import subprocess
import os
import logging

logger = logging.getLogger(__name__)

SSH_CONTROL_SOCKET_PATH = '.ssh-control-sock-%r@%h:%p' 

    

class Ssh(object):

    def __init__(self, host, *args, **kwargs):
        self.host = host
        self.args = [ '-o', 'ControlMaster=auto',
                      '-o', 'ControlPath=%s' % SSH_CONTROL_SOCKET_PATH,
                      '-o', 'ControlPersist=3s' ]

        options = { 'user'              : ['-o', 'User={}'],
                    'port'              : ['-o', 'Port={}'],
                    'host_key_checking' : ['-o', 'StrictHostKeyChecking={}'],
                    'private_key_file'  : ['-o', 'IdentityFile={}'],
                    'config_file'       : ['-F', '{}'],
                    'subsystem'         : ['-s', '{}'] }
        
        for k, v in kwargs.items():
            if k in options:
                self.args += [ arg.format(v) for arg in options[k] ]

        
    def _ssh_args(self, args):
        if isinstance(args, list):
            sshargs = ['/usr/bin/ssh', '{self.host}'.format(self=self)]
            sshargs += self.args + [ '-E', '/dev/null' ]
            sshargs += [' '.join(args)]
        elif isinstance(args, str):
            sshargs = '/usr/bin/ssh {strargs} {self.host} "{args}"'.format(
                self=self, strargs=' '.join(self.args), args=args)
            
        logging.info(sshargs)
        return sshargs

        
    def popen(self, args, stdin=None, stdout=None, stderr=None, shell=True):
        return subprocess.Popen(self._ssh_args(args), shell=shell, close_fds=True,
                                stdin=stdin, stdout=stdout, stderr=stderr)

        
    def call(self, args):
        return subprocess.call(self._ssh_args(args), shell=True)

        
    def check_call(self, args):
        return subprocess.check_call(self._ssh_args(args), shell=True)


    def check_output(self, args):
        return subprocess.check_output(self._ssh_args(args), shell=True)
        
        
    def upload(self, localpath, remotepath='.', recursive=False):
        if recursive is True:
            args = self.args + ['-r']
        else:
            args = self.args

        args = '/usr/bin/scp {args} "{localpath}" "{host}:{remotepath}" >/dev/null'.format(
            host=self.host, args=' '.join(args), localpath=localpath, remotepath=remotepath)
        logging.info(args)
        return subprocess.call(args, shell=True)

        
    def download(self, remotepath, localpath='.', recursive=False):
        if recursive is True:
            args = self.args + ['-r']
        else:
            args = self.args

        args = '/usr/bin/scp {args} "{host}:{remotepath}" "{localpath}" >/dev/null'.format(
            host=self.host, args=' '.join(args), localpath=localpath, remotepath=remotepath)
        logging.info(args)
        return subprocess.call(args, shell=True)
        
        
