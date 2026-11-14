import simd

// Known site->AR transforms; fit from marker centers must reproduce them, including points
// below ground (depth must be measured from the marker plane, even on a sloped floor).
func truth(tiltDegrees: Float) -> simd_float4x4 {
    var m = simd_float4x4(simd_quatf(angle: tiltDegrees * .pi / 180, axis: [1, 0, 0]))
        * simd_float4x4(simd_quatf(angle: 0.7, axis: [0, 1, 0]))
        * simd_float4x4(rows: [[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]])
    m.columns.3 = [1, -0.2, 3, 1]
    return m
}
func apply(_ m: simd_float4x4, _ s: SIMD3<Float>) -> SIMD3<Float> {
    let r = m * SIMD4<Float>(s, 1)
    return [r.x, r.y, r.z]
}
let anchors: [SIMD3<Float>] = [[0, 0, 0], [0.8, 0, 0], [0.85, -0.6, 0], [0.02, -0.58, 0]]
let probes: [SIMD3<Float>] = [[0.3, 1.7, 0], [0.4, -0.3, -0.76], [-1, 2, -1.83]]  // ground + underground

for tilt in [Float(0), 6] {  // level floor, then a 6 degree slope
    let t = truth(tiltDegrees: tilt)
    for count in [3, 4] {
        let fit = fitSiteTransform(anchors.prefix(count).map { (site: $0, ar: apply(t, $0)) })!
        for probe in probes {
            precondition(simd_distance(apply(fit, probe), apply(t, probe)) < 1e-3,
                         "tilt \(tilt), \(count) markers: point \(probe) misplaced")
        }
    }
    // Two markers: plane comes from the tags' face normal (passed as `up`).
    let up = simd_normalize(apply(t, [0, 0, 1]) - apply(t, [0, 0, 0]))
    let two = fitSiteTransform(anchors.prefix(2).map { (site: $0, ar: apply(t, $0)) }, up: up)!
    precondition(simd_distance(apply(two, probes[1]), apply(t, probes[1])) < 1e-3, "two-marker fit wrong")
}
// Markers are ground: every marker must land at site z = 0 after the fit.
let sloped = truth(tiltDegrees: 6)
let fit = fitSiteTransform(anchors.map { (site: $0, ar: apply(sloped, $0)) })!
for a in anchors {
    let back = simd_inverse(fit) * SIMD4<Float>(apply(sloped, a), 1)
    precondition(abs(back.z) < 1e-3, "marker not at ground level")
}
precondition(fitSiteTransform([(site: anchors[0], ar: .zero)]) == nil, "one point must not fit")
print("ok: ground plane follows markers (level and sloped), depth measured from marker plane")
