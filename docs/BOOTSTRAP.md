# BOOTSTRAP: PROJEK RETRORECON (COMMANDO C64 REKONSTRUKSIE)
**Omvattende Lesse Geleer, Uitvoerbare Instruksies & Plan van Aanpak vir Nuwe AI-Agente**

> **Doel van hierdie dokument:**  
> Hierdie dokument dien as die primêre selfstandige beginpunt (**Bootstrap**) vir enige nuwe AI-agent of ontwikkelaar wat die *Commando* (Commodore 64, Capcom / Elite Systems 1985) rekonstruksieprojek vanaf nul (from scratch) wil herbou of voortsit.

---

## 1. DANGENDE OPDRAG AAN DIE NUWE AI-AGENT: LEESVOLGORDE

Voordat jy enige kode skryf, enige lêer wysig of enige opdrag uitvoer, **MOET** jy die volgende dokumente in presies hierdie volgorde bestudeer:

1. **`D00_Bootstrap_masterprompt.md` (v1.3):**
   * *Doel:* Beheer die metodologie, die twee-modus kommunikasiereël, en die vennootgesprek.
   * *Sleutelreël:* Kommunikeer altyd in **Afrikaans**. Gebruik **Modus A** vir gesprekvoering met die gebruiker (*Waar is ons? Wat het ons gevind? Wat beteken dit? Wat doen ons volgende?*) en **Modus B** vir tegniese rekordhouding in die artefak `projekrekord.md`.
2. **`D01_tech_Meesterprompt.md` (v1.1-RC):**
   * *Doel:* Beheer die forensiese bewysstandaarde, 6502/C64 VIC-II/SID masjienkode-analise, toetsgedrewe ontwikkeling (TDD RED → GREEN → REFACTOR) en argitektoniese reëls.
   * *Sleutelreël:* Geen generiese emulators as finale produk nie; suiwer objekgeoriënteerde Python met 50 Hz PAL-tydreëling; geen eksterne pip-afhanklikhede buite die standaardbiblioteek nie.
3. **`D02_Functionele_specificaties.md` (v0.1):**
   * *Doel:* Die funksionele kontrak en waarneembare spelgedrag van die oorspronklike speletjie.
4. **Hierdie dokument (`BOOTSTRAP.md`):**
   * *Doel:* Praktiese lesse geleer, geïdentifiseerde slaggate, stelselkonfigurasies en die stapsgewyse Plan van Aanpak.

---

## 2. DEEL I: LESSE GELEER & KRITIESE SLAGGATE (LESSONS LEARNED)

Hieronder volg die harde, beproefde praktiese lesse wat tydens die eerste bou van hierdie projek ontdek is:

### 2.1 Bronvalstrik: Cracktros vs. Egte Spelvrag (D64 Oorwinning)
* **Die Slaggat:** Die projek het aanvanklik begin met `Commando (1986)(Torquemada).prg` (3.7 KB). Dit was 'n kraak-inleiding (cracktro/stager) en het glad nie die werklike spelkode of -grafika bevat nie.
* **Die Les:** Moenie kraaklêers ontleed nie. Die amptelike skyfbeeld `Commando.d64` (174,848 grepe) bevat die outentieke 43 KB masjienkodelading `COMMANDO.prg` (laaiadres `$0801`, SHA256: `0ee4ef2d99685799a22a3cef1135cd0ff6a6bed8526e375fa7225a959a5a3599`). Gebruik slegs die D64-ekstraksie.

### 2.2 Omgewing & macOS Sandboxing
* **Die Slaggat:** Die stelsel se verstek `python3` wys na 'n virtuele omgewing op 'n eksterne volume (`/Volumes/data1/michiele/venv/venv3.12`). In standaard sandbox-modus veroorsaak toegang daartoe `PermissionError: [Errno 1] Operation not permitted`.
* **Die Les:** 
  * Die gebruiker se amptelike virtuele tolk is:
    ```bash
    source /Volumes/data1/michiele/venv/venv3.12/bin/activate
    ```
    Of direk:
    ```bash
    /Volumes/data1/michiele/venv/venv3.12/bin/python3
    ```
  * Wanneer opdragte met hierdie tolk uitgevoer word, vereis dit `BypassSandbox: true` (wat die gebruiker eenmalig outoriseer).
  * Behou eenvoudige, direkte opdragvorme (`/Volumes/data1/.../python3 script.py`) sonder ingewikkelde dopsubstitusies (`$(...)`), sodat die omgewing die magtiging outomaties kan herken.

### 2.3 Klank- & Musieksintese sonder Eksterne Biblioteke
* **Die Slaggat:** Biblioteke soos `pygame` of `pyaudio` vereis eksterne C-samestelling en pip-installasies wat faal in sekere sandkaste of MacOS-weergawes.
* **Die Les:** 
  * Wiskundige sintese via Python se ingeboude `wave`, `struct` en `math` modules is 100% stabiel, vinnig en lewer perfekte 16-bis 22,050 Hz klanklêers in `/tmp/commando_sounds/`.
  * Afspeel via macOS se inheemse `/usr/bin/afplay` in 'n agtergrond-draad (`threading.Thread` met `subprocess.Popen`) bied nie-blokkerende, kristalhelder klank sonder enige eksterne pip-pakket.
  * Rob Hubbard se 50 Hz SID-musiek (beide die 136 BPM funk C-mineur introtitel en die 98 BPM liriese F-mineur hoëtellingtema) kan suiwer wiskundig met pulswydtemodulasie (PWM) en gefiltreerde ruis gesintetiseer word.

