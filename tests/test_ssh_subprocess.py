
from __future__ import print_function

import unittest
import ssh_subprocess
import subprocess
import os
import sys
import tempfile
import shutil
import filecmp
import logging


def enable_debug():
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

#enable_debug()


class TestSshSubproces(unittest.TestCase):

    
    def setUp(self):
        self.s = ssh_subprocess.Ssh(host='localhost', user = os.environ['USER'], host_key_checking='no')

        
    def test_call(self):
        cmd = 'echo "Hello world" >/dev/null'
        self.assertEqual(self.s.call(cmd), subprocess.call(cmd, shell=True))

        cmd = 'exit 123'
        self.assertEqual(self.s.call(cmd), subprocess.call(cmd, shell=True))

        
    def test_check_call(self):
        cmd = 'echo "Hello world" >/dev/null'
        self.assertEqual(self.s.check_call(cmd), subprocess.check_call(cmd, shell=True))
        
        with self.assertRaises(subprocess.CalledProcessError) as cm:
            self.s.check_call('exit 123')
        e = cm.exception
        self.assertEqual(e.returncode, 123)

        
    def test_check_output(self):
        cmd = 'echo "Hello world"'
        self.assertEqual(self.s.check_output(cmd), subprocess.check_output(cmd, shell=True))


    def test_popen(self):
        p = self.s.popen('cat', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        out, err = p.communicate(b'Hello world!\n')
        self.assertEqual(out, b'Hello world!\n')
        p.wait()

        p = self.s.popen('echo hello >&2',
                         stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        self.assertEqual(err, b'hello\n')
        p.wait()
        


class TestSshFileTransfer(unittest.TestCase):
    

    def setUp(self):
        self.s = ssh_subprocess.Ssh(host='localhost', user=os.environ['USER'], host_key_checking='no')

        self.tmpdir1 = tempfile.mkdtemp(prefix='test-ssh-subprocess-')
        self.tmpdir2 = tempfile.mkdtemp(prefix='test-ssh-subprocess-')

        self.src_file1 = os.path.join(self.tmpdir1, 'src1.txt')
        self.dst_file1 = os.path.join(self.tmpdir1, 'dst1.txt')
        self.src_file2 = os.path.join(self.tmpdir1, 'src2.txt')
        self.dst_file2 = os.path.join(self.tmpdir1, 'dst2.txt')

        with open(self.src_file1, 'w') as f:
            f.write('Hello world 1!')
        with open(self.src_file2, 'w') as f:
            f.write('Hello world 2!')

        
    def tearDown(self):
        shutil.rmtree(self.tmpdir1)
        shutil.rmtree(self.tmpdir2)
            

    def test_upload(self):
        self.assertEqual(self.s.upload(self.src_file1, self.dst_file1), 0)
        self.assertTrue(filecmp.cmp(self.src_file1, self.dst_file1))
        
        self.assertEqual(self.s.upload(self.src_file1, '/non/existing/path/file'), 1)


    def test_download(self):
        self.assertEqual(self.s.download(self.src_file1, self.dst_file1), 0)
        self.assertTrue(filecmp.cmp(self.src_file1, self.dst_file1))

        self.assertEqual(self.s.download(self.src_file1, '/non/existing/path/file'), 1)


    def test_upload_recurse(self):
        self.assertEqual(self.s.upload(self.tmpdir1, self.tmpdir2, recursive=True), 0)
        self.assertTrue(filecmp.dircmp(self.tmpdir1, self.tmpdir2))
        

    def test_download_recurse(self):
        self.assertEqual(self.s.download(self.tmpdir1, self.tmpdir2, recursive=True), 0)
        self.assertTrue(filecmp.dircmp(self.tmpdir1, self.tmpdir2))

