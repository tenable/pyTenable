from setuptools import setup, find_packages

setup(
    name='pyTenable',
    version='0.1.0',
    description='Python library to interface into Tenable\'s products and applications',
    long_description='For more info on pyTenable, please refer to the `documentation site <https://pytenable.readthedocs.io>`_',
    author='Tenable\, Inc.',
    author_email='smcgrath@tenable.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
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
    ],
    keywords='tenable tenable_io securitycenter containersecurity',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'requests>=2.19',
        'python-dateutil>=2.6',
        'lxml>=4.1.1'
    ],
)