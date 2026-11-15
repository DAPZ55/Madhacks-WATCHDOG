import ARKit
import RealityKit
import SwiftUI

// Calibration knob. Tune on the real site.
/// Printed image = black square + white border. tag_image() in edge/tags.py adds 1/6 per side.
let printedToSquareRatio: Float = 4.0 / 3.0
/// Largest correction accepted when moving a tag onto the detected floor. Bigger gap = wrong surface.
let maxFloorSnapM: Float = 0.30
/// See-through ground overlays so the real floor stays readable. Knobs: 0 = invisible, 1 = solid.
let lineOpacity: Float = 0.55
let zoneOpacity: Float = 0.5

@main
struct Vision811App: App {
    var body: some SwiftUI.Scene {
        WindowGroup { ContentView() }
    }
}

struct ContentView: View {
    @StateObject private var model = AppModel()
    @AppStorage("serverHost") private var server = "Madhacks16.local:8000"  // key renamed so the UNO Q default replaces old typed Mac addresses
    @AppStorage("jurisdiction") private var jurisdictionID = "WI"
    @State private var showLegend = false
    @State private var showSetup = false

    private var jurisdiction: Jurisdiction { .named(jurisdictionID) }

    var body: some View {
        ARContainer(model: model, jurisdiction: jurisdiction)
            .ignoresSafeArea()
            .overlay(alignment: .top) { hud }
            .overlay(alignment: .bottom) { dock }
            .sheet(isPresented: $showLegend) { LegendView(jurisdiction: jurisdiction) }
            .sheet(isPresented: $showSetup) { SetupView(server: $server, model: model, jurisdiction: jurisdiction) }
            .preferredColorScheme(.dark)
            .task {  // poll so a newly published revision reaches the phone without a tap
                while !Task.isCancelled {
                    model.refresh(server: server)
                    try? await Task.sleep(for: .seconds(3))
                }
            }
    }

    /// Top: one compact status panel, then only the warnings that currently apply.
    private var hud: some View {
        VStack(spacing: Theme.s2) {
            Panel(translucent: true) {
                HStack(spacing: Theme.s2) {
                    Text("811 Vision").font(Theme.display(22)).textCase(.uppercase).foregroundStyle(Theme.fg)
                    Spacer()
                    if let map = model.map {
                        if map.scale < 1 { Tag(text: "Model 1:\(Int((1 / map.scale).rounded()))", tone: .action) }
                        Tag(text: "Rev \(map.mapRevision)")
                    }
                }
                Text(model.alignNote).font(Theme.body(14)).foregroundStyle(Theme.fg2)
                    .fixedSize(horizontal: false, vertical: true)
            }
            if let problem = model.mapProblem { NoticeBar(text: problem, tone: .danger) }
            if let n = model.map?.discrepancies.count, n > 0 {
                NoticeBar(text: "Warning: \(n) unresolved paint vs layout discrepancy. Both paths shown.")
            }
        }
        .padding(.horizontal, Theme.s3).padding(.top, Theme.s2)
    }

    /// Bottom: controls within thumb reach, then the always-on advisory strip.
    private var dock: some View {
        VStack(spacing: 0) {
            VStack(spacing: Theme.s2) {
                if model.map?.utilities.isEmpty == false {
                    NoticeBar(text: "Simulated depth: pipes drawn at \(jurisdiction.name) minimum-cover rules. Not measured.")
                }
                HStack(spacing: Theme.s2) {
                    Menu {
                        Picker("State rules", selection: $jurisdictionID) {
                            ForEach(Jurisdiction.all) { Text($0.name).tag($0.id) }
                        }
                    } label: {
                        Text("Rules · \(jurisdiction.id)")
                            .font(Theme.label(16)).tracking(1.4).textCase(.uppercase).foregroundStyle(Theme.fg)
                            .lineLimit(1).minimumScaleFactor(0.75)
                            .frame(maxWidth: .infinity, minHeight: Theme.tapHeight)
                            .background(Theme.surface2)
                            .overlay(Rectangle().strokeBorder(Theme.line, lineWidth: Theme.hairline))
                    }
                    .accessibilityLabel("State rules: \(jurisdiction.name)")
                    Button("Legend") { showLegend = true }.buttonStyle(.industrial)
                    Button {
                        showSetup = true
                    } label: {
                        Image(systemName: "gearshape").font(.system(size: 20))
                    }
                    .buttonStyle(.industrialCompact)
                    .accessibilityLabel("Setup")
                }
                Button("Recalibrate") { model.recalibrations += 1 }.buttonStyle(.industrialPrimary)
            }
            .padding(Theme.s3)
            .background(Theme.bg.opacity(0.82))
            AdvisoryFooter(text: "Advisory demo · Not a utility locate · Depth unknown")
        }
    }
}

