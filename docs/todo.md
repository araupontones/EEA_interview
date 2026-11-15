# To do

## Next: rebrand the dashboard (with the brand-designer agent)

- [ ] **Rebrand the dashboard.** Three reviewers said the current look resembles Claude's default style (fonts, colours). Work with the brand-designer agent on a new, distinctive identity: typography, palette, page background, hero and section layout, the waste-hierarchy pyramid, cards, hover cards, buttons and search boxes, the bar chart and the decoupling chart.
  - **Do not change the recycling rates against targets chart** (`dashboard/src/sections/distance_to_target/DistanceToTargetScatter.jsx`): it works well as it is. Keep its colours (red-yellow-blue scale), marks and layout; at most adapt the font if the new typography requires it.
  - Keep the rules that still apply: one meaning per colour across the charts, WCAG AA contrast and colour-blind safety, fonts from Google Fonts or system fonts, D3 maths + React rendering, texts from the lookups.
  - Record the new identity in `docs/communication.md` section 5 and the decision in `docs/decisions.md`.

## Other dashboard tasks

- [ ] Hero, "Not in the figures: 5.0 % ⓘ": decide how to explain it (a short visible line, a pop-up on click, or only in the method note); the ⓘ tooltip is easy to miss and does not work on phones.

## Open data decisions

Not listed here: see the open points in [method_notes.md](method_notes.md#7-open-points). When a decision there leads to work, add the task to this file.
