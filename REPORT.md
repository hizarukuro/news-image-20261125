# REPORT — news-image-20261125: "Wednesday 25 November 2026"

One 1024×1024 image summing up Wednesday 25 November 2026's world news:
35 stories from 9 regions and 18 fields, drawn as a newspaper front page.
The date itself is the masthead. Every story carries an epistemic stamp
(CONFIRMED / OFFICIAL / REPORTED / CLAIM / ONGOING) and a source credit.

## Heroes

1. Pakistan's first astronaut flies to Tiangong — Shenzhou-24 launched 00:18
   UTC from Jiuquan and docked 03:56 UTC; Muhammad Zeeshan Ali, 40, is the
   first Pakistani in orbit and the first foreign astronaut on Tiangong.
   CONFIRMED. Reuters; Xinhua/CMSA.
2. AI doubts crash Asia's chip stocks — Kospi −6.2%, Samsung −9.9%,
   SK Hynix −11.1%; Nasdaq −3.8% and Nvidia −8.5% in the US. CONFIRMED.
   AP; WSJ; CNN.
3. Two oil tankers hit mines and burn in Hormuz, Iran says — two tankers hit
   naval mines and caught fire; Iran's Revolutionary Guards say they took an
   "unauthorised route", not independently confirmed. CLAIM. Reuters (IRNA/IRGC).

## Grid (stories 4–15)

4. Solomons pick Australia for security — treaty signed in Canberra; A$740m
   over 10 years. OFFICIAL. DFAT; Reuters; AP.
5. Coalition strikes Hodeidah port — Hodeidah hit; 4 drones downed over
   Ras Tanura. CONFIRMED. SPA; Reuters.
6. UK energy bills to jump 26% — Ofgem cap £1,723 → £2,166 a year.
   OFFICIAL. Ofgem; Reuters.
7. Russian strikes black out five Ukraine regions — 112 drones launched,
   88 downed; Zaporizhzhia plant loses external power. CONFIRMED.
   Reuters; DTEK.
8. Ukraine says it hit two Russian refineries — Syzran and Kuibyshev,
   Samara region; Reuters could not verify. REPORTED. Reuters; Kyiv.
9. Israeli strike kills Hamas security chief — Abuelouf, wife and two
   children killed in Shati camp. CONFIRMED. Reuters; Gaza.
10. Garment workers win 36% pay rise — floor 12,500 → 17,000 taka.
    OFFICIAL. Reuters.
11. Cartagena hostage siege ends — 20 hostages freed, 1 gunman killed.
    CONFIRMED. Reuters/AFP.
12. US proposes tariffs on 14 economies — China up to 20%, EU 15%.
    OFFICIAL. Reuters/USTR.
13. Knesset backs Oct 7 inquiry — preliminary reading 65–50. OFFICIAL. Reuters.
14. 26 miners trapped in flooded gold mine — Pongkor, Bogor; 3 bodies found.
    CONFIRMED. Reuters; police.
15. Puigdemont to end nine years in exile — returns 12 Dec. OFFICIAL. Reuters.

## Briefs (stories 16–35, one line each)

16. BEIJING — Huawei rejects the Brooklyn verdict and vows to appeal. BBC; AFP.
17. PYONGYANG — North Korea expels the Swiss envoy; 48 hours to leave.
    Reuters; KCNA.
18. KHARTOUM — Sudan's army govt rejects Ethiopia's offer to host talks. SUNA.
19. BRUSSELS — EU proposes a Quantum Act and a €50bn tech fund for AI firms.
    Reuters; Commission.
20. ATHENS — 24-hour strike grounds flights and keeps ferries in port. Reuters.
21. CAPE TOWN — Court voids the 2022 Phala Phala report on Ramaphosa. Moneyweb.
22. WASHINGTON — US Q3 GDP revised up to 4.3%; jobless claims 189,000.
    Reuters; BEA.
23. CANBERRA — October inflation 4.9%; underlying 3.8%; fuel up 6.3%. ABS.
24. BERLIN — Q3 growth revised down to 0.1%; investment falls 1.2%. Destatis.
25. LONDON — Surprise Eurostar walkout cancels at least 6 trains.
    Reuters; Eurostar.
26. CENTURION — Mulder 7/31 and 100 as South Africa sweep Bangladesh 2–0. ICC.
27. TOKYO — JAXA unveils the LUPEX Moon rover; launch set for 2028. AFP/JAXA.
28. NAIROBI — Opposition boycotts electoral-commission talks. Kenyan press.
29. LONDON — Tube drivers to strike Thu 12:00–Fri 12:00; no Circle line. TfL.
30. NEW YORK — Stocks slide: Nasdaq −3.8%, S&P −2.6%, Dow −1.7%. CNN.
31. BEIJING — Anti-graft probe opens into Shanghai party chief Chen Jining.
    Reuters.
