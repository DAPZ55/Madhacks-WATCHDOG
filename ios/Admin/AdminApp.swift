import PhotosUI
import SwiftUI

// 811 Vision Admin: native control panel for the UNO Q edge board.
// Same design system as the AR app (ios/Shared/Theme.swift). Talks to the board's HTTP API.
// ponytail: no login, matching the board (owner's choice for the demo). Private site Wi-Fi only.

@main
struct Vision811AdminApp: App {
    var body: some Scene {
        WindowGroup { RootView() }
    }
}

// MARK: - API

struct BoardStatus: Decodable {
    let host: String
    let uptimeS: Int
    let publishedRevision: Int?
    let publishedAt: String?
    let utilities: Int?
    let modelScale: Double?
    let camera: Bool
    let candidateWaiting: Bool
    let mode: String?
    let monitorState: String?
    let monitorDetail: String?
    var isMonitor: Bool { mode == "monitor" }
}

struct Candidate: Decodable, Equatable {
    struct Marking: Decodable, Equatable, Identifiable {
        let id: String
        let color: String
        let utilityClass: String
        let points: Int
        enum CodingKeys: String, CodingKey { case id, color, utilityClass = "class", points }
    }
    let source: String
    let scannedAt: String
    let modelScale: Double
    let includesSurvey: Bool?
    let utilities: [Marking]
}

struct NetworkState: Decodable {
    let supported: Bool
    let siteWifiConfigured: Bool?
    let ownNetworkAtBoot: Bool?
    let mode: String?
    let connectedTo: String?
    let addresses: [String]?
}

struct SurveyResult: Decodable {
    let anchorsM: [String: [Double]]
    let publishedRevision: Int?
}

struct PublishResult: Decodable { let publishedRevision: Int }
struct TagsInView: Decodable { let needed: [String]; let visible: [String] }
struct ModeResult: Decodable { let mode: String }
struct Ack: Decodable {}

struct BoardError: LocalizedError {
    let message: String
    var errorDescription: String? { message }
}

@MainActor
final class Board: ObservableObject {
    @Published var status: BoardStatus?
    @Published var candidate: Candidate?
    @Published var network: NetworkState?
    @Published var reachable = true
    @Published var message = "Ready."
    @Published var messageTone: Tone = .neutral
    @Published var busy = false
    var host = "Madhacks16.local:8000"

    private let decoder: JSONDecoder = {
        let d = JSONDecoder()
        d.keyDecodingStrategy = .convertFromSnakeCase
        return d
    }()

    func url(_ path: String) -> URL? { URL(string: "http://\(host)\(path)") }

    func call<T: Decodable>(_ method: String, _ path: String, body: Data? = nil, timeout: TimeInterval = 30) async throws -> T {
        guard let url = url(path) else { throw BoardError(message: "bad board address") }
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.httpBody = body
        request.timeoutInterval = timeout
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse else { throw BoardError(message: "no response") }
        guard (200..<300).contains(http.statusCode) else {
            // The board explains every refusal in "detail"; show that, not a status code.
            let detail = (try? JSONSerialization.jsonObject(with: data) as? [String: Any])?["detail"] as? String
            throw BoardError(message: detail ?? "HTTP \(http.statusCode)")
        }
        return try decoder.decode(T.self, from: data)
    }

    func refresh() async {
        do {
            let s: BoardStatus = try await call("GET", "/api/v1/status", timeout: 4)
            status = s
            reachable = true
            candidate = s.candidateWaiting ? try? await call("GET", "/api/v1/candidate", timeout: 4) : nil
            network = try? await call("GET", "/api/v1/network", timeout: 6)
        } catch {
            reachable = false
        }
    }

    /// Run one admin action: shows progress, then the result or the board's own error text.
    func run(_ label: String, _ work: @escaping () async throws -> String) {
        guard !busy else { return }
        busy = true
        message = label + "…"
        messageTone = .neutral
        Task {
            do {
                message = try await work()
                messageTone = .ok
            } catch {
                message = "\(label) failed: \(error.localizedDescription)"
                messageTone = .danger
            }
            busy = false
            await refresh()
        }
    }
}

// MARK: - Shell

struct RootView: View {
    @StateObject private var board = Board()
    @AppStorage("serverHost") private var host = "Madhacks16.local:8000"

