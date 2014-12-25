from setuptools import setup

setup(
    name='plyj',
    version='0.2-dev',
    author='Werner Hahn',
    author_email='werner_hahn@gmx.com',
    packages=['plyj'],
    url='http://github.com/musiKk/plyj',
    license='COPYING',
    description='A Java parser written in Python using PLY. ',
    long_description=open('README.md').read(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing'
    ],
    install_requires=[
        "ply >= 3.4",
    ],
    test_suite='test'
)
