# Method and assumptions (IS 456:2000)
- Flexure: Annex G. xu,max/d = 0.0035/(0.0055+0.87fy/Es). Doubly reinforced uses the Fig. 23B stress-strain curve for fsc.
- T-beams: Annex G-2.2 with yf rule, effective flange width cl. 23.1.2 (lo = L simply supported, 0.7L continuous). Sagging only; flange compression steel not supported.
- Shear: tau_c = 0.85*sqrt(0.8fck)*(sqrt(1+5B)-1)/(6B), B = max(0.8fck/(6.89pt),1), pt capped at 3. Tau_c,max from Table 20. Check at d from the support.
- Deflection: basic L/d 20, 7, 26; kt is a curve fit of Fig. 4; kc from Fig. 5; flanged factor approximates Fig. 6.
- Development length: Ld = phi*0.87fy/(4*tau_bd), tau_bd x 1.6 for deformed bars.
- Loads: one UDL (self-weight optional) and one central or tip point load. Continuous beams use approximate coefficients (wL^2/12, 0.6V), not Table 12.
- Not covered: torsion, curtailment, anchorage detailing, seismic detailing (IS 13920), fire and exposure cover, flange compression steel.

## Columns (rc_beam/column.py, docs/column.js)
- Slenderness cl. 25.1.2 (limit 12), additional moment cl. 39.7.1 without the k reduction, minimum eccentricity cl. 25.4, limit 60 on le/dimension.
- Interaction by strain compatibility (cl. 38.1 stress block, 0.002 strain at 3D/7 when xu > D), 400 strips; compression steel stress reduced by 0.446 fck.
- Biaxial: (Mux/Mux1)^an + (Muy/Muy1)^an <= 1, an from Pu/Puz (cl. 39.6). Steel split equally on two opposite faces.
- Ties: size at least dia/4 and 6 mm, spacing at most min(b, D, 16 dia, 300) (cl. 26.5.3.2). Steel 0.8% to 4%, 4 to 24 bars.
- Not covered: circular columns, shear in columns, helical ties, joints, footings, braced/unbraced frame analysis.

## Round 3 additions
- Stirrup zones are grouped into at most three bands (lowest required spacing, a middle value rounded down to 25 mm, and the largest); each band is never wider than the spacing required inside it.
- Hooks: 135° tails, alternating between the two top corners (bottom corners for a cantilever), on the compression side.
- Curtailment (simply supported, singly reinforced, rectangular only): at least half the bars (minimum two) run into the supports; the rest stop at the theoretical cut-off plus the larger of d and 12 x diameter (cl. 26.2.3.2-3).
- Anchorage: Ld <= 1.3 M1/V + Lo (cl. 26.2.3.3), Lo = min(support width/2 - cover, max(d, 12 x diameter)); not checked for cantilevers.
- IS 13920 member checks added with the switch: web width >= 200 mm, b/D >= 0.3, tension steel 0.24 sqrt(fck)/fy to 2.5%, hoop diameter >= 8 mm. Column confinement area (Ash), strong-column weak-beam and joint rules are NOT implemented.
- Not implemented: two-layer bars, multi-span analysis, torsion, slabs, footings, PDF report.

## Stirrup zones, side steel, column bars, IS 13920, 3D (added)
- Beam stirrups: spacing designed at stations along the span from the shear envelope (cl. 40.4), capped at min(0.75d, 300) and the minimum-steel limit (cl. 26.5.1.5-6), rounded down to 25 mm, minimum 75 mm; first stirrup 50 mm from the support face. Shear is taken as constant between the support and d.
- IS 13920 option: end zones 2d long with spacing at most min(d/4, 8 x smallest bar, 100 mm); elsewhere at most d/2 (cl. 6.3.5). Columns: end zones of max(larger dimension, clear height/6, 450 mm) with spacing at most min(least dimension/4, 100 mm), not below 75 mm (cl. 7.4). Confirm clause numbers against your copy of the code.
- Side-face steel for D > 750 mm: 0.1% of web area split over two faces, 10 mm bars, spacing at most min(300, b) (cl. 26.5.1.3).
- Column bars sit on all four faces (2 to 6 per b-face, 2 to 8 per D-face, at most 32 in total); the interaction uses each bar's real position. Cross-ties are added at every intermediate bar; this is a simplification of cl. 26.5.3.2 (c).
- Column height for tie count is the larger of the two unsupported lengths.
- Bar schedule: straight lengths, 10d hook allowance per stirrup or tie, no laps, curtailment or anchorage. Weight = d^2/162 kg/m. The schedule is built in the browser from the same results as the tables.
- 3D view: stirrup and bar positions come from the design results, drawn to scale. The section readout for continuous beams is indicative.
- Not included: curtailment, torsion, flange compression steel, circular columns.