    var body: some View {
        TabView {
            SiteTab().tabItem { Label("Site", systemImage: "gauge.with.dots.needle.33percent") }
            ScanTab().tabItem { Label("Scan", systemImage: "viewfinder") }
            LiveTab().tabItem { Label("Live", systemImage: "video") }
            SystemTab(host: $host).tabItem { Label("System", systemImage: "wrench.and.screwdriver") }
        }
        .tint(Theme.action)
        .toolbarBackground(Theme.surface, for: .tabBar)
        .toolbarBackground(.visible, for: .tabBar)
        .environmentObject(board)
        .preferredColorScheme(.dark)
        .onChange(of: host, initial: true) { _, new in board.host = new }
        .task {
            while !Task.isCancelled {
                await board.refresh()
                try? await Task.sleep(for: .seconds(3))
            }
        }
    }
}

/// Common page frame: header, sticky result line, scrolling content, advisory footer.
struct Screen<Content: View>: View {
    @EnvironmentObject private var board: Board
    let index: String
    let title: String
    @ViewBuilder var content: Content

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: Theme.s4) {
                ScreenHeader(index: index, title: title)
                content
            }
            .padding(Theme.s4)
        }
        .safeAreaInset(edge: .top, spacing: 0) {
            VStack(spacing: 0) {
                if !board.reachable {
                    NoticeBar(text: "Board unreachable at \(board.host). Check Wi-Fi, or the address under System.", tone: .danger)
                }
                HStack(spacing: Theme.s2) {
                    if board.busy { ProgressView().tint(Theme.action) }
                    Text(board.message).font(Theme.body(13, medium: true)).foregroundStyle(board.messageTone.color)
                        .frame(maxWidth: .infinity, alignment: .leading).lineLimit(3)
                }
                .padding(.horizontal, Theme.s4).padding(.vertical, Theme.s2)
                .background(Theme.surface)
                .overlay(alignment: .bottom) { Rectangle().fill(Theme.line).frame(height: Theme.hairline) }
                .accessibilityElement(children: .combine)
                .accessibilityAddTraits(.updatesFrequently)
            }
        }
        .safeAreaInset(edge: .bottom, spacing: 0) { AdvisoryFooter() }
        .background(Theme.bg.ignoresSafeArea())
    }
}

/// Square segmented choice. Selected option carries an orange edge and a check, not color alone.
struct Choice: View {
    let label: String
    let options: [(value: String, title: String)]
    @Binding var selection: String

    var body: some View {
        VStack(alignment: .leading, spacing: Theme.s1) {
            Text(label).labelStyle(13, Theme.fg3)
            HStack(spacing: Theme.s2) {
                ForEach(options, id: \.value) { option in
                    let on = option.value == selection
                    Button {
                        selection = option.value
                    } label: {
                        HStack(spacing: 6) {
                            if on { Image(systemName: "checkmark").font(.system(size: 12, weight: .bold)) }
                            Text(option.title)
                        }
                        .font(Theme.label(15)).tracking(1.2).textCase(.uppercase)
                        .foregroundStyle(on ? Theme.action : Theme.fg2)
                        .lineLimit(1).minimumScaleFactor(0.7)
                        .frame(maxWidth: .infinity, minHeight: Theme.tapHeight)
                        .background(Theme.surface2)
                        .overlay(Rectangle().strokeBorder(on ? Theme.action : Theme.line, lineWidth: on ? 2 : Theme.hairline))
                    }
                    .buttonStyle(.plain)
                    .accessibilityLabel("\(label): \(option.title)")
                    .accessibilityAddTraits(on ? .isSelected : [])
                }
            }
        }
    }
}

let scaleOptions = [(value: "0.1", title: "Model 1:10"), (value: "1", title: "Real 1:1")]
let stateOptions = [(value: "WI", title: "WI"), (value: "NY", title: "NY"), (value: "CHI", title: "CHI"), (value: "TX", title: "TX")]

func scaleText(_ scale: Double?) -> String { "1:\(Int((1 / max(scale ?? 1, 0.001)).rounded()))" }

// MARK: - Site

struct SiteTab: View {
    @EnvironmentObject private var board: Board
    @State private var anchors: [String: [Double]] = [:]
    @State private var confirmSurvey = false

