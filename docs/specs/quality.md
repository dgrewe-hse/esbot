# Qualitätsmodell nach ISO 25010: ESBot

## 1. Auswahl der Qualitätsmerkmale (Top 4)

### 1.1 Funktionale Angemessenheit (Functional Suitability)
* **Definition:** Der Grad, in dem das System Funktionen bereitstellt, die die erklärten Anforderungen (Lernunterstützung, Quiz-Generierung) erfüllen.
* **Relevanz für ESBot:** Da ESBot ein pädagogisches Werkzeug ist, ist es entscheidend, dass die KI nicht nur "antwortet", sondern didaktisch wertvolle Erklärungen liefert und die Übungen (FR-3) tatsächlich zum Kursinhalt passen.

### 1.2 Performance-Effizienz (Performance Efficiency)
* **Definition:** Die Leistung im Verhältnis zu den verbrauchten Ressourcen unter bestimmten Bedingungen.
* **Relevanz für ESBot:** KI-Inferenz ist ressourcenintensiv. Das System muss trotz der Latenz von Sprachmodellen (LLMs) eine flüssige Interaktion ermöglichen (NFR-2), damit der Lernfluss der Studierenden nicht unterbrochen wird.

### 1.3 Benutzbarkeit (Usability)
* **Definition:** Der Grad, in dem ein Produkt durch bestimmte Benutzer genutzt werden kann, um festgelegte Ziele effektiv und zufriedenstellend zu erreichen.
* **Relevanz für ESBot:** Da das System ohne Schulung (NFR-1) funktionieren soll, muss das Interface selbsterklärend sein. Ein komplizierter Chat würde das eigentliche Ziel – das Lernen – behindern.

### 1.4 Wartbarkeit (Maintainability) – Fokus: Testbarkeit
* **Definition:** Die Leichtigkeit, mit der ein System modifiziert werden kann, um Fehler zu korrigieren oder neue Anforderungen zu implementieren.
* **Relevanz für ESBot:** Im Kontext dieses Kurses ist die **Testbarkeit** (Teilmerkmal der Wartbarkeit) zentral. Das System muss so modular sein, dass der nicht-deterministische Teil (KI) isoliert getestet werden kann.

## 2. Dokumentation der Qualitätsmodelle (Metriken & Ziele)

| Qualitätsmerkmal | Qualitätsziel (Messbar) | Methode / Metrik |
| :--- | :--- | :--- |
| **Funktionale Angemessenheit** | Korrektheit der Quiz-Logik | Prozentsatz korrekt evaluierter Benutzerantworten (FR-4) durch Experten-Review > 90%. |
| **Performance-Effizienz** | Antwortlatenz unter Last | Zeit bis zum ersten Token (TTFT) < 2-5 Sekunden bei 50 parallelen Nutzern. |
| **Benutzbarkeit** | Erlernbarkeit | "Time-to-first-prompt": Ein neuer Nutzer stellt seine erste fachliche Frage in < 30 Sekunden nach dem Login. |
| **Wartbarkeit** | Testbarkeit der Logik | 100% der Backend-Schnittstellen (API) sind durch automatisierte Tests abdeckbar (Mocking-Fähigkeit). |

## 3. Maßnahmen zur Gewährleistung der Testbarkeit

Um den Aspekt der **Testbarkeit** während der Entwicklung von ESBot zu garantieren, schlagen wir folgende spezifische Maßnahmen vor:

### A. Entkopplung durch die Adapter-Pattern
Die KI-Inferenz (Ollama/vLLM) sollte über einen Adapter angesprochen werden. Dies erlaubt es, im Testfall einen "Stub-Adapter" zu verwenden, der vordefinierte Texte zurückgibt. So können wir das Backend testen, ohne teure oder langsame KI-Aufrufe tätigen zu müssen.

### B. Strukturierung der KI-Antworten (Schema-Validation)
Da KI-Output oft unvorhersehbar ist, sollte ESBot die KI zwingen, Antworten (insbesondere bei Quiz-Fragen) in einem strukturierten Format wie JSON auszugeben.
* **Maßnahme:** Automatisierte Tests validieren den Output gegen ein JSON-Schema. Das erhöht die Testbarkeit der "Answer Evaluation" (FR-4) massiv.

### C. Containerisierung für Integrationstests
Damit jeder Entwickler und die CI-Pipeline (Continuous Integration) die gleiche Umgebung haben, wird das gesamte System (UI, Backend, DB) in Docker-Containern bereitgestellt.
* **Maßnahme:** Integrationstests können per Skript eine saubere Test-Datenbank hochfahren und nach dem Test wieder löschen.

### D. Logging & Tracing für Fehlersuche
Um Fehler in der Kette "Nutzer -> Backend -> KI -> Nutzer" zu finden, muss jeder Schritt geloggt werden.
* **Maßnahme:** Implementierung von detaillierten Protokollen, die genau zeigen, welcher Prompt an die KI gesendet wurde. Dies ist essenziell, um "Halluzinationen" der KI von Fehlern im Backend-Code zu unterscheiden.

`Grammtik und Sortierung verbessern mit ChatGPT Version 5.3 (27.03.2026 15:45)`
