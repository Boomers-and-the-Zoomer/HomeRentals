# Instrukser

## Setup

1. Installer [dprint](https://dprint.dev/install/). Dette er verktøyet vi bruker
   for samkjørt autoformattering.
2. Installer [Visual Studio Code](https://code.visualstudio.com/) (VSCode)
   1. Drit i alt som heter AI/KI når du installerer/har installert
   2. Trykk <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd> for å åpne
      "extensions"-panelet eller finn knappen for å åpne panelet på venstre side
      av VSCode.
   3. Installer "[Dprint Code Formatter]"
   4. Installer "[Python]"
   5. (Valgfritt) Installer "[vscode-icons]"
3. Kjør databaseskriptene
4. Juster variablene i `.env`-filen slik at du får koblet deg på din eqen mysql.

[vscode-icons]: https://marketplace.visualstudio.com/items?itemName=vscode-icons-team.vscode-icons
[Python]: https://marketplace.visualstudio.com/items?itemName=ms-python.python
[Dprint Code Formatter]: https://marketplace.visualstudio.com/items?itemName=dprint.dprint

## Verdt å vite om VSCode

- Du kan trykke <kbd>Ctrl</kbd>+<kbd>ø</kbd> for å åpne/lukke en "terminal" på
  bunnen av skjermen. Den kjører automatisk PowerShell, slik som Windows
  Terminal også gjør.
- Filen `.vscode/settings.json` inneholder prosjekt-spesifik konfigurasjon. Den
  er satt opp slik at vi alle bruker samme instillinger på ting som påvirker
  repository'et i en viss grad.

## Manuell Autoformattering

Kjør `dprint fmt`.