    var body: some View {
        Screen(index: "01 · Site", title: "Status") {
            Panel(title: "Board") {
                if let s = board.status {
                    Readout(key: "Board", value: "\(s.host), up \(s.uptimeS / 60) min")
                    Readout(key: "Camera", value: s.camera ? "Connected" : "Not found", tone: s.camera ? .ok : .danger)
                    Readout(key: "Published", value: s.publishedAt ?? "Nothing yet")
                    Readout(key: "On phones now", value: "\(s.utilities ?? 0) utilities · scale \(scaleText(s.modelScale))")
                    Readout(key: "Waiting for review", value: s.candidateWaiting ? "1 scan" : "None", tone: s.candidateWaiting ? .warning : .neutral)
                } else {
                    Text("Waiting for the board…").font(Theme.body(15)).foregroundStyle(Theme.fg2)
                }
            }
            Panel(title: "Operating mode") {
                Choice(label: "Mode", options: [(value: "scan", title: "Scan once"), (value: "monitor", title: "Monitor")],
                       selection: Binding(get: { board.status?.mode ?? "scan" }, set: { new in
                           guard new != board.status?.mode else { return }
                           board.run("Switching to \(new) mode") {
                               let r: ModeResult = try await board.call("POST", "/api/v1/mode?mode=\(new)")
                               return r.mode == "monitor" ? "Monitor mode: board is watching the anchor tags. Keep the camera aimed."
                                                          : "Scan mode: aim once, scan, then the camera is not needed."
                           }
                       }))
                if board.status?.isMonitor == true {
                    let state = board.status?.monitorState ?? ""
                    Readout(key: "Watchdog", value: state == "ok" ? "Tags in place" : state.replacingOccurrences(of: "_", with: " ").capitalized,
                            tone: state == "ok" ? .ok : .danger)
                    Text("Fixed camera. Board checks the anchor tags every 2 seconds and warns every phone if a tag moves, the view is blocked, or the camera drops. " + (board.status?.monitorDetail ?? ""))
                        .font(Theme.body(14)).foregroundStyle(Theme.fg2).fixedSize(horizontal: false, vertical: true)
                } else {
                    Text("One-time scan. Aim the camera, scan from the Scan tab, approve. After that the camera can be moved or unplugged; phones check the tags themselves.")
                        .font(Theme.body(14)).foregroundStyle(Theme.fg2).fixedSize(horizontal: false, vertical: true)
                }
            }
            .disabled(board.busy)
            Panel(title: "Anchor tags") {
                Text("Run after moving any tag or the camera. Saving clears published utilities, because they were placed against the old tag positions.")
                    .font(Theme.body(14)).foregroundStyle(Theme.fg2).fixedSize(horizontal: false, vertical: true)
                Button("Measure tags") {
                    board.run("Measuring tags") {
                        let r: SurveyResult = try await board.call("GET", "/api/v1/survey")
                        anchors = r.anchorsM
                        return "\(r.anchorsM.count) tag(s) measured. Nothing saved."
                    }
                }
                .buttonStyle(.industrial)
                Button("Re-survey and save") { confirmSurvey = true }.buttonStyle(.industrialPrimary)
                ForEach(anchors.keys.sorted(), id: \.self) { name in
                    Readout(key: name, value: String(format: "x %.3f m   y %.3f m", anchors[name]?[0] ?? 0, anchors[name]?[1] ?? 0))
                }
            }
            .disabled(board.busy || board.status?.camera != true)
        }
        .confirmationDialog("Re-survey tags and clear published utilities? You will need to rescan.",
                            isPresented: $confirmSurvey, titleVisibility: .visible) {
            Button("Re-survey and clear", role: .destructive) {
                board.run("Re-surveying") {
                    let r: SurveyResult = try await board.call("POST", "/api/v1/survey")
                    anchors = r.anchorsM
                    return "Tag positions saved. Utilities cleared: scan again."
                }
            }
        }
    }
}

// MARK: - Scan

struct ScanTab: View {
    @EnvironmentObject private var board: Board
    @AppStorage("scanScale") private var scale = "0.1"
    @State private var picked: PhotosPickerItem?
    @State private var tags: TagsInView?

