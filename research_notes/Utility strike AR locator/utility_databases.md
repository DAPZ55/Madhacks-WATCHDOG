# Existing Underground Utility Location Data Sources: Holders, Accuracy, Access, Formats

Research date: 2026-11-14. Sources checked live where possible; older material is flagged.

## Q1. Does the US 811 / one-call system (esp. Wisconsin Diggers Hotline) hold or share utility maps, or only route tickets?

### Takeaway
One-call centers route tickets; they don't publish facility maps. Diggers Hotline (WI) holds member *service-area* footprints for routing, and owners then mark their own lines on the ground with paint and flags. No source shows a public or API map of buried lines from Diggers Hotline. A third-party app could not get line geometry from 811.

### Cited Findings
- Diggers Hotline is a non-profit one-call center connecting excavators with facility owners. It has >1,400 utility members and handles >1 million locate requests a year. An older Stoughton Utilities page says ">1,100 members", so the counts differ by date. — [Diggers Hotline 50th anniversary](https://www.diggershotline.com/news/diggers-hotline-celebrates-50th-anniversary); [Stoughton Utilities](https://www.stoughtonutilities.com/diggershotline.aspx)
- Member facility owners must keep their *service areas* current in the Diggers Hotline system. Tickets go to the members whose facilities may be in the dig area. This is routing data, not line geometry. — [Diggers Hotline compliance program](https://www.diggershotline.com/compliance-program)
- WI statute 182.0175: transmission facility owners must mark facilities within 3 working days of an excavation notice. Excavators must keep an estimated 18-inch minimum clearance from marks for unexposed facilities, reduced once exposed to the greater of 12 in. or 2x the equipment's limit of control. The PSC describes this as an 18-inch buffer zone on each side of a mark. — [WI PSC Diggers Hotline](https://psc.wi.gov/Pages/ForConsumers/DiggersHotline.aspx); [PHMSA WI state law summary (2017)](https://primis.phmsa.dot.gov/Comm/StateDamagePrevention/State%20DP%20Law%20Summary/Wisconsin%20State_DP_Law_Summary_%2020170807.pdf)
- A 2025–26 LRB draft (LRB-2915/P3) would define a "tolerance zone" (18 in. horizontally from a marked facility) and add provisions on mapping underground facilities. It is a draft, and no evidence of enactment was found. — [Diggers Hotline-hosted P3 draft, Jan 2026](https://www.diggershotline.com/assets/uploads/2026/08/P3%20draft%20-%20DPC%20-%20Jan%202026.pdf)
- The Wisconsin Damage Prevention Council lists improving utility mapping data and making it available for planning as a goal. Its Sept 2025 minutes discuss map-data accessibility, so this is an open policy issue, not a delivered product. — [WI DPC minutes 2025-09-11](https://www.diggershotline.com/assets/uploads/2025/09/Minutes%20of%20WI%20DPC%20Meeting%20-%2009112025.pdf); [PSC 2024 DPC slides](https://psc.wi.gov:443/SiteAssets/2024%20PS%20Seminar/04WisconsinDamagePreventionCouncil.pdf)
- WI PSC has a "BEAD Utility Locating" page, which relates to broadband buildout locating. — [PSC BEAD Utility Locating](https://psc.wi.gov/Pages/ServiceType/Broadband/Utility-Locating.aspx)
- National damage context: CGA's 2025 DIRT counted 221,717 unique damage reports, the highest since tracking began. The top 10 root causes account for 86% of damages, led by not calling 811. — [Trenchless Technology on 2025 DIRT](https://trenchlesstechnology.com/cga-releases-2025-dirt-data-summary-trends/)
- CGA (2023 data): "failure to locate accurately and on time" was the root cause in 34% of damages. CGA says records of underground utilities are "often inaccurate or incomplete and largely unavailable to damage prevention stakeholders." — [Trenchless Technology on CGA locating report](https://trenchlesstechnology.com/cga-special-report-examines-factors-driving-damages-associated-with-locating-practices/); [Underground Infrastructure 2024](https://undergroundinfrastructure.com/news/2024/june/common-ground-alliance-report-identifies-risks-opportunities-for-improving-underground-utility-locating-practices)
- CGA follow-up found that generic "locator error" codes often mask specific causes such as mapping problems, tracer wire, or abandoned facilities. — [CGA 2022 DIRT](https://dirt.commongroundalliance.com/2022-DIRT-Report/Damage-Root-Causes-Remain-Consistent)
- Urbint, a vendor to utilities, scores every 811 ticket for strike risk using ticket data plus the utility's own GIS. This shows ticket data flows from one-call centers to *member utilities* and their vendors, not to the public. Southern Company: ~50% of damages fell in 5% of tickets (vendor-reported). — [Urbint damage prevention](https://urbint.com/solutions/urbint-for-damage-prevention); [Itron/Southern Co. case](https://it.itron.com/w/southern-company-gas-reduces-damages-by-30)

### Inferences
- The only 811-derived geometry a third party could plausibly see is a ticket's dig-area polygon and the list of notified members, and only as the excavator who filed the ticket. 811 is not a map source for the app.
- On-the-ground paint marks (made after a ticket) are the "truth" that exists; an app could capture or photograph marks rather than predict them.

### Gaps
- No official Diggers Hotline documentation was found on an API, positive-response system, or whether ticket polygons or member lists are exportable to third parties. Ask Diggers Hotline directly.
- The exact text of WI 182.0175 on mapping obligations for members wasn't retrieved.
- Full 2025 CGA root-cause breakdown (mapping-specific share) not yet located. CGA said a full report was due in fall 2026.

## Q2. Do utilities and municipalities publish GIS layers? (Madison/Dane County, other US cities, OpenStreetMap)

### Takeaway
Yes, for gravity/municipal systems (sanitary sewer, storm sewer, hydrants, streetlights), often as public ArcGIS REST feature services. Madison is a strong example and is directly usable. Pressurized water mains, gas, electric, and telecom are much less often published, usually withheld for security. OSM has millions of hydrant and manhole points but sparse, unverified buried-line data.

### Cited Findings
**City of Madison (verified live via ArcGIS Hub search API and REST, 2026-11-14)**
- The city portal is data-cityofmadison.opendata.arcgis.com, an ArcGIS Hub site rebuilt from a 2012 repository. — [Esri ArcNews](https://www.esri.com/about/newsroom/arcnews/city-of-madison-revamps-open-data-site)
- Public feature services on `maps.cityofmadison.com/arcgis/rest/services/Public/`. Counts are from live REST `returnCountOnly` queries.
  - **Sanitary Sewer Mains** (`OPEN_DATA_ENGR2/MapServer/13`): 24,662 features. Fields include Material, Diameter_in, Slope, Year_installed, Condition, Owner, Maintained_by. — [REST layer](https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DATA_ENGR2/MapServer/13)
  - **Sanitary Sewer Laterals** (`/12`): 67,333 features. Fields include Parcel_no, Private, Connect_to_pvt_main, Tracer_wire, Marker_ball, Year_retired. These are service laterals to parcels, which is unusual and valuable. — [REST layer](https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DATA_ENGR2/MapServer/12)
  - **Storm Sewer Pipes** (`/4`): 44,272 features. **Storm Sewer Structures** (`/2`). **Sanitary Sewer Access Structures** (manholes, `/11`). **Pump Stations** (`/15`). Plus sewer and water easement lines. — [OPEN_DATA_ENGR2 service](https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DATA_ENGR2/MapServer)
  - **Water Hydrant** (`OPEN_DATA_WATER/MapServer/0`): 9,596 features. Per its description, utility hydrants are "actively maintained and updated daily", and private hydrants "should not be considered current." This is the **only** layer in the OPEN_DATA_WATER service. **No water-main pipe layer is public**; only a "Water Main Breaks" point layer exists. — [REST layer](https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DATA_WATER/MapServer/0)
  - **Streetlights**: City-maintained luminaires, Utility-maintained street lights, Street Light Utility Ownership (`OPEN_DATA_TE/MapServer/25,26,28`). These are point assets, not the buried circuit cables. — [OPEN_DATA_TE service](https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DATA_TE/MapServer)
  - Hub "modified" metadata on many ENGR2 items dates to 2017 (epoch 15047xxxxx). UW GeoData archives a "2017" storm sewer snapshot, so check the live service's `Date_modified` field for currency. The city storm system is ~275 miles of pipe and open channel. — [GeoData@Wisconsin](https://geodata.wisc.edu/catalog/CityOfMadison-16e6976dafd9487fa8bcf549c0a23dad11); [Madison engineering onboarding PDF](https://cityofmadison.com/council/documents/HM%20Master%20Alder%20Onboarding_Engineering%20Introduction.pdf)
- MGE (gas and electric) only publishes Diggers Hotline guidance; no public GIS was found. — [MGE Diggers Hotline](https://mge.com/safety-outages/diggers-hotline)

**Other US/intl. examples**
- **Seattle (SPU)** publishes Water Mains and Water Services, in CSV, FGDB, GeoPackage, GeoJSON, KML, Shapefile, and SQLite. It explicitly excludes transmission pipelines and feeder mains "for reasons of water system network security." — [data.gov SPU Water Mains and Services](https://catalog.data.gov/dataset/spu-water-mains-and-services); [Seattle Utilities GIS data](https://seattle.gov/utilities/construction-resources/records-vault/data-resources)
- **San Diego**: hosted Water_Main_SD feature layer (potable distribution) on the SANDAG server. — [SANDAG REST](https://geo.sandag.org/server/rest/services/Hosted/Water_Main_SD/FeatureServer/layers)
- **Houston Public Works** GIS portal offers downloadable data "for commercial and non-commercial purposes." — [Houston Public Works GIS](https://houstonpublicworks.org/geographical-information-systems)
- **Auburn, WA** names its service "WaterVisibleToPublic", which implies a curated public subset. — [Auburn REST](https://gis.auburnwa.gov/hosting/rest/services/Water/WaterVisibleToPublic/MapServer/3/iteminfo?f=pjson)
- **Kitchener, ON**: water mains layer with 16,164 features. **Hamilton NZ**: only a subset is published. — [Kitchener metadata](https://app2.kitchener.ca/appdocs/GISImages/GIS_Web_External/GIS_Metadata_Open_Data/IndividualReports/Water_Mains.pdf); [Hamilton NZ](https://catalogue.data.govt.nz/dataset/water-main-hamilton-city-council8)
- **PHMSA NPMS** covers gas transmission and hazardous liquid pipelines only, with no distribution or gathering lines. The public viewer shows one county at a time, and minimum positional accuracy is ±500 ft. It "must not be used to identify exact locations." Full data is restricted to government agencies and operators (own data only). — [NPMS Public Viewer](https://www.npms.phmsa.dot.gov/AboutPublicViewer.aspx); [NPMS fact sheet](https://primis.phmsa.dot.gov/stakeholder-comms/factsheets/fsnpms)

**OpenStreetMap (taginfo API, queried live 2026-11-14, global counts)**
- `emergency=fire_hydrant`: 2,579,639 objects. `man_made=manhole`: 535,255 (nearly all nodes). `location=underground`: 516,572 (462,606 ways). `man_made=pipeline`: 386,321 (mostly ways). `power=cable`: 189,366 ways. `telecom=line`: 4,244. — [taginfo API](https://taginfo.openstreetmap.org/api/4/tag/stats?key=man_made&value=manhole)
- OSM wiki: `location=underground` marks buried features (pipelines, power cables), and power=cable defaults to underground. The wiki flags verifiability problems for underground equipment. The telecom paths proposal had not reached a vote. — [OSM wiki location=underground](https://wiki.openstreetmap.org/wiki/Tag:location%3Dunderground); [power=cable](https://wiki.openstreetmap.org/wiki/Tag:power=cable); [Telecom paths proposal](https://wiki.openstreetmap.org/wiki/Proposal:Telecom_paths_proposal)

### Inferences
- In Madison, an app could load sanitary mains and laterals, storm pipes, structures, and hydrants today via ArcGIS REST (`/query?f=geojson`). This is open city data, but check the portal's license terms. Water mains, gas (MGE/WE Energies), electric, and fiber would be missing.
- Hydrant and valve-box points imply a water main nearby, usually in the street. That could be a heuristic "likely water main corridor", clearly labeled as an inference.
- OSM buried-line data is far too sparse and unverifiable for safety use. Hydrant and manhole nodes are useful as surface anchors (QL-C-style) for AR registration.
- Global taginfo counts say nothing about Madison coverage. An Overpass query for the Madison bbox would answer that.

### Gaps
- No Dane County utility layers were checked (Dane County LIO/DCiMap). The county likely holds parcels, not utility lines; this is unverified.
- The open-data license or terms of use for Madison layers weren't retrieved.
- San Francisco, Chicago, NYC, and Austin portals weren't confirmed; the search didn't surface water-main layers for them.
- Esri ArcGIS Living Atlas: no evidence found of utility-network buried-line layers. It is believed to carry mostly national infrastructure (e.g., HIFLD-derived transmission lines), but this is unverified.

## Q3. Restrictions: security rules (CEII, DHS), utility reluctance, licensing

### Takeaway
Electric and gas detail is the most locked down. FERC CEII rules (post-9/11) shield detailed engineering and design information and require NDAs. PHMSA restricts NPMS to government users. Water utilities withhold transmission mains (Seattle, Madison). Even the UK's national register bans the public and limits use cases for national-security reasons.

### Cited Findings
- FERC created CEII protections after 9/11. It restricted public access, set up a non-FOIA request process, and requires NDAs. A 2007 report said NDAs made the information "nearly useless to the media." The 2002 proposal discussed oversized maps detailing energy facility specs as restricted material. — [FERC CEII regulations](https://www.ferc.gov/critical-energyelectric-infrastructure-information-ceii-regulations); [Order 662 (2005)](https://www.ferc.gov/sites/default/files/2020-05/OrderNo662.pdf); [SEJ 2007](https://sej.org/node/611); [FR 2002](https://sgp.fas.org/news/2002/09/fr091302.html)
- Order 683 narrowed CEII to "specific engineering, vulnerability, or detailed design information." FERC's 2017 guidelines say CEII is not a mechanism to withhold non-risky information. — [FR 2007](https://www.govinfo.gov/content/pkg/FR-2007-11-14/pdf/E7-22141.pdf); [CEII filing guidelines](https://www.ferc.gov/sites/default/files/2020-04/CEII-Filing-guidelines.pdf). These sources are 2002–2017; current 18 CFR 388.113 text wasn't re-checked.
- NPMS: full access is limited to government agencies (including emergency responders), and operators see only their own lines. The public gets a ±500 ft, county-at-a-time viewer. — [NPMS Public Viewer](https://www.npms.phmsa.dot.gov/AboutPublicViewer.aspx)
- Seattle water excludes transmission and feeder mains "for reasons of water system network security." — [data.gov SPU](https://catalog.data.gov/dataset/spu-water-mains-and-services)
- UK NUAR access is restricted mainly for national security reasons (law-firm note). Prohibited uses include land transactions, business cases, and network-expansion siting. — [Mondaq](https://www.mondaq.com/uk/contracts-and-commercial-law/1695246/the-new-national-underground-asset-register-what-does-it-mean-for-the-energy-infrastructure-sector); [NUAR FAQs](https://www.nuar.uk/faqs)
- CGA: records are "largely unavailable to damage prevention stakeholders." — [Underground Infrastructure 2024](https://undergroundinfrastructure.com/news/2024/june/common-ground-alliance-report-identifies-risks-opportunities-for-improving-underground-utility-locating-practices)

### Inferences
- A consumer app should expect no gas, electric, or fiber line data from US owners without a formal data-sharing agreement. Utilities have liability and security reasons to refuse.
- Displaying third-party data as "where to dig" would create liability. Every source system (NPMS, BYDA, NUAR) disclaims positional accuracy and says to call 811.

### Gaps
- DHS/CISA-specific guidance on publishing utility GIS wasn't retrieved (e.g., HIFLD secure vs. open tiers).
- No sources found on Wisconsin PSC rules on utility GIS disclosure, or Wisconsin public-records exemptions for utility maps.

## Q4. Accuracy: ASCE 38-22 quality levels, record error, abandoned lines, private laterals

### Takeaway
Utility records are Quality Level D (records), which FHWA calls "highly limited" in comprehensiveness and accuracy. Field-verified QL-B and QL-A cost money per site. No authoritative nationwide error percentage was found. Lines from the meter to the house (gas piping, private water and sewer laterals, yard-light and electric feeds) are private and not marked by 811.

### Cited Findings
- ASCE 38-22 levels:
  - **QL-D**: existing records or verbal recollection.
  - **QL-C**: surveyed visible features (manholes, valve boxes) correlated with records; the most commonly used level.
  - **QL-B**: geophysical designating (EM, GPR).
  - **QL-A**: non-destructive exposure (vacuum excavation), giving precise horizontal and vertical position.
  - The standard requires correlating QL-B with records and resolving discrepancies.
  - Sources: [McKissock on ASCE 38-22](https://www.mckissock.com/blog/land-surveyor/utility-mapping-for-surveyors-a-guide-to-sue-and-asce-38-22/); [Rettew](https://www.rettew.com/newsroom/navigating-the-underground-how-subsurface-utility-engineering-quality-levels-guide-smart-decision-making/); [TxDOT 2023 ASCE 38-22 slides](https://www.txdot.gov/content/dam/docs/division/row/utility-week-2023/12-14-23/day3-pm-2-wes-kaisershot-asce-38-22-sue-standard-updates.pdf)
- FHWA: QL-D is "often highly limited in terms of comprehensiveness and accuracy." — [FHWA SUE](https://www.fhwa.dot.gov/programadmin/sueindex.cfm); also [FHWA Utility Data Quality Level (Apr 2026)](https://highways.dot.gov/sites/fhwa.dot.gov/files/Utility_Data_Quality_Level-29Apr2026.docx); [NASEM 2026 guide on depicting utilities](https://www.nationalacademies.org/read/29432/chapter/5)
- Quantified field examples:
  - A VINCI/GRDF pilot found Exodigo detected **57% more utility lines than existing records** at a test site (vendor pilot; no peer-reviewed method). — [datadrivenaec Exodigo profile](https://datadrivenaec.com/tools/exodigo)
  - 4M says public agencies update utility data with lags of "several months to more than a year." — [4M blog](https://www.4manalytics.com/blog/what-is-underground-utility-mapping)
  - The BYDA-commissioned report says plan currency and accuracy are inconsistent and plans "often differ from actual field conditions." — [BYDA 2026 report](https://www.byda.com.au/wp-content/uploads/2026/03/Australias-Underground-Utility-Safety-Reckoning_BYDA_screen-preview.pdf)
- A secondary summary of CGA 2022 data claims 94% of locating-related root causes stemmed from incomplete or inaccurate subsurface data. This is a broad reinterpretation, so treat it with caution. — [GP Radar](https://www.gp-radar.com/article/new-report-highlights-the-cost-of-inaccurate-utility-data-in-the-construction-industry)
- Abandoned facilities and missing tracer wire are recognized specific root causes hidden under "locator error." — [CGA 2022 DIRT](https://dirt.commongroundalliance.com/2022-DIRT-Report/Damage-Root-Causes-Remain-Consistent)
- **Private lines (WI):**
  - Diggers Hotline: private lines are the property owner's responsibility, and owners can hire private locators. — [Diggers Hotline homeowner news](https://www.diggershotline.com/news/5-things-new-homeowner); [Homeowner FAQ](https://www.diggershotline.com/homeowner-faq)
  - Wisconsin Public Service owns mains, service pipes, and meters. Piping beyond the meter belongs to the customer, including buried gas to yard lights, grills, garages, and pool heaters. — [WPS pipeline safety](https://www.wisconsinpublicservice.com/safety/pipeline)
  - Utilities mark "up to the meter and no further" (Colorado 811 and Gopher State One Call, MN, describe the same model). — [Colorado 811](https://www.colorado811.org/resources/blog/private-v-public-utilities-whats-the-difference); [Gopher State One Call](https://gopherstateonecall.org/?p=509)
  - Kenosha Water has a guide on locating customer water and sewer lines. — [Kenosha PDF](https://www.Kenosha.org/images/water/LocatingWaterSewerLines.pdf)
  - In Madison, the sewer lateral layer includes a `Private` flag and Parcel_no, so some private laterals are mapped at the city record level. — [REST layer 12](https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DATA_ENGR2/MapServer/12)

### Inferences
- Any record-derived app overlay is QL-D at best, or QL-C if snapped to surveyed hydrants and manholes. It should be presented as "approximate / records-based, call 811", never as a locate.
- The highest-value gap for homeowners is exactly the private lines 811 skips. Few datasets exist for these; Madison's sewer laterals are a rare exception.

### Gaps
- No authoritative, quantified typical positional offset (e.g., "records are off by X ft on average") was found. ASCE 38-22 appendices and the FHWA/NASEM studies may contain figures but weren't read in full.
- WI-specific legal boundary for electric service drops (utility vs. customer) wasn't confirmed.

## Q5. International national registries

### Takeaway
UK (NUAR) and the Netherlands (KLIC/WIBON) are the most advanced: centralized, mandated, harmonized data. Both still restrict access to asset owners, contractors, or registered excavators per job. None offers open public or app-developer access. Australia (BYDA) and Germany (BIL) are referral portals like US 811 but return owner plans to the enquirer. Singapore is building a mandated 3D digital underground.

### Cited Findings
**UK: NUAR**
- Operated by Ordnance Survey since 2025 (contract awarded; earlier GDS-run).
- Coverage (Sept 2026): >400 asset owners, ~3.2 million km of pipes and cables, >80% of known underground infrastructure in England, Wales, and NI. Includes 100% of electricity DNOs and water companies, >70% of local authorities, and 90% of highway authorities. >230 supply-chain contractors have access. Use is up 115% since OS took over.
- Damage costs are estimated at up to £2.4bn/yr; NUAR's claimed benefit is ≥£400m/yr.
- Gov guidance cites ">600 asset owners", a count conflict with the 400 figure.
- Sources: [ISPreview Sept 2026](https://www.ispreview.co.uk/index.php/2026/09/over-400-asset-owners-join-nuars-uk-map-of-underground-cables-and-pipes.html); [gov.uk NUAR guidance diff Apr 2026](https://govdiff.njk.onl/update/2026-04-27T17:09:00+01:00/www.gov.uk/guidance/national-underground-asset-register-nuar)
- Access is by invitation only: asset owners who share data, plus their authorised contractors. Use is under legally enforceable data access agreements, with monitoring and audit. Permitted uses: strike avoidance, NRSWA s.79-82 duties, HSG47. **The public cannot access it.** No API is mentioned. Data is transformed to the NUAR Harmonised Data Model. — [NUAR FAQs](https://www.nuar.uk/faqs)
- The Data (Use and Access) Act 2025 (Royal Assent June 2025) put NUAR on a statutory footing. GDS plans access for new user groups in 2026–2028 (emergency services, public bodies, members of the public working on their own property). This depends on a consultation planned for spring 2026 and secondary legislation; no confirmation was found that it launched. Scotland uses the separate SCADV. — [GDS blog Jan 2026](https://gdsgeospatial.blog.gov.uk/2026/01/28/towards-a-comprehensive-national-underground-asset-register-integrated-into-the-existing-ecosystem); [NUAR user access expansion](https://www.nuar.uk/news/nuar-user-access-expansion-update)

**Netherlands: KLIC / WIBON (Kadaster)**
- Mechanical digging requires a KLIC-melding to Kadaster 20 to 3 working days before work (exemption: own land, less than 50 cm deep).
- Network operators send their cable and pipe data to Kadaster, and the excavator receives current "gebiedsinformatie" within 2 working days. It must be on site, viewable in the KLIC-viewer.
- Excavators must report deviations from the mapped location to Kadaster (art. 19 WIBON).
- Fee: ~€10.50 per notification (third-party figure, unverified).
- Sources: [RVO WIBON](https://www.rvo.nl/onderwerpen/percelen-registreren/alles-over/graafwerkzaamheden-wibon); [Ondernemersplein](https://ondernemersplein.overheid.nl/wetten-en-regels/graafwerkzaamheden-melden-grondroerdersregeling/); [Rijksoverheid KLIC contact](https://www.rijksoverheid.nl/contact/contactgids/kabels-en-leidingen-informatiecentrum-klic)

**Australia: Before You Dig Australia (BYDA)**
- Free referral service. Plans come from asset owners, not BYDA, and not all owners are members.
- Plans are "indicative only" and don't give exact locations. BYDA's own 2026 report calls currency and accuracy inconsistent.
- Sources: [BYDA free plans](https://www.byda.com.au/2025/11/26/the-free-byda-service-helping-you-access-utility-plans/); [BYDA rural brochure](https://www.byda.com.au/wp-content/uploads/2023/12/Rural-tri-fold-brochure-digital-BYDR0823.1-1.pdf); [BYDA 2026 report](https://www.byda.com.au/wp-content/uploads/2026/03/Australias-Underground-Utility-Safety-Reckoning_BYDA_screen-preview.pdf)

**Germany: BIL and Leico**
- BIL eG is a cooperative founded in 2015; its portal went live 29 Feb 2016 with >100 network partners. Free construction and planning enquiries are routed to operators.
- Leico (formerly infrest, Berlin/Brandenburg, renamed 10 Oct 2023) is a competing portal. There is no single national register.
- Sources: [DGMK](https://dgmk.de/en/news/bil-with-over-100-network-partners/); [Pipeline Journal](https://www.pipeline-journal.net/articles/bil-germany-wide-information-system-pipeline-enquiries); [ZfK Leico](https://www.zfk.de/digitalisierung/smart-city-energy/aus-dem-infrest-leitungsauskunftsportal-wird-leico)

**Singapore**
- SLA's Digital Underground project (since 2017, with Singapore-ETH Centre and City of Zürich) targets a reliable 3D map. The Standard and Specifications for Utility Survey has been progressively mandated for new utilities.
- Data is shared via SLA GeoSpace among utility owners and developers. URA's INPAC coordinates underground planning.
- No completion status was found.
- Sources: [SLA Developing a Digital Underground](https://www.sla.gov.sg/geospatial/resources/onemap-news/developing-a-digital-underground); [GIM International](https://www.gim-international.com/content/news/towards-an-ecosystem-of-underground-utilities-mapping-in-singapore); [URA INPAC](https://www.ura.gov.sg/infrastructure-planning/inpac/)

### Inferences
- Even the gold-standard registries gate access by role and job, and none exposes a public API. A US consumer app shouldn't expect a government-run open underground map.
- NUAR's planned "members of the public working on their own property" tier (2026–28) is the closest analog to a homeowner app. It's worth watching as a precedent.

### Gaps
- KLIC data format (IMKL, GML-based) and positional accuracy weren't retrieved in this pass.
- No sources retrieved for other registries: France (DT-DICT / Guichet Unique), Denmark (LER 2.0), Japan, or New Zealand (beforeUdig).
- No information found on a NUAR API or data export.

## Q6. Commercial aggregators: 4M, Exodigo, Spotr, Urbint, ProStar, Esri

### Takeaway
There are two models. Records-conflation vendors (4M) scrape and digitize public GIS, as-builts, permits, and imagery into a nationwide QL-D-ish layer. Field-sensing vendors (Exodigo) produce QL-B-grade per-site scans. Urbint and ProStar serve utilities' internal damage-prevention workflows. All are enterprise B2B; no public consumer feed was found.

### Cited Findings
- **4M Analytics**:
  - Collects "public utility records from GIS servers, as-builts, permits, satellite imagery" and legacy blueprints. These are digitized, geo-referenced, conflated into a unified map, and verified by geospatial experts, with automated refresh when sources change. It markets this as building the "first nationwide map of utilities."
  - Its preliminary tier relies on existing records, and the company concedes SUE validation is still needed.
  - Customer example: Georgia DOT (Dec 2025).
  - Sources: [4M nationwide map blog](https://4manalytics.com/blog/how-were-building-the-first-nationwide-map-of-utilities); [4M Foundation Utility Data](https://www.4manalytics.com/blog/foundation-utility-data); [SiliconANGLE 2022](https://siliconangle.com/?p=592292); [GlobeNewswire GDOT](https://www.globenewswire.com/de/news-release/2025/12/10/3203325/0/en/4M-s-Utility-AI-Platform-Delivers-Smarter-Faster-Safer-Infrastructure-for-the-Georgia-Department-of-Transportation.html)
- **Exodigo**:
  - On-site multi-sensor non-intrusive scans (GPR, EM, etc.) are AI-fused with records and imagery into 2D/3D BIM-compliant maps and digital twins. Expanded its portfolio in Jul 2026 and raised a $96M Series B.
  - Vendor pilot: 57% more lines than records. No independent peer-reviewed accuracy method is public.
  - Sources: [GlobeNewswire Jul 2026](https://www.globenewswire.com/news-release/2026/07/08/3324153/0/en/Exodigo-Brings-AI-Powered-Subsurface-Intelligence-to-Every-Stage-of-Infrastructure-Delivery-with-Expanded-Solutions.html); [Railway Technology](https://www.railway-technology.com/news/exodigo-96m-series-b-funding/); [datadrivenaec](https://datadrivenaec.com/tools/exodigo)
- **Urbint**: scores 811 tickets using ticket data, the utility's GIS, historical outcomes, and its "Model of the World." Vendor-reported results: National Grid damage-rate reduction (22% in one year per a case study) and SEMCO −21%. — [Urbint](https://urbint.com/solutions/urbint-for-damage-prevention); [casestudies.com National Grid](https://www.casestudies.com/company/urbint/case-study/national-grid-reduces-damages-22-in-1-year-with-urbint); [SEMCO](https://www.casestudies.com/company/urbint/case-study/semco-energy-cuts-third-party-damages-21-with-urbint)
- **ProStar**: publishes/hosts DIRT-related material. No product specifics were retrieved. — [ProStar on issuu](https://issuu.com/prostarcorp/docs/2019_dirt_report_final/s/11176443)

### Inferences
- 4M's method (harvest public ArcGIS REST servers like Madison's) is replicable at small scale by a hackathon team for municipal sewer, storm, and hydrant layers. Gas, electric, and fiber remain the gap 4M fills with permits and imagery, at enterprise prices.
- Partnering or licensing (4M API, NUAR-style agreements) is the only realistic route to private-utility geometry.

### Gaps
- No pages retrieved for Spotr, ProStar product details, or Esri Living Atlas / Utility Network public datasets. Esri's Utility Network is a data model and software used inside utilities, not a public data source (general knowledge, unverified here).
- No pricing or API terms were found for 4M or Exodigo.
