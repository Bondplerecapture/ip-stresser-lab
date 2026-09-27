"""Console entrypoint for ip-stresser-lab.

Wires config -> registry -> host, then either runs a single attack from
CLI args or drops into the interactive console.
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from rich.console import Console

from ip_stresser_lab.bootstrap.config_loader import load_config
from ip_stresser_lab.core.host import PluginHost
from ip_stresser_lab.core.registry import ExtensionRegistry
from ip_stresser_lab.utils.logging_setup import configure_logging

console = Console()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ip-stresser", description="ip-stresser-lab v0.6.3")
    p.add_argument("target", nargs="?", help="target IPv4/hostname")
    p.add_argument("-p", "--port", type=int, default=80, help="target port")
    p.add_argument("-m", "--method", default="syn", help="extension method (syn/udp/http/... )")
    p.add_argument("-t", "--duration", type=int, default=30, help="duration seconds")
    p.add_argument("-c", "--concurrency", type=int, default=64, help="worker count")
    p.add_argument("--config", type=Path, default=Path("config/config.yaml"))
    p.add_argument("--plugin-dir", type=Path, default=Path("plugins"))
    p.add_argument("--list", action="store_true", help="list loaded extensions and exit")
    p.add_argument("-v", "--verbose", action="count", default=0)
    return p


async def _run(args: argparse.Namespace) -> int:
    cfg = load_config(args.config)
    configure_logging(verbosity=args.verbose, log_dir=cfg.get("paths", {}).get("logs", "logs"))

    registry = ExtensionRegistry(plugin_root=args.plugin_dir, config=cfg)
    registry.discover()

    if args.list:
        for name, meta in registry.catalogue().items():
            console.print(f"[cyan]{name}[/] v{meta.version} — {meta.description}")
        return 0

    host = PluginHost(registry=registry, config=cfg)
    await host.start()

    if not args.target:
        console.print("[yellow]no target given — interactive mode not implemented in this build[/]")
        await host.stop()
        return 2

    ext = registry.resolve(args.method)
    if ext is None:
        console.print(f"[red]no extension registered for method '{args.method}'[/]")
        await host.stop()
        return 3

    result = await host.dispatch(
        ext,
        target=args.target,
        port=args.port,
        duration=args.duration,
        concurrency=args.concurrency,
    )
    console.print(f"[green]packets_sent={result.packets_sent} errors={result.errors} eps={result.eps:.0f}[/]")
    await host.stop()
    return 0


def main() -> int:
    args = build_parser().parse_args()
    try:
        return asyncio.run(_run(args))
    except KeyboardInterrupt:
        console.print("\n[red]aborted[/]")
        return 130


if __name__ == "__main__":
    sys.exit(main())