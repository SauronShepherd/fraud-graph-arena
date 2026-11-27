import asyncio
import sys

from fraud_graph_arena.application import create_app

# Playwright closes connections while the Windows Proactor transport is still
# draining them.  The selector policy gives the local test server a quiet,
# deterministic shutdown without changing the application contract.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = create_app()
