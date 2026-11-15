import SwiftUI
import UIKit

// 811 Vision design system. Shared by the AR app and the admin app.
//
// Lineage: the structure of hanbao.build (near-black field, square corners, hairline rules,
// condensed uppercase labels, one loud accent; Antonio / Barlow Condensed / Space Grotesk),
// re-keyed to a job site: asphalt blacks, concrete off-white, hi-vis safety orange, hazard yellow.
//
// Rules of the system:
//  - Corners are square. Depth comes from hairlines and surface steps, not shadows or blur.
//  - Safety orange = the one action color. Hazard yellow + black stripes = warnings only.
//  - Utility marking colors (APWA red/yellow/orange/blue/green) are DATA, never chrome.
//  - Every tap target is at least 48 pt tall (gloves). Text scales with Dynamic Type.

enum Theme {
    // Color tokens
    static let bg = Color(hex: 0x0A0A09)          // asphalt
    static let surface = Color(hex: 0x141412)     // raised panel
    static let surface2 = Color(hex: 0x1F1F1B)    // control fill
    static let fg = Color(hex: 0xF2F0EA)          // concrete white, 17:1 on bg
    static let fg2 = Color(hex: 0xF2F0EA).opacity(0.68)
    static let fg3 = Color(hex: 0xF2F0EA).opacity(0.45)
    static let line = Color(hex: 0xF2F0EA).opacity(0.16)
    static let action = Color(hex: 0xFF6A00)      // hi-vis safety orange, 7.6:1 on bg
    static let onAction = Color(hex: 0x0A0A09)
    static let hazard = Color(hex: 0xFFD400)      // hazard yellow, warnings only
    static let steel = Color(hex: 0x9AA3AD)
    static let ok = Color(hex: 0x3DD68C)
    static let danger = Color(hex: 0xFF5A4F)      // readable as text on bg (6.4:1)
    static let dangerFill = Color(hex: 0xC8261D)

    // Spacing (4-pt grid) and sizes
    static let s1: CGFloat = 4, s2: CGFloat = 8, s3: CGFloat = 12, s4: CGFloat = 16, s5: CGFloat = 24, s6: CGFloat = 32
    static let tapHeight: CGFloat = 48
    static let hairline: CGFloat = 1

    // Type. Sizes are base sizes; all scale with the user's text-size setting.
    static func display(_ size: CGFloat) -> Font { variable("Antonio", size: size, weight: 700, style: .title1) }
    static func label(_ size: CGFloat = 13) -> Font { fixed("BarlowCondensed-SemiBold", size: size, style: .caption1) }
    static func body(_ size: CGFloat = 16, medium: Bool = false) -> Font {
        variable("Space Grotesk", size: size, weight: medium ? 500 : 400, style: .body)
    }
    static func mono(_ size: CGFloat = 13) -> Font { .system(size: size, design: .monospaced) }

    private static func fixed(_ name: String, size: CGFloat, style: UIFont.TextStyle) -> Font {
        let base = UIFont(name: name, size: size) ?? .systemFont(ofSize: size, weight: .semibold)
        return Font(UIFontMetrics(forTextStyle: style).scaledFont(for: base))
    }

    /// Variable font at a given weight (the bundled Antonio and Space Grotesk are variable fonts).
    private static func variable(_ family: String, size: CGFloat, weight: CGFloat, style: UIFont.TextStyle) -> Font {
        let wght = 0x77676874  // 'wght' axis tag
        let descriptor = UIFontDescriptor(fontAttributes: [
            .family: family,
            UIFontDescriptor.AttributeName(rawValue: kCTFontVariationAttribute as String): [wght: weight],
        ])
        let base = UIFont(descriptor: descriptor, size: size)
        // Unknown family falls back to the system font; keep the UI legible either way.
        let usable = base.familyName == family ? base : UIFont.systemFont(ofSize: size, weight: weight >= 600 ? .bold : .regular)
        return Font(UIFontMetrics(forTextStyle: style).scaledFont(for: usable))
    }
}

extension Color {
    init(hex: UInt32) {
        self.init(.sRGB, red: Double((hex >> 16) & 0xFF) / 255, green: Double((hex >> 8) & 0xFF) / 255,
                  blue: Double(hex & 0xFF) / 255, opacity: 1)
    }
}

/// APWA uniform color code. Data colors: only ever used to show a utility marking.
let markingColors: [String: UIColor] = [
    "red": .systemRed, "yellow": .systemYellow, "orange": .systemOrange, "blue": .systemBlue,
    "green": .systemGreen, "purple": .systemPurple, "pink": .systemPink, "white": .white,
]

enum Tone {
    case neutral, action, ok, warning, danger
    var color: Color {
        switch self {
        case .neutral: Theme.fg2
        case .action: Theme.action
        case .ok: Theme.ok
        case .warning: Theme.hazard
        case .danger: Theme.danger
        }
    }
}

// MARK: Text styles

extension View {
    /// Condensed uppercase label with wide tracking: section names, button text, tags.
    func labelStyle(_ size: CGFloat = 13, _ color: Color = Theme.fg2) -> some View {
        font(Theme.label(size)).tracking(size * 0.1).textCase(.uppercase).foregroundStyle(color)
    }
}

// MARK: Components

