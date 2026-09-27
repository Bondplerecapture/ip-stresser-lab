"""Low-level packet construction helpers shared by SYN/UDP/ICMP extensions."""
from __future__ import annotations

import os
import random
import struct


def random_ipv4() -> str:
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def random_mac() -> str:
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))


def ip_header(src: str, dst: str, proto: int, payload_len: int, ident: int | None = None) -> bytes:
    version_ihl = 0x45
    tos = 0
    total_len = 20 + payload_len
    ident = ident if ident is not None else random.randint(0, 0xFFFF)
    flags_frag = 0
    ttl = random.randint(64, 255)
    checksum = 0
    saddr = struct.unpack("!I", bytes(map(int, src.split("."))))[0]
    daddr = struct.unpack("!I", bytes(map(int, dst.split("."))))[0]
    hdr = struct.pack(
        "!BBHHHBBHII", version_ihl, tos, total_len, ident, flags_frag, ttl, proto, checksum, saddr, daddr
    )
    return hdr


def tcp_syn_header(src_port: int, dst_port: int, seq: int | None = None) -> bytes:
    seq = seq if seq is not None else random.randint(0, 0xFFFFFFFF)
    ack = 0
    data_offset = 5 << 4
    flags = 0x02  # SYN
    window = 65535
    checksum = 0
    urg = 0
    return struct.pack("!HHIIBBHHH", src_port, dst_port, seq, ack, data_offset, flags, window, checksum, urg)


def requires_raw_socket() -> bool:
    """True on Windows when we need to send raw frames (admin + Npcap)."""
    return os.name == "nt"