from setuptools import setup, find_packages
import os

with open('tenable/version.py', 'r') as vfile:
    exec(vfile.read())

try:
    long_description = open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'README.rst')).read()
except:
    long_description = 'Please refer to https://pytenable.readthedocs.io'
    print('! could not read README.rst file.')

setup(
    name='pyTenable',
    version=version,  # noqa
    description=('Python library to interface into Tenable\'s '
                 'products and applications'
                 ),
    author='Tenable, Inc.',
    long_description=long_description,
    author_email='smcgrath@tenable.com',
    url='https://github.com/tenable/pytenable',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='tenable tenable_io securitycenter containersecurity',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'requests>=2.26',
        'python-dateutil>=2.6',
        'semver>=2.8.1',
        'restfly>=1.4.5',
        'marshmallow>=3.6',
        'python-box>=4.0',
        'defusedxml>=0.5.0',
        'urllib3>=1.26.5',
        'typing-extensions>=4.0.1',
        'dataclasses>=0.8;python_version=="3.6"',
    ],
)
