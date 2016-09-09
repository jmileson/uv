import os.path
import jaydebeapi
from getpass import getpass
from argparse import ArgumentParser

driver = 'com.ibm.u2.jdbc.UniJDBCDriver'
conn_str = 'jdbc:ibm-u2://{host}:31438/{account};user={user};password={password}'
if os.path.isabs(__file__):
    root = os.path.dirname(os.path.dirname(__file__))
else:
    root = os.path.dirname(os.getcwd())
lib = os.path.join(root, 'lib')


def extract_name(cursor, meta):
    cursor._rs = meta
    cursor._meta = meta.getMetaData()
    res = cursor.fetchmany(25)
    return [r[3] for r in res]


def main(hostname, user, password):
    conn = jaydebeapi.connect(driver,
                              conn_str.format(host=hostname, account='ODBC', user=user, password=password),
                              [os.path.join(lib, 'unijdbc.jar'), os.path.join(lib, 'asjava.zip')])
    cursor = conn.cursor()

    table_meta = conn.jconn.getMetaData().getTables(None, None, '%', None)
    tables = extract_name(cursor, table_meta)

    column_meta = conn.jconn.getMetaData().getColumns(None, None, '%', None)
    extract_name(cursor, column_meta)


    print('complete')


if __name__ == '__main__':
    parser = ArgumentParser('UV - Perform querying tasks against UV, like a freaking pro')
    parser.add_argument('-o', '--hostname', metavar='hostname', help='hostname to connect')
    parser.add_argument('-u', '--user', metavar='user', help='username to connect as')

    args = parser.parse_args()

    if not args.hostname:
        args.hostname = input("Enter UV Hostname: ")

    if not args.user:
        args.user = input("Enter UV User Name: ")

    password = getpass("Enter password for {}: ".format(args.user))
    main(args.hostname, args.user, password)