32. BEIJING — Wang Yi meets Dutch counterpart over the Nexperia dispute. Reuters.
33. BAMAKO — Cheap FPV drones reshape the Sahel insurgency; 187 attacks.
    Reuters.
34. WASHINGTON — Storm heads for the East Coast on Thanksgiving. Reuters.
35. MUMBAI — Sensex +1,502 to 83,938; Nifty +1.85%; rupee 8-month high.
    Hindu BusinessLine.

## Design choices

- Warm paper background, ink text, deep red accent, navy secondary; serif
  masthead, sans body. Every card has its own flat drawn scene — no
  icon-only cards — and a uniform chip/stamp/source row.
- "THE DAY IN UTC" strip: 8 timed stamps (00:18 liftoff → 21:00 Nasdaq close).
- "THE NUMBERS" band: 112 drones fired at Ukraine; 88 downed; 145 drones
  downed over Samara; 4.9% Australia inflation; 4.3% US GDP; €50bn EU tech
  fund. None of these figures repeats as a grid-card chip.
- World map with numbered pins 1–35, placed by each story's place; pins in
  the same city are jittered apart (London, Brussels, Beijing, Washington,
  Canberra, Gaza/Israel).
- DATE CHECK box lists seven older stories that were deliberately left out,
  each with its real date (Huang's Nvidia return Mon 23 Nov; Sooryavanshi's
  204 Tue 24 Nov; WHO Akwe evacuation Tue 24 Nov; Huawei verdict Tue 24 Nov;
  Riyadh tower hit Tue 24 Nov; Abu Nahel killed Tue 24 Nov; UN femicide
  brief Tue 24 Nov), plus the line that every story on the page happened or
  was first reported on Wednesday 25 November 2026.
- Footer: stamp legend, the honesty line "Scenes are drawn illustrations,
  not photographs.", and the full source list.

## Winner-grammar audit

- Date masthead: giant serif "Wednesday 25 November 2026" across the full
  width, no brand above it. Yes.
- Breadth strip: "35 STORIES · 9 REGIONS · 18 FIELDS · ALL FROM THIS
  WEDNESDAY" (counts computed from the story list, not typed). Yes.
- UTC timeline strip with 8 stamps. Yes.
- Epistemic stamp on every hero and grid card, plus the legend in the
  footer and a source on every card and brief. Yes.
- Every grid card illustrated with a specific flat scene. Yes.
- Numbered briefs with city lead-ins and sources. Yes.
- Map with pins matching story numbers. Yes (pins generated from the same
  story list as the cards).
- DATE CHECK box with real dates. Yes.
- Honesty footer. Yes.

## Tidiness audit

- One numbering source: all numbers (heroes, grid, briefs, map pins) come
  from the single ordered STORIES list in render.py; no number is typed
  twice. Verified by construction.
- Uniform chip styling: data chips are pale gold with ink text everywhere;
  stamps are coloured chips with white text everywhere.
- Uniform brief lead-ins: every brief is "CITY — one sentence. (Sources)".
- No stat-band figure repeats as a grid chip: checked — the six stat-band
  figures (112, 88, 145, 4.9%, 4.3%, €50bn) do not appear in any grid chip.
- Aligned columns and baselines: grid is 4 columns × 3 rows on a fixed
  lattice; briefs are two columns of ten on a fixed 12.5 px pitch; the
  timeline is 4 × 2 on a fixed grid.

## Inspection and fixes

I inspected the render at full size (crops of the top, grid, and bottom
sections) and at ~300 px. Defects found and fixed:

1. The footer ran 13 px past the bottom of the canvas — the sources line
   was cut off. Fixed by trimming section gaps (kicker, masthead, timeline,
   heroes, stat band, grid gaps, briefs pitch, map height) and enlarging
   the DATE CHECK box so its closing line sits inside the border. The
   footer now ends at y = 1015 of 1024.
2. The DATE CHECK closing line straddled the box's bottom border. Fixed by
   the same box enlargement (box 66 → 76 px).
3. Every data chip (heroes and grid) was drawn starting at the card's right
   edge, so chips were clipped off the page. Fixed by right-aligning chips
   from their measured width; the tag font shrinks from 7 px to 6 px on the
   two cards where tag + chip would otherwise touch.
4. The source credits on grid cards 8 and 9 were truncated with an
   ellipsis ("Reuters; Ukraine Gener…", "Reuters; Gaza Interior …").
   Fixed by shortening the credit lines to "Reuters; Kyiv" and
   "Reuters; Gaza" (the full attributions are in this report).

Final check: entry.png is 1024×1024, 211,416 bytes (limit 1,048,576).
main.py is standard library only (os, shutil) and copies entry.png byte
for byte; verified by two clean-environment runs into fresh directories
with identical sha256 output.
