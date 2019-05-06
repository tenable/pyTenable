from setuptools import setup, find_packages
import os

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
    version='0.3.18',
    description='Python library to interface into Tenable\'s products and applications',
    author='Tenable, Inc.',
    long_description=long_description,
    author_email='smcgrath@tenable.com',
    url='https://github.com/tenable/pytenable',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='tenable tenable_io securitycenter containersecurity',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'requests>=2.19',
        'python-dateutil>=2.6',
        'semver>=2.8.1',
    ],
    extras_require={
        'NessusReportv2': 'lxml>=4.1.1',
        'PWCertAuth': 'requests-pkcs12>=1.3',
    }
)