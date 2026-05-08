# Security Policy

Agent Forge is a Codex plugin and skill repository. It currently ships documentation, manifests, and workflow instructions rather than executable runtime services.

## Supported Versions

Security fixes target the default branch until versioned releases exist. After stable tags are published, supported versions will be documented here.

## Reporting a Vulnerability

Do not open a public issue for a suspected vulnerability.

Use GitHub private vulnerability reporting if it is enabled for the repository. If it is not available, contact the maintainer through GitHub profile contact options and include:

- A concise description of the issue.
- Affected files or workflow behavior.
- Reproduction steps or proof of concept.
- Expected impact.

## Scope

Relevant reports include:

- Plugin or marketplace manifest behavior that could mislead installation.
- Skill instructions that could cause unintended writes, credential exposure, or unsafe automation.
- Documentation that encourages insecure use of Codex or local credentials.

General feature requests should use the issue templates instead.
