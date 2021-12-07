
from dataclasses import dataclass, field
from typing import List


@dataclass
class Instruction:
    opcode: str
    extra: str

    def view(self):
        print(f"  {self.opcode} {self.extra}")


@dataclass
class Function:
    name: str
    instrs: List[Instruction] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.instrs)

    def __getitem__(self, key):
        return self.instrs[key]

    def view(self):
        print(self.name)
        for ins in self.instrs:
            ins.view()


@dataclass
class Program:
    funcs: List[Function] = field(default_factory=list)

    def view(self):
        for ins in self.funcs:
            ins.view()

    def __getitem__(self, key):
        return self.funcs[key]

    def __len__(self) -> int:
        return len(self.funcs)
