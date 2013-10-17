The http_tunnel.py and ssh_tunnel.py scripts are examples of http and ssh tunneling respectively using 
python and pexpect module for controlling and automating programs.

Scripts functionality and considerations:

	* Scripts run on background at server start signaled on /etc/rc.local file:
		- python /path_to_file/http_tunnel.py &
		- python /path_to_file/ssh_tunnel.py &

	* Scripts execute the following tunnel commands:
		- /usr/bin/ssh -NnTxi /root/cie.if -R your_port:localhost:22 -l your_user your_domain.com
		- /usr/bin/ssh -NnTxi /root/cie.if -R your_port:localhost:80 -l your_user your_domain.com &

	* Scripts watch over processes created by commands above. If execution is finished by any reason, 
	  the scripts will try to execute the tunnel command again.

Notes:
	* Tunnel commands can be interchanged by any other command that is appropriated for you.
	* localhost:22 corresponds to ssh port in local server
	* localhost:80 corresponds to http port in local server
	* Text "your_port" corresponds to remote server port for communication.