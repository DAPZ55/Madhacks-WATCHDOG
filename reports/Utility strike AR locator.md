# Capture the paint, don't guess the pipe

Buried-utility maps exist, but nobody can get the full map. Most US cities publish their sewer, storm and hydrant layers. Gas, electric, fiber and often water mains stay locked behind utility security and liability rules. 811 routes tickets and never shares line geometry. The best national registries (UK NUAR, Dutch KLIC) still gate access by job and role. A phone app can draw the public layers in AR today. Madison is unusually good: it publishes **24,662 sanitary mains, 67,333 sewer laterals, 44,272 storm pipes and 9,596 hydrants** as open ArcGIS services. Without RTK hardware, though, the phone's error is **about 1 m at best (Google VPS) and 2–10 m on GPS**. That is 2 to 22 times the 18-inch half-width of Wisconsin's tolerance zone, before counting errors in the records themselves. Wisconsin law also requires *everyone*, homeowners included, to call Diggers Hotline 3 working days before any dig. So the brainstorm's core promise, "a rough idea of where to dig", is technically weak and legally risky. The strongest version flips the AI's job from predicting what is buried to reading what is on the surface:
- recognize and AR-anchor 811 paint marks, with an alert when a shovel or bucket gets within 18 inches
- explain what 811 will and won't mark on your lot
- show public records only as wide, labeled uncertainty bands behind a "call 811" gate

For Madhacks, build that hybrid: Madison sewer/storm/hydrant layers as the AR "wow", YOLO hydrant/manhole detection to snap alignment, and paint-mark capture as the defensible product.

## Records exist for gravity pipes and hydrants, not for the lines people hit

