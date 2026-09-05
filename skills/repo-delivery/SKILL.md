---
name: repo-delivery
description: Improve repository onboarding, installation, upgrades, packaging, and release verification. Use when building or changing how users obtain, run, update, or remove a product, or when adopting a repeatable delivery workflow in a repository.
---

# Repository delivery

Make the first successful use easy to explain and prove. Choose the delivery
method from the repository's product, audience, and existing constraints.

## Establish the local contract

Inspect the canonical checkout, instructions, dirty work, package metadata,
release history, installer, README, and existing acceptance checks. Distinguish
the latest published release from a development branch. Preserve active work.

Use an existing delivery document if present. Otherwise add a short
`docs/DELIVERY.md` containing this repository's chosen distribution channel,
supported platforms, exact validation commands, state-preservation requirements,
and release authority. Link it from development instructions and the pull
request template. Keep these details out of global instructions.

## Choose what fits

| Product | Preferred starting point | User-path proof |
|---|---|---|
| Skill or agent plugin | Native host installation; standalone skill ZIP only when that host accepts it | Correct archive layout, actual discovery, namespaced invocation, update and removal |
| Local CLI | Existing package manager or source bootstrap | Fresh environment, locked dependencies, first offline command, update and recovery |
| Library | Its ecosystem package | Install the packed artifact in a separate consumer and import public exports |
| Web app or service | Existing deployment system | Authorized deployment revision, user entry point, health check, rollback and retained data |
| Desktop app | Platform-native package | Install, launch, permissions, update, uninstall and retained user data |

Adapt the choice for private repositories and managed devices. Do not add a
marketplace, daemon, global installer, or hosted CI merely for consistency.
Do not assume a desktop agent, cloud chat, CLI, and uploaded skill have the same
filesystem, executable, or authentication access. Verify current host behavior
against local tools and official documentation when making capability claims.

## Implement only the relevant pieces

Lead the README with what the user gains, then one recommended path for each
supported audience or app. Put prerequisites, commands, and troubleshooting in
one installation guide. Keep optional technical alternatives secondary.

Provide a way to identify the installed version and diagnose readiness. Make
updates refresh the actual installed code or dependencies. Describe exactly
what is preserved and how to recover. Use the native uninstall when available;
never delete user data merely because it shares an installation folder.

Separate package presence, integrity, app discovery, authentication, provider
readiness, and successful task execution. A check for one does not prove the
others. Dry-run must not perform the installation it is previewing.

## Verify and hand off

Run deterministic checks before model review. Test the documented first-use
path in a disposable environment with the candidate files, then repeat setup.
Cover update drift, failure recovery, and removal when those behaviors changed.
Keep test credentials and tools isolated; report missing prerequisites instead
of silently changing an account or machine policy.

For a published package or release, verify the downloaded artifact, version,
contents, license notices, and source revision. Do not claim a release from a
local build alone. Record exact commands and outcomes, tested platforms, and
user paths that remain unverified. Apply the repository's review and approval
rules; this skill grants no additional publishing, merge, deployment, or
destructive-cleanup permission.

For ordinary feature fixes, run only the applicable existing checks. Revisit
the delivery contract when installation, dependencies, public entry points,
provider capabilities, packaging, or deployment behavior changes.
