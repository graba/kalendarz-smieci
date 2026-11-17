#!/usr/bin/env python3
"""Generuje smieci.ics z harmonogram.json.
Wydarzenia całodniowe, przypomnienie o 21:00 dzień wcześniej (TRIGGER:-PT3H).
Użycie: python3 generate.py"""
import json
from collections import defaultdict
from datetime import date, timedelta

d = json.load(open("harmonogram.json", encoding="utf-8"))
days = defaultdict(list)
for frakcja, daty in d["terminy"].items():
    for s in daty:
        days[date.fromisoformat(s)].append(frakcja)

def esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")

L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//kalendarz-smieci//PL", "CALSCALE:GREGORIAN",
     "METHOD:PUBLISH", "X-WR-CALNAME:Odbiór śmieci", "X-WR-TIMEZONE:Europe/Warsaw",
     "REFRESH-INTERVAL;VALUE=DURATION:P1D", "X-PUBLISHED-TTL:P1D"]
for day in sorted(days):
    fr = ", ".join(days[day])
    L += ["BEGIN:VEVENT",
          f"UID:smieci-{day:%Y%m%d}@kalendarz-smieci",
          f"DTSTAMP:{day:%Y%m%d}T000000Z",  # stały: plik zmienia się tylko przy zmianie harmonogramu
          f"DTSTART;VALUE=DATE:{day:%Y%m%d}",
          f"DTEND;VALUE=DATE:{day + timedelta(1):%Y%m%d}",
          "SUMMARY:" + esc(f"🗑️ Odbiór: {fr}"),
          "DESCRIPTION:" + esc(f"Odbiór od 6:30 – wystaw pojemniki/worki wieczorem dzień wcześniej.\nHarmonogram {d['okres']}: {d['zrodlo']}"),
          "TRANSP:TRANSPARENT",
          "BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + esc(f"Wystaw śmietniki: {fr}"),
          "TRIGGER:-PT3H", "END:VALARM",
          "END:VEVENT"]
L.append("END:VCALENDAR")

def fold(line):
    b = line.encode("utf-8"); out = []
    while len(b) > 75:
        cut = 75 if not out else 74
        while (b[cut] & 0xC0) == 0x80: cut -= 1
        out.append(b[:cut].decode()); b = b[cut:]
    out.append(b.decode())
    return "\r\n ".join(out)

open("smieci.ics", "w", encoding="utf-8", newline="").write("\r\n".join(fold(l) for l in L) + "\r\n")
print(f"{len(days)} dni odbioru -> smieci.ics")
