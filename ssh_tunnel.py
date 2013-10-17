#!/usr/bin/python

"""This starts an SSH tunnel to a given host. If the SSH process ever dies then
this script will detect that and restart it.""" 

import pexpect
import time
import os
import threading
from subprocess import Popen, PIPE, STDOUT

class TunnelThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True

    def stop_tunnel(self):
        self.running = False

    def start_tunnel(self):
        try:
            ssh_tunnel = pexpect.spawn(tunnel_command, timeout=4800)
            ssh_tunnel.expect ('password:')
            ssh_tunnel.sendline (X)
            time.sleep (2) # Cygwin is slow to update process status.

            p = Popen('ps -eo pid,lstart,cmd | grep "' + tunnel_command + '"', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
            output = p.stdout.read().split("\n")[0]
            command = "echo $'\nHTTP tunnel restarted, new processs info:\n%s' >> /path_to_log_file/ssh_tunnel_log" % output
            os.system(command)
            ssh_tunnel.expect(pexpect.EOF)
	 
        except Exception, e:
            command = "echo $'\nHTTP TIMEOUT reached at : ' %s >> /path_to_log_file/ssh_tunnel_log" % time.asctime()
            os.system(command)
      
    def run(self):  
        self.start_tunnel()
        threading.Thread.__init__(self) 	

tunnel_command = '/usr/bin/ssh -NnTxi /root/cie.if -R your_port:localhost:22 -l your_user your_domain.com'
host = 'your_domain.com'

#Credentials
user = 'your_user'
X = 'your_password'

def get_process_info ():

    # This seems to work on both Linux and BSD, but should otherwise be considered highly UNportable.
    ps = pexpect.run ('ps ax -O ppid')
    pass


def main ():

    t = TunnelThread()    

    while True:
        try:
            ps = pexpect.spawn ('nmap -p your_port your_domain.com')
            time.sleep(1)
            net_status = ps.expect (['closed','open'])

            ps = pexpect.spawn ('pgrep -f "%s"' % tunnel_command)
            time.sleep (0.1)
            ppid = ps.read()
            ps.close()

            if not ppid:
                time.sleep(3)
                t.start()

            elif net_status == 0 and ppid: 
                ps = pexpect.spawn ('pkill -9 -f "%s"' % tunnel_command)
                time.sleep(3)
                t = TunnelThread()
                t.start()

            time.sleep(2)
	   
        except pexpect.EOF:
            pass

	
if __name__ == '__main__':
    main ()


