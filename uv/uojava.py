import jpype
import os.path
from getpass import getpass


# ensure that the uniobjects package in included in the jvm
if os.path.isabs(__file__):
    root = os.path.dirname(os.path.dirname(__file__))
else:
    root = os.path.dirname(os.getcwd())
lib = os.path.join(root, 'lib')
ou = os.path.join(lib, 'asjava.zip')
default_jvm = jpype.get_default_jvm_path()
jpype.startJVM(default_jvm, '-Djava.class.path={}'.format(ou))

passwd = getpass()
UniSession = jpype.JPackage('asjava').uniobjects.UniSession
sess = UniSession()
try:
    sess.connect('jssrhl2', 'jmileson', passwd, 'JSS')
    parts = sess.openFile('PARTS')
    data = parts.read('010G.11')
    prov = sess.dynArray(data)
finally:
    sess.disconnect()
    jpype.shutdownJVM()
print('Complete')