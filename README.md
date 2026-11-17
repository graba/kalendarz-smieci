# kalendarz-smieci

Harmonogram odbioru odpadów (Gmina Lesznowola, zabudowa jednorodzinna) jako subskrybowany kalendarz.

- `harmonogram.json` – terminy dla każdej frakcji + link do źródłowego PDF gminy
- `generate.py` – generuje `smieci.ics` (wydarzenia całodniowe, przypomnienie o 21:00 dzień wcześniej)
- `smieci.ics` – plik do subskrypcji:
  `webcal://raw.githubusercontent.com/graba/kalendarz-smieci/main/smieci.ics`

Aktualizowane automatycznie raz w tygodniu, gdy gmina opublikuje nowy lub zmieniony harmonogram.
