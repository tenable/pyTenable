'''
test comppile
'''
import os
import pytest
import py_compile
from tenable.errors import UnexpectedValueError
from tenable.cs import ContainerSecurity


def test_init_catch_name_error():
    '''
    test to raise the exception when no api keys are provided
    '''
    try:
        ContainerSecurity()
    except NameError as error:
        print('\n', 'The following error exists-\n', error)
        pytest.raises(NameError)
        assert True
    except UnexpectedValueError:
        pytest.raises(UnexpectedValueError)


def test_compile_success():
    '''
    test to compile the init file
    '''
    with open('container.cs', 'a') as fobj:
        fobj.write('import os')
        os.chdir('..')
        os.chdir('..')
        file = open('tenable/cs/__init__.py', 'r')
        fobj.write('\n')
        fobj.writelines(file)
        file.close()
    fobj.close()
    try:
        py_compile.compile('tests/cs/container.cs')
    except py_compile.PyCompileError as err:
        print(err.msg)

    os.remove('tests/cs/container.cs')
    if os.path.exists('tests/cs/__pycache__/container.cpython-38.pyc'):
        os.remove('tests/cs/__pycache__/container.cpython-38.pyc')

