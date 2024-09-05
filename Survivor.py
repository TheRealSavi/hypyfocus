from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Generator import Generator
    from Toolbox import Toolbox

from Hyperfocus import Hyperfocus
from Skillcheck import SkillCheck


class Survivor:
    def __init__(self, item: Toolbox, hyperfocusEnabled: bool):
        self.item = item
        self.skillCheckInstance = SkillCheck()
        self.hyperfocus = Hyperfocus()
        self.hyperfocusEnabled = hyperfocusEnabled

    def repair(self, gen: Generator):
        self.item.repairGen(gen, self)

    def getItem(self):
        return self.item

    def getSkillCheckInstance(self):
        return self.skillCheckInstance

    def getHyperfocus(self):
        return self.hyperfocus