/// Connection and rules details, off the main screen so the camera view stays clear.
struct SetupView: View {
    @Binding var server: String
    @ObservedObject var model: AppModel
    let jurisdiction: Jurisdiction
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: Theme.s4) {
                ScreenHeader(index: "Setup", title: "Connection")
                Panel(title: "Edge server") {
                    Text("Address of the UNO Q on the site Wi-Fi.").font(Theme.body(14)).foregroundStyle(Theme.fg2)
                    TextField("host:port", text: $server)
                        .font(Theme.mono(15)).foregroundStyle(Theme.fg)
                        .keyboardType(.URL).autocorrectionDisabled().textInputAutocapitalization(.never)
                        .padding(.horizontal, Theme.s3).frame(minHeight: Theme.tapHeight)
                        .background(Theme.surface2)
                        .overlay(Rectangle().strokeBorder(Theme.line, lineWidth: Theme.hairline))
                        .accessibilityLabel("Edge server address")
                    Button("Refresh map") { model.refresh(server: server) }.buttonStyle(.industrialPrimary)
                    Text(model.mapNote).font(Theme.body(13)).foregroundStyle(model.mapProblem == nil ? Theme.fg2 : Theme.danger)
                        .fixedSize(horizontal: false, vertical: true)
                }
                Panel(title: "Active rules") {
                    Readout(key: "Jurisdiction", value: jurisdiction.name)
                    Readout(key: "One-call", value: jurisdiction.oneCall)
                    Readout(key: "Tolerance zone", value: String(format: "%.0f in each side", jurisdiction.toleranceIn))
                }
                Button("Done") { dismiss() }.buttonStyle(.industrial)
            }
            .padding(Theme.s4)
        }
        .background(Theme.bg.ignoresSafeArea())
        .preferredColorScheme(.dark)
    }
}

struct ARContainer: UIViewRepresentable {
    @ObservedObject var model: AppModel
    let jurisdiction: Jurisdiction

    func makeCoordinator() -> Coordinator { Coordinator(model: model) }

    func makeUIView(context: Context) -> ARView {
        let view = ARView(frame: .zero)
        context.coordinator.view = view
        view.session.delegate = context.coordinator
        return view
    }

    func updateUIView(_ view: ARView, context: Context) {
        let c = context.coordinator
        let newMap = model.map?.mapRevision != c.loadedRevision
        let newRules = jurisdiction.id != c.jurisdiction?.id
        c.jurisdiction = jurisdiction
        let recalibrate = model.recalibrations != c.recalibrations
        c.recalibrations = model.recalibrations
        if newMap || recalibrate {
            c.load(model.map)  // new revision or Recalibrate: forget anchor poses, restart tracking, realign
        } else if newRules {
            c.rebuild()  // same map, different state rules: redraw only, keep alignment
        }
    }

    /// ARSession delegate callbacks arrive on the main queue (default delegateQueue).
    final class Coordinator: NSObject, ARSessionDelegate {
        let model: AppModel
        weak var view: ARView?
        var loadedRevision: Int?
        var jurisdiction: Jurisdiction?
        var recalibrations = 0