    private var scanMode: Bool { board.status?.isMonitor != true }
    private var allTagsVisible: Bool { tags.map { $0.visible.count == $0.needed.count } ?? false }

    var body: some View {
        Screen(index: "02 · Scan", title: "Scan and publish") {
            if scanMode {
                Panel(title: "One-time site scan") {
                    if let tags {
                        Readout(key: "Tags in view", value: "\(tags.visible.count) of \(tags.needed.count)" + (tags.visible.isEmpty ? "" : " · " + tags.visible.joined(separator: " ")),
                                tone: allTagsVisible ? .ok : .warning)
                    } else {
                        Readout(key: "Tags in view", value: board.status?.camera == true ? "Checking…" : "No camera", tone: .warning)
                    }
                    Text("Aim the camera until every anchor tag is in view. One press then measures the tags and scans the markings together. After approval the camera is no longer needed.")
                        .font(Theme.body(14)).foregroundStyle(Theme.fg2).fixedSize(horizontal: false, vertical: true)
                    Button("Scan site now") {
                        board.run("Surveying tags and scanning") {
                            let c: Candidate = try await board.call("POST", "/api/v1/scan_site?model_scale=\(scale)", timeout: 60)
                            return "\(c.utilities.count) marking(s) found. Review below, then approve."
                        }
                    }
                    .buttonStyle(.industrialPrimary)
                    .disabled(!allTagsVisible)
                }
                .disabled(board.busy)
                // Poll tag visibility only while this panel is on screen; stopping frees the camera.
                .task {
                    while !Task.isCancelled {
                        if board.status?.camera == true, !board.busy {
                            tags = try? await board.call("GET", "/api/v1/tags", timeout: 8)
                        }
                        try? await Task.sleep(for: .seconds(1.5))
                    }
                }
            }
            Panel(title: "1 · Get a picture") {
                Choice(label: "Scale", options: scaleOptions, selection: $scale)
                PhotosPicker(selection: $picked, matching: .images) {
                    Text("Choose picture to upload")
                        .font(Theme.label(16)).tracking(1.4).textCase(.uppercase).foregroundStyle(Theme.fg)
                        .frame(maxWidth: .infinity, minHeight: Theme.tapHeight)
                        .background(Theme.surface2)
                        .overlay(Rectangle().strokeBorder(Theme.line, lineWidth: Theme.hairline))
                }
                if !scanMode {
                    Button("Capture from overhead camera") {
                        board.run("Capturing from camera") {
                            let c: Candidate = try await board.call("POST", "/api/v1/capture?model_scale=\(scale)")
                            return "\(c.utilities.count) marking(s) found. Review below, then approve."
                        }
                    }
                    .buttonStyle(.industrial)
                    .disabled(board.status?.camera != true)
                }
                Text("Picture must show all 4 anchor tags. Processing happens on the board.")
                    .font(Theme.body(13)).foregroundStyle(Theme.fg2)
            }
            .disabled(board.busy)

            Panel(title: "2 · Review, then publish") {
                if let c = board.candidate {
                    Text("From \(c.source) at \(c.scannedAt), scale \(scaleText(c.modelScale))." + (c.includesSurvey == true ? " Includes new tag positions." : "") + " Not on phones until approved.")
                        .font(Theme.body(14)).foregroundStyle(Theme.fg2).fixedSize(horizontal: false, vertical: true)
                    ForEach(c.utilities) { marking in
                        HStack(spacing: Theme.s3) {
                            Rectangle().fill(Color(uiColor: markingColors[marking.color] ?? .gray))
                                .overlay(Rectangle().strokeBorder(Theme.line, lineWidth: Theme.hairline))
                                .frame(width: 18, height: 18)
                                .accessibilityHidden(true)
                            Text(marking.id).font(Theme.mono(14)).foregroundStyle(Theme.fg2)
                            Text("\(marking.color) · \(marking.utilityClass)").font(Theme.body(15, medium: true)).foregroundStyle(Theme.fg)
                            Spacer()
                            Text("\(max(0, marking.points - 2)) bends").labelStyle(12, Theme.fg3)
                        }
                        .accessibilityElement(children: .combine)
                    }
                    if c.utilities.isEmpty {
                        NoticeBar(text: "No markings detected in this picture.")
                    }
                    Button("Approve and publish to phones") {
                        board.run("Publishing") {
                            let _: PublishResult = try await board.call("POST", "/api/v1/publish")
                            return "Published. Phones update within 3 seconds."
                                + (c.includesSurvey == true ? " Camera no longer needed." : "")
                        }
                    }
                    .buttonStyle(.industrialPrimary)
                    Button("Reject") {
                        board.run("Rejecting") {
                            let _: Ack = try await board.call("POST", "/api/v1/reject")
                            return "Scan discarded. Nothing changed on phones."
                        }
                    }
                    .buttonStyle(.industrial)
                } else {
                    Text("No scan waiting for review.").font(Theme.body(15)).foregroundStyle(Theme.fg2)
                }
            }
            .disabled(board.busy)
        }
        .onChange(of: picked) { _, item in
            guard let item else { return }
            picked = nil
            board.run("Processing upload on board") {
                guard let raw = try await item.loadTransferable(type: Data.self),
                      // Photos are often HEIC, which the board cannot read: re-encode as JPEG.
                      let jpeg = UIImage(data: raw)?.jpegData(compressionQuality: 0.9) else {
                    throw BoardError(message: "could not read that picture")
                }
                let c: Candidate = try await board.call("POST", "/api/v1/scan?model_scale=\(scale)", body: jpeg, timeout: 60)
                return "\(c.utilities.count) marking(s) found. Review below, then approve."
            }
        }
    }
}

