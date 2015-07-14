
# ssh-subprocess

[![Build Status](https://travis-ci.org/tsaarni/ssh-subprocess.svg?branch=master)](https://travis-ci.org/tsaarni/ssh-subprocess)

*ssh-subprocess* is a small Python module that provides
[subprocess](https://docs.python.org/2/library/subprocess.html) -like
API for executing commands remotely over SSH.  The module depends on
*OpenSSH* for the SSH functionality and requires non-interactive 
(e.g. public key) authentication. 

The module also supports SCP file transfer for uploading and
downloading files and directories.


### Tutorial


#### Prepare SSH connection

First establish connection towards remote server:

```python
import ssh_subprocess

ssh = ssh_subprocess.Ssh(host='hostname', user='joe', host_key_checking='no')
```


#### Run commands

To execute command:

```python
result = ssh.call('echo "Hello world!" > message')
```

just like `call()` in *subprocess*, `call()` in *ssh-subprocess*
returns the exit status of the command.  In this case it is the exit
status of `echo` command.  Also `check_call()` variant is
available. It raises `subprocess.CalledProcessError` in case of
non-zero exit status.

If you want to read the output printed by the remotely executed
command:

```python
message = ssh.check_output('cat message')
print message
```

This will print out the contents of the remote text file:

> Hello world!

Lastly, `popen()` allows also writing to `stdin` of remotely executed
command:

```python
p = ssh.popen('cat', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
out, err = p.communicate('Hello world!\n') # write 'Hello world!\n' to stdin of 'cat'
print out
```

See the documentation of
[subprocess](https://docs.python.org/2/library/subprocess.html) for
more information.


#### Transfer files

Files and directories can be uploaded and downloaded by using `upload()`
and `download()`:

```python
ssh.upload('myfile', '/tmp/myfile.txt')
ssh.download('/home/joe/myfiles', '.', recursive=True)
```