        private var map: SiteMap?
        private let worldAnchor = AnchorEntity(world: .zero)
        private let siteRoot = Entity()  // children are in site-frame meters
        // ponytail: last seen pose per anchor is kept forever; age them out if ARKit drift shows.
        private var observed: [String: simd_float4x4] = [:]
        /// Where each marker's sight line meets the real floor (LiDAR plane). Used as its true position.
        private var floorPoint: [String: SIMD3<Float>] = [:]
        private var aligned = false
        private var trackingOK = false

        init(model: AppModel) { self.model = model }

        func load(_ map: SiteMap?) {
            guard let view else { return }
            self.map = map
            loadedRevision = map?.mapRevision
            observed.removeAll()
            floorPoint.removeAll()
            aligned = false
            siteRoot.isEnabled = false
            rebuild()
            guard let map else { view.session.pause(); return }
            if worldAnchor.scene == nil {
                worldAnchor.addChild(siteRoot)
                view.scene.addAnchor(worldAnchor)
            }

            let config = ARWorldTrackingConfiguration()
            config.detectionImages = Set(map.anchors.compactMap { anchor in
                guard let cg = UIImage(named: anchor.id)?.cgImage else { return nil }
                let ref = ARReferenceImage(cg, orientation: .up,
                                           physicalWidth: CGFloat(anchor.sizeM * printedToSquareRatio))
                ref.name = anchor.id
                return ref
            })
            config.maximumNumberOfTrackedImages = 4
            config.planeDetection = [.horizontal]  // the real floor is the ground reference
            // ARKit measures each tag's real size itself, so a small size_m error does not shift the overlay.
            config.automaticImageScaleEstimationEnabled = true
            view.session.run(config, options: [.resetTracking, .removeExistingAnchors])
            model.alignNote = "Point camera at an anchor tag."
        }

        /// Redraw all utilities from the map using the selected state's labels, tolerance zone, and cover rules.
        func rebuild() {
            siteRoot.children.removeAll()
            guard let map, let rules = jurisdiction else { return }
            let k = map.scale  // scale model: shrink real-world rule distances, grow length labels back
            var zonePaths: [(SIMD3<Float>, SIMD3<Float>)] = []  // every path gets a tolerance zone
            for utility in map.utilities {
                let color = markingColors[utility.markingColor] ?? .white
                let entry = rules.entry(color: utility.markingColor)
                // Paint evidence: tolerance-zone corridor + solid line. Layout evidence: thin white-edged line. Never merged.
                for (a, b) in segments(utility.surfaceMarking) {
                    siteRoot.addChild(strip(a, b, width: 0.04, lift: 0.006, color: color, opacity: lineOpacity))
                }
                for (a, b) in segments(utility.uploadedLayout) {
                    siteRoot.addChild(strip(a, b, width: 0.05, lift: 0.004, color: .white, opacity: lineOpacity * 0.7))
                    siteRoot.addChild(strip(a, b, width: 0.02, lift: 0.008, color: color, opacity: lineOpacity))
                }
                zonePaths += segments(utility.surfaceMarking) + segments(utility.uploadedLayout)
                // Pipe + labels follow the layout path if there is one, else the paint path.
                let path = segments(utility.uploadedLayout).isEmpty ? segments(utility.surfaceMarking)
                                                                    : segments(utility.uploadedLayout)
                // Display depth: state minimum-cover rule, else the map's hypothetical value. Never depth_m.
                let depth = (entry?.coverM ?? utility.simulatedDepth).map { $0 * k }
                for (a, b) in path {
                    siteRoot.addChild(label(String(format: k < 1 ? "~%.1f m" : "~%.2f m", simd_length(b - a) / k),
                                            at: (a + b) / 2 + [0, 0, 0.06], size: k < 1 ? 0.022 : 0.04))
                    if let depth, depth > 0 {
                        siteRoot.addChild(pipe(a, b, depth: depth, radius: max(0.006, 0.025 * k), color: color))
                    }
                }
                if let start = path.first?.0 {
                    let name = entry?.label ?? utility.utilityClass
                    let cover = entry?.coverIn.map { String(format: " · min cover %.0f in, simulated", $0) }
                        ?? " · depth unknown"
                    siteRoot.addChild(label(name + cover, at: start + [0, 0, 0.13], size: k < 1 ? 0.016 : 0.022))
                }
            }
            if let zones = toleranceZones(zonePaths, halfWidth: rules.toleranceM * k) {
                siteRoot.addChild(zones)
            }
        }

