import SwiftUI

/// Per-state marking labels, tolerance zone, and minimum-cover rules. Data: jurisdictions.json.
/// Everything here is display-only. Minimum cover at installation is NOT a measured depth.
struct Jurisdiction: Decodable, Identifiable {
    struct Entry: Decodable, Identifiable {
        let color: String
        let label: String
        let coverIn: Float?
        let basis: String
        let verified: Bool
        var id: String { color }
        var coverM: Float? { coverIn.map { $0 * 0.0254 } }
        var coverText: String { coverIn.map { String(format: "%.0f in (%.2f m)", $0, $0 * 0.0254) } ?? "no figure" }
    }

    let id: String
    let name: String
    let oneCall: String
    let law: String
    let toleranceIn: Float
    let toleranceNote: String
    let toleranceVerified: Bool
    let entries: [Entry]

    var toleranceM: Float { toleranceIn * 0.0254 }
    func entry(color: String) -> Entry? { entries.first { $0.color == color } }

    static let all: [Jurisdiction] = {
        struct File: Decodable { let jurisdictions: [Jurisdiction] }
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        // Bundled file we ship; a decode failure is a build mistake, so crash loudly.
        let url = Bundle.main.url(forResource: "jurisdictions", withExtension: "json")!
        return try! decoder.decode(File.self, from: Data(contentsOf: url)).jurisdictions
    }()

    static func named(_ id: String) -> Jurisdiction { all.first { $0.id == id } ?? all[0] }
}

/// Table: marking color -> utility type and minimum cover, for the selected state.
struct LegendView: View {
    let jurisdiction: Jurisdiction
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: Theme.s4) {
                ScreenHeader(index: "Legend", title: jurisdiction.name)
                Panel(title: "Rules") {
                    Readout(key: "One-call", value: jurisdiction.oneCall)
                    Readout(key: "Law", value: jurisdiction.law)
                    Readout(key: "Tolerance zone", value: String(format: "%.0f in each side", jurisdiction.toleranceIn))
                    Text(jurisdiction.toleranceNote + (jurisdiction.toleranceVerified ? "" : " (unverified)"))
                        .font(Theme.body(13)).foregroundStyle(Theme.fg2).fixedSize(horizontal: false, vertical: true)
                }
                Panel(title: "Marking color · Utility · Minimum cover") {
                    ForEach(Array(jurisdiction.entries.enumerated()), id: \.element.id) { index, entry in
                        if index > 0 { Rectangle().fill(Theme.line).frame(height: Theme.hairline) }
                        HStack(alignment: .top, spacing: Theme.s3) {
                            Rectangle()
                                .fill(Color(uiColor: markingColors[entry.color] ?? .gray))
                                .overlay(Rectangle().strokeBorder(Theme.line, lineWidth: Theme.hairline))
                                .frame(width: 22, height: 22)
                                .accessibilityLabel(entry.color)
                            VStack(alignment: .leading, spacing: 2) {
                                Text(entry.label).font(Theme.body(16, medium: true)).foregroundStyle(Theme.fg)
                                Text("Min. cover: " + entry.coverText).font(Theme.body(14)).foregroundStyle(Theme.fg)
                                HStack(alignment: .firstTextBaseline, spacing: Theme.s2) {
                                    Text(entry.basis).font(Theme.body(12)).foregroundStyle(Theme.fg2)
                                        .fixedSize(horizontal: false, vertical: true)
                                    if !entry.verified { Tag(text: "Unverified", tone: .warning) }
                                }
                            }
                        }
                    }
                }
                NoticeBar(text: "Minimum cover is what the rule required at installation. Actual depth differs: regrading, erosion, old work. It is never a measured depth and never permission to dig.")
                Button("Done") { dismiss() }.buttonStyle(.industrial)
            }
            .padding(Theme.s4)
        }
        .background(Theme.bg.ignoresSafeArea())
        .preferredColorScheme(.dark)
    }
}
