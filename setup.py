from setuptools import setup

setup(
    name='plyj',
    version='0.0.1',
    author='Werner Hahn',
    author_email='werner_hahn@gmx.com',
    packages=['plyj'],
    url='http://github.com/musiKk/plyj',
    license='COPYING',
    description='A Java parser written in Python using PLY. ',
    long_description=open('README.md').read(),
    install_requires=[
        "ply >= 3.4",
    ],
)
