
import re
import subprocess

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

p_addr = re.compile("0x[0-9a-fA-F]{16}")

innermost_cache = {}
outtermost_cache = {}

# TODO: manually change this field
VMLINUX_PATH = "/home/alan/Work/s2e/projects/kernel44/vmlinux"

genhtml = False

outterMost = False

def addr2line(matchobj):
    if outterMost:
        cache = outtermost_cache
    else:
        cache = innermost_cache
    addr = matchobj.group(0)
    if addr in cache:
        return cache[addr]

    result = subprocess.check_output("addr2line -f -i -e %s %s" % (VMLINUX_PATH, addr), shell=True)
    result = result.decode('ascii')
    lines = result.strip().split('\n')
    if outterMost:
        funcname = lines[-2]
        srcfile, lineno = lines[-1].split(':')
    else:
        funcname = lines[0]
        srcfile, lineno = lines[1].split(':')
    print(funcname)
    print(srcfile + ':' + lineno)
    srcfile = '/'.join(srcfile.split('/')[7:])
    repl_str = srcfile + ':' + lineno + '(' + funcname + ')'
    if genhtml:
        repl_str = '<a href="/source/%s?lineno=%s" target="_blank">%s</a>' % (srcfile, lineno, repl_str)
    cache[addr] = repl_str
    return repl_str


@app.route("/")
def main():
    return render_template('addr2line.html')

@app.route("/translate", methods=['POST', 'GET'])
def translate():
    global outterMost
    if request.method == 'POST':
        log = request.form['log']
        inner_outter = request.form.get('inner_outter')
        if inner_outter == 'inner':
            outterMost = False
        elif inner_outter == 'outter':
            outterMost = True
        log = p_addr.sub(addr2line, log)
        print(log)
        return log
    else:
        return ""


