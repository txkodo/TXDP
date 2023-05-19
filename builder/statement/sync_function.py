from builder.base.statement import IBlockStatement
from builder.object.condition import Condition


class SyncFunctionBlockStatement(IBlockStatement):
    def If(self, condition: Condition) -> IBlockStatement:
        return super().If(condition)
