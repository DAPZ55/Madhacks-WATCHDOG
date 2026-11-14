import simd

// Site frame S (meters): +X from A1 to A2, +Y on the ground, +Z up. Markers sit at z = 0:
// the marker plane IS ground level, and depth is measured straight down from it.
// ARKit world frame: +Y up (gravity), right-handed.
// Check: tools/test_transform.sh

/// Fit T_A_from_S so the site's z = 0 plane passes through the observed markers.
/// - 3+ markers (not in a line): ground plane = plane through the marker centers. Works on sloped floors.
/// - 1-2 markers: ground normal = `up` (the tags' own face normal), squared against the baseline.
/// Then yaw within that plane + translation by least squares.
func fitSiteTransform(_ pairs: [(site: SIMD3<Float>, ar: SIMD3<Float>)],
                      up hint: SIMD3<Float> = [0, 1, 0]) -> simd_float4x4? {
    guard pairs.count >= 2 else { return nil }
    let n = Float(pairs.count)
    let qc = pairs.map { $0.site }.reduce(.zero, +) / n
    let pc = pairs.map { $0.ar }.reduce(.zero, +) / n
    let q = pairs.map { $0.site - qc }
    let p = pairs.map { $0.ar - pc }

    // Ground normal from every marker triangle, each flipped to match the site's winding so
    // "up" needs no guess. Bigger triangles weigh more (cross product length = 2 x area).
    var normal = SIMD3<Float>.zero
    for i in 0..<p.count {
        for j in (i + 1)..<p.count {
            for k in (j + 1)..<p.count {
                let c = simd_cross(p[j] - p[i], p[k] - p[i])
                normal += simd_cross(q[j] - q[i], q[k] - q[i]).z < 0 ? -c : c
            }
        }
    }
    if simd_length(normal) < 1e-5 {  // two markers, or all in a line: use the tags' face normal
        let baseline = p.max { simd_length($0) < simd_length($1) } ?? .zero
        guard simd_length(baseline) > 1e-4 else { return nil }
        let b = simd_normalize(baseline)
        normal = hint - simd_dot(hint, b) * b
        guard simd_length(normal) > 1e-4 else { return nil }
    }
    let e3 = simd_normalize(normal)
    let e1 = simd_normalize(simd_cross(e3, abs(e3.x) < 0.9 ? [1, 0, 0] : [0, 1, 0]))
    let e2 = simd_cross(e3, e1)

    // Yaw inside the ground plane: site (x, y) onto AR (e1, e2).
    var sinSum: Float = 0, cosSum: Float = 0
    for (a, b) in zip(q, p) {
        let bx = simd_dot(b, e1), by = simd_dot(b, e2)
        sinSum += a.x * by - a.y * bx
        cosSum += a.x * bx + a.y * by
    }
    guard abs(sinSum) + abs(cosSum) > 1e-6 else { return nil }  // all points stacked: yaw unknown
    let yaw = atan2(sinSum, cosSum)
    let rot = simd_float3x3(columns: (cos(yaw) * e1 + sin(yaw) * e2, -sin(yaw) * e1 + cos(yaw) * e2, e3))
    let t = pc - rot * qc
    return simd_float4x4(columns: (SIMD4(rot.columns.0, 0), SIMD4(rot.columns.1, 0),
                                   SIMD4(rot.columns.2, 0), SIMD4(t, 1)))
}
