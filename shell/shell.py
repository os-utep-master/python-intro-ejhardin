#! /usr/bin/env python3

import os, sys, time, re
import fileinput

pid = os.getpid()
prompt = ""
try:
    prompt = os.environ['PS1']
except:
    prompt = "$ "

while True:
    inputs = input(prompt)
    args = re.split(" ", inputs) #["wc", "p3-exec.py"]

    if args[0] == "exit":
        os.write(2, ("Exiting...\n").encode())
        sys.exit(0)

    elif args[0] == "cd":
        try:
            os.chdir(args[1])
        except:
            os.write(2,("Could not change directory\n").encode())

    else:
        os.write(2, ("About to fork (pid:%d)\n" % pid).encode())
        rc = os.fork()

        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
    
        elif rc == 0:                   # child
            os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % (os.getpid(), pid)).encode())

            if args[0].startswith("./") or args[0].startswith("/"):
                try:
                    os.execve(args[0], args, os.environ) # try to exec program
                except FileNotFoundError:             # ...expected
                    pass                              # ...fail quietly
            else:
                for dir in re.split(":", os.environ['PATH']): # try each directory in the path
                    program = "%s/%s" % (dir, args[0])
                    os.write(2, ("Child:  ...trying to exec %s\n" % program).encode())
                    try:
                        os.execve(program, args, os.environ) # try to exec program
                    except FileNotFoundError:             # ...expected
                        pass                              # ...fail quietly

            os.write(2, ("Child:    %s: Command not found\n" % args[0]).encode())
            sys.exit(1)                 # terminate with error

        else:                           # parent (forked ok)
            os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                         (pid, rc)).encode())
            childPidCode = os.wait()
            childExitCode = (int)(childPidCode[1]) / 256
            childPidCode = (childPidCode[0], childExitCode)
            os.write(2, ("Parent: Child %d terminated with exit code %d\n" % 
                         childPidCode).encode())
	
