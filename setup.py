from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()    

setup(
    name='scalation_kernel',
    version='1.1.12',
    packages=['scalation_kernel'],
    description='ScalaTion kernel for Jupyter',
    long_description=readme,
    author='Michael E. Cotterell',
    author_email='mepcott@uga.edu',
    url='https://github.com/scalation/scalation_kernel',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Education',        
        'Framework :: Jupyter',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
    ],
    install_requires=[
        'ipykernel',
        'pexpect',
        'mako',
        'matplotlib',
    ],
    keywords='jupyter kernel scala scalation',
)
