import paramiko
import os

NODES = ['192.168.1.200','192.168.1.217','192.168.1.229']
names = {'192.168.1.153': 'tylersdurden',
         '192.168.1.200': 'root',
         '192.168.1.217': 'pi',
         '192.168.1.229': 'pi'}


def swap(fname,destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def initialize(peers):
    os.system('ifconfig | grep inet | grep netmask | grep broadcast | cut -b 14-28 >> ip.txt')
    my_ip = swap('ip.txt', True).pop().replace('\n', '')

    my_p = int(my_ip.replace('.', ''))
    for peer in peers:
        try:
            p = int(peer.replace('.', ''))
            if my_p == p:
                peers.remove(peer)
        except ValueError:
            pass
    return my_ip, peers


def get_creds(peer):
        os.system('cp KEYS/' + peer.replace('.', '') + '.txt encrypted.txt')
        os.system('cp KEYS/' + peer.replace('.', '') + '.key key.txt')
        os.system('python aes.py -d >> data.txt; rm encrypted.txt key.txt')
        pw = swap('data.txt', True).pop().split('Result: ')[1].replace(' ', '')
        uname = names[peer]
        return uname, pw


def ssh_command(ip, user, passwd, command, verbose):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    response = ''
    try:
        client.connect(ip, username=user, password=passwd)
        ssh_session = client.get_transport().open_session()
        response = ''
        if ssh_session.active:
            ssh_session.exec_command(command)
            if verbose:
                response = ssh_session.recv(1024)
                print '%s@%s:~$ %s [Executed]' % (user, ip, command)
                print '%s@%s:~$ %s' % (user, ip, response)
                return response

    except paramiko.ssh_exception.NoValidConnectionsError:
        print "Could not connect to %s" % ip
    return response