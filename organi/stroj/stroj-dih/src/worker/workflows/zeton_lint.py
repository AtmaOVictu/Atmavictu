"""Delovni tok ŽETON-LINT: oblike nujnih žetonov izhoda."""

from typing import List

from pydantic import BaseModel

import mistralai.workflows as workflows

from worker.logic import zeton


class ZetonLintInput(BaseModel):
    zetoni: List[dict]


@workflows.activity()
async def sodi(zetoni: List[dict]) -> dict:
    """Aktivnost: vsak žeton ena sodba po obliki."""
    return zeton.lint(zetoni)


@workflows.workflow.define(
    name="zeton-lint",
    workflow_display_name="ŽETON lint",
    workflow_description=(
        "Preverba oblik žetonov izhoda: md5, ISO datumi, ISO TIK, "
        "ure z Z, slovenski datumi. Ena oblika, ena sodba."
    ),
)
class ZetonLint:
    @workflows.workflow.entrypoint
    async def run(self, input: ZetonLintInput) -> dict:
        return await sodi(input.zetoni)
