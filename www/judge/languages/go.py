import subprocess
from django.conf import settings

def system(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE).communicate()

COMPILE_MEMORY_LIMIT = settings.JUDGE_SETTINGS['MINMEMORYSIZE']
LANGUAGE = "Go"
EXT = "go"
VERSION = " ".join(system(["go", "version"])[0].strip().split(" ")[2:])
ADDITIONAL_FILES = []

def setup(sandbox, source_code):
    sandbox.write_file(source_code, "submission.go")
    compiled = sandbox.run("go build -o a.out submission.go", stdout=".stdout",
                           stderr=".stderr", time_limit=10,
                           memory_limit=COMPILE_MEMORY_LIMIT)
    if compiled.split()[0] != "OK":
        return {"status": "error",
                "message": sandbox.read_file(".stderr")}
    return {"status": "ok"}

def run(sandbox, input_file, time_limit, memory_limit):
    result = sandbox.run("./a.out", stdin=input_file, time_limit=time_limit,
                         memory_limit=memory_limit,
                         stdout=".stdout", stderr=".stderr")
    toks = result.split()
    if toks[0] != "OK":
        return {"status": "fail", "message": result, "verdict": toks[0] }
    return {"status": "ok", "time": toks[1], "memory": toks[2], "output": ".stdout"}
