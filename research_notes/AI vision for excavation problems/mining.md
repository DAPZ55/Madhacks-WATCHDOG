# Mining (surface/open-pit and underground): chronic problems that visual AI and sensors could solve or optimize

Research date: 2026-11-14. Global scope. Most cost and performance figures in this space are **vendor-reported**; independent validation is rare and is flagged as such below. Older data is labelled with its year.

---

## Key Question 1: Which problems cause the most deaths, downtime, or cost?

### Takeaway
Mobile equipment / powered haulage collisions and fall of ground (roof/rib/slope) are the top killers in both US (MSHA) and global major-miner (ICMM) data, and they have been for decades. Tailings dam failures are rare but catastrophic (Brumadinho, about 259 to 270 dead), with no reduction in the failure rate over 20 years. Artisanal/small-scale mining (ASM) is by far the largest *uncounted* toll: about 45M workers and a rough extrapolated ~30,000 deaths/yr. On the cost and downtime side, GET (bucket tooth) loss into crushers, conveyor belt rips, poor blast fragmentation and ore/waste misrouting (dilution) are the chronic money sinks.

### Cited Findings

#### Fatality overview
- US 2025: MSHA counted **33** accident-related mining deaths, up 27% from **26 in 2024**. **Powered haulage was the leading cause (13 of 33)**, machinery second (6). 25 were at metal/nonmetal operations and 8 at coal. These figures come from a Pit & Quarry summary of MSHA data surfaced via search; see the MSHA fatality reports index, e.g. [MSHA Dec 18 2025 final report](https://www.msha.gov/data-reports/fatality-reports/2025/december-18-2025-fatality/final-report) and [North American Mining, 18th fatality of 2025](https://northamericanmining.com/index.php/2025/09/03/msha-reports-18th-fatality-of-2025/).
- MSHA issued a safety alert after **10 miners were killed between Jan 3 and Mar 5, 2025**, and described powered haulage as the most common cause of fatal accidents in mining. [AIHA, Mar 27 2025](https://www.aiha.org/news/250327-msha-issues-safety-alert-following-deaths-of-10-miners-in-early-2025)
- A secondary blog claims 13 powered-haulage deaths in 2025 was the highest since 2006. This is unverified against MSHA. [heavyvehicleinspection.com](https://heavyvehicleinspection.com/industries/mining/mining-powered-haulage-safety-fatality-prevention)
- ICMM members (24 companies) in 2024: **42 fatalities** (36 in 2023, 33 in 2022), the third consecutive annual increase. **Mobile equipment/transportation was the #1 hazard: 9 deaths (21%)**, with fall of ground second. South Africa operations accounted for 15 (35%). [Global Mining Review, Jul 2025](https://www.globalminingreview.com/mining/11072025/icmm-reports-2024-safety-performance-of-members/); [Engineering News, Jul 2025](https://www.engineeringnews.co.za/article/icmm-reports-third-consecutive-year-of-increased-fatalities-among-member-companies-2025-07-10)
- ICMM 2025 report: **39 fatalities**, and **34 of the 39 came from four hazards: fall of ground, mobile equipment, working at height, inrush/outburst**. The 2024 total was revised to 43. [Engineering News, Jul 30 2026](https://engineeringnews.co.za/article/icmm-calls-for-further-action-as-fatalities-among-members-remain-relatively-high-2026-07-30); [CIM Magazine 2026](https://magazine.cim.org/en/news/2026/icmm-highlights-the-need-to-strengthen-critical-controls-en/)

#### Problem 1: Haul truck / light vehicle collisions and operator fatigue
- **Persistence:** powered haulage has been the leading US mining killer for many years. MSHA calls it "the most common cause of fatal accidents in mining." [AIHA](https://www.aiha.org/news/250327-msha-issues-safety-alert-following-deaths-of-10-miners-in-early-2025)
- **Scale:** 13/33 US deaths in 2025, and 21% of ICMM member deaths in 2024 (see above).
- **Fatigue sensing:** the Caterpillar Driver Safety System (built on Seeing Machines) had captured **nearly 2 million fatigue and distraction events**. In one trial, **42 fatigue events were recorded in one week across six haul trucks**. Seeing Machines claims Guardian reduces fatigue events by **>94%** (vendor claim; no independent study found). [Mining.com, Cat dealers](https://www.mining.com/web/cat-dealers-delivering-safety-technology-to-reduce-operator-fatigue-and-distraction); [Cat "An eye opener"](https://wwwawsqaext.cat.com/en_US/articles/customer-stories/safety/an-eye-opener.html)
- An Optalert case study (competitor) claims a 98% drop in fatigue alerts and +5% production at a South American mine (vendor). [Optalert](https://www.optalert.com/?p=10211)
- Seeing Machines has a 2025 Mozal (Mozambique smelter/haulage) case study. [Seeing Machines Mozal 2025 PDF](https://seeingmachines.com/wp-content/uploads/2025/10/Case-study-Mozal-2025.pdf)
- 2016 US trucking (not mining) trials: microsleep events fell 100%, 75% and 71% across three fleets. [TruckingInfo](https://www.truckinginfo.com/news/driver-fatigue-distraction-detected-by-guardian-system-from-seeing-machines)
- Recent fatal example: a 63-year-old foreman with 41 years' experience pinned between a tractor and a steel arch support underground (Dec 2025). This shows that experience does not prevent pinning and struck-by events. [MSHA final report](https://www.msha.gov/data-reports/fatality-reports/2025/december-18-2025-fatality/final-report)

#### Problem 2: Fall of ground: underground roof/rib falls
- Historically ground falls caused **nearly 50% of fatalities in US bituminous underground coal**. In 1999 to 2008, roof, rib and face falls caused **nearly 40% of all underground fatalities** (older data). Pillar recovery is ≤10% of underground coal production but **>25% of ground-fall deaths**. [NIOSH Ground Falls](https://www.cdc.gov/niosh/mining/topics/GroundControlOverview.html); [NIOSH ctirgf PDF](https://cdc.gov/NIOSH/mining/UserFiles/works/pdfs/ctirgf.pdf)
- Existing monitoring: microseismic monitoring, mechanical extensometers, load cells, electromechanical roof monitors, plus NIOSH-funded early-warning modules (developers claimed savings exceed module cost). [NIOSH](https://cdc.gov/niosh/mining/topics/ground-falls.html)
- Fall of ground is the **#2 ICMM hazard in 2024** and one of the top-4 hazards behind 34/39 deaths in 2025. [Global Mining Review](https://www.globalminingreview.com/mining/11072025/icmm-reports-2024-safety-performance-of-members/)

#### Problem 3: Pit slope / highwall instability and rockfall
- **Existing sensing:** GroundProbe (Orica) real- and synthetic-aperture slope radars claim **sub-millimetre** movement accuracy. Doppler radar (e.g. RGR-Velox) gives instant rockfall alerts. IDS GeoRadar Guardian "Ai.DA" uses AI to separate real movement from noise and can process up to 6 radars at once. [GroundProbe radar types](https://www.groundprobe.com/?p=19639); [Orica blog 2025](https://www.orica.com/news-and-media/blog/2025/the-different-types-of-radars-in-mining-engineering)
- **Camera-based work:** a 2024 University of Arizona/ARMA paper describes a prototype **thermal-camera rockfall detection/tracking/alarm system** (GroundProbe Tucson) using a security-grade camera costing about **US$8,000**. This shows that camera rockfall detection is viable at a modest hardware cost. [UA ARMA 2024 PDF](https://mining.arizona.edu/sites/default/files/2024-08/2024_Development%20of%20a%20Prototype%20Thermal%20Imaging%20Rockfall%20Detection%20System_Potter_ARMA.pdf)
- An April 2026 trade article reports a next-gen GroundProbe system integrating radar + LiDAR + AI for pit walls and tailings (single-source, unverified). [geomechanics.io](https://www.geomechanics.io/news/article/orica-groundprobe-next-gen-system-slope-monitoring-shifts-explained-for-mine-engineers)
- Slope stability is described as a "risky business" with ongoing tech advances. [E&MJ](https://www.e-mj.com/features/tech-advances-aim-to-tame-the-risky-business-of-slope-stability/)

#### Problem 4: Tailings dam failures
- **Brumadinho (Vale, Jan 2019):** 259 confirmed dead + 11 missing (peer-reviewed 2020). Other sources cite 240 to 270 depending on missing persons. [PMC 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7970857); [Mining.com](https://mining.com/?p=1099113)
- Failure rate has **not improved**: a constant **0.09 failures per billion tonnes** in both 2000–09 and 2010–19. World Mine Tailings Failures forecast 18 "very serious" failures for 2015–2024, the worst decade on record. [Mining.com analysis](https://mining.com/?p=1099113)
- **No complete global registry of tailings dams exists**. Fewer than half of disclosure requests to companies were answered in the post-Brumadinho investor inquiry. [NS Energy](https://www.nsenergybusiness.com/news/tailings-dams-inquiry-mtsi/); [The Conversation](https://theconversation.com/investors-push-for-positive-global-change-in-tailings-management-120904)
- The Global Tailings Review was co-convened by ICMM, UNEP and PRI (it produced the 2020 GISTM standard; outcomes were not captured in my sources). [The Narwhal](https://thenarwhal.ca/global-standards-prevent-mine-tailings-disasters-mount-polleyreport/)

#### Problem 5: GET (bucket tooth) loss jamming crushers
- Canadian gold mine: **US$430K loss per incident** of a tooth jamming the crusher (vendor case study). [Weir Motion Metrics LoaderMetrics PDF](https://www.global.weir/globalassets/resources/product-pdfs/motion-metrics/weir-motion-metrics-loadermetrics.pdf)
- South American iron mine (32 shovels/loaders): **83 teeth lost into the crusher in one year, about 400 h downtime (about 5 h per tooth)** (vendor). [Weir PDF](https://www.global.weir/globalassets/resources/product-pdfs/motion-metrics/weir-motion-metrics-loadermetrics.pdf)
- Studies at copper mines in the US, Chile and Kazakhstan found that missing GET can cause **>120 h crusher downtime/yr** (vendor-cited). [Weir PDF](https://www.global.weir/globalassets/resources/product-pdfs/motion-metrics/weir-motion-metrics-loadermetrics.pdf)
- **Existing products:** Motion Metrics (UBC PhD spin-out, now part of Weir ESCO) ShovelMetrics and LoaderMetrics (2016) use cameras on shovels/loaders for missing-tooth and wear detection. [Mining Technology ShovelMetrics](https://www.mining-technology.com/products/shovelmetrics/); [E&MJ GET advances](https://www.e-mj.com/features/advances-with-ground-engaging-tools-improve-safety-and-availability/); [Coal Age](https://coalage.com/?p=46246); [CIM ML equipment monitoring](https://magazine.cim.org/en/technology/equipment-monitoring-through-machine-learning)

#### Problem 6: Conveyor belt damage (rips) and oversize
- A ripped belt can cost **upwards of AU$100,000** (SICK, a sensor vendor). [SICK](https://www.sick.com/sg/en/solution-solved-on-detecting-holes-rips-and-missing-staples-in-conveyor-belts/w/page_00007XHX)
- A Vale co-authored paper calls missed longitudinal rips "catastrophic" due to financial loss and maintenance-crew risk, and implements **edge-AI rip detection**. [Scitepress 2021](https://www.scitepress.org/Papers/2021/104472/pdf/index.html)
- Vendor claims of US$250K+ per catastrophic tear and US$2.1M in one case are marketing figures. [iFactory](https://ifactoryapp.com/ai-vision-camera/mining-company-prevents-2-1m-conveyor-belt-catastrophic-failure)
- The time between first cut and belt stop determines the length of belt destroyed, so camera → PLC stop latency is the key metric. [Roboflow belt rip](https://roboflow.com/ai/belt-rip-prevention)
- Main technical obstacles: dust, low light, moisture. [Opsio coal conveyor](https://opsiocloud.com/blogs/coal-conveyor-belt-monitoring-vision/)

#### Problem 7: Rock fragmentation after blasting
- **Persistence:** image-based sizing dates to at least 1986 (WipFrag, University of Waterloo). That is 40 years of effort, and accuracy problems still persist. [Similarweb listing for WipFrag app](https://similarweb.com/app/apple/1528397837/vs/1592711060)
- **Fines estimation remains a major source of error** in image analysis. A 2021 deep net on muckpile orthomosaics beat manual labelling on mean percent error. [Bamford et al., IJRMMS 2021](https://www.dynsyslab.org/wp-content/papercite-data/pdf/bamford-ijrmms21.pdf)
- A 2024 *Minerals* paper used Segment Anything (SAM) for fragment segmentation and **outperformed Split-Desktop 4.0** on its test set. [SAM fragmentation paper](https://bohrium.dp.tech/paper/arxiv/0e4f5bd9ffbbd1ba2c75117b539342a57e42c4c3f6e92395c7cfb88291a7fba2)
- 2025 arXiv: automated deep segmentation + spatial statistics for post-blast fragmentation; RIT structure-aware segmentation work. [arXiv 2507.20126](https://arxiv.org/abs/2507.20126v1); [RIT](https://www.rit.edu/dirs/research/structure-aware-segmentation-post-blast-rock-fragmentation-analysis)
- Orica FRAGTrack (part of BlastIQ) uses binocular cameras + hybrid 2D/3D on face shovels and conveyors (vendor claims accuracy, no independent numbers). [Mining.com](https://www.mining.com/web/new-orica-digital-fragmentation-measurement-technology-key-unlocking-downstream-benefits/)
- Roboflow hosts public rock-fragmentation models and datasets, a starting point for small teams. [Roboflow](https://roboflow.com/ai/rock-fragmentation-analysis)

#### Problem 8: Ore vs waste discrimination, dilution, grade control at the face
- MineSense ShovelSense (bucket-mounted XRF/EM sensors): across **9 open-pit copper mines (2023)**, each system diverted **5.9% of measured trucks from ore→waste** and **7.2% from waste→ore**. Shifts with 80 to 100% coverage saw **+4% recovery and +8% more Cu in concentrate** vs <20% coverage. [CIM 2024](https://cim.org/news/2024/minesense)
- Freeport Chino: **>10% truck diversions** at high-contrast contacts. [MineSense](https://minesense.com/?p=927)
- The scale of the misclassification (about 13% of trucks combined) shows that block-model grade control misroutes a large share of material. That is the dilution/ore-loss problem. Benefits depend on ore-body contrast. [CIM 2024](https://www.cim.org/industry-partners/spotlights-2024/minesense/)
- Bulk-sorting value prediction validated against ShovelSense diversions at a Cu porphyry. [Queen's 2022 PDF](https://geomet.engineering.queensu.ca/wp-content/uploads/2022-07-Faraj-Bulk-Ore-Sorting-web.pdf)

#### Problem 9: Misfires, flyrock and blast hazards
- Surface blasting injury causes (US, 1978–1993, old data): **lack of blast-area security, flyrock, premature blasts, misfires**. [GroundProbe BlastVision article](https://www.groundprobe.com/?p=17740)
- At Anglo American surface mines, blast video review showed **minor flyrock exceedances occur much more frequently than reported**. This is direct evidence that cameras reveal hidden risk. [IIMP WMC Track 6](https://iimp.org.pe/WMC/actas/Track-6-Mining-Engineering-and-Mine-Planning/81/)
- GroundProbe BlastVision: a high-speed camera on a UAV detects misfired holes, out-of-sequence firing, stemming ejection and flyrock tracking. [Orica BlastVision](https://www.orica.com/digital-solutions/geosolutions/groundprobe/blastvision); [Australian Manufacturing](https://www.australianmanufacturing.com.au/groundprobe-launches-blastvision-a-world-first-in-blast-analytics/)

#### Problem 10: Dust (silica / coal) and gas
- Black lung affects **about 20% of tenured Central Appalachian coal miners** (highest in 25+ years), with 1 in 20 having the most severe form (PMF). One cited cause is cutting more quartz-bearing rock in thinner seams. [WKYU, Aug 2026](https://www.wkyufm.org/2026-08-21/high-rates-of-black-lung-disease-have-coal-miner-advocates-demanding-action); [Yale e360](https://e360.yale.edu/features/black-lung-pennsylvania)
- MSHA 2024 silica rule halves the PEL to **50 µg/m³** (from 100), but **federal courts stayed enforcement**, and a new MSHA proposal is awaited as of 2026. [Hoptown Chronicle](https://hoptownchronicle.org/?p=85379); [WKYU 2026](https://www.wkyufm.org/2026-08-21/high-rates-of-black-lung-disease-have-coal-miner-advocates-demanding-action)
- Upper Big Branch (2010, methane + coal-dust explosion, 29 dead): 71% of 24 autopsied miners had black lung. [Reimagine Appalachia](https://reimagineappalachia.org/help-protect-miners-from-black-lung-disease/)

#### Problem 11: Drill-hole and core logging
- Datarock: ML/CV on standard **RGB core photos** produces fracture logs, RQD, vein orientation and chip analysis, and claims **up to 80% faster** consistent logging (vendor). It converted **45,000 m** of historical core imagery at one customer. [Datarock](https://datarock.com.au/rethinking-geological-logging-through-a-machine-learning-lens/); [Datarock AI vs expert](https://datarock.com.au/advance-gold-mine-plans-landingpage/); [AEGC 2023 paper](https://zenodo.org/records/7980756/files/AEGC_2023_ID226.pdf)
- Hyperspectral core scanning is fast and non-destructive. Maximum value requires acquisition soon after drilling and real-time on-site processing. [GTK Finland](https://www.gtk.fi/en/current/hyperspectral-technology-enhances-the-quality-and-accuracy-in-drill-core-loggings/); [Frontiers 2024](https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2024.1433662/full)
- Manual logging is inconsistent between geologists, which is why "consistent, audit-ready" outputs are the selling point. [Datarock "Crossing the chasm"](https://datarock.com.au/reflections-on-crossing-the-chasm/)

#### Problem 12: Artisanal and small-scale mining (ASM) hazards
- About **45 million** people work in ASM (World Bank Delve). A rough extrapolation gives **about 30,000 deaths/yr**, but **no comprehensive ASM fatality database exists**. [World Bank 2021](https://www.worldbank.org/en/news/opinion/2021/10/19/opinion-to-achieve-decent-work-we-must-improve-the-health-and-safety-of-hidden-artisanal-miners); [Delve "How unsafe is ASM"](https://www.delvedatabase.org/resources/how-unsafe-is-asm-counting-and-contextualizing-fatality-frequency-rates)
- DRC: unofficial estimates up to 2,000 ASM deaths/yr. India 2018: official 120, possibly up to 20,000. Ghana: 622 deaths over 14 years. [Delve PDF](https://delvedatabase.org/uploads/resources/2020-SoS_OHS-1_How-unsafe-is-ASM.pdf)
- Ground collapse dominates: Zimbabwe Q1 2026 collapses caused **54% of mining deaths (35)**. Early 2024 saw **>70 dead in Mali** and **>100 in Venezuela (Bulla Loca)**. [Ziyah News](https://ziyahnews.co.zw/zimbabwe-records-64-artisanal-mining-deaths/); [The Ethos](https://the-ethos.co/artisanal-mine-collapses-renew-focus-on-where-gold-comes-from/)

### Inferences
- Ranking by deaths (industrial mining): mobile equipment/powered haulage > fall of ground (underground roof/rib + slope) > other hazards (working at height, inrush/outburst, machinery). By total deaths globally, ASM likely dwarfs industrial mining, but the data is extrapolated.
- Ranking by low-frequency/catastrophic risk: tailings dams (hundreds dead per event, constant failure rate).
- Ranking by chronic operational cost: dilution/ore loss (about 13% of trucks misrouted where sensors are installed), GET-into-crusher (hundreds of hours/yr per site), belt rips (AU$100K+ per event), and poor fragmentation (downstream crusher/mill energy, not quantified in my sources).
- Long-term chronic disease (silicosis/black lung) is a large and growing killer that sits outside "accident" statistics. It is regulatorily stalled in the US as of 2026.

### Gaps
- MSHA's 2024 fatality breakdown by category and the official 2025 classification table were not fetched directly. The 13/33 powered-haulage figure comes via a Pit & Quarry summary and should be checked at msha.gov.
- No independent (non-vendor) cost figures for GET loss, belt rips or fatigue reduction.
- No quantified global cost of poor fragmentation (energy/throughput) found in this session.
- No current global methane-explosion fatality numbers. Recent major coal-mine explosions (e.g. Turkey, China, Kazakhstan, Colombia) were not researched.
- Global Tailings Review/GISTM implementation status as of 2026 was not captured.

---

## Key Question 2: What sensing exists today, and where are the gaps?

### Takeaway
Mature, expensive, vendor-locked sensing exists for nearly every problem: slope radar (GroundProbe, IDS), fatigue cameras (Seeing Machines/Cat DSS, Optalert), GET cameras (Motion Metrics/Weir), bucket XRF/EM grade sensing (MineSense), fragmentation (WipFrag, Split, FRAGTrack), drone blast video (BlastVision), and core photo ML (Datarock). The gaps are cost and coverage (tier-1 mines only), dust/lighting robustness, fines/occlusion accuracy, lack of independent validation, siloed data, and almost no sensing for ASM or small quarries.

### Cited Findings
- **Slope:** radar gives sub-mm accuracy, Doppler rockfall alerts, and AI noise filtering (Ai.DA). A thermal camera rockfall prototype uses a about US$8K camera, which shows cameras complement radar for rockfall *tracking*. [GroundProbe](https://www.groundprobe.com/?p=19639); [UA ARMA 2024](https://mining.arizona.edu/sites/default/files/2024-08/2024_Development%20of%20a%20Prototype%20Thermal%20Imaging%20Rockfall%20Detection%20System_Potter_ARMA.pdf)
- **Fatigue:** in-cab eye/face tracking (Seeing Machines Guardian; Cat DSS) and Optalert (eyelid IR glasses). Vendor claims are >94% and 98% reductions, with no independent study found. [Mining.com](https://www.mining.com/web/cat-dealers-delivering-safety-technology-to-reduce-operator-fatigue-and-distraction); [Optalert](https://www.optalert.com/?p=10211)
- **GET:** camera-based missing-tooth/wear detection on shovels and loaders (Motion Metrics, since about 2016 for loaders). Weir ESCO now bundles it with its GET products, a vendor tie-in. [Weir PDF](https://www.global.weir/globalassets/resources/product-pdfs/motion-metrics/weir-motion-metrics-loadermetrics.pdf); [E&MJ](https://www.e-mj.com/features/advances-with-ground-engaging-tools-improve-safety-and-availability/)
- **Grade/ore sorting:** MineSense bucket sensors. Value depends on ore-body contrast. Reported deployments are copper-heavy (9 Cu mines). [CIM 2024](https://cim.org/news/2024/minesense)
- **Fragmentation:** 2D tools (WipFrag since 1986, Split-Desktop), 3D stereo (FRAGTrack). Known weakness: **fines estimation**. SAM-based research already beats Split-Desktop 4.0 on test data. [Bamford 2021](https://www.dynsyslab.org/wp-content/papercite-data/pdf/bamford-ijrmms21.pdf); [SAM paper](https://bohrium.dp.tech/paper/arxiv/0e4f5bd9ffbbd1ba2c75117b539342a57e42c4c3f6e92395c7cfb88291a7fba2)
- **Blast:** UAV high-speed video for misfire/flyrock (BlastVision). Video review revealed flyrock exceedances are under-reported. [Orica BlastVision](https://www.orica.com/digital-solutions/geosolutions/groundprobe/blastvision); [IIMP WMC](https://iimp.org.pe/WMC/actas/Track-6-Mining-Engineering-and-Mine-Planning/81/)
- **Conveyor:** line-scan/area cameras and laser sensors for rips, holes and staples (SICK). Edge-AI rip detection was trialled with Vale. Accuracy claims (95%+) are vendor-only, and dust and light are the main problems. [SICK](https://www.sick.com/sg/en/solution-solved-on-detecting-holes-rips-and-missing-staples-in-conveyor-belts/w/page_00007XHX); [Scitepress](https://www.scitepress.org/Papers/2021/104472/pdf/index.html)
- **Underground ground control:** extensometers, load cells, microseismic and electromechanical roof monitors. Wider use of rib bolting, roof screen and inside-control bolters is still recommended, which implies an adoption gap. [NIOSH](https://cdc.gov/niosh/mining/topics/ground-falls.html)
- **Core logging:** RGB photo ML (Datarock) and hyperspectral scanners. Hyperspectral value depends on fast on-site processing. [Datarock](https://datarock.com.au/rethinking-geological-logging-through-a-machine-learning-lens/); [Frontiers 2024](https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2024.1433662/full)
- **Tailings:** no global registry; disclosure is weak. Radar + LiDAR + AI for tailings was reportedly launched in 2026 (unverified). [NS Energy](https://www.nsenergybusiness.com/news/tailings-dams-inquiry-mtsi/); [geomechanics.io](https://www.geomechanics.io/news/article/orica-groundprobe-next-gen-system-slope-monitoring-shifts-explained-for-mine-engineers)
- **ASM:** no fatality database; "no way to validate worldwide figures." [Delve](https://www.delvedatabase.org/resources/how-unsafe-is-asm-counting-and-contextualizing-fatality-frequency-rates)

### Inferences
- Pattern: each tool is a single-purpose, per-machine hardware sale priced for tier-1 miners. Mid-tier mines, quarries/aggregates (a large share of MSHA metal/nonmetal deaths) and ASM are underserved.
- Most performance claims (94%, 98%, 80% faster, 95%+ accuracy) are vendor-reported. An open benchmark/dataset would itself be a contribution.
- Foundation vision models (SAM, open-vocabulary detectors) have only reached mining in research papers so far (fragmentation). Commercial products mostly predate them.
- Tailings monitoring is the biggest disclosure/data gap. Satellite InSAR + optical change detection over *all* dams (including undisclosed ones) is a plausible open-data play, but this was not researched here.

### Gaps
- Pricing for commercial systems (radar, ShovelMetrics, Guardian, MineSense) was not found.
- No independent field accuracy for FRAGTrack/WipFrag, conveyor AI or GET cameras.
- Proximity detection / collision avoidance systems (CAS) and MSHA's surface mobile equipment written-safety-program rule were not researched in this session. Status and gaps of CAS should be checked.
- Gas monitoring (methane detectors, tube bundle) and real-time dust monitors (CPDM) were not specifically researched.

---

## Key Question 3: Where are the clearest openings for camera- or cheap-sensor AI (and small-team feasibility)?

### Takeaway
The best openings for a small team are problems with (a) visible, image-based signals, (b) public data or easy synthetic data, and (c) an incumbent that is expensive or hardware-locked. These are fragmentation from phone/drone photos, GET missing-tooth detection, conveyor rip/oversize detection, blast-video misfire/flyrock analytics, core-photo logging, and fatigue/proximity alerts on commodity hardware. ASM collapse warning is the highest-impact but hardest-to-deploy opening.

### Cited Findings
- SAM-based segmentation already beats commercial Split-Desktop 4.0 on a test set, so foundation models lower the barrier for fragmentation tools. [SAM paper](https://bohrium.dp.tech/paper/arxiv/0e4f5bd9ffbbd1ba2c75117b539342a57e42c4c3f6e92395c7cfb88291a7fba2)
- Public rock-fragmentation and belt-rip models and datasets exist on Roboflow Universe. [Roboflow fragmentation](https://roboflow.com/ai/rock-fragmentation-analysis); [Roboflow belt rip](https://roboflow.com/ai/belt-rip-prevention)
- The thermal rockfall prototype uses an about US$8K off-the-shelf security camera, so cheap-camera slope/rockfall work is feasible. [UA ARMA 2024](https://mining.arizona.edu/sites/default/files/2024-08/2024_Development%20of%20a%20Prototype%20Thermal%20Imaging%20Rockfall%20Detection%20System_Potter_ARMA.pdf)
- Edge-AI rip detection was implemented in a Vale-linked study, so commodity edge hardware is adequate. [Scitepress](https://www.scitepress.org/Papers/2021/104472/pdf/index.html)
- Datarock works on ordinary RGB core photos, and decades of core-tray photos sit in mine archives (45,000 m in one case). [Datarock](https://datarock.com.au/advance-gold-mine-plans-landingpage/)
- Blast videos already reveal under-reported flyrock, so automating that review is a clear task. [IIMP WMC](https://iimp.org.pe/WMC/actas/Track-6-Mining-Engineering-and-Mine-Planning/81/)

### Inferences
Feasibility for a hackathon / small startup team. These ratings are my judgment, not sourced.

| Problem | Visual-AI / sensor approach | Incumbents | Gap | Small-team feasibility |
|---|---|---|---|---|
| Rock fragmentation | Phone/drone photo → SAM segmentation → PSD curve (P50/P80), scale via reference object | WipFrag, Split, FRAGTrack | Fines error, occlusion, cost, 3D scaling | **High** (public datasets, SAM works) |
| GET / bucket tooth loss | Camera on bucket/loader or at crusher feed: tooth count/missing detection, metal-in-feed detection | Motion Metrics/Weir | Tied to Weir GET; retrofit cost | **High** for a demo (object detection); hard to field (vibration, dust) |
| Conveyor rip / oversize / tramp metal | Line-scan or area camera + edge model → PLC stop; oversize rock sizing on belt | SICK, belt-specific vendors | Dust/light robustness, no independent accuracy data | **High** (demo); medium (field) |
| Blast video: misfire / flyrock / fume | Drone video → explosion-sequence detection vs blast plan, flyrock trajectory tracking | BlastVision | Proprietary; review often manual | **Medium-High** |
| Core logging | RGB tray photo → RQD, fracture count, lithology classes | Datarock, hyperspectral scanners | Geologist inconsistency; legacy archives | **High** (pure image ML) |
| Operator fatigue/distraction | Commodity IR camera + face-landmark eye-closure (PERCLOS) model | Seeing Machines, Optalert, Cat DSS | Cost for small fleets/quarries | **High** (demo); regulatory/trust bar high |
| Haul-road collisions / proximity | Camera-based person/vehicle detection for blind spots on haul trucks and LVs | CAS/proximity systems (not researched) | Blind spots, small operators | **Medium** |
| Slope/highwall rockfall | Fixed camera / time-lapse change detection + optical flow; thermal for night | GroundProbe, IDS radar | Radar cost; cameras weather-limited | **Medium** |
| Tailings dam monitoring | Satellite optical/SAR change detection (seepage, beach width, cracks), drone photogrammetry | Radar/InSAR services | No global registry; weak disclosure | **Medium** (open satellite data); impact high |
| Ore/waste discrimination | Face photo / hyperspectral → ore class; combined with grade sensors | MineSense (XRF/EM), hyperspectral | Contrast-dependent; RGB alone is weak for grade | **Low-Medium** (needs assays for labels) |
| Underground roof/rib | Photogrammetry/LiDAR change detection on rib/roof, crack detection from cap-lamp or vehicle cameras | Extensometers, microseismic | Dark, dusty; adoption gap | **Low-Medium** |
| Dust/gas | Cheap optical PM sensors + camera-based dust-plume detection | CPDM, fixed gas detectors | Silica-specific sensing is hard | **Low** (silica needs lab/FTIR) |
| ASM collapse/hazard | Phone app: pit-wall photo → crack/overhang hazard score; satellite mapping of ASM sites | Essentially none | No data, no connectivity, no buyer | **Medium** (tech), **Low** (deployment/business) |

- Strongest hackathon picks: (1) fragmentation from photos, (2) GET missing-tooth / metal-in-crusher-feed detection, (3) conveyor rip/oversize, (4) core-photo RQD. Each has visible targets, public or synthetic data, and quantified economics (US$430K/GET incident; AU$100K+/belt rip; 5 h downtime per lost tooth).
- Strongest *impact* picks: haul-truck blind-spot/fatigue for small quarries (powered haulage is the #1 US killer), and ASM pit-wall hazard scoring (collapses cause about 54% of Zimbabwe's mining deaths).

### Gaps
- No interviews or buyer data on willingness to pay among mid-tier mines/quarries.
- Public dataset availability for GET, underground roof imagery and tailings was not verified (only fragmentation and belt-rip were confirmed on Roboflow).
- No research on regulatory acceptance (e.g. whether MSHA credits camera-based CAS).
