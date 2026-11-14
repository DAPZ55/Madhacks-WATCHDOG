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

/// APWA uniform color code.
let markingColors: [String: UIColor] = [
    "red": .systemRed, "yellow": .systemYellow, "orange": .systemOrange, "blue": .systemBlue,
    "green": .systemGreen, "purple": .systemPurple, "pink": .systemPink, "white": .white,
]

/// Table: marking color -> utility type and minimum cover, for the selected state.
struct LegendView: View {
    let jurisdiction: Jurisdiction
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            List {
                Section("Rules") {
                    LabeledContent("One-call center", value: jurisdiction.oneCall)
                    LabeledContent("Law", value: jurisdiction.law)
                    LabeledContent("Tolerance zone", value: String(format: "%.0f in each side", jurisdiction.toleranceIn))
                    Text(jurisdiction.toleranceNote + (jurisdiction.toleranceVerified ? "" : " (unverified)"))
                        .font(.footnote).foregroundStyle(.secondary)
                }
                Section("Marking color, utility type, minimum cover") {
                    ForEach(jurisdiction.entries) { entry in
                        HStack(alignment: .top, spacing: 12) {
                            Circle()
                                .fill(Color(uiColor: markingColors[entry.color] ?? .gray))
                                .overlay(Circle().stroke(.secondary))
                                .frame(width: 22, height: 22)
                                .accessibilityLabel(entry.color)
                            VStack(alignment: .leading, spacing: 2) {
                                Text(entry.label).font(.headline)
                                Text("Min. cover: " + entry.coverText)
                                Text(entry.basis + (entry.verified ? "" : " (unverified)"))
                                    .font(.footnote).foregroundStyle(.secondary)
                            }
                        }
                    }
                }
                Section {
                    Text("Minimum cover is what the rule required when the line was installed. Actual depth differs: regrading, erosion, old installations. It is never a measured depth and never permission to dig.")
                        .font(.footnote)
                }
            }
            .navigationTitle(jurisdiction.name)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar { Button("Done") { dismiss() } }
        }
    }
}