// MARK: - Live

struct LiveTab: View {
    @EnvironmentObject private var board: Board
    @AppStorage("liveScale") private var scale = ""
    @AppStorage("liveState") private var state = "WI"
    @State private var running = false
    @State private var frame: UIImage?
    @State private var problem: String?

    var body: some View {
        Screen(index: "03 · Live", title: "Overhead camera") {
            Panel(title: "View") {
                Choice(label: "Depth scale", options: [(value: "", title: "As map")] + scaleOptions, selection: $scale)
                Choice(label: "State rules", options: stateOptions, selection: $state)
                Button(running ? "Stop live view" : "Start live view") { running.toggle() }
                    .buttonStyle(running ? .industrial : .industrialPrimary)
                    .disabled(board.status?.camera != true)
            }
            if let frame {
                Image(uiImage: frame).resizable().scaledToFit()
                    .overlay(Rectangle().strokeBorder(Theme.line, lineWidth: Theme.hairline))
                    .accessibilityLabel("Live overhead camera with detected anchors and simulated-depth pipes")
            }
            if let problem { NoticeBar(text: problem, tone: .danger) }
            if board.status?.camera != true { NoticeBar(text: "No camera found. Plug the webcam into the hub.", tone: .danger) }
        }
        // Restarts whenever the view options change; stops when the tab disappears, freeing the camera.
        .task(id: "\(running)|\(scale)|\(state)") {
            guard running else { frame = nil; return }
            while !Task.isCancelled {
                let path = "/api/v1/snapshot?state=\(state)" + (scale.isEmpty ? "" : "&scale=\(scale)")
                do {
                    guard let url = board.url(path) else { break }
                    var request = URLRequest(url: url)
                    request.timeoutInterval = 8
                    let (data, response) = try await URLSession.shared.data(for: request)
                    if (response as? HTTPURLResponse)?.statusCode == 200, let image = UIImage(data: data) {
                        frame = image
                        problem = nil
                    } else {
                        problem = "Camera did not return a frame."
                    }
                } catch is CancellationError {
                    break
                } catch {
                    problem = "Live view lost: \(error.localizedDescription)"
                }
                try? await Task.sleep(for: .milliseconds(250))
            }
        }
        .onDisappear { running = false }
    }
}

// MARK: - System

struct SystemTab: View {
    @EnvironmentObject private var board: Board
    @Binding var host: String
    @State private var pending: Pending?

