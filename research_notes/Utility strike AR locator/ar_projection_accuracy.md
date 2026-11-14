# AR Projection of Buried Utilities onto a Phone/Tablet Camera View: Positioning, Registration, Products, and Achievable Accuracy

Research date: 2026-11-14. US-first. Source dates are noted where they matter. "Vendor claim" means a figure the vendor reports about itself with no independent check found.

## 1. Phone positioning options and real-world accuracy compared with the 811 tolerance zone

### Takeaway
Phone GNSS alone gives about 2 to 10+ m error in cities. That is roughly 5 to 20 times wider than Wisconsin's 18-inch (about 0.46 m) tolerance zone, so it supports only "which side of the street" guidance. Google's VPS (ARCore Geospatial API) typically gets to about 1 m, with an upper bound under about 5 m, and is free to try in Street View areas. Only an external RTK receiver (about $1.6k to $2.7k for an Emlid Reach RX; under $1k is possible on Android with ArduSimple/u-blox) reliably gets centimeter positions, and that only needs sky view.

### Cited Findings
**811 / Wisconsin tolerance zone**
- Wis. Stat. § 182.0175(2)(am)3 requires an estimated minimum clearance of 18 inches between a marked, unexposed underground facility and the cutting edge or point of power-operated excavating equipment. PHMSA's state summary lists Wisconsin's tolerance zone as 18". — [PHMSA Wisconsin State DP Law Summary (2017)](https://primis.phmsa.dot.gov/Comm/StateDamagePrevention/State%20DP%20Law%20Summary/Wisconsin%20State_DP_Law_Summary_%2020170807.pdf); [Wis. Stat. 182.0175](https://docs.legis.wisconsin.gov/statutes/statutes/182/0175/2?up=1)
- Diggers Hotline (WI) says state law sets an 18-inch buffer on each side of a marked facility, with no mechanized equipment inside it (hand digging only). Notice is required at least 3 business days before excavating. — [Diggers Hotline homeowner FAQ](https://www.diggershotline.com/homeowner-faq); [WI PSC Diggers Hotline page](https://psc.wi.gov/Pages/ForConsumers/DiggersHotline.aspx)
- The sources disagree on whether hand digging is strictly required. The PHMSA summary marks "hand digging required in tolerance zone" as "No", while the Diggers Hotline FAQ says only hand digging is allowed. A 2025–2026 Diggers Hotline draft bill would add limits on power equipment inside the 18-inch zone, and it does not appear to be enacted. — [PHMSA summary](https://primis.phmsa.dot.gov/Comm/StateDamagePrevention/State%20DP%20Law%20Summary/Wisconsin%20State_DP_Law_Summary_%2020170807.pdf); [Diggers Hotline draft (Jan 2026)](https://www.diggershotline.com/assets/uploads/2026/08/P3%20draft%20-%20DPC%20-%20Jan%202026.pdf)

**Consumer and dual-frequency phone GNSS**
- On a Xiaomi Mi8 dual-frequency phone, L5 differential GNSS plus Doppler filtering reached 1.75 m horizontal and 4.56 m vertical accuracy. Static convergence to 1 m took 102 min, which is not usable for live AR. — [Sensors 2022, PMC9788430](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9788430/)
- In Hong Kong urban canyons, 3D-mapping-aided GNSS with phone L1+L5 averaged within about 10 m. L5 helps mainly through better multipath resistance (shorter chip length). — [NAVIGATION 2021 (ION)](https://navi.ion.org/content/68/4/727); [PolyU paper PDF](https://www.polyu.edu.hk/aae/ipn-lab/us/publications/Fullpaper/Urban%20Positioning_3D%20Mapping%20Aided%20GNSS%20using%20Dual-Frequency%20Pseudorange%20Measurements%20from%20Smartphones.pdf)
- Singapore static tests saw about 5 to 10 m error, and L5 improved Mi 9 accuracy by about 20–40% (student project, lower confidence). — [NTU repository](https://libmast.utm.my/Record/ntu-10356%2F140089/Description)

**Google ARCore Geospatial API / VPS**
- Google's ARCore reference says VPS position accuracy is typically better than 5 m and often around 1 m, with rotation accuracy better than 5°. — [ARCore Unity GeospatialPose reference](https://developers.google.com/ar/reference/unity-arf/struct/Google/XR/ARCoreExtensions/GeospatialPose)
- Google's Android XR docs (2026) say VPS "can often" deliver sub-meter position and sub-degree orientation when it localizes. This is a best case. — [Android XR Geospatial docs](https://developer.android.com/develop/xr/jetpack-xr-sdk/arcore/geospatial)
- Accuracy values are reported as 68th-percentile confidence radii. The heading accuracy field is deprecated in favor of an orientation yaw accuracy value. — [GeospatialPose reference](https://developers.google.com/ar/reference/unity-arf/struct/Google/XR/ARCoreExtensions/GeospatialPose)
- Coverage: VPS works wherever Google Street View exists. The localization model is built from "tens of billions of images" and spans "nearly all countries". Some ARCore devices do not support Geospatial. — [ARCore Geospatial overview](https://developers.google.com/ar/develop/geospatial)
- Google's Android quickstart sample allows anchor placement only once horizontal accuracy is 10 m or better. This is a sample threshold the developer can change, not a spec. — [ARCore Java Geospatial quickstart](https://developers.google.com/ar/develop/java/geospatial/quickstart)
- Independent test (Horvath, Toth, Barsi, IEEE/ION PLANS 2025): VPS reached sub-meter accuracy only under favorable conditions (distinctive landmarks, good imagery). This was checked against RTK-surveyed control points on a short track and a city-block loop. The numeric results are paywalled. — [ION abstract](https://www.ion.org/publications/abstract.cfm?articleID=20196)
- One developer's anecdotal test reported a best horizontal accuracy reading of a little over 2 m in an open field in Chicago, where Street View features are scarce. — [Sam Robertson blog](https://samrobertson-dev.vercel.app/blog/arcore-camera-geolocating)

**Apple ARKit location anchors (ARGeoTrackingConfiguration)**
- Geotracking works only outdoors and only in specific supported areas. Apps should check with `checkAvailability(at:)` at runtime. — [Apple ARGeoTrackingConfiguration docs](https://developer.apple.com/documentation/arkit/argeotrackingconfiguration.md)
- At launch (WWDC20) it covered the SF Bay Area, New York, Chicago and Miami. A later forum reply named five areas (Bay Area, LA, NY, Chicago, Miami), all in the US at that time (2020–2021 info, likely expanded since). — [WWDC20 notes](https://wwdcnotes.com/documentation/wwdc20-10611-explore-arkit-4/); [Apple forum thread](https://developer.apple.com/forums/thread/654417)

**Niantic Spatial (formerly Lightship) VPS**
- Niantic's docs claim centimeter-level position and orientation "in seconds", but only at VPS-activated (pre-mapped) locations. No independent test was found. — [Niantic Spatial VPS docs](https://www.nianticspatial.com/docs/nsdk/features/lightship_vps/)

**RTK GNSS add-ons**
- Emlid Reach RX launched at $1,599. Current US listings range from about $1,889 to $2,199, and a network-rover kit is $2,658. It feeds iOS/Android over Bluetooth and pulls NTRIP corrections through the phone's internet connection. The RX2 adds IMU tilt compensation (£2,099). — [Informed Infrastructure](https://informedinfrastructure.com/index.php/post/emlid-released-reach-rx-pocket-sized-rtk-rover-for-1599); [Advexure](https://advexure.com/products/emlid-reach-rx); [Unmanned Tech RX2](https://www.unmannedtechshop.co.uk/products/emlid-reach-rx2)
- The ArduSimple RTK Calibrated Surveyor Kit (u-blox based) connects to Android over USB OTG or Bluetooth and claims <1 cm with NTRIP up to 35 km. It is not iOS compatible. No price was found. — [Mouser ArduSimple](https://www.mouser.co.za/new/ardusimple/ardusimple-rtk-calibrated-surveyor-kit)
- In a tunnel test, an iPhone with an RTK receiver got a full RTK fix on only 10–15% of images, so RTK fails without sky view. — [Pix4D blog](https://www.pix4d.com/blog/smartphones-mapping-underground-infrastructure-Pix4D)

### Inferences
- Error budget compared with the 18" (0.46 m) zone:
  - Phone GNSS (2–10 m) fails the zone outright.
  - VPS at about 1 m typical gives about 2x the zone half-width at best and up to about 10x at worst.
  - RTK at 1–5 cm fits easily, but **positioning is not the dominant error once RTK is used**. Heading error and the accuracy of the utility map itself then dominate (see section 2).
- Heading error matters as much as position error. A 5° yaw error displaces a pipe drawn 5 m away by about 0.44 m (5 m × tan 5°), which alone uses up the whole 18" zone. A 1° error at 5 m is about 9 cm.
- For a "rough idea where to dig" hackathon demo, the ARCore Geospatial API (free, works in any Street View area, which includes Madison WI streets) is the right default. Fall back to manual alignment (section 2) where VPS confidence is poor. Plan RTK as the production upgrade path.

### Gaps
- I found no Google-published 95th-percentile error figure for VPS, and the numeric results of the ION PLANS 2025 test are paywalled.
- I could not retrieve the current ARKit geotracking city list (Apple's docs page did not render). Check whether Madison, WI is covered with `checkAvailability`, though it is likely not.
- No current ArduSimple or bare u-blox ZED-F9P price was found. My understanding from memory is that sub-$500 board kits exist, but this is unverified.
- No current Niantic VPS coverage map was found.

## 2. Registration by visual anchors (PnP / landmark localization), plus depth/occlusion rendering

### Takeaway
I found no published system that solves the camera pose from GIS-surveyed hydrants, manholes and curbs and reports field accuracy for utility AR. The closest work uses facade landmarks, Street View point clouds, or manholes as tracked features, with sub-meter results. In practice, the pragmatic method is a one- or two-point manual alignment: tap a known hydrant or manhole whose GIS coordinates you hold, then let ARKit/ARCore VIO hold the pose. Esri's own SDK uses exactly this pattern (a calibration UI for heading and elevation).

### Cited Findings
- Esri ArcGIS Maps SDK "world-scale" AR has two modes:
  - Geospatial tracking uses Google Street View/VPS. It requires ARCore authentication, gives the best accuracy, and needs no manual calibration.
  - World tracking uses device GPS, so accuracy depends on GPS. Esri recommends a calibration UI so users can correct heading and elevation.
  - — [Esri Kotlin: Display global scenes in AR](https://developers.arcgis.com/kotlin/scenes-3d/display-global-scenes-in-augmented-reality/)
- Esri's Swift toolkit WorldScaleSceneView now accepts other VPS providers for localization. — [Esri Swift toolkit releases](https://github.com/Esri/arcgis-maps-sdk-swift-toolkit/releases)
- "Metric Localization using Google Street View" used manholes as distinctive reference points, with AprilTag ground truth. It reports that error grows with distance to the tracked features. — [arXiv 1503.04287](https://arxiv.org/pdf/1503.04287)
- GIS-assisted detection work (Ardeshir et al.) frames localization as 6-DoF pose against geo-registered data, using GIS priors such as traffic signs, streetlights and fire hydrants. Li & Snavely's worldwide 3D-point-cloud pose estimation reports sub-meter-level results. — [GIS-Assisted Object Detection and Geospatial Localization](https://www.researchgate.net/publication/300358520_GIS-Assisted_Object_Detection_and_Geospatial_Localization); [Li & Snavely, Worldwide Pose Estimation](https://landmark.cs.cornell.edu/docs/global_pose.pdf)
- Microsoft's ALPS localized street landmarks from Street View. Hydrants were hardest because they are dense, so they alias. It found 87% of hydrants within 10 m. — [ALPS (Microsoft Research)](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/07/ALPS_camera_ready_version.pdf)
- "Spotter" (arXiv, 2026) uses geo-referenced facade landmarks, PnP and a Kalman filter for 6-DoF pose in GPS-degraded urban areas. I did not verify its numbers. — [arXiv 2608.23290](https://arxiv.org/pdf/2608.23290)
- A review cited in utility-AR literature puts registration accuracy of earlier utility AR systems at about 30 cm to 3 m. A BeiDou + SLAM system reached 0.6 m with real-time differential corrections. — [Mobile AR framework for underground pipe O&M, Tunnelling & Underground Space Tech. 2023](https://www.sciencedirect.com/science/article/abs/pii/S0886779823000895)
- Su, Talmaki, Cai & Kamat (2013) model "spatial bands" with a stated probability of enclosing a utility's true location. The method's success depends on the quality of the utility location data. — [Springer Professional](https://www.springerprofessional.de/uncertainty-aware-visualization-and-proximity-monitoring-in-urba/10801434)

### Inferences
- **Two-point manual registration is the hackathon method.** The user stands over or taps 2 known GIS points (hydrant, manhole lid, valve box) visible on the ARKit/ARCore ground plane. That fixes translation and yaw, and VIO handles the rest. Expected error is then dominated by:
  - GIS feature coordinate error (often sub-meter for survey-grade utility GIS, but often meters for digitized as-builts)
  - the tap/placement error of about 5–20 cm
  - VIO drift over walk distance
  
  This is my estimate, not a measured figure.
- Automatic YOLO-detect-then-PnP on hydrants/manholes is feasible but hard. Manhole lids lie on the ground plane, so a ray-cast onto the ARKit plane plus the GIS coordinate gives a point correspondence directly, with no full PnP needed. Hydrant aliasing (ALPS) means you need a GPS/VPS prior to tell which hydrant is which.
- Depth rendering: show pipes as an "x-ray" trench or cutaway box, sunk below the detected ground plane, with a depth label. Render the uncertainty as a buffer band (as Su et al. do) instead of a thin line. That is the honest way to show "dig here roughly".

### Gaps
- I found no paper reporting measured registration error for hydrant/manhole-landmark PnP in utility AR. This is an open gap.
- I did not retrieve sources on ARKit/ARCore occlusion APIs (LiDAR depth, ARCore Depth API) for x-ray rendering. These are standard SDK features, but I have no citation in these notes.

## 3. Existing AR utility visualization products: accuracy, price, data, users

### Takeaway
Commercial products all reach "centimeter" accuracy the same way: an external RTK/GNSS receiver (Leica, Trimble Catalyst, Bad Elf, Emlid) feeding the phone, plus the utility's own GIS (mostly Esri). The cm figures are vendor claims with no independent field validation found. Prices run from hundreds to a few thousand dollars per seat per year, plus receiver hardware.

### Cited Findings
- **vGIS** (Esri/Autodesk/Leica partner):
  - Claims cm-level overlays. With a Leica GS18, the CEO says it gets "within 7 mm".
  - Tilting the device temporarily degrades accuracy to about 1 to 4–5 cm (software tilt compensation has a lag). He also says accuracy does not degrade with distance walked.
  - A case study (Warsaw Bridge) says it helped avoid line strikes.
  - — [vGIS/Leica partner page](https://leica-geosystems.com/products/gis-collectors/gis-partners/vgis); [vGIS high-accuracy AR for SUE](https://prod-meemim-vgis-io-testing.azurewebsites.net/?p=106); [Bad Elf vGIS](https://www.bad-elf.com/pages/vgis); [ForConstructionPros on vSite](https://www.forconstructionpros.com/equipment/worksite/underground/article/22908368/vgis-extends-augmented-reality-solution-with-vsite)
- **Trimble SiteVision**:
  - Claims cm accuracy with the Catalyst DA2 GNSS receiver (Bluetooth), on iOS/Android, pole- or handle-mounted. An Integrated Positioning System variant with a DA1 antenna over USB is Android only.
  - Pulls data from Trimble NIS (electric), Trimble Unity (water) and Trimble Business Center. The pitch is to "reveal hidden infrastructure such as underground utilities".
  - The SiteVision Universal AR Unlimited subscription bundles Catalyst, but only for SiteVision.
  - A reseller notes the cm accuracy holds "in supported environments" and depends on sky view.
  - — [Trimble SiteVision product page](https://geospatial.trimble.com/en/products/software/trimble-sitevision); [SiteVision utilities](https://sitevision.trimble.com/utilities); [SiteVision FAQ](https://sitevision.trimble.com/?p=42); [Geo Week News 2019](https://www.geoweeknews.com/articles/trimble-brings-high-accuracy-to-augmented-reality-with-sitevision/)
- **ProStar PointMan**:
  - Claims to capture and display the precise location of underground infrastructure "to the centimeter".
  - A 2025 Pix4D partnership adds 3D AR visualization of buried assets. It is bundled with Bad Elf RTK receivers.
  - The pricing page lists a $695 tier and a $6,950 tier, with RTK corrections from $250 per license. An older page lists PointManPlus at $295/seat/yr and PointManPro at $2,495/seat (2-seat minimum). Confirm current pricing.
  - — [PointMan pricing](https://pointman.com/pricing/); [ProStar–Pix4D PR](https://seekingalpha.com/pr/20061598-prostar-and-pix4d-partner-to-provide-precision-3d-augmented-reality-of-critical-underground); [Bad Elf PointMan](https://bad-elf.com/pages/pointman)
- **Esri ArcGIS Maps SDKs (Swift/Kotlin/.NET) world-scale AR**: these are developer SDKs, not finished products. They use Google VPS or device GPS, with optional pluggable VPS providers and a calibration UI (see section 2). — [Esri Kotlin AR docs](https://developers.arcgis.com/kotlin/scenes-3d/display-global-scenes-in-augmented-reality/)
- **Academic utility-AR systems**: LARA paired an RTK GNSS device with a regular smartphone and reports real-time cm-level acquisition. A MATEC 2019 paper describes a tablet with RTK and claims sub-cm, though it is unclear whether that was field-measured. — [LARA (ResearchGate)](https://www.researchgate.net/publication/314105419_LARA_A_location-based_and_augmented_reality_assistive_system_for_underground_utilities'_networks_through_GNSS); [MATEC 2019](https://www.matec-conferences.org/articles/matecconf/pdf/2019/44/matecconf_suslille2019_02009.pdf)

### Inferences
- Every serious product = RTK receiver + utility-owned GIS + phone AR. The hard part commercially is the **data**: utility GIS access and its accuracy. Rendering is not the problem. A hackathon team without utility GIS data has to use public layers (city water/sewer GIS where published) or fake data, and should state that clearly.
- The users are utility owners, SUE (subsurface utility engineering) firms and contractors with existing GIS. These are not homeowners calling 811.

### Gaps
- I found nothing on Augview, Unearth, Arvizio, AmeriAR, Bentley SYNCHRO/iTwin AR, Hexagon/Leica native AR, or Esri Field Maps AR beyond vGIS–Leica. The searches returned nothing usable within budget.
- I found no vGIS or SiteVision list prices.
- I found no independent (non-vendor) field validation of any product's cm claim.

## 4. Research studies on AR for excavation/utility locating, with measured errors

### Takeaway
The Univ. of Michigan line (Talmaki, Dong, Kamat 2010; Su, Talmaki, Cai, Kamat 2013) set the architecture: GIS-derived 3D utility models, RTK GPS on the excavator, geo-referenced AR, and uncertainty bands for proximity warnings. I could not retrieve their measured error figures. The ASCE smartphone study (Fenais et al.) concluded that phones without external high-accuracy GPS are not adequate for underground construction.

### Cited Findings
- Talmaki, Dong & Kamat (Construction Research Congress 2010, ASCE pp. 91–101): 3D utility models built from geospatial databases and superimposed on the excavator workspace using geo-referenced AR plus RTK GPS. The work was validated in a simulated static excavation with DTE Energy. — [TRID 923675](https://trid.trb.org/view/923675); [Scipedia Talmaki et al 2010a](https://scipedia.com/public/Talmaki_et_al_2010a)
- Su, Talmaki, Cai & Kamat (2013), "Uncertainty-aware Visualization and Proximity Monitoring in Urban Excavation: a Geospatial AR Approach": probability bands around utilities, plus proximity monitoring between the excavator and the bands. — [Springer Professional](https://www.springerprofessional.de/uncertainty-aware-visualization-and-proximity-monitoring-in-urba/10801434); [Bohrium/arXiv mirror](https://bohrium.dp.tech/paper/arxiv/56d8767adabfae2eee1bfbed)
- Exploratory analysis of AR visualization for right-of-way excavation safety (TRB). — [TRID 1335204](https://trid.trb.org/View/1335204)
- Fenais et al., ASCE Journal of Pipeline Systems Engineering and Practice: compared smartphones with and without external GPS against a total-station reference at 16 points. They concluded that current smartphones cannot be adopted in underground construction without higher-accuracy integrated GPS. — [ASCE DOI 10.1061/(ASCE)PS.1949-1204.0000474](https://doi.org/10.1061/(ASCE)PS.1949-1204.0000474)
- A review states that the accurate locations of at least 50% of buried assets remain unknown. Excavation is the largest cause of utility strikes. — [MDPI Infrastructures 4(4):60](https://mdpi.com/2412-3811/4/4/60/htm)
- Earlier utility-AR registration accuracy ranges from about 30 cm to 3 m. BeiDou + SLAM reached 0.6 m with RTD. — [Tunnelling & Underground Space Tech. 2023](https://www.sciencedirect.com/science/article/abs/pii/S0886779823000895)

### Inferences
- The map is usually the bigger error than the phone. If about 50% of buried asset locations are not accurately known, even perfect AR registration only faithfully displays an uncertain map. The product framing should be "pre-locate guidance; 811 marks remain authoritative".
- Rendering uncertainty bands (Su et al.) is the research-backed UI pattern, and it maps neatly onto the 18" tolerance zone: draw the pipe plus an 18" band plus the registration error band.

### Gaps
- I could not access the numeric results of Fenais et al. (ASCE, paywalled, and the ASU repository returned 403) or of the Kamat group papers. I found no cm figures for them.
- I found no recent (2024–2026) excavator-mounted AR field trial with measured errors.

## 5. Practical stack for a hackathon prototype

### Takeaway
Build a native app. iPhone Safari still does not support WebXR immersive-ar in 2026 (contested by one blog), so three.js/WebXR is Android-Chrome-only. The fastest route that gets geo-anchoring is Unity AR Foundation plus ARCore Extensions (Geospatial works on both iOS and Android), or native ARCore Geospatial on Android. On-device YOLO11n runs at about 7–17 ms per frame in CoreML, so live hydrant/manhole detection is affordable.

### Cited Findings
- WebXR on iOS Safari: most 2026 sources say it is unsupported on iPhone and that Apple has announced no plans. visionOS 2 Safari does support WebXR. One mid-2026 blog claims Safari 18 ships immersive-ar on iOS, which contradicts the others and is unverified. iPhone web AR alternatives are AR Quick Look (USDZ), or 8thwall.org/Zappar camera-based SDKs. — [threejsresources WebXR browsers](https://threejsresources.com/webxr/browsers); [threejsresources AR](https://threejsresources.com/ar); [Wikipedia WebXR](https://en.wikipedia.org/wiki/WebXR); [tobias-weiss.org (outlier)](https://tobias-weiss.org/content/webxr-ai-2026-platform-state/)
- ARCore Geospatial API has a Unity AR Foundation path (ARCore Extensions) and an iOS SDK, as Google publishes separate unity-arf, ios, java and c guides. — [ARCore Geospatial Unity VPS check](https://developers.google.com/ar/develop/unity-arf/geospatial/check-vps-availability); [ARCore iOS VPS check](https://developers.google.com/ar/develop/ios/geospatial/check-vps-availability?authuser=4)
- Esri's Maps SDKs (Swift/Kotlin) ship a ready WorldScaleSceneView AR component that can consume Esri feature layers directly. — [Esri Kotlin AR toolkit](https://github.com/Esri/arcgis-maps-sdk-kotlin-toolkit/tree/main/toolkit/ar)
- YOLO speeds:
  - Ultralytics iOS app docs: about 7 ms in-app compared with about 1.8 ms in the isolated benchmark (the gap is pipeline/thermal contention).
  - Roboflow: YOLO11 went from 21 FPS (PyTorch) to 85 FPS after CoreML export.
  - Community model card: about 30–60 FPS on iPhone 11–14.
  - — [Ultralytics yolo-ios-app performance.md](https://github.com/ultralytics/yolo-ios-app/blob/main/docs/performance.md); [Roboflow iOS models](https://blog.roboflow.com/best-ios-object-detection-models/); [HF yolo11n-coreml](https://huggingface.co/riddhimanrana/yolo11n-coreml)

### Inferences
- Recommended hackathon architecture:
  1. Unity + AR Foundation + ARCore Extensions (Geospatial). Alternatively, use native Swift ARKit with the ARCore Geospatial iOS SDK.
  2. Load utility lines as GeoJSON in lat/lon/depth, and place them as geospatial or terrain anchors.
  3. Gate on the reported horizontal/yaw accuracy, and show "low confidence" when accuracy is over 1.5 m or yaw error is over 3°.
  4. Offer a "tap the hydrant/manhole" two-point realign as a fallback.
  5. Render pipes below the ground plane with a translucent cutaway, plus an 18" tolerance band widened by the reported error.
  6. YOLO detection of hydrants/manholes is a stretch feature, used to auto-suggest realign points.
- Expected accuracy without RTK is about 0.5 to 2 m in Street-View-covered streets, which fits "rough idea of where to dig / where to call 811 about". It is not good enough to excavate without 811 marks. With RTK plus a good heading lock, about 5–15 cm is plausible (my estimate, built from vendor figures and the heading-error arithmetic in section 1).

### Gaps
- I found no measured ARCore Geospatial accuracy specifically on iOS compared with Android.
- I have no direct citation for ARCore Streetscape Geometry / Depth API occlusion performance.
- I did not verify that Madison, WI has VPS coverage. Check with `checkVpsAvailability` on site.
