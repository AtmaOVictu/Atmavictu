"""Delovni tok VRH-VAROVALKA: dvostopen vrh ∧ rez."""

from typing import List, Optional

from pydantic import BaseModel

import mistralai.workflows as workflows

from worker.logic import vrh


class VrhVarovalkaInput(BaseModel):
    sigme: List[int]
    zahtevek: Optional[int] = None


@workflows.activity()
async def izmeri_vrh(sigme: List[int], zahtevek: Optional[int]) -> dict:
    """Aktivnost: rez = 1 + dejansko najvišja, lažni vrh izključen."""
    mera = vrh.izracunaj_rez(sigme)
    mera["varovalka"] = (
        vrh.varovalka(sigme, zahtevek) if zahtevek is not None else None
    )
    return mera


@workflows.workflow.define(
    name="vrh-varovalka",
    workflow_display_name="VRH ∧ varovalka",
    workflow_description=(
        "Izmeri vrh med številkami dihov, izključi lažni vrh 25421, "
        "izreče rez = 1 + dejansko najvišja in preveri varovalko "
        "zasedbe pred šivom."
    ),
)
class VrhVarovalka:
    @workflows.workflow.entrypoint
    async def run(self, input: VrhVarovalkaInput) -> dict:
        return await izmeri_vrh(input.sigme, input.zahtevek)