### 2.4 Tkinter Beeldformaat: PNG bo JPEG
* **Die Slaggat:** `tkinter.PhotoImage` ondersteun nie JPEG-beelde (`.jpg`) sonder die Pillow-biblioteek nie.
* **Die Les:** Skakel enige eksterne titelskermkuns (`intro.jpg`) vooraf om na 'n 960x600 PNG (`intro.png`). Tkinter laai PNG-lêers blitsvinnig en inheems. Voorsien altyd 'n gladde terugval op die prosessuele 3D C64 COMMANDO-vektorlogo as die prentlêer nie gevind word nie.

### 2.5 TDD & Speltoestand-Isolasie
* **Die Slaggat:** Toe die speletjie uitgebrei is met 'n titelskerm (`GameMode.TITLE`), het bestaande eenheidstoetse wat `game.update()` geroep het, begin faal omdat die enjin in titelskermmodus was en nie spelersbeweging opgedateer het nie!
* **Die Les:**
  * Laat `GameState.__init__` by verstek begin met `start_mode: GameMode = GameMode.PLAYING`.
  * In die werklike spelbekendstelling (`run_commando()`), skep die speletjie met `start_mode=GameMode.TITLE`.
  * Dit verseker dat alle outomatiese toetse dadelik die speelveld toets, terwyl die speletjie self met die regte titelskerm en musiek vir die menslike speler begin.
  * Hoëtellingstoetse moet altyd 'n tydelike lêer (`/tmp/test_highscores.json`) gebruik om te verhoed dat data uit vorige spelrondtes toetse laat faal.

---

## 3. DEEL II: PLAN VAN AANPAK (FASE VIR FASE VAN NUL AF)

As jy die projek vanaf 0 moet herbou, volg hierdie presiese, beproefde ingenieursfases:

```
[Fase 0: Omgewing] ──> [Fase 1: Forensika] ──> [Fase 2: SID Klank] ──> [Fase 3: MVP Demo 0]
                                                                               │
[Fase 6: Afronding] <── [Fase 5: Inkrement 3] <── [Fase 4: Inkrement 2] <─────┘
```

### Fase 0: Omgewingsvalidering
1. Bevestig dat die virtuele omgewing aktief is:
   ```bash
   /Volumes/data1/michiele/venv/venv3.12/bin/python3 -V
   ```
2. Skep die standaard gidsstruktuur:
   * `./tests/` (alle toetse hoort streng hier).
   * `./extracted_d64/` (bronartefakte).
3. Skep die projekrekord `projekrekord.md` (Modus B).

### Fase 1: Forensiese Bron-onttrekking (Werkstroom A)
1. Ontleed `Commando.d64` en onttrek `COMMANDO.prg` (43,005 grepe, laaiadres `$0801`).
2. Teken die forensiese bewyse aan in `projekrekord.md`:
   * **VIC-II Bank:** CIA2 Port A (`$DD00`) stel Bank 3 (`$C000`–`$FFFF`).
   * **Skermgeheue:** `$E000` (`$D018 = #$80`).
   * **Sprite Pointers:** `$E3F8`–`$E3FF`.
   * **Kleurskema:** `$D025 = 15` (ligrys), `$D026 = 0` (swart), `$D027 = 5` (groen).
   * **8-Rigting Beheer:** Chris Butler se hoekkodes by `$376F`–`$384B` wat geskryf word na `$04E0`:
     `0=UP, 2=UP_RIGHT, 4=RIGHT, 6=DOWN_RIGHT, 8=DOWN, 10=DOWN_LEFT, 12=LEFT, 14=UP_LEFT`.

### Fase 2: SID Klank- & Musiek-argitektuur (`sound_effects.py`)
1. Implementeer `sound_effects.py` met suiwer `wave` / `struct` sintese:
   * `shoot`: Geweerskoot (geraas + dalende sinus).
   * `explosion`: Handgranaat (lae rommel + gefiltreerde ruis).
   * `grenade_throw`: Paraboliese gooi-toon.
   * `enemy_hit`: Vyandelike sneuwelgeluid.
   * `rescue`: POW-bevryding (C5-E5-G5-C6 arpeggio-chime).
   * `pickup`: Voorraadkrat optel (880 Hz -> 1760 Hz bliep).
   * `victory`: Heroïese triomffanfare.
   * `theme`: Rob Hubbard 136 BPM C-mineur introwysie (16de-noot funk baslyn + melodie).
   * `highscore`: Rob Hubbard 98 BPM F-mineur hoëtelling-wysie (Subtune 2).
