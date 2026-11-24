<!-- SPDX-License-Identifier: CERN-OHL-S-2.0 -->

# ADR 0057: Coordinated original colour-chain fanout study

Date: 2026-10-28
Status: Authorized for ignored feasibility experiments; no canonical chain replacement selected.

The driver-port screen restricted to sixteen long original In4 colour segments adds no control route. Adjacent original colour geometry also contains many short staircase segments; fixing those internal vertices can prevent the coordinated displacement needed for a legal unchanged-size microvia. This decision permits an ignored whole-chain shove screen in the same x = 80–86 mm, y = 7–12.5 mm region.

Only original 215-edge COL_* In4 0.20 mm track segments intersecting that region may be movable. All component poses/pads, source vias, every accepted added copper item, all power/ground/USB and other original copper stay fixed. Short internal vertices within the eligible same-net chain may move. Endpoints where the chain attaches to retained copper, every pad/via contact and every external branch must remain contacted on the original layer. Preserve every 65-edge physical pad group and all earlier proofs. This is an experimental exception to ADR 0053's individual-segment endpoint freeze only for internal vertices of a wholly enumerated chain, not for external attachments.

Use unchanged 0.20 mm widths/clearance and 0.30/0.10 mm adjacent microvias for prospective new routes. Reject a prospective result if colour changes extend beyond a documented local port box, add more than 2 mm net track length per affected colour, lose an external contact, require moving a source via or degrade any old physical group/full native finding. Exact unchanged source pieces must remain in the selected inventory even if the exchange writer coalesces them. A session-format score is not native evidence.

Canonical selection would require a new exact original-chain/replacement/boundary-contact catalog, independent native proof of all retained/source interfaces, lower native/physical-pad opens, unchanged full 104 intrinsic findings, stable replay, source/LED checks and fault guards. Existing source-removal policy remains unchanged until that gate is implemented and recorded. No canonical chain replacement is currently selected.

Colour-path current/voltage drop, parasitic loading, timing/return and HDI/assembly effects remain unqualified. No current setting, pin map, protection/enable boundary or firmware changes are authorized. The board is unbuilt; independent Gate A remains mandatory before fabrication, and no manufacturing output is released.

The first In4-only whole-chain exchange screen made no new connection. A second ignored screen may also move original 0.20 mm COL_* B.Cu segments intersecting the U1 port region x = 80–91 mm, y = 0.7–12.5 mm. Apply the same external-contact, fixed-via, retained-addition, length and native acceptance limits. This broadens only the ignored feasibility scope; canonical source-removal policy is unchanged.

## Recorded exchange-screen outcome

The sixteen-long-segment, 327-segment In4-chain and 1,104-segment In4/B screens each retain the engine's 393 unjoined-item score and 239 fixed-model findings. These are exchange-model statistics, not the native 65-edge/104-finding counts. No new control, ground or VLED join is selected from any session. Inspection of the local engine confirms that ignored-net classes exclude routing jobs without making their traces shove-fixed; that skip setting does not explain the stalled screens. Native source policy remains unchanged: no whole-chain replacement is accepted. Subsequent exact single-segment TEMP_OK work is governed separately by ADR 0053.
