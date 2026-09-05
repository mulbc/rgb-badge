<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0005: Project licensing

- Status: Accepted
- Date: 2026-09-05

## Context

The repository is public during early development and is intended to become a usable open-source hardware project. Hardware source and software have different ecosystem conventions.

## Decision

License hardware, mechanical, manufacturing and hardware-documentation sources under CERN-OHL-S-2.0. License firmware and software tooling under Apache-2.0. Preserve the original licences and attribution of any third-party material.

## Consequences

- Distributed modified hardware documentation remains subject to the strongly reciprocal CERN-OHL-S terms.
- Firmware and tooling can be reused under the permissive Apache-2.0 terms.
- Each new file must follow the licence map and carry an SPDX identifier where its format permits.