/// Diagonal black/yellow hazard tape. Decorative edge for warnings; hidden from VoiceOver.
struct HazardStripe: View {
    var height: CGFloat = 6
    var body: some View {
        Canvas { context, size in
            context.fill(Path(CGRect(origin: .zero, size: size)), with: .color(Theme.hazard))
            let step = max(size.height, 6) * 2
            var x = -size.height
            while x < size.width {
                var path = Path()
                path.move(to: CGPoint(x: x, y: size.height))
                path.addLine(to: CGPoint(x: x + size.height, y: 0))
                path.addLine(to: CGPoint(x: x + size.height + step / 2, y: 0))
                path.addLine(to: CGPoint(x: x + step / 2, y: size.height))
                path.closeSubpath()
                context.fill(path, with: .color(.black))
                x += step
            }
        }
        .frame(height: height)
        .accessibilityHidden(true)
    }
}

/// Raised panel: surface fill, hairline border, optional label tab on the top edge.
struct Panel<Content: View>: View {
    var title: String?
    var translucent = false
    @ViewBuilder var content: Content

    var body: some View {
        VStack(alignment: .leading, spacing: Theme.s3) {
            if let title {
                Text(title).labelStyle(13, Theme.action).accessibilityAddTraits(.isHeader)
            }
            content
        }
        .padding(Theme.s4)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Theme.surface.opacity(translucent ? 0.86 : 1))
        .overlay(Rectangle().strokeBorder(Theme.line, lineWidth: Theme.hairline))
    }
}

/// Small bordered status tag: "REV 33", "1:10", "LIVE".
struct Tag: View {
    let text: String
    var tone: Tone = .neutral
    var body: some View {
        Text(text)
            .labelStyle(12, tone.color)
            .padding(.horizontal, Theme.s2).padding(.vertical, 3)
            .overlay(Rectangle().strokeBorder(tone.color.opacity(0.7), lineWidth: Theme.hairline))
            .fixedSize()
    }
}

/// Warning or status line. Warnings get hazard tape on the leading edge AND a text prefix,
/// so meaning never depends on color alone.
struct NoticeBar: View {
    let text: String
    var tone: Tone = .warning
    var body: some View {
        HStack(alignment: .top, spacing: Theme.s2) {
            Rectangle().fill(tone.color).frame(width: 4)
            Text(text).font(Theme.body(13, medium: true)).foregroundStyle(Theme.fg)
                .frame(maxWidth: .infinity, alignment: .leading)
                .fixedSize(horizontal: false, vertical: true)
        }
        .padding(.vertical, Theme.s2).padding(.trailing, Theme.s3)
        .background(Theme.bg.opacity(0.88))
        .overlay(Rectangle().strokeBorder(Theme.line, lineWidth: Theme.hairline))
    }
}

struct IndustrialButtonStyle: ButtonStyle {
    enum Kind { case primary, secondary, danger }
    var kind: Kind = .secondary
    var compact = false
    @Environment(\.isEnabled) private var enabled

    func makeBody(configuration: Configuration) -> some View {
        let fill: Color = switch kind { case .primary: Theme.action; case .secondary: Theme.surface2; case .danger: Theme.dangerFill }
        let ink: Color = kind == .primary ? Theme.onAction : Theme.fg
        return configuration.label
            .font(Theme.label(compact ? 14 : 16)).tracking(1.4).textCase(.uppercase)
            .foregroundStyle(ink)
            .lineLimit(1).minimumScaleFactor(0.75)
            .padding(.horizontal, compact ? Theme.s3 : Theme.s4)
            .frame(maxWidth: compact ? nil : .infinity, minHeight: Theme.tapHeight)
            .background(fill)
            .overlay(Rectangle().strokeBorder(kind == .secondary ? Theme.line : .clear, lineWidth: Theme.hairline))
            .opacity(enabled ? (configuration.isPressed ? 0.7 : 1) : 0.4)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
            .contentShape(Rectangle())
    }
}

extension ButtonStyle where Self == IndustrialButtonStyle {
    static var industrial: IndustrialButtonStyle { .init() }
    static var industrialPrimary: IndustrialButtonStyle { .init(kind: .primary) }
    static var industrialDanger: IndustrialButtonStyle { .init(kind: .danger) }
    static var industrialCompact: IndustrialButtonStyle { .init(compact: true) }
}

/// Key/value row for spec-sheet style readouts.
struct Readout: View {
    let key: String
    let value: String
    var tone: Tone = .neutral
    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: Theme.s3) {
            Text(key).labelStyle(13, Theme.fg3)
            Spacer(minLength: Theme.s2)
            Text(value).font(Theme.body(15, medium: true))
                .foregroundStyle(tone == .neutral ? Theme.fg : tone.color)
                .multilineTextAlignment(.trailing)
        }
        .accessibilityElement(children: .combine)
    }
}

/// Screen title in the display face, with a short index label above it.
struct ScreenHeader: View {
    let index: String
    let title: String
    var body: some View {
        VStack(alignment: .leading, spacing: 2) {
            Text(index).labelStyle(13, Theme.action)
            Text(title).font(Theme.display(34)).foregroundStyle(Theme.fg).textCase(.uppercase)
                .accessibilityAddTraits(.isHeader)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

/// Always-on safety footer: hazard tape + the advisory line.
struct AdvisoryFooter: View {
    var text = "Advisory demo · Not a utility locate · Never permission to dig"
    var body: some View {
        VStack(spacing: 0) {
            HazardStripe(height: 5)
            Text(text).labelStyle(11, Theme.fg2)
                .frame(maxWidth: .infinity).padding(.vertical, 6).padding(.horizontal, Theme.s3)
                .multilineTextAlignment(.center)
                .background(Theme.bg)
        }
    }
}
