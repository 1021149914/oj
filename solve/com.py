import time
import subprocess
dir_work='./'

def compile(language):
    build_cmd={
        "g++":"g++ main.cpp -o2 -Wall -lm --static -DONLINE_JUDGE -o main",
        "java":"javac Main.java",
        "python3":"python3 -m py_compile main.py"
    }
    p=subprocess.Popen(build_cmd[language],shell=True,cwd=dir_work,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    if p.returncode==0:
        return True
    print(err,out)
    return False


compile("g++")
