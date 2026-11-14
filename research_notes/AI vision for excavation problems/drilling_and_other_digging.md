# Drilling and Other (Non-Construction) Digging: Chronic Problems Open to Visual AI / Sensors

Scope note: research done 2026-11-14 with ~19 web searches (no full-text reads of paywalled SPE papers). Many cost figures are old (2004-2015) or vendor-sourced; each is flagged. Per-problem summary table with feasibility ratings is in the final section's Inferences.

## Which problems are the costliest or deadliest?

### Takeaway
By money, drilling non-productive time (NPT) is the biggest item: published estimates run from roughly $1B to over $8B a year industry-wide, with stuck pipe and lost circulation the leading causes, and lost circulation alone eating 10-30% of geothermal well cost. By lives, landmines/ERW are far deadlier than anything else in scope (6,279 casualties in 2024, 90% civilian). Excavation damage to buried utilities and pipelines is the most frequent chronic problem: about 222k reported US damages in 2025, rising, at an estimated ~$30B/yr societal cost.

### Cited Findings
**Drilling NPT (oil & gas)**
- A 2004 industry study (published in Offshore, cited by Halliburton/Landmark) put drilling-trouble events at "almost $8 billion every year". Geopressure-related NPT alone is also cited at >$8B/yr. These figures are old — [Offshore Magazine](https://www.offshore-mag.com/drilling-completion/article/16755153/data-visualization-real-time-monitoring-improve-drilling-efficiency)
- A much lower estimate puts drilling NPT at ~US$1B/yr to operators, with lost circulation named a "principal culprit" — [Hart Energy / E&P](https://hartenergy.com/exclusives/its-whole-new-game-23288)
- Vendor claim: NPT is "up to 25% of total rig time". This is marketing, so treat it with caution — [Provectus case study](https://provectus.com/case-studies/oil-gas-upstream-drilling-npt-genai.md)
- Stuck pipe: the commonly cited estimate is >$250M/yr industry-wide, with other sources saying "hundreds of millions" or "billions" — [ASU-hosted paper](https://research.asu.edu.eg/bitstream/123456789/182384/1/V6026.pdf); [World Oil 2022](https://www.worldoil.com/magazine/2022/february-2022/features/drilling-technology-simple-solution-rapidly-recovers-stuck-drillstring-in-remote-well/); [Iraqi J. Chem. Pet. Eng. 2023](https://doaj.org/article/4052c38f59fc4bbbb820cf8c9f78d288)
- In a dataset of 1,000+ wells, 25% reported stuck pipe, 31% lost circulation and 48% rig/equipment failure. The source paper's region and date are unclear — [EKB journal paper](https://journals.ekb.eg/article_19508_5573882078d1bcfe50001b59660e0435.pdf)
- Sources disagree by close to an order of magnitude ($1B vs $8B), and their NPT definitions differ. I found no recent IADC/SPE benchmark with a single authoritative number — see the same sources above.

**Geothermal drilling**
- Lost circulation averages ~10% of total well cost in mature geothermal fields and often >20% in exploration and developing fields — [Stanford Geothermal Workshop 2020 (Saleh)](https://pangea.stanford.edu/ERE/db/GeoConf/papers/SGW/2020/Saleh.pdf)
- Other estimates: up to 30% of drilling cost (Geothermics 2023), "one fourth or more" (older DOE report) and 15% (PetroWiki). A 2017 study found lost circulation was the leading cause of NPT on a geothermal project — [eScholarship](https://escholarship.org/content/qt1h60g7xt/qt1h60g7xt.pdf?t=s5wtnv); [OSTI](https://www.osti.gov/servlets/purl/801407); [PetroWiki](https://petrowiki.spe.org/Geothermal_drilling_and_completion)
- Non-drilling time can reach 15-35% of total geothermal well cost — [UNU-GTP 2013](https://rafhladan.is/bitstream/handle/10802/7667/UNU-GTP-2013-16.pdf?sequence=1)
- Wells are 35-50% of total geothermal project capex — [DOE](https://www.energy.gov/node/4817222)

**Rig-floor safety**
- The US oil and gas extraction fatality rate was 27.5 per 100,000 workers over 2003-2009, against 3.9 for all US workers. This data is old — [ISHN (NIOSH data)](https://www.ishn.com/articles/99967-how-to-reduce-the-high-fatality-rate-in-oil-gas)
- NIOSH 2015-16: vehicle incidents caused 28% of fatalities, contact injuries 24%, caught-between/crushed 9% and struck-by 9%. In 2017 there were 69 fatalities, 13% struck-by and 9% caught-between — [CDC NIOSH 2015-16](https://www.cdc.gov/niosh/topics/fog/data2015-2016.html); [CDC NIOSH 2017](https://www.cdc.gov/niosh/topics/fog/data2017.html)
- An industry article claims 3 in 5 fatalities come from struck-by/caught-in/caught-between hazards. This conflicts with the NIOSH tables above, which put those categories well under half — [ISHN](https://www.ishn.com/articles/96330-how-to-prevent-struck-by-and-caught-in-hazards-from-causing-injuries)
- NIOSH found a statistically significant correlation between rig count and the annual fatality rate (1993-2006) — [ISHN](https://www.ishn.com/articles/99967-how-to-reduce-the-high-fatality-rate-in-oil-gas)

**Landmines / UXO / ERW**
- Landmine Monitor 2025 (covering 2024): at least 6,279 casualties (1,945 killed, 4,325 injured), the highest since 2020. 90% were civilians and 46% of civilian casualties were children. Myanmar had the most (2,029), followed by Syria (1,015), Afghanistan (624) and Ukraine (293). Improvised mines caused the most casualties (2,077) — [Landmine Monitor 2025 Major Findings](https://the-monitor.org/api/assets/reports/Landmine-Monitors/LMM2025/Downloads/LM2025-Major-Findings_EN.pdf); [UN News](https://news.un.org/en/story/2025/12/1166476)
- Preliminary 2025 data: >5,000 killed or injured in the 40 countries reviewed, with Syria highest at 1,602. International victim-assistance funding fell 23%. Five states (Estonia, Finland, Latvia, Lithuania, Poland) have begun withdrawing from the Mine Ban Treaty — [NPA](https://www.npaid.org/mine-action-and-disarmament/news/new-data-shows-thousands-of-civilians-killed-and-injured-by-landmines-and-explosive-remnants-of-war); [UN DPPA](https://dppa.un.org/en/landmine-casualties-hit-four-year-high-treaty-setbacks-deepen)
- Legacy WWII UXO in Germany: an often-repeated estimate is ~2,000 tonnes uncovered per year, mostly during construction. This traces to a single KMBD estimate cited in 2015. Regional Berlin figures conflict (56 t/yr vs 631 t/yr for Berlin+Brandenburg). About 15% of bombs reportedly failed to detonate. Sites must be certified UXO-clear before construction — [Smithsonian](https://www.smithsonianmag.com/history/seventy-years-world-war-two-thousands-tons-unexploded-bombs-germany-180957680/); [Euronews 2015](https://www.euronews.com/2015/05/02/berlin-still-detonating-live-wwii-bombs-buried-deep-underground); [Wikipedia: WWII bomb disposal in Europe](https://en.wikipedia.org/wiki/World_War_II_bomb_disposal_in_Europe)

**Utility / pipeline strikes (incl. DIY and post-hole digging)**
- CGA DIRT counted 196,977 unique damage reports in 2024 (damage rate up ~2.7%) and 221,717 in 2025. The 2025 CGA Index of 102 means damages are up 8 points since 2023. The top 10 root causes account for 85-86% of damages, and telecom/CATV plus natural gas account for 87% of damaged facilities — [Compact Equipment (2024)](https://compactequip.com/business/cga-releases-2024-dirt-report-findings-highlights-need-for-industry-improvements/); [Urbint](https://www.urbint.com/blog/2024-dirt-report-damage-rates-rise-2.7-heres-the-path-forward); [Trenchless Technology (2025)](https://trenchlesstechnology.com/cga-releases-2025-dirt-data-summary-trends/)
- In the 2022 data, damages with no 811 notification made up >25% of all damages, and 77% of those were by professional excavators (so ~23% were homeowners and others) — [Link2Build](https://link2build.ca/news/articles/2023/september/dirt-report-finds-more-excavation-related-damage-to-buried-utilities)
- A PHMSA 2026 advisory bulletin counts >875 excavation-related pipeline incidents since 2005, with 40 fatalities, 166 serious injuries and ~$322M in property damage. It estimates the annual US cost of utility damage across all utility types at nearly $30B — [Federal Register / PHMSA 2026](https://public-inspection.federalregister.gov/2026-07752.pdf)
- From 1993 to 2012 there were 1,630 third-party excavation pipeline incidents, causing 141 deaths, 440 injuries and ~$370M in damage — [PHMSA Report to Congress 2014](https://www.phmsa.dot.gov/sites/phmsa.dot.gov/files/docs/Report%20to%20Congress%20on%20Excavation%20Damage%20-%20October%202014.pdf)

**Agriculture / soil**
- Compaction "can reduce yields by as much as 60% in affected areas" (vendor-linked trade press, an upper bound rather than an average). SmartProbe pilot farmers cut subsoiling by up to 90% — [Precision Farming Dealer](https://www.precisionfarmingdealer.com/articles/6088-new-smartprobe-app-identifies-soil-compaction)

### Inferences
- In money terms the ranking is roughly: drilling NPT (billions/yr, but dominated by oil & gas majors) > US utility strikes (~$30B societal, which is diffuse and borne by many small actors) > geothermal lost circulation (a smaller industry but a large share of each well's cost). In lives, mines/ERW dominate (~6k casualties/yr), with rig-floor deaths in the tens per year in the US.
- Utility-strike damages keep rising despite 811 programs, which shows the existing process (one-call plus paint marks) has hit a ceiling. That makes it a "chronic" problem by definition.

### Gaps
- No current (2024-2026) authoritative IADC/SPE figure for industry-wide NPT % or $; IADC DDR-based benchmarks are paywalled or not surfaced.
- Homeowner/DIY share of 2024/2025 DIRT damages, and fence-post-specific counts, were not in the public summaries (likely in the full report/dashboard).
- No measured global dredging cost of turbidity/spoil overruns found.
- No count found of construction projects halted by unexpected human-remains discoveries, or of what those halts cost.
- No recent NIOSH fatality tables (post-2017) retrieved.

## What sensing exists, and what are the gaps?

### Takeaway
Rig-floor computer vision (H&P, Nabors, Seadrill) and shaker-mounted cuttings cameras now exist as pilots and early products, and so does AI dull-grading of bits. Accuracy, robustness and independent validation lag behind, and almost nothing uses cameras for kick or lost-circulation detection, which is still done with flow and pit-volume sensors. In demining, drone RGB plus ML works for surface ordnance, but buried and vegetated mines remain hard. Archaeology has strong LiDAR/DL site detection but chronic false positives. GPR+ML for graves works in labs but is inconsistent in the field.

### Cited Findings
**Rig-floor red-zone CV**
- H&P's PDS Redzone system analyzes camera frames around the pipe delivery system and alarms when a person is in the zone while it is active. A two-camera pilot logged 154 alerts over 114 active days, and the same cameras did drill-pipe tally. H&P calls it the first of its kind on a rig (SPE-208764-MS) — [H&P SPE 208764](https://www.helmerichpayne.com/media/technical-publications/A-Better-Set-of-Eyes-Computer-Vision-Technology-to-Monitor-Safety-Zones-and-Automate-Drill-Pipe-Tally-SPE-208764-MS.pdf)
- Nabors' Active Buffer Zone (ABZ) uses open-source detection algorithms. Nabors says human supervision and administrative controls are still needed — [IADC DEC minutes 2023](https://iadc.org/wp-content/uploads/2023/07/DEC2223_Minutes.pdf); [Drilling Contractor](https://drillingcontractor.org/digitalization-pushes-rig-alarm-alert-systems-into-the-next-frontier-65789)
- Seadrill's Vision IQ uses lidar plus AI for offshore red-zone monitoring and launched around 2019 — [Offshore Magazine](https://www.offshore-mag.com/vessels/article/14038494/seadrill-launches-ai-enabled-safety-technology-for-offshore-drilling); [OE Digital](https://www.oedigital.com/news/469685-seadrill-using-ai-to-monitor-the-red-zone)
- Rolloos' Red Zone System runs camera-based CV on NVIDIA GPUs — [NVIDIA blog](https://blogs.nvidia.com/?p=45355); [JPT: AI eyes on the rig](https://jpt.spe.org/ai-eyes-on-the-rig-computer-vision-boosts-oilfield-safety)
- Gap: I found no independent data showing reduced injuries. Rig cameras are often placed for security sightlines rather than safety-model angles (from search summaries of practitioner commentary) — same sources as above.

**Cuttings and shale-shaker image analysis (replacing visual mud logging)**
- Patents cover a CNN on a camera mounted on a non-vibrating part of the shaker that classifies cuttings vs debris, segmentation of cuttings and cavings (cavings indicate wellbore instability, a precursor to stuck pipe), and auto-adjusting camera settings — [USPTO 11719089](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11719089); [USPTO 12437385](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12437385); [Google Patents US11802474](https://patents.google.com/patent/US11802474)
- A JPT-reported Permian trial of autonomous cameras plus an image model measured cuttings recovery rates, but results varied by ~20%, which was "not yet good enough" — [JPT: Seeing the unseen](https://jpt.spe.org/seeing-the-unseen-computer-vision-in-action-restricted)
- A Marcellus proof of concept (AADE) used transfer learning on video from 11 wells (>200,000 ft drilled). SPE-208509-MS covers ML-driven CV for cuttings analysis — [AADE paper](https://www.aade.org/download_file/force/4682/635); [SPE 208509](https://www.sciencegate.app/document/10.2118/208509-ms)
- Vendor: Vertechs BoreSens uses high-resolution cameras plus AI for the shape, size and morphology of flowback cuttings (vendor claim) — [Vertechs PDF](https://vertechs.com/uploads/sfile/20260109/641180f33a266ceaf57390037224206b.pdf)

**Bit wear / dull grading**
- Manual IADC dull grading is subjective: two evaluators may assign different codes to the same bit. Cutters fill <20% of an image, which makes this a small-object detection problem — [arXiv 2410.14282 (YOLO for bit failure causes)](https://arxiv.org/pdf/2410.14282); [SPE Drill Bit Forensics (Ugarte)](https://file.streaming.spe.org/wp-content/uploads/2024/02/22133520/Drill-Bit-Forensics-and-Dull-Grade-Measurements-Esteban-Ugarte.pdf)
- Approaches include YOLOv5 transfer learning over 8 classes with U-Net labeling, one-stage damaged-cutter classification (Ali et al., SPE 2020) and a quantitative CV wear workflow (Yang et al., Petroleum Science 2024). The IADC system is still the dominant reporting standard (AADE 2025) — [SPE: AI to Drill Bit Forensics](https://file.streaming.spe.org/wp-content/uploads/2024/02/22133728/Application-of-AI-to-Drill-Bit-Forensics.pdf); [Petroleum Science 2025](https://cup.edu.cn/petroleumscience/docs/2025-01/80c6298a8dcd4409bb1506d543c207a7.pdf); [AADE](https://www.aade.org/download_file/force/4982/664)

**Kick detection**
- Standard detection compares flow-out with flow-in plus pit volume. Flow-out readings suffer from heave, mud transfers and tank-level imprecision, and pump-off kicks are hard to catch with fixed thresholds — [USPTO 10060208](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10060208); [USPTO 9708898](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9708898)
- Threshold-based pit alarms produce many false alarms, a "major hindrance for early detection" — [NTNU SPE 112212](https://www.ipt.ntnu.no/~kleppe/pub/ie2008/pdfs/spe112212.pdf)
- An LSTM on field data detected gas kicks earlier than the tank-volume method. A pilot-scale Coriolis return-line meter achieved a detection delay of ~2-7 s — [LSU repository](https://repository.lsu.edu/petroleum_engineering_pubs/670); [MUN](https://research.library.mun.ca/14569); [OGJ kick-prediction framework](https://www.ogj.com/drilling-production/article/55363193/kick-prediction-framework-predicts-offshore-loss-of-well-control)
- Gap: I found no camera- or vision-based monitoring of the return flow line or flowline/shaker fluid level in the literature searched.

**Landmines / UXO**
- Safe Pro AI's SpotlightAI moved from thermal to drone RGB plus ML because visual imagery was more consistent for surface ordnance in Ukraine. It claims ~90% detection under optimal conditions, >757,516 drone images processed (Oct 2024) and >150 ordnance types recognized. It struggles with buried or vegetated mines (company and founder claims) — [IEEE Spectrum](https://spectrum.ieee.org/clear-land-mines-drones-ai-2668391125); [DroneLife](https://dronelife.com/2024/10/28/spotlightai-processes-drone-images-to-identify-landmines/); [Scientific American](https://www.scientificamerican.com/article/drones-and-ai-could-locate-land-mines-in-ukraine/)
- A research preprint fuses RGB and LWIR thermal, with a dataset of 12,078 images. Thermal detects presence well but type poorly — [arXiv 2512.20487](https://arxiv.org/pdf/2512.20487v1)

**Archaeology (site discovery, sherd sorting)**
- Iberian burial-mound detection with DL plus Sentinel-2: 89.5% detection rate, precision 0.97, recall 0.64, and 10,527 mounds flagged over ~30,000 km² (the largest such application) — [Remote Sensing 2021 (Berganzo-Besga et al.)](https://discovery-pp.ucl.ac.uk/10136958/1/Berganzoetal.2021.pdf)
- A detector benchmark found FCOS mAP of 68.1-78.6%. A CNN on DTMs (Germany) reached ≥77% precision. Reviews note that LiDAR mound detection is "characterised by a very large presence of false positives" because archaeological morphology blends with natural features — [RUB thesis 2023](https://hss-opus.ub.rub.de/opus4/frontdoor/index/index/year/2023/docId/10217); [Remote Sensing (DOAJ)](https://doaj.org/article/99bc46c61b5c47e6bec2b734d914c312); [core.ac.uk](https://core.ac.uk/download/479013297.pdf)
- ArchAIDE (EU H2020) sherd recognition: 83.8% top-5 accuracy for the appearance/decoration model (ResNet-101) and 62.8% top-5 for shape. Small, heterogeneous training sets were a constraint — [CORDIS](https://cordis.europa.eu/article/id/411445); [Internet Archaeology 52](https://intarch.ac.uk/journal/issue52/7/3.html)

**Graves / human remains**
- A Bournemouth PhD built ML for GPR burial detection: ~93% grave/no-grave image classification, ~96% localization in radargrams and 94% on timeslices. It was released as the free web app "Reilig", but trained on medieval Irish and proxy data — [Green 2020 thesis](https://eprints.bournemouth.ac.uk/34284/1/GREEN%2C%20Ashely_Ph.D._2020.pdf)
- A 2025 South Texas cemetery study found GPR inconsistent: some graves gave strong signals, some voids, and many went undetected. It recommends multi-method fusion. A NIJ project applies predictive modeling plus GPR to missing-person searches — [Bohrium review link](https://bohrium.dp.tech/paper/arxiv/705cfce62a91f6ad75b8eb74876b649d296c7a60465bc8ce2b591730d4a55bbd); [NIJ](https://nij.ojp.gov/index%2Ephp/library/publications/finding-missing-and-unidentified-application-predictive-modeling-ground)

**Dredging**
- ESA-backed PLUMES (VITO) is building AI segmentation of dredge plumes in satellite imagery because existing algorithms "often fail" to detect plumes and quantify turbidity — [ESA EO4Society PLUMES](https://eo4society.esa.int/projects/plumes/); [OOS2025 abstract](https://meetingorganizer.copernicus.org/OOS2025/OOS2025-1383.html)
- EOMAP delivered physics-based satellite turbidity maps every ~2 days for 2+ years on an NW Australia dredge project, noting that in-situ sensors give only point measurements. DHI offers near-real-time maps within hours of overpass. Port of Miami plumes covered 127-228 km², at least 5x the pre-dredge extent, and natural resuspension and river plumes confound attribution — [Dredging Today](https://dredgingtoday.com/?p=48619); [DHI flyer](https://www.dhigroup.com/-/media/shared%20content/dhi/flyers%20and%20pdf/solution%20flyers/sediment%20mapping%20from%20space%20-%20dhi%20gras%20solution.pdf); [AGU 2016](https://ui.adsabs.harvard.edu/abs/2016AGUOSEC33A..04B/abstract)
- Current compliance monitoring relies on CTD/turbidity sensors on seabed frames or buoys. One project uses balloon-mounted cameras calibrated against turbidity — [PIANC abstract](https://coms.events/pianc-panama/data/abstracts/en/abstract_0147.html); [Planetek](https://www.planetek.it/en/projects/near_real_time_sea_turbidity_satellite_monitoring)

**Agriculture / tile drainage / soil**
- A smartphone machine-vision model (autoencoder CNN plus random forest) predicts sand, clay and silt with R² of 0.98-0.99 (Zhao et al., Agronomy 2022; validation design not checked) — [UiTM DOAJ record](https://openaccess.library.uitm.edu.my/find/Record/doaj-art-7999737dc36c4c81859244f7c55bece1)
- SmartProbe pairs a phone app with a handheld penetrometer to map compaction — [Precision Farming Dealer](https://www.precisionfarmingdealer.com/articles/6088-new-smartprobe-app-identifies-soil-compaction)
- Tile-drain detection: a USGS UNet on panchromatic satellite imagery reached 93-96% accuracy but only 52-54% balanced accuracy (it largely misses the minority drain class). Improved U-Net/ViT models have public code. A 2024 systematic review covers 19 studies. A UAV thermal tile-mapping literature exists, but I found no DL model trained on drone thermal imagery — [USGS](https://www.usgs.gov/index.php/publications/machine-learning-model-delineate-sub-surface-agricultural-drainage-satellite-imagery); [Papers with Code](https://astro.paperswithcode.com/paper/advanced-deep-learning-architectures-for); [KU systematic review](https://researchprofiles.ku.dk/da/publications/systematic-review-of-the-detection-of-subsurface-drainage-systems/); [EGU26](https://meetingorganizer.copernicus.org/EGU26/EGU26-10817.html)

### Inferences
- Common gap pattern: the sensing hardware exists, but models are trained on small, site-specific datasets and fail on generalization and false positives (cuttings ±20%, archaeology FPs, GPR inconsistency, USGS 52% balanced accuracy). No public benchmark datasets exist for cuttings, rig floor or kicks, whereas archaeology and landmines have some open data.
- Drilling CV is gated by access more than technology: rigs, shakers and bits belong to operators and contractors, so data is proprietary and pilots stay inside companies like H&P and Nabors.
- Kick and lost-circulation detection is a sensor-fusion and time-series problem. Cameras are not established there, so a camera on the flowline or shaker is novel but unproven.

### Gaps
- No independent validation of rig red-zone CV injury reduction.
- No quantified accuracy published for commercial cuttings-CV products (Vertechs and others).
- Magnetometer/EMI plus excavator-mounted UXO sensing for construction digging was not researched in depth (searches returned only tonnage stats).
- No AI products found for shale-shaker screen-tear or overflow detection specifically, though patents mention shaker cameras.

## Where are the clearest openings for camera- or cheap-sensor-based AI (with feasibility for a small team)?

### Takeaway
The best small-team openings are those with cheap cameras, public or creatable data, and a human user who already does the task by eye: phone-based cuttings and cavings classification, bit dull-grading from photos, sherd and artifact sorting, drone-RGB surface-ordnance flagging, a phone "before you dig" assistant for DIY and post-hole digging, and drone/satellite tile-drain and site-feature mapping. Deep subsurface problems (buried UXO, graves, kicks) need GPR, magnetometers or flow sensors and are poor hackathon fits.

### Cited Findings
- Visual mud logging and IADC dull grading are manual and subjective, and existing CV attempts are at the proof-of-concept stage (±20% accuracy on cuttings, YOLO for bits). This leaves room for better models and tools — [JPT](https://jpt.spe.org/seeing-the-unseen-computer-vision-in-action-restricted); [arXiv 2410.14282](https://arxiv.org/pdf/2410.14282)
- H&P showed that two ordinary cameras can do both red-zone detection and pipe tally, so commodity cameras are sufficient — [H&P SPE 208764](https://www.helmerichpayne.com/media/technical-publications/A-Better-Set-of-Eyes-Computer-Vision-Technology-to-Monitor-Safety-Zones-and-Automate-Drill-Pipe-Tally-SPE-208764-MS.pdf)
- Drone RGB beat thermal for surface ordnance in Ukraine (company claim), and an RGB+LWIR dataset of 12,078 images is public via arXiv — [IEEE Spectrum](https://spectrum.ieee.org/clear-land-mines-drones-ai-2668391125); [arXiv 2512.20487](https://arxiv.org/pdf/2512.20487v1)
- ArchAIDE was limited by small datasets, and its top-5 accuracy (84%) leaves room for foundation-model and few-shot approaches — [Internet Archaeology](https://intarch.ac.uk/journal/issue52/7/3.html)
- The Reilig GPR app shows ML-on-radargram tools can be shipped as free web apps — [Green 2020](https://eprints.bournemouth.ac.uk/34284/1/GREEN%2C%20Ashely_Ph.D._2020.pdf)
- No-notification damages are >25% of US utility damages and 23% of those are non-professional. Damages keep rising despite 811 — [Link2Build](https://link2build.ca/news/articles/2023/september/dirt-report-finds-more-excavation-related-damage-to-buried-utilities); [Trenchless Technology](https://trenchlesstechnology.com/cga-releases-2025-dirt-data-summary-trends/)

### Inferences
Per-problem summary. Feasibility (H/M/L) is for a hackathon or seed-stage team and is my own judgment based on the findings above.

| # | Problem | Persisted since | Scale / impact | Why unsolved | AI / sensor angle | Existing solutions & gaps | Feasibility |
|---|---|---|---|---|---|---|---|
| 1 | Stuck pipe | Since rotary drilling (~1900s) | >$250M to billions/yr; 25% of wells in one dataset | Multi-causal; data siloed | Shaker camera for cavings volume/shape (an instability precursor) + torque/drag time-series ML | Patents and pilots; ±20% accuracy | M (prototype on public cuttings images or lab rocks; field data hard to get) |
| 2 | Lost circulation (O&G + geothermal) | Decades; a top geothermal NPT cause | 10-30% of geothermal well cost | Fractured formations; detected late from pit volume | Flow-out/pit ML; camera on flowline/shaker to see returns drop | Sensor-based ML is research-stage; I found no vision approach | L-M |
| 3 | Kicks / well control | Since the 1900s (blowouts) | Low frequency, catastrophic (Macondo-class) | Noisy flow-out, false alarms | LSTM/ESN on flow; Coriolis meters; camera on return line is unexplored | Research only for vision | L (safety-critical, needs rig data) |
| 4 | Bit dull grading | IADC code since 1987 | Drives bit selection and ROP | Subjective human grading | Phone photo → cutter detection → IADC code | Academic YOLO, SPE work, vendor internal tools | H (photo datasets feasible; clear UI deliverable) |
| 5 | Cuttings description / mud logging | Visual logging for ~100 yrs | Lithology errors, workforce shortage | Microscope work by humans, subjective | Shaker cam or phone microscope → lithology, size, cavings | Patents, Vertechs, Marcellus PoC; accuracy unproven | H for a demo, M for a product |
| 6 | Rig-floor red zone | Ongoing; O&G fatality rate ~7x the US average (2003-09) | ~9% caught-between, 9-13% struck-by deaths | Admin controls fail; camera angles | Person detection + zone polygons + equipment-state input | H&P, Nabors ABZ, Seadrill lidar, Rolloos; no outcome data | H (off-the-shelf detectors; hard part is equipment-state integration) |
| 7 | Shaker monitoring (screen tears, overflow, mud loss) | Decades | Mud cost, solids control | Manual walk-arounds | Fixed camera anomaly detection | Patents only | M-H |
| 8 | Landmines/ERW in clearance & farming | Post-conflict, decades | 6,279 casualties in 2024 | Buried and vegetated mines; huge areas; funding down 23% | Drone RGB/thermal + DL for surface items; GPR/magnetometer fusion | SpotlightAI (~90% surface, claimed); weak on buried | M (surface detection demo feasible with public data; field deployment needs partners) |
| 9 | WWII UXO in construction digs (Europe) | 80 years | ~2,000 t/yr found in Germany (old estimate) | Ferrous clutter; deep bombs | Magnetometer-on-excavator + ML anomaly classification | Commercial survey firms; not researched in depth | L |
| 10 | Archaeological site discovery | Pre-LiDAR to now | Sites destroyed before being recorded | False positives | LiDAR/Sentinel DL detectors | Many academic models; heavy FPs | M-H (open LiDAR/DTMs) |
| 11 | Excavation documentation & artifact/sherd sorting | Forever | Backlog of unprocessed finds | Small datasets; specialist bottleneck | Phone recognition, photogrammetry, few-shot ViT | ArchAIDE 84% top-5 | H |
| 12 | Graves / remains during digging | Ongoing (e.g., residential-school searches, construction finds) | Project halts, legal and cultural harm | GPR is inconsistent | ML on GPR radargrams; multi-sensor fusion | Reilig (93-96% on lab data) | M (radargram data exists; field generalization weak) |
| 13 | Dredge plume / turbidity compliance | Decades | Plumes 5x baseline extent (Miami) | Point sensors; natural turbidity confounds | Satellite/drone/camera segmentation + in-situ calibration | EOMAP, DHI, ESA PLUMES (in progress) | M-H (Sentinel-2 free) |
| 14 | Utility/pipeline strikes, incl. DIY and fence posts | Since buried utilities; 811 since 1970s-2000s | ~222k US damages (2025); ~$30B/yr; 40 pipeline deaths since 2005 | Bad maps, skipped 811, mark misreads | Phone CV that reads paint marks, flags, and visible meters/risers; AR overlay of 811 tickets | Urbint and others do risk scoring; no consumer tool found | H (phone app; mark-color/flag detection is easy CV) |
| 15 | Soil compaction & texture | Since mechanized ag | Up to 60% local yield loss (vendor ceiling) | Penetrometer surveys are tedious | Phone image texture (R² ~0.98); penetrometer + app | SmartProbe; academic models | H |
| 16 | Tile drain mapping before digging/trenching | Legacy tile from the 1800s-1900s, unmapped | Broken tile when trenching or retiling | Lines invisible; maps lost | Drone thermal/RGB + U-Net segmentation | USGS satellite UNet (52% balanced accuracy); no thermal-drone DL found | M-H |

- Clearest openings: (a) bit dull grading and cuttings/cavings classification from photos, because the task is visual, done by humans today, and existing CV accuracy is weak; (b) a phone "dig-safe" assistant for homeowners and post-hole digging, because damages are rising and I found no consumer CV tool; (c) drone tile-drain or archaeology feature mapping on free data; (d) rig red-zone CV, which is technically easy but crowded by incumbents and needs rig access.
- The biggest blocker across drilling is data access. A small team should plan on public images (papers, Kaggle-style rock and cuttings sets, synthetic renders) or partner with a university rig or water-well driller.

### Gaps
- I did not verify that public datasets for cuttings, PDC bit photos or rig-floor video exist. This needs a targeted search on Kaggle, Zenodo and Volve/Equinor.
- Water-well drilling problems (mostly small contractors, little published data) were not covered by any source found.
- Pipeline right-of-way encroachment monitoring (satellite/drone change detection by vendors such as Orbital Insight-type firms) was not researched in this pass.