        func session(_ session: ARSession, didAdd anchors: [ARAnchor]) { observe(anchors, session) }
        func session(_ session: ARSession, didUpdate anchors: [ARAnchor]) { observe(anchors, session) }

        private func observe(_ anchors: [ARAnchor], _ session: ARSession) {
            var changed = false
            for case let image as ARImageAnchor in anchors where image.isTracked {
                let name = image.referenceImage.name ?? ""
                observed[name] = image.transform
                if let hit = floorHit(session, toward: image.transform) { floorPoint[name] = hit }
                changed = true
            }
            if changed { refit() }
        }

        /// ARKit knows a tag's direction from the camera precisely but its distance only roughly
        /// (judged from apparent size). The floor plane from LiDAR is precise. So: shoot the
        /// camera-to-tag sight line at the floor and take that hit as the tag's position.
        private func floorHit(_ session: ARSession, toward tag: simd_float4x4) -> SIMD3<Float>? {
            guard let cam = session.currentFrame?.camera.transform.columns.3 else { return nil }
            let origin = SIMD3<Float>(cam.x, cam.y, cam.z)
            let center = SIMD3<Float>(tag.columns.3.x, tag.columns.3.y, tag.columns.3.z)
            guard simd_distance(origin, center) > 0.05 else { return nil }
            for target in [ARRaycastQuery.Target.existingPlaneGeometry, .existingPlaneInfinite, .estimatedPlane] {
                let query = ARRaycastQuery(origin: origin, direction: simd_normalize(center - origin),
                                           allowing: target, alignment: .horizontal)
                let hits = session.raycast(query).map {
                    SIMD3<Float>($0.worldTransform.columns.3.x, $0.worldTransform.columns.3.y, $0.worldTransform.columns.3.z)
                }
                // The floor under the tag, not a table the ray crossed: nearest hit to ARKit's own estimate,
                // and reject anything implausibly far from it.
                if let best = hits.min(by: { simd_distance($0, center) < simd_distance($1, center) }),
                   simd_distance(best, center) < maxFloorSnapM {
                    return best
                }
            }
            return nil
        }

        private func refit() {
            guard let map else { return }
            var pairs: [(site: SIMD3<Float>, ar: SIMD3<Float>)] = []
            for anchor in map.anchors {
                guard let t = observed[anchor.id] else { continue }
                pairs.append((anchor.position, floorPoint[anchor.id] ?? SIMD3(t.columns.3.x, t.columns.3.y, t.columns.3.z)))
            }
            // One tag: borrow heading from the tag itself. Convention: tag lies flat, its printed
            // top edge points toward site +Y. (ARKit image anchor: -Z is the image's top.)
            if pairs.count == 1, let anchor = map.anchors.first(where: { observed[$0.id] != nil }),
               let t = observed[anchor.id] {
                let ahead = t * SIMD4<Float>(0, 0, -0.5, 1)
                // Shift the heading point by the same floor correction as the tag itself.
                let shift = pairs[0].ar - SIMD3(t.columns.3.x, t.columns.3.y, t.columns.3.z)
                pairs.append((anchor.position + [0, 0.5, 0], SIMD3(ahead.x, ahead.y, ahead.z) + shift))
            }
            // Markers are ground level. With 3+ tags the ground plane goes through their centers;
            // with fewer, it follows the tags' own faces (image anchor +Y = out of the print).
            var faceUp = SIMD3<Float>.zero
            for anchor in map.anchors {
                if let t = observed[anchor.id] { faceUp += SIMD3(t.columns.1.x, t.columns.1.y, t.columns.1.z) }
            }
            // Floor found: it is level, so "up" is gravity. Otherwise fall back to the tags' faces.
            let onFloor = map.anchors.filter { floorPoint[$0.id] != nil }.count
            let up: SIMD3<Float> = onFloor > 0 ? [0, 1, 0] : (simd_length(faceUp) > 0 ? simd_normalize(faceUp) : [0, 1, 0])
            guard let fit = fitSiteTransform(pairs, up: up) else { return }
            siteRoot.transform = Transform(matrix: fit)
            aligned = true
            siteRoot.isEnabled = trackingOK
            let ids = map.anchors.map(\.id).filter { observed[$0] != nil }
            model.alignNote = "Aligned on " + ids.joined(separator: ", ")
                + (onFloor == ids.count ? ". Ground = real floor at markers."
                   : ". Floor not found yet for \(ids.count - onFloor) tag(s); keep scanning the floor.")
        }

