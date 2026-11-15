import Foundation
import simd

// Canonical map object (spec 8.1). snake_case JSON -> camelCase via decoder strategy.
struct SiteMap: Decodable {
    struct Anchor: Decodable {
        let id: String
        let positionM: [Float]
        let sizeM: Float  // side of the black square, meters
        var position: SIMD3<Float> { SIMD3(positionM[0], positionM[1], positionM[2]) }
    }
    struct Path: Decodable {
        let centerlineM: [[Float]]
        var points: [SIMD3<Float>] { centerlineM.filter { $0.count == 3 }.map { SIMD3($0[0], $0[1], $0[2]) } }
    }
    struct Utility: Decodable {
        let utilityId: String
        let utilityClass: String
        let markingColor: String
        let surfaceMarking: Path?
        let uploadedLayout: Path?
        let depthM: Float?  // nil = unknown. Never invent a value.
        let depthStatus: String
        /// Presentation-only depth. Drawn only when status is "hypothetical", always labeled simulated.
        let displayDepthM: Float?
        let displayDepthStatus: String?
        var simulatedDepth: Float? { displayDepthStatus == "hypothetical" ? displayDepthM : nil }
        let evidenceRelationship: String
    }

    let siteId: String
    let mapRevision: Int
    let anchors: [Anchor]
    let utilities: [Utility]
    /// < 1 means the site is a scale model (0.1 = 1:10). Display-only quantities are scaled by it.
    let modelScale: Float?
    var scale: Float { min(max(modelScale ?? 1, 0.001), 1) }

    var hasSimulatedDepth: Bool { utilities.contains { $0.simulatedDepth != nil } }
    var discrepancies: [Utility] { utilities.filter { $0.evidenceRelationship == "discrepancy_requires_review" } }

    static func decode(_ data: Data) throws -> SiteMap {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        let map = try decoder.decode(SiteMap.self, from: data)
        // Trust boundary: reject malformed anchors instead of crashing on index.
        guard map.anchors.allSatisfy({ $0.positionM.count == 3 && $0.sizeM > 0 }) else {
            throw DecodingError.dataCorrupted(.init(codingPath: [], debugDescription: "bad anchor"))
        }
        return map
    }
}

final class AppModel: ObservableObject {
    @Published var map: SiteMap?
    @Published var mapNote = "Loading map…"
    /// Non-nil when the map is missing or may be stale; shown as a warning in the HUD.
    @Published var mapProblem: String?
    @Published var alignNote = "Point camera at an anchor tag."
    /// Bumped by the Recalibrate button; the AR view restarts alignment when it changes.
    @Published var recalibrations = 0

    private let cacheURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        .appendingPathComponent("map.json")

    /// Fetch the published map; fall back to the cached copy and say so.
    func refresh(server: String) {
        Task { @MainActor in
            var fresh = false
            if let url = URL(string: "http://\(server)/api/v1/maps/latest") {
                var request = URLRequest(url: url)
                request.timeoutInterval = 3
                if let (data, response) = try? await URLSession.shared.data(for: request),
                   (response as? HTTPURLResponse)?.statusCode == 200,
                   (try? SiteMap.decode(data)) != nil {
                    try? data.write(to: cacheURL, options: .atomic)
                    fresh = true
                }
            }
            guard let data = try? Data(contentsOf: cacheURL), let loaded = try? SiteMap.decode(data) else {
                map = nil
                mapNote = "No map available. Join the site Wi-Fi and tap Refresh."
                mapProblem = mapNote
                return
            }
            map = loaded
            if fresh {
                mapNote = "Map revision \(loaded.mapRevision) (\(loaded.siteId))"
                mapProblem = nil
            } else {
                let saved = (try? cacheURL.resourceValues(forKeys: [.contentModificationDateKey]))?
                    .contentModificationDate
                let age = saved.map { $0.formatted(date: .abbreviated, time: .shortened) } ?? "unknown time"
                mapNote = "SERVER UNREACHABLE. Cached revision \(loaded.mapRevision) from \(age). May be out of date."
                mapProblem = mapNote
            }
        }
    }
}
