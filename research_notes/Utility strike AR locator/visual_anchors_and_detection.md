# Visual Anchors for Inferring Buried Utilities, and Detecting Them with Vision Models

Research date: 2026-11-14. Sources are mostly search-result snippets plus a few full fetches. Several primary PDFs (Madison Part VII specs, the full ISARC 2024 paper) could not be read in full; those points are flagged.

## Which surface features reveal buried utilities, and what placement conventions let you infer the route?

### Takeaway
Many surface features are reliable evidence that a utility is present, and each points to a specific type: hydrants and valve boxes mean water, manholes with lettering mean sewer, water, or telecom, gas meters mean gas, and 811 paint is color-coded by utility. Inferring the *route* between features depends on local conventions: which side of the street each utility goes on, depth minimums, and straight hydrant leads and service runs. These conventions vary by jurisdiction. No national layout exists, so any route projection is a jurisdiction-specific prior, not a rule.

### Cited Findings

**Paint marks and flags (APWA Uniform Color Code), the most direct surface anchor**
- APWA colors: Red = electric power lines, cables, conduit, lighting cables. Yellow = gas, oil, steam, petroleum, gaseous materials. Orange = communication, alarm, signal lines. Blue = potable water. Green = sewers and drain lines. Purple = reclaimed water, irrigation, slurry. White = proposed excavation. Pink = temporary survey markings. — [APWA Uniform Color Code](https://www.apwa.org/wp-content/uploads/Uniform-Color-Code-1.pdf); [CGA Best Practices App. B](https://www.bluestakes.org/pdfs/CGA_BestPractices_ApxB.pdf)
- The APWA document is dated Rev. 4/99, and the colors are consistent across sources. Other countries differ: for example, Australia uses orange for electricity. — [APWA ColorCode 2021 reprint](https://cdn.shopify.com/s/files/1/0520/1913/4624/files/APWA_ColorCode_2021.pdf); [What the Colors Mean (JEA)](https://www.jaxenergy.com/images/uploads/resources/What_the_Colors_Mean.pdf)
- Wisconsin's one-call center (Diggers Hotline) and neighboring one-call centers publish guides to locator marking symbols. — [Gopher State One Call, Locator Language](https://gopherstateonecall.org/?p=448); [MISS DIG marking guidelines](https://missdig811.org/cm/dpl/downloads/content/151/MDPB_Marking_Guidelines_Mar_2017_Update.pdf)

**Side-of-street and corridor conventions (vary by jurisdiction)**
- Castle Pines, CO: gas mains on the south and west sides of the street. Electric, cable, and communications on the north and east sides. — [Castle Pines Ch. 4 Utility Locations](https://castlepinesco.gov/wp-content/uploads/2022/10/Chapter4-Utility-Locations.pdf)
- Forest Grove, OR: in the typical 24 ft section, water and storm sewer go on the south and west, and sanitary sewer goes on the north and east. Offsets across the section are 3', 6', 6', 6', 3'. — [Forest Grove 313 Typical Utility Location](https://forestgrove-or.gov/DocumentCenter/View/652/313-Typical-Utility-Location-PDF)
- Apex, NC: water on the north and east, sanitary sewer and gas on the south and west. Vertical separation minimums are 18" between water and sewer and 12" for other utilities. The search tool's extracted text was partly garbled. — [Apex NC 300.10](https://www.apexnc.org/DocumentCenter/View/4041)
- Concord, NC: gas is placed opposite the water line, and water sits about 1 ft inside the sidewalk edge. — [Concord Typical Roadway Utility Location](https://www.concordnc.gov/Portals/0/Concord/Departments/Engineering/Documents/2021-Standards/2021-Standards-MISC/CoC%20Std%20-%20Typical%20Roadway%20Utility%20Location.pdf)
- Colorado Springs: gas and electric services generally on the topographic high side of the lot, water and wastewater on the low side. Minimum depths: gas 30", underground electric 44", water and wastewater 60". — [Colorado Springs street plan](https://Parks.Coloradosprings.gov/system/files/2023-04/street_plan_view_20230323_reduced.pdf)
- Sioux Falls: utility locations come from a set of drawings keyed to right-of-way (ROW) width and pavement width, not a single fixed offset. — [Sioux Falls Design Standards Ch. 4](https://www.siouxfalls.gov/files/assets/public/v/1/planning-and-development/construction-mgmt-amp-design/engineering-design-standards/design_standards_ch4.pdf)
- Other cities publish similar "typical utility location" standard drawings: Larimer County CO, Wasatch County UT, SeaTac WA, Garner NC, Spokane Valley, and Caltrans. — [Larimer Ch. 12](https://www.larimer.gov/sites/default/files/uploads/2021/ch12_-_utility_locations_2.pdf); [Wasatch Fig. 10](https://wasatchcounty.gov/downloads/file/693/figure-10-typical-utility-locations); [MnDOT sample utility plan](https://www.dot.state.mn.us/metro/finaldesign/pdf/sampleplan/inputil.pdf)

**Burial depths**
- Wisconsin water mains (NR 811.73): minimum cover is 5 ft unless the DNR finds it unnecessary. The DNR *recommends* 6.5 ft. — [Wis. Admin. Code NR 811.73](https://d1tvxue8o4w0fl.cloudfront.net/regulation/wisconsin-administrative-code/agency-department-of-natural-resources/environmental-protection-water-supply/chapter-nr-811-requirements-for-the-operation-and-design-of-community-water-systems/subchapter-x-distribution-systems/section-nr-81173-installation-of-mains)
- Wisconsin private water mains and services must go below the predicted frost depth (plumbing code SPS 382.40). — [SPS 382.40(8)](https://docs.legis.wisconsin.gov/document/administrativecode/SPS%20382.40(8)(a))
- Wisconsin local variation: one municipal standard (Franklin, WI) requires 6 ft minimum cover on water mains. New Berlin allows 4 ft minimum *with insulation*. — [Franklin WI Ch. 5 Design Stds](https://www.franklinwi.gov/Files/Engineering/ConstructionDesignStandards/Chap5-Updated-Design-Stds-4-7-2021.pdf); [New Berlin specs](https://www.newberlinwi.gov/DocumentCenter/View/7063)
- City of Madison: Part VII of the Standard Specifications ("Water Mains and Service Laterals") covers hydrant installation (§704.7) and service laterals. One revision added a concrete block under the hydrant lead valve. A detail drawing note says a dimension "D" shall be 48" when the water main is under 10". It is unclear what "D" measures, so do not treat it as cover depth. I could not open the full PDF; the 2020 Part7 URL returned 404. — [Madison Std Specs page](https://cityofmadison.com/engineering/developers-contractors/standard-specifications); [Madison 2023 Complete Spec Book](https://www.cityofmadison.com/business/pw/documents/StdSpecs/2023/CompleteSpecBook.pdf); [Madison Standard Detail Drawings](https://www.cityofmadison.com/business/PW/documents/StandardDetailDrawings.pdf)
- Federal gas (49 CFR 192.327): buried gas **mains** need a 24-inch minimum cover. Transmission lines need 30" in Class 1 normal soil and 36" in Class 2–4 normal soil (18"/24" in consolidated rock). States or municipalities may allow less cover under conditions. — [49 CFR 192.327 (Cornell LII)](https://www.law.cornell.edu/cfr/text/49/192.327)
- NEC Table 300.5 (customer-side wiring, 0–1000 V), from secondary sources: 24" for direct-buried cable, 18" for listed nonmetallic raceway, 6" for rigid or intermediate metal conduit. Verify against the adopted NEC edition. — [EC&M, Requirements for Underground Cables and Raceways](https://www.ecmweb.com/national-electrical-code/article/20902845/stumped-by-the-code-requirements-for-underground-cables-and-raceways); [Laguna Hills Pipe Burial Depths](https://www.lagunahillsca.gov/DocumentCenter/View/7825/Pipe-Burial-Depths)

**Hydrant-to-main geometry (strong local route prior)**
- A hydrant connects to the main through a short lead with an auxiliary (gate) valve and valve box, branching from a tee on the main. Fort Wayne's detail requires 5 ft cover on the hydrant lead and 18" separation from other utilities, with a 6" auxiliary valve and box restrained to the elbow. — [Fort Wayne W-15](https://www.cityoffortwayne.org/images/stories/Utilities/docs/Water_Details/W-15.pdf)
- WSSC (MD): the lead should be "as short as possible", laid level, with restrained joints, and the barrel is at most 8 ft. — [WSSC W-24](https://www.wsscwater.com/files/live/sites/wssc/files/PDFs/W-24-2008_18415.pdf)
- Cal Poly: the hydrant sits 18–21" from the curb face, and a 42" clear sidewalk is required. One code sets the auxiliary valve at least 30" from the hydrant. — [Cal Poly 6310 Fire Hydrant Assembly](https://afd.calpoly.edu/facilities/planning-capital-projects/construction-standard/docs/standard-details/6310-Fire-Hydrant-Assembly.pdf); [ecode360](https://ecode360.com/33457344)

**Cover lettering as a utility-type cue**
- Municipal casting specs often require "SEWER"/"S" or "WATER"/"W" cast into covers. Lacey, WA water covers say "WATER" in large letters, while its sewer covers carry a city logo. — [Ann Arbor SD-GU-5](https://a2gov.org/media/y5jbjojv/sd-gu-5-model.pdf); [Lacey WA KB](https://laceywa.qscend.com/311/knowledgebase/article/410)
- Caveats: Scottish Water says any cover type can be used on public or private sewers. NYC lore says a blank cover with vent holes usually means sewer, with exceptions. OSM tags unmarked covers as "plain". — [Scottish Water FactSheet 15](https://www.scottishwater.co.uk/-/media/ScottishWater/Document-Hub/Factsheets-and-Leaflets/Factsheets/240420SW_FactSheet_15_2020_update_v2_web.pdf); [NYC manhole field guide](https://donburmeister.com/Lids/LID_PAGES/LID3202.html); [OSM Key:manhole](https://wiki.openstreetmap.org/wiki/Key:manhole)

### Inferences
- Rough strength of each anchor for **route** inference:
  - Fresh 811 paint and flags are strongest: they are the locator's own trace of the line, already color-typed.
  - Next come connected pairs: hydrant plus nearby valve box (the lead runs about perpendicular to the main, which sits a short distance away), and a sequence of manholes (sewers run straight between manholes, so connect the dots).
  - Meters, risers, and curb stops show where a service enters, and usually imply a roughly perpendicular service run from the main to the house. This is not cited above; it is a working assumption to validate.
  - Weakest: pad-mount transformers, pedestals, streetlights, and irrigation heads. They show presence, but cables can take many paths.
- The side-of-street convention is local: Castle Pines puts gas on the south/west side, while Apex puts *water* on the north/east side and gas on the south/west. A Madison app must use Madison/MGE/Madison Water Utility practice or learn it from local GIS data, not a national template.
- Wisconsin water at 5–6.5 ft is much deeper than gas mains (24" federal minimum) or NEC electric (18–24"). So the shallow-and-likely-to-be-hit utilities (gas, electric, telecom) are the ones with the least predictable surface anchors.
- Older neighborhoods: no source quantified the deviation from standards. Treat standards as priors and expect exceptions: abandoned lines, pre-standard layouts, and alley-fed services.

### Gaps
- Could not read the full City of Madison Part VII. Still unknown: Madison's main offset from curb, curb stop location (usually at or near the property line, not confirmed for Madison), and specified cover.
- No primary source found for typical **gas service line** depth (49 CFR 192.361) or **NESC** utility-side electric depth (Rule 352). The common figures of 12–18" for gas services and 30"+ for primary electric come from memory, not verified here.
- No Madison Gas & Electric (MGE) or Wisconsin Public Service Commission (PSC) construction standard was found for gas or electric location.
- No study quantifies how often real installations deviate from standard corridor layouts, in older neighborhoods or elsewhere.
- Not researched in depth: patched-asphalt trench scars, telecom/CATV pedestals, pad-mount transformers, utility marker posts, and riser conduits on poles. No sources were gathered on their placement rules.

## Has anyone inferred buried utility routes from surface features, street-view, or aerial imagery?

### Takeaway
Yes, though only in a few works. Academic examples: graph neural network (GNN) link prediction of sewer connections between known manholes (ISARC 2024, ROC AUC about 94–95%), and manhole detection in orthophotos followed by rule-constrained tree-graph connection (France, 2016). The commercial leader, 4M Analytics, fuses records, satellite and aerial imagery, and object detection with human expert verification, and is adding street-level imagery of hydrants, poles, and valves to validate its maps. A 2023 Nature Communications paper on street-view grid mapping says image-only methods cannot map underground power lines.

### Cited Findings
- Zhang & Cai (Purdue), ISARC 2024: predict underground utility lines from visible anchor points (manholes) plus spatial context from ground features such as roads. The pipeline is relational data model → graph → GNN. Reported ROC AUC for sewer line connections between manholes: **94.12%** on the abstract page. A search snippet gave **95.24%**, so the figures conflict. Dataset size and architecture were not visible. — [ISARC 2024 abstract page](https://www.iaarc.org/publications/2024_proceedings_of_the_41st_isarc_lille_france/underground_utility_network_completion_based_on_spatial_contextual_information_of_ground_facilities_and_utility_anchor_points_using_graph_neural_networks.html); [full text PDF](https://www.iaarc.org/publications/fulltext/120_ISARC_2024_Paper_249.pdf)
- Derras et al. (LIRMM), IEEE JSTARS 2016: detect circular manhole covers in high-resolution aerial orthophotos to locate buried networks. Related work connects the detected manholes into a tree-shaped graph constrained by industry rules. Tested in Prades-le-Lez, France. — [LIRMM JSTARS PDF](https://www.lirmm.fr/~subsol/WWW/JSTARS.0516.pdf); [HAL](https://hal-lirmm.ccsd.cnrs.fr/lirmm-01275684/document)
- Automation in Construction 2020 (White Rose eprints): map buried utilities from partial observations (manhole observations plus sensor measurements) using optimization. — [White Rose eprint](https://eprints.whiterose.ac.uk/159454/8/1-s2.0-S0926580519305436-main.pdf)
- Nature Communications 2023: maps distribution grids from street view, road networks, and building maps. The authors state that methods using only remote sensing or street view **cannot detect underground power lines**. — [Nature Comms s41467-023-39647-3](https://www.Nature.Com/articles/s41467-023-39647-3); see also [Climate Change AI, NeurIPS 2019 street-view grid mapping](https://www.climatechange.ai/papers/neurips2019/31)
- 4M Analytics (founded 2019, Austin TX) combines construction blueprints, as-builts, permits, public GIS records, satellite and aerial imagery (including time-lapse), and object detection. Geospatial experts verify and correct the predicted lines. Customers include Georgia DOT and Minnesota DOT (12,000 highway miles reported). Accuracy claims are the company's own, not independently validated. — [4M blog, nationwide map](https://4manalytics.com/blog/how-were-building-the-first-nationwide-map-of-utilities); [4M product](https://4manalytics.com/product); [GlobeNewswire GDOT](https://www.globenewswire.com/de/news-release/2025/12/10/3203325/0/en/4M-s-Utility-AI-Platform-Delivers-Smarter-Faster-Safer-Infrastructure-for-the-Georgia-Department-of-Transportation.html); [Kurrant, MnDOT](https://kurrant.com/?p=46963); [GoGeomatics](https://gogeomatics.ca/underground-utility-mapping-by-air-space-and-ai)
- 4M and Bee Maps: road-level imagery of hydrants, poles, valves, and road and curb features is used to "correlate, validate, or challenge" what is believed to be underground. Both companies describe this as still being explored. No accuracy figures. — [Bee Maps blog](https://beemaps.com/blog/4m-analytics-accelerates-utility-mapping-with-spatial-ai)

### Inferences
- The proven pattern is "detect anchors, then connect them with domain-rule graphs or a GNN", and it works best for **gravity sewer**: manholes at every junction or bend, with straight runs between them. It does not carry over well to gas, electric, or fiber, which have no regular surface access points.
- Even 4M treats imagery as corroboration layered on records, with humans in the loop. That suggests "imagery alone → route" is not trusted at production scale.
- For a small team: in an AR locator, project routes only between anchor pairs of the same utility type (manhole→manhole, hydrant→valve→main). Show them as probabilistic corridors, not lines, and give 811 paint top priority when present.

### Gaps
- No paper was found that infers buried routes directly from street-level (ground) photos or video. The existing work uses aerial imagery or anchor locations that are already known.
- Full methods and dataset details of the ISARC 2024 paper could not be read; the PDF did not extract.

## Detection: datasets, pretrained models, accuracy, failure modes, and OCR of cover text

### Takeaway
Off-the-shelf labels exist for manholes, catch basins, fire hydrants, utility poles, street lights, and junction boxes: Mapillary Vistas v2.0 (segmentation) and Mapillary's platform detections. COCO includes "fire hydrant", so any pretrained YOLO detects hydrants out of the box. Manhole-cover YOLO papers report roughly 93–95% mAP on small, narrow datasets. Utility poles reach about 90% mAP with DETR on Street View. Valve boxes, curb stops, gas meters, and 811 paint have little or no public data. Reading cover text with OCR is an established technique and the best cue for cover type, but blank or unmarked covers and non-standard castings need a fallback.

### Cited Findings

**Datasets and class lists**
- Mapillary Vistas v2.0 (124 classes) includes Catch Basin, Fire Hydrant, Junction Box, Manhole, Utility Pole, Street Light, and Pole. Labels are of the form `object--manhole` and `object--support--utility-pole`. The class list comes from community mmseg configs; check the official docs. — [HF mmseg mapillary.py](https://huggingface.co/spaces/KyanChen/TTP/blame/refs%2Fpr%2F1/mmseg/datasets/mapillary.py); [Vistas ICCV 2017](https://research.mapillary.com/publication/iccv17a); [Vistas overview blog](https://jiaruixu.github.io/2018/05/02/Mapillary-Vistas-Dataset)
- The Mapillary platform auto-generates map "point features" for 42 object classes, including fire hydrants, manholes, and utility poles. These are separate from the Vistas labels and can be queried as existing detections. — [Mapillary blog, 42 new classes](https://blog.mapillary.com/update/2019/01/23/updating-maps-with-cameras-42-new-point-features.html); [Mapillary help](https://help.mapillary.com/hc/en-us/articles/360021883552)
- Roboflow Universe: many small manhole-cover datasets exist. The largest has about 2,297 images. The "FYP Manhole Detection" set has classes MF, catchpit, concrete-cover, drainage-manhole, gully, telecom-pit, and valve, but low use and about 3 years old. No gas-meter class was found. — [Manhole cover detection (2297 imgs)](https://universe.roboflow.com/ff-vt4js/manhole-cover-detection); [FYP Manhole Detection](https://universe.roboflow.com/new-workspace-kjbmt/fyp-manhole-detection-gv9sm); [Manhole Cover Dataset YOLO](https://universe.roboflow.com/create-dataset-for-yolo/manhole-cover-dataset-yolo); [utility poles: mapillary_lisa_melded](https://universe.roboflow.com/utility-poles-wgcam/mapillary_lisa_melded_01)
- OHL-UK dataset (BMVC 2025): 4,570 Google Street View images of utility poles and warning signs. The authors say the dataset and checkpoints are released. — [BMVC 2025 paper](https://bmva-archive.org.uk/bmvc/2025/assets/papers/Paper_976/paper.pdf); [arXiv 2608.04061](https://arxiv.org/pdf/2608.04061)

**Reported accuracy**
- Improved YOLOX on 637 dash-cam images of manhole covers: mAP of 95% normal, 94% broken, 93% sunk. — [Frontiers Built Env. 2024](https://www.frontiersin.org/articles/10.3389/fbuil.2024.1337984/full)
- EEFA-YOLO (Scientific Reports 2025), manhole cover condition (good, broken, lost, misaligned): mAP at least 1.5% higher than the YOLOv11 baseline. Absolute values were not captured. — [DOAJ, Sci Rep 2025](https://doaj.org/article/00fa6a8c0a9140eca5c6ceebda597cec)
- Real-time manhole detection (MGB-YOLO, modified YOLOv5s vs YOLOv7/v8s): 1,000 campus-road images augmented to 6,000. — [PMC10542779](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10542779/)
- YOLOv11 on Google Street View for manhole covers and drainage grates: Turkish paper reporting mAP@0.5 and mAP@0.5:0.95; values not captured. — [DergiPark](https://dergipark.org.tr/en/download/article-file/4322644)
- Dhaka road damage with a Manhole class: 78.1% image-level accuracy. — [arXiv 2510.03797](https://arxiv.org/abs/2510.03797v1)
- Utility poles, DETR on Street View: 90.43% mAP for poles and 88.26% for warning signs. — [BMVC 2025](https://bmva-archive.org.uk/bmvc/2025/assets/papers/Paper_976/paper.pdf)
- **Localization is the weak link:** RetinaNet pole detection on Street View with line-of-bearing geolocation put only 2.6%, 47%, and 79% of poles within 1 m, 5 m, and 10 m of truth. — [Zhang et al., Sensors 2018](https://mdpi.com/1424-8220/18/8/2484)

**OCR of cover text**
- Cover text is "the most important feature" for telling cover types apart, and recognizing it is the most effective way to classify covers. On UAV and aerial images the text detail is lost, so the authors localize the text and apply GAN super-resolution before classifying. — [MDPI Applied Sciences 14(7):2769](https://mdpi.com/2076-3417/14/7/2769)
- Commercial aerial providers already classify circular manhole covers as a feature class. — [Nearmap 867-111 circular manhole cover](https://help.nearmap.com/kb/articles/867-111-circular-manhole-cover)

### Inferences
- For a phone or AR camera at close range, looking down from about 1.5–2 m, cover text is far more legible than in aerial images. A detect, crop, and OCR pipeline should work for "SEWER", "WATER", "STORM", "GAS", "TELEPHONE", "ELECTRIC", and similar. The utility-name lexicon is small, so fuzzy matching against it should handle rust and wear. This has not been benchmarked in the sources.
- The reported 93–95% mAP figures come from small, single-site datasets and probably overstate field performance on Madison streets. Expect to fine-tune on a few hundred locally captured images per class.
- Classes with no public data that the team would have to label itself: valve boxes and curb stops (small, often covered by grass, soil, or snow), gas meters and risers, telecom pedestals, pad-mount transformers, utility marker posts, 811 paint lines and flags, and trench patches. Paint could plausibly use color segmentation plus a detector, since APWA colors are standardized.
- Failure modes noted or implied: small objects at distance; occlusion by parked cars, snow, or leaves, which matters for Wisconsin winters; look-alike circular covers across utilities (needs OCR or vent-pattern features); and meter-level geolocation error from monocular images (Sensors 2018). In AR, ARKit/ARCore depth should help, but it is unverified here.

### Gaps
- No COCO per-class AP for "fire hydrant" was retrieved. No dedicated hydrant-detection paper was found.
- No public datasets were found for gas meters, valve boxes, curb stops, 811 paint marks, or utility flags.
- No benchmark of close-range OCR accuracy on manhole cover text was found.
- No sources were found on detecting asphalt trench scars or patches as utility indicators. Pavement-crack and patch datasets likely exist but were not searched.