**811 is a router, not a map.** Diggers Hotline has more than 1,400 utility members and handles more than 1 million locate requests a year. Members keep only their *service areas* current for routing, then mark their own lines with paint and flags ([Diggers Hotline](https://www.diggershotline.com/news/diggers-hotline-celebrates-50th-anniversary); [compliance program](https://www.diggershotline.com/compliance-program)). No public API or map export was found. The only 811-derived geometry a third party could ever see is its own ticket's dig polygon. The Wisconsin Damage Prevention Council lists better mapping data as a goal, so this is an open policy question, not a product ([WI DPC minutes, Sept 2025](https://www.diggershotline.com/assets/uploads/2025/09/Minutes%20of%20WI%20DPC%20Meeting%20-%2009112025.pdf)).

**Security and liability keep the shallow, dangerous utilities private.**
- FERC's post-9/11 CEII rules shield detailed energy design information behind NDAs ([FERC CEII](https://www.ferc.gov/critical-energyelectric-infrastructure-information-ceii-regulations)).
- PHMSA's pipeline map covers transmission lines only. Its public viewer is accurate to ±500 ft and "must not be used to identify exact locations" ([NPMS](https://www.npms.phmsa.dot.gov/AboutPublicViewer.aspx)).
- Seattle publishes its water mains but withholds transmission and feeder mains "for reasons of water system network security" ([data.gov SPU](https://catalog.data.gov/dataset/spu-water-mains-and-services)).
- Madison publishes hydrants but **no water-main layer**, only main-break points. MGE (gas and electric) publishes no GIS ([Madison OPEN_DATA_WATER](https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DATA_WATER/MapServer/0); [MGE](https://mge.com/safety-outages/diggers-hotline)).

| Source | What it holds | Who can access | Accuracy / caveat | Role in the app |
|---|---|---|---|---|
| **Madison ArcGIS REST** (`OPEN_DATA_ENGR2`, `_WATER`, `_TE`) | Sanitary mains 24,662; laterals 67,333 (with `Private`, `Tracer_wire` flags); storm pipes 44,272; manholes; hydrants 9,596; streetlights | Public, `query?f=geojson` | Records (QL-D). Many item dates are 2017, so check `Date_modified`. License terms not checked | **Core overlay + anchor coordinates** ([sanitary mains](https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DATA_ENGR2/MapServer/13); [laterals](https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DATA_ENGR2/MapServer/12); [streetlights](https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DATA_TE/MapServer)) |
| **OpenStreetMap** | 2.58M hydrants, 535k manholes, 189k `power=cable` ways (global) | Open | Buried lines are sparse and unverifiable. Madison coverage unknown (run Overpass) | Anchors and fallback outside Madison ([taginfo](https://taginfo.openstreetmap.org/api/4/tag/stats?key=man_made&value=manhole)) |
| **Diggers Hotline / 811** | Member service areas, tickets | Members; an excavator sees only their own ticket | Paint on the ground is the only "truth" | Ticket gate, not a data source |
| **PHMSA NPMS** | Gas transmission and hazardous-liquid lines | Public viewer, one county at a time | ±500 ft | None |
| **4M Analytics** | Nationwide map conflated from public GIS, permits, as-builts and imagery | Enterprise | Records-grade; SUE validation still needed | Partner later ([4M](https://4manalytics.com/blog/how-were-building-the-first-nationwide-map-of-utilities)) |
| **Exodigo** | Per-site multi-sensor AI scans | Enterprise | 57% more lines than records in one pilot **[vendor]** | Not relevant to an MVP ([datadrivenaec](https://datadrivenaec.com/tools/exodigo)) |
| **UK NUAR** | ~3.2M km of pipes and cables, >400 asset owners | Invitation only. A public tier "on their own property" is planned for 2026–28 but not confirmed | Owner count conflicts: gov.uk says >600 | Precedent for homeowner access ([ISPreview](https://www.ispreview.co.uk/index.php/2026/09/over-400-asset-owners-join-nuars-uk-map-of-underground-cables-and-pipes.html); [NUAR FAQs](https://www.nuar.uk/faqs); [GDS blog](https://gdsgeospatial.blog.gov.uk/2026/01/28/towards-a-comprehensive-national-underground-asset-register-integrated-into-the-existing-ecosystem)) |
| **Netherlands KLIC** | Operator data per dig, delivered within 2 working days | Registered excavators, per notification | Excavators must report deviations | Model for "ticket unlocks data" ([RVO WIBON](https://www.rvo.nl/onderwerpen/percelen-registreren/alles-over/graafwerkzaamheden-wibon)) |
| **Australia BYDA / Germany BIL** | Referral portals that return owner plans | The enquirer | BYDA calls plans "indicative only" | Same as 811 ([BYDA](https://www.byda.com.au/2025/11/26/the-free-byda-service-helping-you-access-utility-plans/); [DGMK](https://dgmk.de/en/news/bil-with-over-100-network-partners/)) |
| **Singapore Digital Underground** | Mandated 3D utility survey, in progress | Utility owners and developers | No completion status found | Long-term model ([SLA](https://www.sla.gov.sg/geospatial/resources/onemap-news/developing-a-digital-underground)) |

**Even complete records are low quality.**
- Records are ASCE 38 Quality Level D, which FHWA calls "highly limited" in comprehensiveness and accuracy ([FHWA](https://www.fhwa.dot.gov/programadmin/sueindex.cfm)).
- Snapping records to surveyed hydrants and manholes only raises them to QL-C ([McKissock](https://www.mckissock.com/blog/land-surveyor/utility-mapping-for-surveyors-a-guide-to-sue-and-asce-38-22/)).
- One review says the accurate locations of **at least 50% of buried assets remain unknown** ([MDPI Infrastructures](https://mdpi.com/2412-3811/4/4/60/htm)).
- No authoritative "records are off by X ft" figure was found. That is the biggest unknown in the error budget.

**Private lines are the homeowner's real blind spot.** Utilities mark "up to the meter and no further." Diggers Hotline will not mark propane lines, lines after the meter, sewer laterals, sprinklers, ornamental lighting, or feeds to barns and garages ([Diggers Hotline FAQ](https://www.diggershotline.com/homeowner-faq); [Colorado 811](https://www.colorado811.org/resources/blog/private-v-public-utilities-whats-the-difference)). Madison's lateral layer is a rare public dataset that reaches into this gap.

## A phone alone misses the 18-inch zone by 2x to 22x

Wisconsin's tolerance zone is 18 inches (0.46 m) either side of a mark ([Wis. Stat. 182.0175](https://docs.legis.wisconsin.gov/statutes/statutes/182/0175/3)). Every phone positioning option except RTK is wider than that before any record error is added.

| Method | Horizontal error | vs. 0.46 m | Notes |
|---|---|---|---|
| Phone GNSS, urban | 2–10 m; the best dual-frequency result was 1.75 m, after 102 min static | 4–22x | Unusable for live AR ([Sensors 2022](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9788430/); [ION 2021](https://navi.ion.org/content/68/4/727)) |
| **ARCore Geospatial (VPS)** | Typically ~1 m, bound <5 m; rotation <5° | ~2–11x | Free; wherever Street View exists. Sub-meter only near distinctive landmarks ([ARCore ref](https://developers.google.com/ar/reference/unity-arf/struct/Google/XR/ARCoreExtensions/GeospatialPose); [ION PLANS 2025](https://www.ion.org/publications/abstract.cfm?articleID=20196)) |
| ARKit geotracking | Limited US cities | Madison likely unsupported **[unverified]** | Check `checkAvailability` ([Apple](https://developer.apple.com/documentation/arkit/argeotrackingconfiguration.md)) |
| Two-point tap on known hydrant/manhole | Est. 5–20 cm tap error + GIS point error + drift | Unknown | **My estimate**; no measured study found. Esri uses this calibration pattern ([Esri](https://developers.arcgis.com/kotlin/scenes-3d/display-global-scenes-in-augmented-reality/)) |
| Earlier utility-AR systems | 30 cm–3 m; BeiDou+SLAM 0.6 m | ~1–6x | ([TUST 2023](https://www.sciencedirect.com/science/article/abs/pii/S0886779823000895)) |
| RTK add-on (Emlid Reach RX, ~$1.9–2.7k) | 1–5 cm; fails without sky view | Fits | Heading and map then dominate ([Advexure](https://advexure.com/products/emlid-reach-rx); [Pix4D](https://www.pix4d.com/blog/smartphones-mapping-underground-infrastructure-Pix4D)) |
| vGIS + Leica GS18 / Trimble SiteVision / PointMan | "7 mm" / "cm" | Fits | **[vendor]**, no independent validation ([vGIS/Leica](https://leica-geosystems.com/products/gis-collectors/gis-partners/vgis); [SiteVision](https://geospatial.trimble.com/en/products/software/trimble-sitevision)) |

**Heading errors matter as much as position errors.** A 5° yaw error moves a pipe drawn 5 m away by 0.44 m, which uses up the whole tolerance zone; 1° costs about 9 cm. The independent ASCE smartphone study concluded that phones without external high-accuracy GPS cannot be adopted for underground construction ([Fenais et al.](https://doi.org/10.1061/(ASCE)PS.1949-1204.0000474)). Even the official ground truth is fuzzy: Miss Dig calls marks "approximate", and EM locator depth estimates carry about ±15–20% error ([Miss Dig 811](https://www.missdig811.org/homeowner.html); [Projul](https://projul.com/blog/construction-underground-utility-locating-methods-guide)).

**Inferring routes from visual anchors only works for sewers.**
- Sewers run straight between manholes. A GNN predicting sewer links between manholes scored a ROC AUC of **94–95%** (the paper's sources disagree on the exact figure) ([ISARC 2024](https://www.iaarc.org/publications/2024_proceedings_of_the_41st_isarc_lille_france/underground_utility_network_completion_based_on_spatial_contextual_information_of_ground_facilities_and_utility_anchor_points_using_graph_neural_networks.html)).
- Hydrant leads branch short and roughly perpendicular to the main ([Fort Wayne W-15](https://www.cityoffortwayne.org/images/stories/Utilities/docs/Water_Details/W-15.pdf)).
- Shallow lines have no regular surface anchors. Federal gas mains need only 24 inches of cover, and customer electric needs 18–24 inches ([49 CFR 192.327](https://www.law.cornell.edu/cfr/text/49/192.327); [EC&M](https://www.ecmweb.com/national-electrical-code/article/20902845/stumped-by-the-code-requirements-for-underground-cables-and-raceways)). Wisconsin water mains sit at 5–6.5 ft ([NR 811.73](https://d1tvxue8o4w0fl.cloudfront.net/regulation/wisconsin-administrative-code/agency-department-of-natural-resources/environmental-protection-water-supply/chapter-nr-811-requirements-for-the-operation-and-design-of-community-water-systems/subchapter-x-distribution-systems/section-nr-81173-installation-of-mains)).
- Side-of-street conventions flip between cities: Castle Pines puts gas south/west, while Apex puts water north/east ([Castle Pines](https://castlepinesco.gov/wp-content/uploads/2022/10/Chapter4-Utility-Locations.pdf); [Apex](https://www.apexnc.org/DocumentCenter/View/4041)).
- A Nature Communications grid-mapping paper states that street-view methods **cannot detect underground power lines** ([Nature Comms 2023](https://www.Nature.Com/articles/s41467-023-39647-3)).

So a "YOLO sees a streetlight, so here's the cable" feature would be guessing.

**Detection works for anchors.**
- COCO includes "fire hydrant", so any pretrained YOLO finds hydrants.
- Mapillary Vistas labels manholes, catch basins, junction boxes, poles and streetlights.
- Roboflow has manhole sets of up to about 2,297 images ([Roboflow](https://universe.roboflow.com/ff-vt4js/manhole-cover-detection)).
- Manhole-cover papers report 93–95% mAP, but on small single-site data ([Frontiers 2024](https://www.frontiersin.org/articles/10.3389/fbuil.2024.1337984/full)).
- Cover text ("SEWER", "WATER") is "the most important feature" for classifying covers ([MDPI Appl. Sci.](https://mdpi.com/2076-3417/14/7/2769)).
- YOLO11n runs at about 7 ms in-app on iPhone via CoreML ([Ultralytics](https://github.com/ultralytics/yolo-ios-app/blob/main/docs/performance.md)).
- No public dataset exists for valve boxes, curb stops, gas meters or 811 paint.
- Geolocating detections from monocular images is weak: only 47% of poles fell within 5 m ([Sensors 2018](https://mdpi.com/1424-8220/18/8/2484)). Use detections to *snap* alignment, not to place utilities.

## Wisconsin law makes "where to dig" the wrong promise

- **Everyone must call.** "Excavation" covers any earth-moving with tools, with no homeowner or hand-tool exemption. Notice is due 3 working days ahead. Madison says this applies to homeowners in their own yards ([Wis. Stat. 182.0175](https://docs.legis.wisconsin.gov/statutes/statutes/182/0175); [City of Madison](https://www.cityofmadison.com/node/20706)). Diggers Hotline: "it doesn't matter how deep you are digging" ([FAQ](https://www.diggershotline.com/homeowner-faq)).
- **The 18-inch rule.** The statute keeps power equipment an estimated 18 inches from a mark for unexposed facilities. Once a line is exposed, the distance drops to the greater of 12 inches or twice the equipment's limit of control. Diggers Hotline tells homeowners only hand digging is allowed in the zone, while PHMSA's 2017 summary lists hand digging as not required. A 2026 draft bill would tighten this; it is not enacted ([statute](https://docs.legis.wisconsin.gov/statutes/statutes/182/0175/3); [PHMSA summary](https://primis.phmsa.dot.gov/Comm/StateDamagePrevention/State%20DP%20Law%20Summary/Wisconsin%20State_DP_Law_Summary_%2020170807.pdf); [draft](https://www.diggershotline.com/assets/uploads/2026/08/P3%20draft%20-%20DPC%20-%20Jan%202026.pdf)).
- **Penalties.**
  - Gas violations: up to $25,000 per violation, per day.
  - Other violations: $2,000 per offense.
  - Residential owners digging their own property are exempt from these forfeitures, but civil damage claims survive.
  - Obliterating marks is a misdemeanor.
  - The one-call system must warn callers that private facilities, propane specifically, are not included.
  - ([statute](https://docs.legis.wisconsin.gov/statutes/statutes/182/0175/3))
- **App liability is untested.** No case or published disclaimer for a consumer estimator app was found. Private locators limit liability by contract and position themselves as a supplement to the 811 locate ([Global News](https://globalnews.ca/news/9910634/digging-disaster-costly-renovation-calgary-couple/amp)). Locators themselves get sued: USIC faces the Glendale house-explosion suit ([WRDW](https://www.wrdw.com/2026/10/09/digging-dangers-why-underground-utility-damage-is-rise/)). A product whose core pitch invites reliance ("where to dig") undercuts its own disclaimer. That is an inference, not a ruling.

**Safe framing rules for any variant:**
- Say "where records expect lines", never "where to dig" or "safe to dig".
- Gate any line overlay behind a 811/Diggers Hotline ticket number or a "call now" step.
- Label every overlay "Records-based (QL-D). Not a locate. Does not satisfy your duty to call 811."
- Show what 811 *won't* mark on your lot (propane, sprinklers, garage feeds, laterals).
- Never show a green "clear" zone. The absence of a drawn line means unknown, not empty.

## Enterprises own the map; the homeowner and the faded mark are unowned

**Damage data points to where the losses are.** The 2025 DIRT preview counted **221,717 damages**. Root-cause groups:
- No 811 notification: **22.3%**
- Locator failures (not marked 14.2% + mismarked 9.2% + no response 4.2%): **27.6%**
- Failing to keep clearance after verifying marks (14.8%) or digging before potholing (7.2%): **22.0%**

Telecom took 51% of hits ([Cabling Install, Aug 2026](https://www.cablinginstall.com/design-install/news/55396303/underground-utility-damage-worsened-in-2025-and-telecom-networks-got-hit-the-most)). In 2025, **46%** of homeowners planning a DIY dig said they would skip 811, mostly because the job seemed "too shallow" ([Pumper](https://www.pumper.com/online_exclusives/2025/04/survey-finds-46-of-americans-plan-to-dig-without-contacting-811-beforehand)). In 2021, though, 60% of no-notification damages came from professionals ([CGA 2021 DIRT](https://dirt.commongroundalliance.com/2021-DIRT-Report/Executive-Summary)). A homeowner-only app addresses a minority of damage, while a mark-keeping tool for small contractors aims at the larger "clearance" pool.

| Player | What it does | Overlap with this idea |
|---|---|---|
| vGIS, Trimble SiteVision, ProStar PointMan (+Pix4D), Esri AR SDK | AR of a utility's own GIS, with RTK | Direct, but enterprise-only and needs owner data. PointMan tiers run $295–$6,950 **[verify]** ([PointMan](https://pointman.com/pricing/)) |
| 4M Analytics, Exodigo | Subsurface maps ($45M Series A; $96M Series B, $214M total) | Data layer, not consumer ([4M](https://www.4manalytics.com/blog/4m-analytics-secures-30-million-in-series-a-extension-to-become-the-google-maps-of-the-subsurface); [Railway Tech](https://www.railway-technology.com/news/exodigo-96m-series-b-funding/)) |
| Urbint and Locusview (bought by Itron for $325M and $525M) | Ticket risk scoring, digital as-builts | Utility-side; up to 35% fewer strikes **[vendor]** ([Refresh Miami](https://refreshmiami.com/news/itron-to-acquire-miami-based-urbint-in-325m-deal-to-expand-ai-powered-solutions/); [Zacks](https://www.zacks.com/stock/news/2794237/itri-boosts-resiliency-solutions-portfolio-with-525m-locusview-buyout)) |
| Irth Insights, iFactory | AI checks locate photos for paint/flag color vs. ticket | **Closest to mark capture**, sold to utilities and locators **[vendor]** ([Irth](https://irthsolutions.com/damage-prevention/insights-for-damage-prevention)) |
| UtiliSync, BOSS811 (~$2,500/user/yr), Utilocate ($25/user/mo), Automate811 | Ticket management, locate photos | Contractor workflow; aggregator pricing **[verify]** ([Capterra](https://capterra.com/p/206223/BOSS811/)) |
| DigAlert app | Consumer 811 ticket scheduling | Ticketing only ([SDG&E](https://sdgenews.com/article/you-dig-get-app)) |

**No consumer app that estimates buried-line positions was found.** That is white space, but partly because it is the riskiest framing.

| User | Pain | Served by 811? | Will pay? |
|---|---|---|---|
| DIY homeowner (fence, deck, garden) | Thinks job is too shallow; doesn't know what gets marked | Public lines only | No evidence |
| Rural/suburban owners with propane, garages, irrigation | Private lines never marked | **No** | Already pay private locators |
| Small fencing/landscaping contractors | Faded marks, disputes; fencing/landscaping cause 7% of telecom damage | Yes | Plausible; peers pay $300–2,500/user/yr for ticket tools |
| Locators and their insurers | Evidence after strikes | n/a | Yes (Irth market) |
| Municipal crews, plumbers, lateral contractors | Sewer/lateral position | Partly | Plausible (inference) |

## Rank the variants: read the surface, don't predict the subsurface

| Rank | Variant | Why it ranks here | Damage pool it targets | Legal risk |
|---|---|---|---|---|
| **1** | **Mark Keeper**: recognize APWA paint colors and flags, AR-anchor and geotag them with ticket number and timestamp, alert when the phone or shovel tip comes within 18 inches | Uses truth that already exists; relative AR tracking beats absolute geolocation; the AI task (color/shape) is easy; evidence log has buyers; Irth proves the AI concept is credible | Clearance and potholing failures (22.0%), faded marks | Low ("record of marks as placed, not a locate") |
| **2** | **Pre-call planner**: "what 811 will and won't mark at this address", private-line checklist (propane warning), one-tap Diggers Hotline, 3-working-day countdown | Pushes users toward compliance; cheap to build; addresses the 46% who skip | No notification (22.3%), private lines | Lowest |
| **3** | **Records X-ray**: AR overlay of public sewer/storm/lateral/hydrant layers with uncertainty bands, snapped to detected manholes/hydrants | Real data in Madison, great demo; but covers deep gravity systems people rarely hit and can't show gas/electric/fiber | Planning context, lateral work | Moderate; needs a ticket gate |
| 4 | **Private-locator referral** | Fills the statutory gap and makes money; not a tech demo | Private lines | Low–moderate (referral liability) |
| 5 | **At-the-bucket cab camera** (prior report's #1) | High value, but needs an excavator or sandbox rig; could be Mark Keeper's v2 | Clearance failures | Low |
| 6 | **Anchor-inference "AI guesser"**: YOLO anchors → predicted gas/electric/fiber routes, "rough idea where to dig" | Weakest physics (no anchors for shallow lines), weakest data, worst liability; invites people to skip 811 | Would *grow* no-notification damage | **Highest** |

**The non-obvious point:** variant 1 sidesteps the whole accuracy problem. Once the paint is captured, the phone only needs to know where it is *relative to the marks in the same session*, which ARKit/ARCore track locally rather than via GPS. Absolute VPS accuracy matters only for re-finding marks on a later visit. This is an inference; drift was not measured in these notes.

## Hackathon MVP: "Dig Aware", combining records, marks and the 811 gate

**Pitch:** "See what the city's records expect under you, capture what the locator actually marked, and never forget the 18-inch zone." It combines variants 1, 2 and 3. Variant 3 is the visual hook; variants 1 and 2 are the defensible product.

**Data (pre-fetch for the demo block, cache as GeoJSON):**
- Madison `OPEN_DATA_ENGR2` layers 13 (sanitary mains), 12 (laterals), 4 (storm pipes), 11 (manholes) and 2 (storm structures), plus `OPEN_DATA_WATER/0` (hydrants), via `/query?where=1=1&geometry=<bbox>&outSR=4326&f=geojson`.
- OSM Overpass for `emergency=fire_hydrant` and `man_made=manhole` as a cross-check and a fallback outside Madison.
- Show depth as a code-based label ("water ≥5 ft per WI code; sewer depth unknown"). The layer fields seen (material, diameter, slope, year) do not include depth.

**AR stack:**
- Unity + AR Foundation + ARCore Extensions (Geospatial works on iOS and Android). The faster alternative is native Android ARCore Geospatial.
- Skip WebXR: iPhone Safari does not support immersive AR ([threejsresources](https://threejsresources.com/webxr/browsers)).
- Esri's `WorldScaleSceneView` (Kotlin/Swift toolkit) can consume the feature layers directly if a team member knows Esri ([Esri toolkit](https://github.com/Esri/arcgis-maps-sdk-kotlin-toolkit/tree/main/toolkit/ar)).

**Alignment, in order of fallback:**
1. **VPS localize.** Run `checkVpsAvailability` at the demo site first. Show the reported horizontal accuracy and yaw accuracy. Flag low confidence above 1.5 m or 3° (a working threshold, not a spec).
2. **Snap to anchors.** YOLO detects a hydrant or manhole. Ray-cast the box's ground contact onto the AR plane, match it to the nearest GIS point of that type within the VPS error radius, and apply a translation correction. A second anchor fixes yaw.
3. **Manual two-tap.** The user taps two known features. This is Esri's calibration pattern.

**Detection:**
- YOLO11n pretrained (hydrant from COCO), fine-tuned on Roboflow manhole data plus about 200–300 photos shot around Madison on day one.
- Crop each cover and OCR it ("SANITARY", "STORM", "WATER") to type it.
- Paint marks: HSV color segmentation for APWA colors (red, yellow, orange, blue, green, purple, white, pink) plus line fitting. No dataset exists, so shoot your own on chalk or paper mats.

**Uncertainty UI (the honest part):**
- Draw each pipe as a translucent trench sunk below the ground plane, colored by APWA code.
- Band half-width = **18 in. tolerance + live registration error (VPS σ or post-snap residual) + a record allowance** (no sourced value exists; pick a conservative constant like 1 m and label it). This follows the Su/Kamat uncertainty-band approach ([Su et al. 2013](https://www.springerprofessional.de/uncertainty-aware-visualization-and-proximity-monitoring-in-urba/10801434)).
- Draw the inner 18-inch band hatched ("hand-dig only once marked").
- The band visibly shrinks when an anchor snap succeeds. That is the demo's "aha".
- Badges: "Records (QL-D) · City of Madison · updated <date>" and a "Gas / electric / fiber / water mains: NOT SHOWN, not public" banner.

**Safety gate:**
- The home screen is the planner: address → "811 will mark: …; you must hire a locator for: …", plus a Diggers Hotline button and a working-day countdown.
- The AR records view requires entering a ticket number or tapping "I've called / I'm planning".
- There is no "dig here" button. Tapping a spot gives "Within X m of recorded sewer. Wait for marks; hand-dig within 18 in."

**Demo script (about 3 minutes):**
1. *Hook (20 s):* "221,717 utility strikes last year. 46% of DIYers skip 811. And no app tells you what 811 won't mark."
2. *Plan (30 s):* Enter a Madison address. The app lists what gets marked and flags that the garage feed, sprinklers and propane won't be. Tap "Call Diggers Hotline"; the countdown starts.
3. *X-ray (60 s):* Outside on a street with a manhole and hydrant, VPS localizes ("±1.2 m"). A wide green sewer corridor and lateral appear. YOLO boxes the manhole, OCR reads "SANITARY", the snap fires and the band visibly narrows. A banner states gas and electric aren't shown.
4. *Mark Keeper (60 s):* On a cardboard or sandbox mat with yellow and red chalk lines, the app recognizes "yellow = gas" and "red = electric", anchors them and saves a timestamped record. Walk a shovel tip toward the line: the phone buzzes at 18 inches.
5. *Close (10 s):* "We don't guess where it's safe to dig. We make sure you call, remember what was marked, and stay out of the zone."

Don't spray real paint on public ground for the demo. Fake marks could mislead real crews, and Wisconsin treats marks as legally significant.

**Scope triage:** Must have: planner screen, GeoJSON overlay with VPS, bands, paint color capture with the 18-inch alert. Stretch: YOLO snap, cover OCR, laterals per parcel, export of the evidence log as a PDF.

## Main risks

- **Data gap:** The shallow lines people actually hit (gas, electric, fiber) are absent, and Madison has no water-main layer. Judges may ask "so what does it show?" Answer with marks and private-line awareness.
- **Data currency and license:** Several Madison items date to 2017, and the portal's terms of use weren't checked.
- **Accuracy:** VPS coverage and quality in Madison are unverified. Heading error can silently add about 0.4 m at 5 m. Snow, leaves and parked cars hide anchors in Wisconsin winters.
- **Detector overconfidence:** Published 93–95% mAP figures come from small single-site sets. Expect worse performance on Madison castings.
- **Automation bias and liability:** Any overlay can read as permission. The no-green-zone, ticket-gate and "not a locate" rules are non-negotiable. Case law is absent, so the risk is unpriced, not zero.
- **Security optics:** Rendering infrastructure in AR is fine with public sewer data. Adding scraped gas or electric data would invite CEII-style objections.
- **Business:** No evidence homeowners pay for apps. Money is in contractors, locators and 811-center outreach budgets.

## Conclusion

The question "can a phone show where pipes are?" turns out to be mostly a *data* question, and the honest answer is "only the pipes nobody is hitting." The map is a bigger source of error than the phone. Even perfect registration only renders a QL-D record that may be meters off or missing entirely. The opening for AI vision is therefore the surface, not the subsurface. Paint marks, flags, manhole lettering and hydrants are standardized and visible, and a phone can track itself relative to them far better than it can locate itself on Earth.

For Madhacks, the winning move is to use Madison's unusually rich public layers as a hook and pivot the product to compliance and memory. That means telling people what won't be marked, capturing what was, and guarding the 18-inch line. Watch the UK's planned NUAR public tier and Wisconsin's draft mapping provisions. If either opens owner data to the public with a ticket, the records overlay could become a real product.
