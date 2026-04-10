# Base Technologies

## User Interface (UI) – Tier 1

### Mögliche Optionen

**Webanwendung:**

* Angular
* Vue.js
* Svelte

**Desktop:**

* Windows Forms App

**Mobile:**

* Android Studio

### Entscheidung: Angular

**Begründung:**

* Das gesamte Team verfügt bereits über Erfahrung mit Angular.
* Eine webbasierte Anwendung ist plattformunabhängig und auf allen Geräten nutzbar.

  * Native Apps oder Windows-Forms-Anwendungen wären hingegen gerätegebunden.
* Basierend auf der Aufgabenstellung wird ein eher einfaches Interface erwartet.

  * Voraussichtlich umfasst die Anwendung 2–3 Seiten:

    * Hauptseite
    * Einstellungsseite
    * Optionale Login-Seite

---

## Application Backend – Tier 2

### Mögliche Optionen

* .NET (C#)
* Spring Boot (Java)

### Entscheidung: .NET (C#)

**Begründung:**

* Höhere Erfahrung im Team mit dieser Technologie.
* Bereits vorhandenes Know-how im Bereich Load Balancing.
* Nutzung von internem Caching ist bekannt und erprobt.

---

## Datenbank – Tier 3

### Mögliche Optionen

* MySQL
* SQLite
* MongoDB
* PostgreSQL

### Entscheidung: PostgreSQL

**Begründung:**

* Vorhandene Erfahrung im Team.
* Bereits eine laufende Instanz auf einem privaten Server verfügbar, öffentlich erreichbar unter `local.braincrush.org`.

---

## LLM Inference Engine (optional)

Aktuell wird auf die Integration eines LLM verzichtet.

**Begründung:**

* Vermeidung zusätzlicher Kosten.
* Keine Nutzung von privaten oder ressourcenintensiven LLM-Infrastrukturen geplant.

---

# Gruppenorganisation

| Rolle                                                                    | Name           | HS-ID  |
| ------------------------------------------------------------------------ | -------------- | ------ |
| Design Manager (verantwortlich für finale UI-Entscheidungen)             | Leon Kirasic   | 777511 |
| Scrum Master / Project Lead (Ticketverteilung und Fortschrittskontrolle) | Jan Schröter   | 770437 |
| Dokumentationsprüfer (Vollständigkeit und Qualität der Dokumentation)    | Jan Rörhle     | 777840 |
| Test Manager (Verantwortung für Tests)                                   | Alle           | 000000 |
| QA (Sicherstellung der Einhaltung der Anforderungen)                     | Benjamin Supke | 777354 |

**Begründung der Aufteilung:**
Die Rollenverteilung basiert auf den jeweiligen Vorerfahrungen sowie den individuellen Präferenzen innerhalb der Gruppe.

`Grammtik verbessern mit ChatGPT Version 5.3 (22.03.2026 17:45)`