2. Skep `SoundManager` met agtergrond-lus via `/usr/bin/afplay`.

### Fase 3: Minimum Lewensvatbare Speelbare Enjin (Demo 0 & Inkrement 1)
1. **TDD RED:** Skryf toetse in `tests/test_commando.py`:
   * Speler posisie, lewens (3), granate (6), Chris Butler 8-rigting kodes.
   * Handgranaat met paraboliese boog, vlugtyd en ontploffingsradius.
   * Sandsakke wat koeëls blokkeer.
2. **TDD GREEN:** Implementeer kern in `commando.py`:
   * `Direction`, `Player`, `Bullet`, `Grenade`, `Explosion`, `Obstacle`, `GameState`.
   * Vaste 50 Hz (20 ms) tydstap op Tkinter Canvas (320x200 skaal x3 = 960x600).
   * Vlak 1 (Die Buitepos) met vertikale skermrol (1250 px wêreldhoogte).
   * Vestinghek 1 met hekwagte.
3. **Kry Goedkeuring:** Laat die gebruiker die spel toets.

### Fase 4: Inkrement 2 — Gevorderde AI, Vragmotors & Vlak 2
1. **TDD RED:** Toetse vir hurkende vyande, hardloopoffisiere, vragmotor-ontplooiing, en Vlak 2-oorgang.
2. **TDD GREEN:**
   * `CROUCHING_GUNNER`: Hurk agter sandsakke (onkwesbaar teen koeëls), staan periodiek op om te skiet.
   * `OFFICER_RUNNER`: Hoëspoed-flankeerder.
   * `Truck`: Ry in, stop op y=800, laai 3 troepe af en ry weg.
   * **Vlak 2 (Rivier & Hangbrug):** Vloeiende blou water (`ObstacleType.RIVER`), houthangbrug (`ObstacleType.BRIDGE`), brugwagte en Vestinghek 2.
3. **Kry Goedkeuring:** Laat die gebruiker Vlak 2 voltooi en goedkeur.

### Fase 5: Inkrement 3 — Gyselaars (POWs), Kratte, Vlak 3 & Hall of Fame
1. **TDD RED:** Toetse vir POW-redding, friendly fire, kratoptel, Vlak 3-oorwinning en `highscores.json`.
2. **TDD GREEN:**
   * `Hostage` (POW): Gevange soldaat. As wag doodgemaak word, hardloop hy vry ("THANKS!") vir +1,000 punte. As hy per abuis geskiet word, sneuwel hy sonder punte.
   * `SupplyCrate`: Houtkiste met "G" wat +3 granate en +500 punte gee.
   * **Vlak 3 (Woestynvesting):** Woestyngrond, diep loopgrawe, 4 elite hekwagte, en finale oorwinningskerm (+25,000 bonus).
   * `HighScoreManager`: Stoor en laai top-5 rekords vanaf `highscores.json`.
3. **Kry Goedkeuring:** Laat die gebruiker die hele speletjie deurspeel.

### Fase 6: Finale Afronding & Vrystelling
1. **Titelskerm & Logo:**
   * Outentieke C64 Commando-laaiskerm (`intro.png`).
   * Prosessuele 3D C64 COMMANDO militêre stensil-logo met skaduwees en geel glanse.
2. **Attract Demo-modus:**
   * `DemoAI`: Neem Joe outomaties oor na 8 sekondes van speler-onaktiwiteit.
   * `Space` of `Enter` begin dadelik 'n regte spelersessie.
3. **Naam-invoerstelsel:**
   * Sleutelbordnaam-invoer met knipperende wyser by nuwe hoëtellings voor oorskakeling na Hall of Fame.
4. **CRT-skandeerlyne:**
   * Outentieke 1084S-monitor lyne (wissel af met `C`).
5. **Konfigurasie:**
   * `ConfigManager` wat instellings bewaar in `config.json`.
6. **Dokumentasie:**
   * Dateer `README.md` en `projekrekord.md` op.

---

## 4. DEEL III: TEGNIESE KONTROLYS VIR DIE NUWE AI-AGENT

Wanneer jy die projek herbou of uitbrei, kontroleer altyd hierdie lys voor jy aanmeld:

* [ ] Is die virtuele tolk `/Volumes/data1/michiele/venv/venv3.12/bin/activate` gebruik?
* [ ] Slaag alle eenheidstoetse 100% foutloos?
  ```bash
  /Volumes/data1/michiele/venv/venv3.12/bin/python3 -m unittest discover -s tests
  ```
* [ ] Is alle toetse uitsluitlik in `./tests/` geplaas?
* [ ] Is daar GEEN eksterne pip-installasies bygevoeg nie?
* [ ] Is `projekrekord.md` bygewerk met die nuwe status?
* [ ] Is die gebruiker in **Afrikaans** geantwoord volgens **Modus A** (*Waar is ons? Wat het ons gevind? Wat beteken dit? Wat doen ons volgende?*)?

---
*Gedokumenteer op 24 Oktober 2026 vir Projek RETRORECON.*