        func session(_ session: ARSession, cameraDidChangeTrackingState camera: ARCamera) {
            if case .normal = camera.trackingState { trackingOK = true } else { trackingOK = false }
            siteRoot.isEnabled = trackingOK && aligned  // hide overlay rather than show it wrong
            if !trackingOK { model.alignNote = "TRACKING LOST. Overlay hidden. Move slowly, re-aim at a tag." }
            else if aligned { refit() }
        }
    }
}

private func segments(_ path: SiteMap.Path?) -> [(SIMD3<Float>, SIMD3<Float>)] {
    guard let points = path?.points, points.count >= 2 else { return [] }
    return Array(zip(points, points.dropFirst()))
}

/// Flat strip on the ground between two site-frame points.
private func strip(_ a: SIMD3<Float>, _ b: SIMD3<Float>, width: Float, lift: Float,
                   color: UIColor, opacity: Float) -> Entity {
    let d = b - a
    var material = UnlitMaterial(color: color)
    if opacity < 1 { material.blending = .transparent(opacity: .init(floatLiteral: opacity)) }
    let entity = ModelEntity(mesh: .generateBox(size: [simd_length(d), width, 0.001]), materials: [material])
    entity.position = (a + b) / 2 + [0, 0, lift]
    entity.orientation = simd_quatf(angle: atan2(d.y, d.x), axis: [0, 0, 1])
    return entity
}

