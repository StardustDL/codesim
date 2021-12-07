import pathlib
import subprocess
from tempfile import TemporaryDirectory
import logging
from codesim import get_temp_directory
from codesim.langs.cpp.models import Function, Instruction, Program

logger = logging.getLogger("cpp-compiler")


def compile(src: str):
    temp = get_temp_directory()
    codeFile = temp.joinpath("src.cpp")
    outFile = temp.joinpath("out.o")
    codeFile.write_text(src, encoding="utf-8")
    logger.info("Compiling")
    result = subprocess.run(
        ["g++", str(codeFile.absolute()), "-O2", "-o", str(outFile.absolute())], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8")
    result.check_returncode()
    return outFile


def objdump(objfile: pathlib.Path) -> Program:

    logger.info("Dumping")

    result = subprocess.run(
        ["objdump", "-d", "--no-show-raw-insn", str(objfile.absolute())], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8")
    result.check_returncode()

    output = result.stdout.splitlines()

    lines = len(output)
    cur = 0
    result = Program()

    while cur < lines:
        line = output[cur]
        cur += 1
        terms = line.strip().split(" ")
        if len(terms) != 2 or not terms[1].startswith("<") or not terms[1].endswith(">:"):
            continue
        func = Function(terms[1][1:-2])

        p = cur
        while p < lines:
            l = output[p].strip()
            p += 1
            if l == "":
                break
            if l == "...":
                continue
            try:
                terms = [s.strip() for s in l.split(":")[1].strip().split(" ") if s.strip()]
                opcode = terms[0]
                extra = terms[1] if len(terms) > 1 else ""
                func.instrs.append(Instruction(opcode, extra))
            except Exception as ex:
                logger.error(
                    f"Failed to analysis '{l}' of {func.name}.", exc_info=ex)
        cur = p

        result.funcs.append(func)

    return result
