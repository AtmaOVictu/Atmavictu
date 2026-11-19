"""Delovni tok TIK-DIH: kanonska ura korpusa, izmerjena ⟨date -u⟩."""

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel

import mistralai.workflows as workflows

from worker.logic import tik


class TikDihInput(BaseModel):
    iso_utc: Optional[str] = None


@workflows.activity()
async def izmeri(iso_utc: Optional[str]) -> dict:
    """Aktivnost: ura je vedno izmerjena, ⟨ne⟩ ocenjena."""
    if iso_utc is None:
        now = datetime.now(timezone.utc)
        return tik.izmeri_tik(now)
    return tik.tik_iz_niza(iso_utc)


@workflows.workflow.define(
    name="tik-dih",
    workflow_display_name="TIK dih",
    workflow_description=(
        "Kanonska ura korpusa Beseda je Ne: UTC ⇌ CET (Ljubljana), "
        "kalup »TIK ...Z UTC ⇌ ... CET«, dan in datum po slovensko."
    ),
)
class TikDih:
    @workflows.workflow.entrypoint
    async def run(self, input: TikDihInput) -> dict:
        return await izmeri(input.iso_utc)