    enum Pending: String, Identifiable {
        case own, join, reboot, poweroff
        var id: String { rawValue }
        var question: String {
            switch self {
            case .own: "Switch the board to its own Wi-Fi (811-Vision)? This app will disconnect until you join that network."
            case .join: "Rejoin the hotspot? Turn the hotspot on first. If it is not found, the board returns to its own network."
            case .reboot: "Reboot the board now?"
            case .poweroff: "Shut down the board now? It needs a power cycle to start again."
            }
        }
        var confirm: String {
            switch self {
            case .own: "Switch to own network"
            case .join: "Rejoin hotspot"
            case .reboot: "Reboot"
            case .poweroff: "Shut down"
            }
        }
    }

    var body: some View {
        Screen(index: "04 · System", title: "Board") {
            Panel(title: "Connection") {
                Text("Board address. Works on both networks: Madhacks16.local:8000. On the board's own Wi-Fi also 10.42.0.1:8000.")
                    .font(Theme.body(14)).foregroundStyle(Theme.fg2).fixedSize(horizontal: false, vertical: true)
                TextField("host:port", text: $host)
                    .font(Theme.mono(15)).foregroundStyle(Theme.fg)
                    .keyboardType(.URL).autocorrectionDisabled().textInputAutocapitalization(.never)
                    .padding(.horizontal, Theme.s3).frame(minHeight: Theme.tapHeight)
                    .background(Theme.surface2)
                    .overlay(Rectangle().strokeBorder(Theme.line, lineWidth: Theme.hairline))
                    .accessibilityLabel("Board address")
            }
            Panel(title: "Network") {
                if let n = board.network, n.supported {
                    let ready = n.siteWifiConfigured == true
                    Readout(key: "Mode", value: n.mode == "own_network" ? "Own network 811-Vision" : n.mode == "joined" ? "Joined \(n.connectedTo ?? "")" : "No Wi-Fi",
                            tone: n.mode == "offline" ? .danger : .neutral)
                    Readout(key: "Address", value: (n.addresses ?? []).joined(separator: ", "))
                    if !ready { NoticeBar(text: "Own network not set up. Run edge/setup_wifi.sh on the board once.") }
                    Button("Switch to own network") { pending = .own }.buttonStyle(.industrial)
                        .disabled(!ready || n.mode == "own_network")
                    Button("Rejoin hotspot") { pending = .join }.buttonStyle(.industrial)
                        .disabled(!ready || n.mode != "own_network")
                    Toggle(isOn: Binding(get: { n.ownNetworkAtBoot == true }, set: { on in
                        board.run("Saving boot setting") {
                            let _: Ack = try await board.call("POST", "/api/v1/network/boot?own=\(on)")
                            return on ? "At power-on: hotspot if found, else own network." : "At power-on: hotspot only."
                        }
                    })) {
                        Text("At power-on, start own network if no hotspot is found").font(Theme.body(15)).foregroundStyle(Theme.fg)
                    }
                    .tint(Theme.action).frame(minHeight: Theme.tapHeight).disabled(!ready)
                } else {
                    Text("Network control is only available on the UNO Q.").font(Theme.body(15)).foregroundStyle(Theme.fg2)
                }
            }
            .disabled(board.busy)
            Panel(title: "Power") {
                Text("Shut down before unplugging when you can.").font(Theme.body(14)).foregroundStyle(Theme.fg2)
                Button("Reboot board") { pending = .reboot }.buttonStyle(.industrial)
                Button("Shut down board") { pending = .poweroff }.buttonStyle(.industrialDanger)
            }
            .disabled(board.busy)
        }
        .confirmationDialog(pending?.question ?? "", isPresented: Binding(get: { pending != nil }, set: { if !$0 { pending = nil } }),
                            titleVisibility: .visible) {
            if let action = pending {
                Button(action.confirm, role: action == .poweroff ? .destructive : nil) {
                    switch action {
                    case .own, .join:
                        board.run(action.confirm) {
                            let _: Ack = try await board.call("POST", "/api/v1/network?mode=\(action.rawValue)")
                            return action == .own ? "Switching. Join Wi-Fi 811-Vision on this phone." : "Switching. Turn the hotspot on now."
                        }
                    case .reboot, .poweroff:
                        board.run(action.confirm) {
                            let _: Ack = try await board.call("POST", "/api/v1/power?action=\(action.rawValue)")
                            return action == .reboot ? "Rebooting. Back in about a minute." : "Shutting down. Safe to unplug in 20 seconds."
                        }
                    }
                }
            }
        }
    }
}
