# Systemanforderungsspezifikation (SRS): ESBot

## 1. Funktionale Anforderungen (FR)

| ID | Name der Anforderung | Beschreibung |
| :--- | :--- | :--- |
| **FR-1** | **Konversations-Interface** | Das System muss eine chatbasierte Benutzeroberfläche bereitstellen, über die Benutzer textbasierte Anfragen stellen und KI-generierte Erklärungen erhalten können. |
| **FR-2** | **Kontextbezogene Erklärungen** | Das System soll Erklärungen zu kursrelevanten Themen generieren, die spezifisch auf den Kontext der Benutzeranfrage zugeschnitten sind. |
| **FR-3** | **Übungsgenerierung** | Das System muss es Benutzern ermöglichen, explizit Quizfragen oder Übungsaufgaben zu einem bestimmten Lernthema anzufordern. |
| **FR-4** | **Automatisierte Auswertung** | Das System soll Antworten der Benutzer auf generierte Quizfragen bewerten und Feedback zur Korrektheit sowie zu Verbesserungsmöglichkeiten geben. |
| **FR-5** | **Sitzungspersistenz** | Das System muss den Interaktionsverlauf (Nachrichten und Metadaten) in einer Datenbank speichern, damit Benutzer Lernprozesse sitzungsübergreifend fortsetzen können. |
| **FR-6** | **Vertiefende Prompts** | Das System soll nach einer Erklärung proaktiv Klärungsfragen oder Vorschläge zur Vertiefung des Themas ("Deep Dive") anbieten. |
| **FR-7** | **RESTful API Zugriff** | Das Backend muss alle Kernfunktionen (Chat, Sitzungsverlauf, Quiz-Generierung) über eine dokumentierte REST-API zur Verfügung stellen. |
| **FR-8** | **KI-Inferenz-Integration** | Das System muss eine Verbindung zu externen oder lokalen LLM-Providern (z. B. Ollama, vLLM) herstellen, um Prompts zu verarbeiten und Antworten zu generieren. |

## 2. Nicht-funktionale Anforderungen (NFR)

### 2.1 Technische & Qualitätsattribute
* **NFR-1: Benutzbarkeit (Usability)**
  * Die Benutzeroberfläche muss intuitiv gestaltet sein, sodass Erstbenutzer ohne formale Einweisung eine Lernsession starten können.
* **NFR-2: Performance**
  * Die KI-Antwort (das erste Token) sollte bei einer Last von bis zu 50 gleichzeitig aktiven Benutzern innerhalb von **2–5 Sekunden** erscheinen.
* **NFR-3: Zuverlässigkeit & Fehlerbehandlung**
  * Bei einem Timeout oder Ausfall des KI-Dienstes muss das System eine benutzerfreundliche Fallback-Meldung anzeigen (z. B. "Der KI-Assistent ist vorübergehend nicht erreichbar"), anstatt Fehlermeldungen des Backends (Stack Traces) auszugeben.
* **NFR-4: Skalierbarkeit**
  * Backend- und KI-Inferenz-Layer müssen horizontal skalierbar sein, um eine unabhängige Ressourcenverteilung je nach Verkehrsaufkommen zu ermöglichen.
* **NFR-5: Sicherheit**
  * Das System muss eine Eingabevalidierung (Sanitization) implementieren, um Prompt-Injection zu verhindern.
  * Sitzungsdaten müssen isoliert sein; Benutzer dürfen nur Zugriff auf ihren eigenen Interaktionsverlauf haben.

### 2.2 Entwicklung & Wartung
* **NFR-6: Modularität**
  * Das System muss eine strikte Trennung zwischen Frontend (Tier 1), Backend (Tier 2) und Datenbank/Inferenz (Tier 3) einhalten.
* **NFR-7: Testbarkeit**
  * Die Architektur muss Entwurfsmuster wie **Dependency Injection** unterstützen, damit der KI-Inferenzdienst für automatisierte Tests durch einen **Mock-Dienst** ersetzt werden kann.
* **NFR-8: Observability (Beobachtbarkeit)**
  * Das System soll alle API-Request/Response-Zyklen sowie Prompt/Response-Paare der KI zu Debugging- und Qualitätsüberwachungszwecken protokollieren (unter Ausschluss personenbezogener Daten).

---

## 3. Systemrelevante Randbedingungen
* **Webbasiert:** Das System muss über gängige moderne Webbrowser (Chrome, Firefox, Safari) ohne lokale Installation zugänglich sein.
* **Nicht-Determinismus:** Die Validierung der Anforderungen muss berücksichtigen, dass KI-Antworten bei identischen Prompts variieren können. Tests sollten sich daher auf die Struktur und den pädagogischen Nutzen konzentrieren, nicht auf exakte Textübereinstimmung.

`Grammtik und Sortierung verbessern mit ChatGPT Version 5.3 (27.03.2026 15:45)`
