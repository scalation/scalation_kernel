from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='scalation_kernel',
    version='1.0',
    packages=['scalation_kernel'],
    description='ScalaTion kernel for Jupyter',
    long_description=readme,
    author='Michael E. Cotterell',
    author_email='mepcott@uga.edu',
    url='https://github.com/scalation/scalation_kernel',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'ipykernel',
        'pexpect',
        'mako',
    ],
)
