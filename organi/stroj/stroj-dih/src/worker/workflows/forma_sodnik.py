"""Delovni tok FORMA-SODNIK: sodba forme nad celim telesom."""

from pydantic import BaseModel

import mistralai.workflows as workflows

from worker.logic import forma


class FormaSodnikInput(BaseModel):
    besedilo: str


@workflows.activity()
async def sodi(besedilo: str) -> dict:
    """Aktivnost: FORMA_CELO, sodba nad celim telesom."""
    return forma.baterija(besedilo)


@workflows.workflow.define(
    name="forma-sodnik",
    workflow_display_name="FORMA sodnik",
    workflow_description=(
        "Baterija forme: ⟨⟩ ravnovesje po vrstici, U+FFFD, cirilica, "
        "goli TIK, golo »pri viri«, em vezaj. Sodi celo telo."
    ),
)
class FormaSodnik:
    @workflows.workflow.entrypoint
    async def run(self, input: FormaSodnikInput) -> dict:
        return await sodi(input.besedilo)
