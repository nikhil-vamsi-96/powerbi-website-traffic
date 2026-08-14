# Dashboard Blueprint — Website Traffic Analysis

Build this as a 2-page Power BI report. Import `website_sessions.csv`,
name the table `WebSessions`, then paste in the measures from
`dax_measures.txt` before building visuals.

## Page 1: Traffic Overview

**Top row — KPI cards (4 cards):**
1. `[Total Sessions]`
2. `[Bounce Rate]` — conditional color red if >50%
3. `[Conversion Rate]` — format as %
4. `[Avg Session Duration (sec)]`

**Middle row:**
- **Line chart (full width):** Sessions by Date (Axis: Date, Values: `[Total Sessions]`) — this is the headline visual, put it first and make it wide. Add a trend line via the Analytics pane.

**Bottom row — three visuals:**
- Donut chart: Sessions by Traffic Source (Legend: TrafficSource, Values: Count of SessionID)
- Bar chart: Sessions by Device (Axis: Device, Values: Count of SessionID)
- Map or bar chart: Sessions by Country (Top 6)

**Slicers (top of page):** Date range, Traffic Source, Device

---

## Page 2: Conversion & Engagement Drivers

**Top row:**
- Bar chart: `[Conversion Rate]` by Traffic Source, sorted descending — this is the most actionable chart in the whole report; put it top-left
- Bar chart: `[Bounce Rate]` by Device

**Middle row:**
- Table: TrafficSource | `[Total Sessions]` | `[Conversion Rate]` | `[Bounce Rate]` | `[Avg Session Duration (sec)]` — the channel-performance summary table a marketing manager would actually use to decide budget allocation
- Column chart: Avg Daily Sessions, Weekday vs Weekend (use the two DAX measures directly as two columns)

**Bottom row:**
- Scatter chart: X = `[Bounce Rate]`, Y = `[Conversion Rate]`, Size = `[Total Sessions]`, Legend = TrafficSource — shows at a glance which channels are both high-volume AND high-converting (upper right = best channels)

**Slicers:** Country, Date range

---

## Design Notes
- Use one accent color per traffic source consistently across both pages (e.g., Organic Search = green, Paid Search = orange) so a viewer doesn't have to re-learn the color key per page.
- The scatter chart on Page 2 is the standout analytical visual — it answers "where should marketing spend go" in one glance, which is exactly the kind of insight that makes a portfolio project memorable in an interview.
- Add a text callout under the Page 1 KPI cards noting the headline finding (e.g., "Email converts 4x better than Social despite 7x less volume") — this primes anyone reviewing the dashboard to look for it.