/// All tolerance zones as ONE mesh: orange zebra stripes, 50% see-through.
/// Stripes are laid out on a single site-wide diagonal grid and kept only where a point is within
/// `halfWidth` of any path. So overlapping zones share one continuous pattern: no doubled color,
/// no seams, nothing coplanar to flicker.
private func toleranceZones(_ paths: [(SIMD3<Float>, SIMD3<Float>)], halfWidth: Float) -> Entity? {
    guard !paths.isEmpty, halfWidth > 0 else { return nil }
    let segs = paths.map { (SIMD2($0.0.x, $0.0.y), SIMD2($0.1.x, $0.1.y)) }
    func inZone(_ p: SIMD2<Float>) -> Bool {
        segs.contains { a, b in
            let ab = b - a
            let t = simd_length_squared(ab) > 0 ? min(max(simd_dot(p - a, ab) / simd_length_squared(ab), 0), 1) : 0
            return simd_distance(p, a + t * ab) <= halfWidth
        }
    }
    let period = min(max(halfWidth * 0.6, 0.012), 0.12)  // stripe + gap; shrinks for scale models
    let lanes = 3                                        // each stripe is 3 thin lanes: smoother zone edges
    let laneWidth = period / 2 / Float(lanes)
    let step = period / 12
    let along = SIMD2<Float>(1, 1) / Float(2).squareRoot()   // stripe direction (45 degrees)
    let across = SIMD2<Float>(-1, 1) / Float(2).squareRoot()

    var uMin = Float.infinity, uMax = -Float.infinity, vMin = Float.infinity, vMax = -Float.infinity
    for p in segs.flatMap({ [$0.0, $0.1] }) {
        uMin = min(uMin, simd_dot(p, along) - halfWidth); uMax = max(uMax, simd_dot(p, along) + halfWidth)
        vMin = min(vMin, simd_dot(p, across) - halfWidth); vMax = max(vMax, simd_dot(p, across) + halfWidth)
    }

    var positions: [SIMD3<Float>] = []
    var indices: [UInt32] = []
    var band = (vMin / period).rounded(.down) * period
    while band < vMax {
        for lane in 0..<lanes {
            let v0 = band + Float(lane) * laneWidth, v1 = v0 + laneWidth
            var runStart: Float?
            var s = uMin
            while s <= uMax + step {
                let inside = s <= uMax && inZone(along * s + across * ((v0 + v1) / 2))
                if inside, runStart == nil { runStart = s - step / 2 }
                if !inside, let start = runStart {
                    let end = s - step / 2
                    let i = UInt32(positions.count)
                    for (u, v) in [(start, v0), (end, v0), (end, v1), (start, v1)] {  // counter-clockwise from above
                        let p = along * u + across * v
                        positions.append([p.x, p.y, 0.002])
                    }
                    indices += [i, i + 1, i + 2, i, i + 2, i + 3]
                    runStart = nil
                }
                s += step
            }
        }
        band += period
    }
    guard !indices.isEmpty else { return nil }
    var descriptor = MeshDescriptor(name: "toleranceZones")
    descriptor.positions = MeshBuffers.Positions(positions)
    descriptor.primitives = .triangles(indices)
    guard let mesh = try? MeshResource.generate(from: [descriptor]) else { return nil }
    var orange = UnlitMaterial(color: .systemOrange)
    orange.blending = .transparent(opacity: .init(floatLiteral: zoneOpacity))
    orange.faceCulling = .none
    return ModelEntity(mesh: mesh, materials: [orange])
}

/// Pipe at a SIMULATED depth below a ground path, plus a translucent curtain tying it to the surface
/// line so it reads as "under here" instead of floating. Illustration only.
private func pipe(_ a: SIMD3<Float>, _ b: SIMD3<Float>, depth: Float, radius: Float, color: UIColor) -> Entity {
    let d = b - a
    let length = simd_length(d)
    let root = Entity()
    root.position = (a + b) / 2
    root.orientation = simd_quatf(angle: atan2(d.y, d.x), axis: [0, 0, 1])  // local +X runs along the path

    let tube = ModelEntity(mesh: .generateCylinder(height: length, radius: radius),
                           materials: [UnlitMaterial(color: color)])
    tube.orientation = simd_quatf(from: [0, 1, 0], to: [1, 0, 0])  // cylinder axis is +Y
    tube.position = [0, 0, -depth]

    var glass = UnlitMaterial(color: color)
    glass.blending = .transparent(opacity: 0.25)
    let curtain = ModelEntity(mesh: .generateBox(size: [length, 0.003, depth]), materials: [glass])
    curtain.position = [0, 0, -depth / 2]

    root.addChild(tube)
    root.addChild(curtain)
    return root
}

/// Floating text tag on a dark plate that always faces the phone. `size` = letter height in meters.
private func label(_ string: String, at position: SIMD3<Float>, size: CGFloat) -> Entity {
    let mesh = MeshResource.generateText(string, extrusionDepth: 0.001, font: .boldSystemFont(ofSize: size))
    let text = ModelEntity(mesh: mesh, materials: [UnlitMaterial(color: .white)])
    text.position = -mesh.bounds.center + [0, 0, 0.002]  // text origin is bottom-left; center it

    var dark = UnlitMaterial(color: .black)
    dark.blending = .transparent(opacity: 0.7)
    let pad = Float(size) * 0.75
    let plate = ModelEntity(mesh: .generatePlane(width: mesh.bounds.extents.x + pad,
                                                 height: mesh.bounds.extents.y + pad, cornerRadius: pad / 3),
                            materials: [dark])
    let root = Entity()
    root.addChild(plate)
    root.addChild(text)
    root.position = position
    root.components.set(BillboardComponent())
    return root
}
