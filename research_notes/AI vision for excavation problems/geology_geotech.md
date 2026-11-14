# Geology, Geotechnical Engineering and Site Investigation: Long-Standing Problems That Visual AI or Sensors Could Address

Notes compiled 2026-11-14. Research budget was tight (about 17 tool calls), so several figures are secondhand or dated; each is flagged. Feasibility ratings for a small team (hackathon or startup) are my own judgement and appear only under Inferences.

## Q1. How much do unforeseen ground conditions cost? (studies giving a % of claims or of overruns)

### Takeaway
Ground risk is a persistent, well-documented driver of claims, but a clean global "% of all overruns" figure does not exist. The best numbers are: (a) HKA's claims database, where "unforeseen physical conditions" affected about 18-30% of projects depending on region and sector; (b) US highway data (NCHRP 2016), where geotechnical overruns average about 3% of contract cost against about 1% spent on site investigation; and (c) tunnelling, where a US study of 87 tunnels found claims equal to about 12% of construction cost. Under-investment in site investigation is the recurring root cause.

### Cited Findings
- HKA's analysis of more than 1,800 capital projects worldwide (US$2.2 trillion CAPEX) found disputes costing more than US$91.3 billion. Claimed costs averaged 33.6% of committed CAPEX, and schedule overruns averaged about 16 months (67.1% of planned schedule). These figures cover all claim causes, not ground conditions alone. — [Seequent, citing HKA CRUX report](https://www.seequent.com/why-do-unforeseen-site-conditions-continue-to-impact-civil-projects/)
- In HKA's data, "unforeseen physical conditions" rank #4 among claim causes in the Americas and #9 worldwide. Scope change ranks #1. — [Seequent / HKA](https://www.seequent.com/why-do-unforeseen-site-conditions-continue-to-impact-civil-projects/)
- HKA CRUX: unforeseen physical conditions affected 29.6% of projects in Canada and 18.5% in the US, 24.1% of buildings projects and 21.4% of transportation projects. (Search-snippet level; full report not opened.) — [HKA](https://www.hka.com/article/designs-on-better-outcomes-getting-to-the-crux-of-time-and-cost-overruns-on-capital-projects/)
- US highways (NCHRP synthesis, 2016): geotechnical overruns averaged about 3% of contract cost, against an average of about 1% of contract cost spent on site investigation. Subsurface-related change orders approach about 1% of agencies' total new-construction budgets. — [National Academies Press, NCHRP (book 21926)](https://www.nap.edu/read/21926/chapter/2) (secondhand via search snippet; the page redirected and was not opened)
- UK (Mott MacDonald and Soil Mechanics Ltd, 1994), 58 transport projects: no direct correlation was found between site-investigation spend and overrun, but modest increases in site-investigation spend as a % of the award "significantly decreased the probability of overruns". This is old data, cited secondhand. — [Boutsis et al. 2020, Infrastructures (White Rose eprint)](https://eprints.whiterose.ac.uk/id/eprint/185999/1/infrastructures-05-00073-v2.pdf)
- Tunnelling: the USNCTT study of 87 tunnel projects found claims equal to about 12% of overall construction cost (Gould 1995, dated). The Channel Tunnel overran by 78% in total cost, 66% in construction cost and 77% in tunnelling cost, partly attributed to ground and ground-investigation issues. — [Boutsis et al. 2020, MDPI Infrastructures 5(9):73](https://www.mdpi.com/2412-3811/5/9/73)
- Ground-related factors "have often been the origin of contractual claims with significant time and cost overruns" (Hytiris et al. 2014). — [WIETE 2014](http://www.wiete.com.au/journals/WTE&TE/Pages/Vol.12,%20No.3%20(2014)/15-Hytiris-N.pdf)
- A counter-view: "unforeseen ground conditions" are often blamed for overruns when the real cause is planners who systematically underestimate or ignore known risk. — [arXiv 1901.11123](https://arxiv.org/pdf/1901.11123)
- An ISSMGE compilation of overrun-factor studies places ground-related risks high in several rankings, for example a South African study. — [ISSMGE](https://www.issmge.org/uploads/publications/1/141/617.pdf)

### Inferences
- The economics come down to a ratio: about 1% of contract spent on site investigation is followed by about 3% in geotechnical overruns (US highways), and roughly 12% claims in tunnels. Anything that makes investigation data cheaper, denser or more consistent attacks the cause directly. The pitch "turn the 1% into better information" is defensible.
- The problem has persisted for more than 30 years (Mott MacDonald 1994, USNCTT, the Channel Tunnel in the 1990s, HKA in the 2020s), which suggests the bottleneck is structural (cost and sparsity of subsurface sampling, contractual risk allocation), not a lack of awareness.

### Gaps
- I could not open the original HKA CRUX report or the NCHRP synthesis to verify the region and sector percentages or methods. The well-known UK claim that "ground is the largest single source of risk" (Institution of Civil Engineers / Site Investigation Steering Group, "Without site investigation ground is a hazard", 1991-93) was not found in a citable source this session.
- No reliable global $/year figure exists for ground-related overruns.

## Q2. What has been tried, problem by problem, and where does it fall short?

### Takeaway
Every sub-problem has 10-40 years of research behind it and at least one commercial attempt. The common failures are: (1) systems that are expensive and lab- or truck-bound (hyperspectral core scanners, InSAR processing, DAS interrogators); (2) accuracy claims that are vendor-reported and site-specific, with no independent benchmarks; (3) ML models trained on small, region-specific datasets that do not use engineering classification schemes (USCS, RMR/Q/GSI); and (4) poor field usability. Cheap-camera and edge-AI tools for the field geologist or engineer remain underserved.

### Cited Findings

#### 2a. Subsurface uncertainty: sparse boreholes and interpolation between them
- Problem: boreholes sample a tiny fraction of the ground volume, and stratigraphy between holes is interpolated by hand or by kriging. US highway practice spends about 1% of contract cost on site investigation (see Q1). — [NCHRP via NAP](https://www.nap.edu/read/21926/chapter/2)
- Research methods that quantify stratigraphic uncertainty from sparse boreholes:
  - XGBoost with geological priors (CityU Hong Kong patent). — [CityU](https://www.cityu.edu.hk/kto/industry/find-new-opportunities-our-ip-portal-0/g/generation-three-dimensional-geological-model)
  - Markov random field, Bayesian ML and image-warping stochastic simulation (2025). — [Frontiers in Built Environment 2025](https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2025.1651919/pdf)
  - GANs trained on 3D training images, where adding geophysics helps. — [ISSMGE](https://www.issmge.org/uploads/publications/1/141/1090.pdf)
  - Semi-supervised deep learning with pseudolabels for sparsely drilled urban areas. — [GMD preprint gmd-2023-11](https://gmd.copernicus.org/preprints/gmd-2023-11/gmd-2023-11-ATC3.pdf)
  - Bi-LSTM with dense CRF. — [PolyU](https://ira.lib.polyu.edu.hk/bitstream/10397/116457/1/Liu_Probabilistic_Stratigraphic_Modelling.pdf)
- Shortfall: most of this work is preprints, conference papers or patents, often benchmarked on simulated sites, so real-site performance is unproven. — (same sources, synthesis)
- Commercial: Seequent (Leapfrog) frames unforeseen site conditions as a modelling and data-integration problem. — [Seequent](https://www.seequent.com/why-do-unforeseen-site-conditions-continue-to-impact-civil-projects/)

#### 2b. Manual drill-core logging (RQD, lithology, fractures)
- Datarock (Australia) automates RQD and recovery from core-tray photos. It claims 30,000 m of RQD generated in about 15 minutes and a customer that "replaced all previous manual RQD and Recovery", but it publishes no accuracy figures. — [Datarock](https://datarock.com.au/); [Coring Magazine](https://coringmagazine.com/article/datarock-bespoke-solution-ai-mining/); [International Mining 2020](https://im-mining.com/2020/06/10/datarock-machine-learning-drill-core-analysis-tool-hits-major-milestone/)
- Datarock itself describes geotechnical logging as "inherently subjective", varying with experience, training, judgement and site familiarity (vendor source). — [Datarock help: QA/QC predicted vs manual](https://help.datarock.com.au/knowledge-base/how-to-qa-qc-predicted-and-manually-logged-geotech-data)
- Minalyze (Minalyzer CS: XRF plus imagery plus core topography) supports semi-automatic RQD. In the LKAB trial with Sentian AI, the partners claimed evaluation time fell "from weeks to minutes, with increased accuracy" (partner claim). — [International Mining 2021](https://im-mining.com/2021/12/14/lkab-starts-core-logging-automation-digitalisation-process-with-minalyzer-cs/)
- Corescan, now "Powered by Epiroc", does hyperspectral mineralogy plus laser-profile RQD. An academic methodology paper on Corescan laser data reported average RQD error of 2.58% (540 sandstone core rows) and 3.17% (90 limestone rows). This is a preliminary method paper. — [Corescan](https://corescan.com.au/services/hyperspectral-mineralogy/); [ResearchGate methodology paper](https://www.researchgate.net/publication/304478208_Proposed_Methodology_for_Utilising_Automated_Core_Logging_Technology_to_Extract_Geotechnical_Index_Parameters)
- Veracio (formerly Boart Longyear) also markets core-scanning products. — [Veracio brochure 2024](https://www.veracio.com/wp-content/uploads/2025/05/CoreScanning_Oct24_Digital.pdf)
- Human variability: the core-logging case study by Morrell and Pere (2023) reports logger expertise ranging "from low to very high", with "significant potential for variability" in captured data. — [ACG Morrell](https://papers.acg.uwa.edu.au/d/2335_36_Morrell/36_Morrell.pdf)
- Mechanical (drilling-induced) breaks logged as natural fractures artificially lower RQD. This is a classic judgement error. — [ACG Lawrence](https://papers.acg.uwa.edu.au/d/2535_45_Lawrence/45_Lawrence.pdf)
- Observer bias in fracture data is measurable across four common sampling approaches. — [Solid Earth 10:487, 2019](https://se.copernicus.org/articles/10/487/2019/se-10-487-2019.pdf)
- RQD itself (Deere, 1960s) is contested; see "RQD: Time to Rest in Peace" (2016). — [Geotechpedia](https://geotechpedia.com/Publication/Show/4893/RQD--TIME-TO-REST-IN-PEACE)
- Shortfall: vendors focus on mining (high core volumes, rich clients) and on lab or scanner hardware. Accuracy claims are vendor-reported. Civil and geotechnical site-investigation core (small jobs, soil plus rock) is largely unserved.

#### 2c. Field soil classification (visual-manual USCS, ASTM D2488)
- D2488 is explicitly a non-laboratory method. When precise classification is needed, D2487 (lab) "shall be used". Its precision "is dependent on the competence of the personnel". Its stated value is grouping samples so that only a minimum number of lab tests is needed. The current edition is D2488-26. — [ASTM D2488-26](https://store.astm.org/d2488-26.html); [ASTM D2488-00 text](https://softbank.iust.ac.ir/Railway/Codes/ASTM-standard/ASTM_2004_Standards/ASTM%202004%20PART%20IB/ASTM%202004%20Volume%2004.08%20Soil%20and%20Rock%20(I)%20D%20420%20-%20D%205611/D%202488%20-%2000%20%20_RDI0ODG_.pdf)
- University teaching practice runs lab tests only on selected samples to verify the field call, and some D2488 checks (for example the HCl reaction) are skipped in practice. — [U. Alabama CE340 lab manual](https://adhc.lib.ua.edu/ce340/wp-content/uploads/2021/05/Geotechnical_Laboratory_Manual.pdf)
- Smartphone and CNN soil classification exists, but on agronomic or regional classes, not USCS:
  - Soil-MobiNet: about 93% test accuracy on 9 Indian soil types. — [MDPI Sensors 23(15):6709, 2023](https://mdpi.com/1424-8220/23/15/6709)
  - Light-SoilNet: 97.2%, weaker on loam, sandy loam and loamy sand. — [Bohrium](https://www.bohrium.com/paper-details/smart-soil-image-classification-system-using-lightweight-convolutional-neural-network/949164356296245375-2452)
  - Texture CNNs: about 99.6-99.9% at 20-60 cm photo distance, on custom data. — [MDPI AgriEngineering 5(1):23](https://mdpi.com/2624-7402/5/1/23)
  - An iPhone 7 study on clay, sand and gravel used only 60 verification images. — [Bohrium](https://www.bohrium.com/paper-details/artificial-intelligence-system-for-supporting-soil-classification/812533954262335488-64194)

#### 2d. Rock mass characterisation (joint mapping, RMR/Q/GSI) from outcrops and cut faces
- Battulwar et al. (2021) state-of-the-art review: "not one single method" automatically characterises discontinuities accurately in minimal time, and there is a gap in efficient block-size computation from 3D models. — [JRMGE 2021 (DOAJ)](https://doaj.org/article/7af71d1eca944c3999deab74c9af47dc)
- Daghigh et al. (2022) critical review of discontinuity-plane extraction from photogrammetry or LiDAR point clouds lists persistent challenges. — [TU Delft repository](https://research.tudelft.nl/files/146852197/1_s2.0_S009830042200190X_main.pdf)
- Deep-learning pipelines combine point-cloud classification, RANSAC plane fitting and DBSCAN clustering into joint sets (NIOSH-funded Battulwar dissertation). — [CDC Stacks](https://stacks.cdc.gov/view/cdc/207475)
- Newer work: synthetic point clouds with PointNet++ to work around the shortage of labels, and point-voxel-point networks from XYZ-only input. — [Bull. Eng. Geol. Env. 2024](https://springerlink.bibliotecabuap.elogim.com/content/pdf/10.1007/s10064-024-03658-1.pdf); [J. Central South Univ. 2026](https://journal.hep.com.cn/jocsu/EN/10.1007/s11771-026-6391-2)
- Remaining issues: dependence on labelled data, sensitivity to point-cloud quality, poor automation of roughness, persistence and block size, and poor inter-operator replicability even for lineament interpretation (Scheiber et al. 2015, six operators). — [Solid Earth 2019 supplement](https://se.copernicus.org/preprints/se-2018-135/se-2018-135-AC3-supplement.pdf)

#### 2e. Tunnelling face and TBM rock-mass assessment
- A TBM-mounted camera with a self-convolution attention fusion network classifies rock mass condition from muck images, reported as "accurate and efficient" in field tests. — [Sci. Reports 2022, Chen et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8810907/)
- CNN classification of conveyor-belt muck fragments, and muck block morphology correlated with fracturing and TBM thrust per revolution. — [x-mol / TUST](https://www.x-mol.com/paperRedirect/1361468803448606720); [Bohrium](https://bohrium.dp.tech/paper/arxiv/e43e2d7ff9dcdfc728faee43d249131eed58d538ba269cd106e724b491bd8d13)
- Rock mass integrity grade from fragment images with an SE-Inception-VGG19 network (2025). — [HEP journal 2025](https://journal.hep.com.cn/sue/EN/10.1016/j.sue.2025.10.001)
- Shortfall: these remain research prototypes, largely from Chinese TBM projects. I found no commercial product or drill-and-blast face-mapping product in this search.

#### 2f. Landslides and slope failure: detection and early warning
- Scale: about US$20 billion per year average economic loss (about 17% of US$121 billion yearly global disaster losses, 1980-2013). More than 55,000 deaths in 2004-2016, excluding seismically triggered landslides. — [Geoenvironmental Disasters 2022 review](https://link.springer.com/article/10.1186/s40677-022-00205-6)
- InSAR limits:
  - Geometric distortion, decorrelation, atmospheric delay, and difficulty with 3D motion. — [PMC review](https://pmc.ncbi.nlm.nih.gov/articles/PMC13468315/)
  - Not competitive alone as a real-time early-warning system because of the 6-12 day revisit. — [MDPI Remote Sensing 18(7):1081](https://www.mdpi.com/2072-4292/18/7/1081)
  - Unwrapping errors cause "severe underestimations", and rapid shallow failures can occur with "little to no detectable warning". — [NHESS 26:863, 2026 (Achoma, Peru)](https://nhess.copernicus.org/articles/26/863/2026/)
  - Detection depends on slope orientation, rate, vegetation and resolution. — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1878522015003768)
- In-situ landslide early-warning systems dominate, but their "high cost makes it impractical to monitor all the landslides". — [Eng. Geology 2024](https://www.sciencedirect.com/science/article/abs/pii/S0013795224003715)
- ML on InSAR: InSAR-YOLOv8 for wide-area detection. — [Sci. Reports 2024](https://www.nature.com/articles/s41598-024-84626-3)
- Fibre optics: distributed sensing in trenches or boreholes can detect precursory movement and covers large areas at high frequency. Brillouin extenso-inclinometers give centimetric strain resolution (EGU26). FBG plus MEMS hybrids are described as cost-effective (Xinpu landslide). — [Frontiers Earth Sci 2025](https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2025.1570413/text); [EGU26-18343](https://meetingorganizer.copernicus.org/EGU26/EGU26-18343.html); [Geoscience Frontiers 2024](https://doaj.org/article/8da9eafbee824c61af99551e65ae99fe)
- Cost data points: a MEMS multi-module inclinometer at about €70/m; coaxial cable about 55% cheaper than an inclinometer casing. — [encyclopedia.pub](https://encyclopedia.pub/entry/54174)
- Low-cost IoT slope monitoring is a research field (Darjeeling Himalayas). — [PMC7273224](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7273224/)

#### 2g. Sinkholes and karst
- US karst and sinkhole damage averages at least US$300 million per year, "probably much lower than the actual cost" because there is no national tracking. Older FEMA (1997) figure: at least US$125 million per year for all subsidence. — [USGS FAQ](https://usgs.gov/faqs/how-much-does-sinkhole-damage-cost-each-year-united-states); [USGS publication 70155910](https://pubs.usgs.gov/publication/70155910)
- Few states track costs, none does at federal level, and insurance data is not available. Karst occurs in 48 states, with the worst damage in FL, TX, AL, MO, KY, TN and PA. — [USGS](https://www.usgs.gov/publications/cost-karst-subsidence-and-sinkhole-collapse-united-states-compared-other-natural)

#### 2h. Expansive soils (and liquefaction)
- Expansive soils: at least US$2.3 billion per year (1974), "more than twice" flood, hurricane, tornado and earthquake damage. Estimates rose to up to US$9 billion per year (1980s) and perhaps US$15 billion (1990s). There has been no recent analysis. — [TRID 1974](https://trid.trb.org/view/133235); [Frontiers Built Env. 2021 (Louisiana)](https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2021.754761/epub)
- The Colorado Geological Survey says annual losses are "regularly estimated" to exceed tornadoes, floods, earthquakes and hurricanes combined. The ASCE "1/4 of US homes damaged" figure is secondhand only. — [CGS](https://coloradogeologicalsurvey.org/hazards/expansive-soil/); [geology.com](https://geology.com/articles/expansive-soil.shtml)

#### 2i. Exploration geology (mineral prospecting from imagery and data)
- KoBold Metals (TerraShed data platform plus Machine Prospector) found Mingomba copper, Zambia, in about 3 years versus decade-long cycles. It raised US$537 million (Jan 2025) and was raising US$200 million in Nov 2025 (US$163.4 million closed per SEC filing). — [TechCrunch 2025](https://techcrunch.com/2025/01/02/kobold-used-ai-to-find-copper-now-investors-are-piling-in-to-the-tune-of-537m); [Axios Nov 2025](https://www.axios.com/pro/climate-deals/2025/11/17/kobold-200-million-minerals)
- Unverified claims: traditional drill success "as low as 0.5%" versus about 75% claimed for AI targeting (Earth AI). KoBold reportedly hit mineralisation in 8 of 10 holes in Quebec in 2022. Both are secondary sources. — [Skillings](https://skillings.net/mineral-discovery-ai-exploration-2-0-reducing-costs-by-40/); [Proactive Investors](https://www.proactiveinvestors.com.au/companies/news/1054215/ai-is-powering-a-new-era-of-mineral-discovery-1054215.html)

### Inferences
Feasibility ratings are for a small team in a hackathon (H) or a 6-18 month startup (S). The scale is High, Medium or Low. These are my estimates.

- **Core-box photo logging for civil site investigation (RQD, recovery, fracture count, mechanical vs natural break):** H High, S High. Phone or webcam photos of core trays, segmentation (SAM-style plus a fine-tuned detector), and RQD computed per run. Incumbents (Datarock, Minalyze, Corescan) target mining. The gap is cheap, small-job, geotech-firm workflows and the AGS/DIGGS export formats, which is an inference.
- **Visual-manual USCS assistant (photo plus guided manual tests: dilatancy, toughness, dry strength, plus optional cheap sensors such as a moisture probe or pocket penetrometer):** H High (demo), S Medium. Existing image models do not use USCS classes. The work needs a labelled dataset tied to D2487 lab results, which is the moat. It should be pitched as a decision aid and a sample-grouping aid, matching D2488's stated purpose, not as a lab replacement.
- **Phone or drone photogrammetry for joint sets (orientation, spacing, persistence) leading to RMR/GSI suggestions:** H Medium (SfM plus RANSAC plus DBSCAN is doable in a weekend using open tools), S Medium. Roughness, aperture and infill still need humans.
- **Excavation-face or muck camera for rock class during tunnelling, drill-and-blast or open cut:** H Medium, S Medium-Low (needs site access and data). The research proves the concept, and commercialisation is open.
- **Landslide or slope monitoring with cheap sensors (MEMS tilt nodes, LoRa, time-lapse camera change detection) fused with free Sentinel-1 InSAR:** H Medium, S Medium. InSAR is good for screening but too slow for warnings, and in-situ systems are too expensive to deploy everywhere. A sub-US$100/node tier fills that gap.
- **Borehole-log digitisation plus probabilistic 3D stratigraphy (OCR of legacy PDF logs, then GP or ML interpolation with uncertainty):** H Medium, S High value. Legacy logs sit in PDFs, and the research methods exist but are not productised for mid-size consultants.
- **Sinkholes and expansive soils:** H Low-Medium. Data scarcity is the core issue (no national sinkhole tracking). A crowd-sourced phone app for reporting cracks and depressions, with CV triage, is more plausible than prediction.
- **Mineral prospecting from imagery:** H Low for meaningful results; heavily capitalised incumbents (KoBold, Earth AI) already lead.

### Gaps
- No independent, peer-reviewed accuracy benchmark for Datarock, Minalyze or Corescan RQD and lithology outputs was found. No published inter-observer variability statistic specifically for RQD was found.
- No published misclassification rate for field visual-manual USCS against lab D2487 was found.
- Liquefaction: not researched this session. There is no cited data on CPT/ML liquefaction triggering or on its cost.
- Groundwater mapping and geological field mapping (for example StraboSpot or AI-assisted outcrop mapping): not covered this session.
- Commercial monitoring vendors (Sixense, Geocomp, Measurand ShapeArray, Imago): I found no cited data on pricing or capability gaps. The DAS vs MEMS cost comparison is not like-for-like.
- Landslide death figures conflict across eras: about 600 per year in 1971-74 versus more than 4,000 per year implied for 2004-2016. — [AEG/EEG](https://pubs.geoscienceworld.org/aeg/eeg/article/xxiii/1/11/137265/Economic-Losses-and-Fatalities-Due-to-Landslides); [Geoenv. Disasters](https://link.springer.com/article/10.1186/s40677-022-00205-6)

## Q3. Where are the clearest openings for camera- or cheap-sensor-based AI?

### Takeaway
The clearest openings sit where (1) a human currently makes a visual judgement against a standard (RQD, USCS visual-manual, joint orientation and spacing, rock class at a face), (2) incumbents are mining-focused or hardware-heavy, and (3) the output plugs into an existing deliverable (boring log, RMR sheet, monitoring alert). Core-tray photo RQD for civil site investigation, a USCS visual-manual copilot and phone-photogrammetry joint mapping are the most hackathon-tractable. Low-cost slope sensor nodes fused with free InSAR, and legacy borehole-log digitisation feeding probabilistic ground models, are the strongest startup wedges.

### Cited Findings
- The money sits with ground risk under-investigated at about 1% of contract and producing about 3% overruns (US highways) and about 12% claims in tunnels. — [NCHRP via NAP](https://www.nap.edu/read/21926/chapter/2); [Boutsis et al. 2020](https://www.mdpi.com/2412-3811/5/9/73)
- Logging subjectivity is acknowledged by both vendors and practitioners. — [Datarock help](https://help.datarock.com.au/knowledge-base/how-to-qa-qc-predicted-and-manually-logged-geotech-data); [ACG Morrell](https://papers.acg.uwa.edu.au/d/2335_36_Morrell/36_Morrell.pdf)
- Photo-based RQD at scale is technically proven in mining (30,000 m in about 15 minutes, as a vendor claim). — [Datarock](https://datarock.com.au/)
- Visual-manual classification is by design a skill-dependent field triage step. — [ASTM D2488](https://store.astm.org/d2488-26.html)
- No single method automates discontinuity characterisation well. — [Battulwar 2021](https://doaj.org/article/7af71d1eca944c3999deab74c9af47dc)
- In-situ landslide early-warning systems are too costly to monitor every slope, and InSAR is too slow for real-time warning. — [Eng. Geology 2024](https://www.sciencedirect.com/science/article/abs/pii/S0013795224003715); [MDPI RS 2026](https://www.mdpi.com/2072-4292/18/7/1081)
- Camera-on-TBM rock classification works in field tests, but I found no commercial product. — [Sci. Reports 2022](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8810907/)

### Inferences
- Ranked openings for a camera-first hackathon build (excavation context), with feasibility:
  1. **Excavation-face or trench-wall AI logger:** phone video of a test pit, trench or cut face gives soil and rock units, layer boundaries, a USCS guess, seepage spots and a joint overlay, output as a draft log. This merges openings 2b, 2c and 2d and is High for a demo.
  2. **Core-tray RQD/recovery app for geotech consultants:** High.
  3. **Joint-set extraction from phone SfM of a rock cut, giving a stereonet and spacing that feed RMR/GSI:** Medium-High.
  4. **"As-found vs as-predicted" ground comparison during excavation:** cameras log the actual strata exposed and compare them with the ground model or borehole logs, flagging differing-site-conditions evidence early. This is a contractual and claims value proposition tied directly to Q1, and is Medium.
  5. **Cheap MEMS tilt plus time-lapse-camera slope or excavation-wall monitoring with anomaly alerts:** Medium (hardware adds risk).
- Defensibility comes from labelled data linked to lab tests and outcomes, not from model architecture. Open foundation models (segmentation, SfM) remove most of the modelling difficulty.
- Main adoption risks: professional liability (engineers sign logs), standards conformance (ASTM/BS/Eurocode 7), and site-to-site domain shift (lighting, wet vs dry soil, core photo quality).

### Gaps
- I found no market-size data for geotechnical site-investigation software or for logging labour cost per metre of core.
- I found no evidence on whether any product does trench or test-pit wall logging from video. This may be an open niche, but absence of evidence in a short search is weak signal.
- Uptake of the newest open-source tools (for example Segment Anything adapted to core and outcrops) was not checked.
