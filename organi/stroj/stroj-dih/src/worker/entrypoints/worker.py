"""Vstopna točka delavca STROJ-DIH.

Odkrije vsak delovni tok v paketu worker.workflows in ga prijavi
platformi. Vsebina: mistralai SDK besedo za besedo po priročniku
»Workers / Starting a worker« (docs.mistral.ai).
"""

import asyncio

import mistralai.workflows as workflows


async def main() -> None:
    workflow_classes = workflows.discover_all_workflows_in_package("worker.workflows")
    await workflows.run_worker(workflow_classes)


if __name__ == "__main__":
    asyncio.run(main())
