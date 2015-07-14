#!/usr/bin/env python
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

from setuptools import setup

setup(name             = 'ssh-subprocess',
      version          = '0.1.0',
      description      = 'subprocess-like execution of commands remotely over SSH',
      long_description = open('README.md').read(),
      author           = 'Tero Saarni',
      author_email     = 'tero.saarni@gmail.com',
      url              = 'https://github.com/tsaarni',
      py_modules       = [ 'ssh_subprocess' ],
      test_suite       = 'tests',
  )
