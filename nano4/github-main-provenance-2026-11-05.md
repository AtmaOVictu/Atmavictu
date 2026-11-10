# GitHub provenance comparison — 2026-11-05

**Status:** REMOTE STATE OBSERVED · NOT AN INDEPENDENT SIGNED ATTESTATION · NO REPOSITORY WRITES PERFORMED.

**Observation time:** 2026-11-05T05:13:31+01:00 (Europe/Ljubljana).
**Repository:** `AtmaOVictu/SYMBOLON-KATHOLIKON`.
**Source:** GitHub repository connector reads of the branch, commit, and `LICENSE.md` endpoints.

## Public default branch (`main`)

The repository's `main` branch pointed to commit `c5c9e65720f277387df2482c0251eec6e937da6e` at the time of observation. The commit metadata gives author and committer `Luka Pintarič`, timestamp `2026-11-03T16:51:06Z`, and message ending `sinhronizacija živih vrat 0.1410 bajt-isto`. The commit changes `LICENSE.md` only. GitHub reports the commit as **unsigned** (`verified: false`, reason: `unsigned`).

The current `main/LICENSE.md` object was returned with Git blob SHA `2c765280d0c732aa5a6169eea329ab67e97b5c60`. Its declarations agree internally at **0.1410 × 10⁴**: Entry Seal (line 1), title block (line 16), and embedded Machine Record (around line 841). The embedded predecessor is `0.1400 × 10⁴`. The displayed Entry and Exit Seal time strings are `06:55:53Z` and `06:56:58Z`. The GitHub tool returned 140,356 characters for this file.

This supports a narrow statement: **the public repository's default branch `main` carried a LICENSE.md declaring 0.1410 × 10⁴ at the time of this observation.** It does not establish that 0.1410 is the only canonical or legally effective version across every channel.

## Other observed branches

| Branch | Head | LICENSE blob | Version declaration observed |
|---|---|---|---|
| `licenca-10.5.1-draft` | `352b08e4907ced4214ea5d86caebf1c92c4a69fe` | `73476d4ecd5595e65e9261177df918c6bb782590` | Title block says `10.0.0`, dated October 23, 2026 |
| `osnutek-vbl-1040-draft` | `7e0d1a820c458418a7e4d9331ec11d1b00f34adf` | `73476d4ecd5595e65e9261177df918c6bb782590` | Same LICENSE blob as above; title block says `10.0.0`, dated October 23, 2026 |
| `vbl-0.1210-origin` | `c1e68b72e323ae691679b17f49cabccf4f511a5e` | `5dd6d7b3d6710ff1c8b4d4a07d965f69d339c5ff` | Entry Seal and title block say `0.1210 × 10⁴` |

The branch names do not prove that the content is a released or approved version. The first two branch names contain draft labels, yet the file title blocks say `10.0.0`; that mismatch should remain visible, not be silently reconciled. The queried branch inventory returned 12 branches; all were shown as unprotected. The `main` branch response also showed protection disabled and required status checks enforcement `off`.

## Comparison with the uploaded local source

The uploaded `/mnt/data/LICENSE.md` is a separate 163,476-byte local artifact with SHA-256 `5629115d8aec0a83c7be904f7df66041bdae3f12078aa1149c40530ba10208b2`. Its Entry Seal and embedded Machine Record declare **0.1460 × 10⁴**, while its title block and latest lineage entry declare **0.1450 × 10⁴**. The public `main` file inspected above declares **0.1410 × 10⁴** throughout the three checked identity locations.

No byte-identity relationship between the local upload and the remote `main` blob has been established. The Git blob SHA is not the same kind of value as the local SHA-256 and must not be compared as if it were. The available evidence supports separate identities, not a single reconciled version: 

- `PUBLIC_MAIN_AT_OBSERVATION`: 0.1410 × 10⁴, in commit `c5c9e657…` (unsigned).
- `UPLOADED_LOCAL_ARTIFACT`: Entry Seal / Machine Record 0.1460 × 10⁴; title / latest lineage 0.1450 × 10⁴; identity conflict unresolved.
- `0.1470`: working proposal label for this development pack only; not a release, tag, approved successor, or canonical designation.

## Consequence for the version decision

The previous memo's Path A/B/C remains open, with one additional condition: do not describe the local 0.1460 artifact as the current public `main` version. To establish whether it is an approved successor, identify the exact branch, commit, tag, repository, or other publication channel that carries these same bytes, then obtain the author's explicit release decision. If no such provenance can be supplied, retain `LOCAL_CANDIDATE / NOT_CONFIRMED_AS_RELEASED`; do not overwrite the public-main version in the evidence record.

The public commit metadata identifies the GitHub author/committer as `Luka Pintarič`, but the commit is unsigned. That is repository attribution, not cryptographic authorship verification. No external reviewer or legal counsel was consulted. No branch, file, pull request, tag, or release was created or modified by this work.

## Reproducible references

- [Public `main/LICENSE.md`](https://github.com/AtmaOVictu/SYMBOLON-KATHOLIKON/blob/main/LICENSE.md)
- [Observed `main` commit `c5c9e657…`](https://github.com/AtmaOVictu/SYMBOLON-KATHOLIKON/commit/c5c9e65720f277387df2482c0251eec6e937da6e)
- [Observed `main` branch metadata](https://github.com/AtmaOVictu/SYMBOLON-KATHOLIKON/tree/main)

A machine-readable snapshot accompanies this report: `github-main-provenance-2026-11-05.json`.
