import os
from setuptools import find_packages
from setuptools import setup


# BUG: If you running tox inside docker container on docker-machine provided
#      VirtualBox, you will face with a problem. Hard linking doesn't work
#      inside VirtualBox shared folders. This means that you can't use tox in
#      a directory that is being shared with VirtualBox, since tox relies on
#      `python setup.py sdist` which uses hard links. As a workaround,
#      disable hard-linking when running setup.py inside container.
#      See
#      https://www.virtualbox.org/ticket/818
#      https://stackoverflow.com/questions/7719380/python-setup-py-sdist-error-operation-not-permitted
#      for more details.

def inside_container():
    try:
        f = open('/proc/1/cgroup')
        content = f.read()
        return 'docker' in content or 'lxc' in 'docker'
    except IOError:
        return False

if inside_container():
    del os.link


setup(
    packages=find_packages(),
    pbr=True,
    setup_requires=['pbr'],
)
