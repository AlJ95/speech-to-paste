import openai
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL


class TextCleaner:
    def __init__(self):
        if not OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY ist nicht gesetzt. Bitte fügen Sie einen API-KEY in der .env-Datei hinzu.")
        
        # Konfiguriere OpenAI Client für OpenRouter
        self.client = openai.OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL
        )
        self.model = OPENROUTER_MODEL

    def clean_text(self, text: str) -> str:
        """
        Bereinigt den übergebenen Text mit Hilfe eines LLM von OpenRouter.
        
        Args:
            text (str): Der zu bereinigende Text
            
        Returns:
            str: Der bereinigte Text
        """
        if not text.strip():
            return text

        try:
            # Erstelle den Prompt für Textbereinigung
            system_prompt = """Du bist ein hilfreicher Assistent, der transkribierten Text aus Gesprächen bereinigt. Deine Aufgabe ist es:
1. Grammatikalische Fehler zu korrigieren
2. Füllwörter und Redundanzen zu entfernen
3. Den Text lesbar und verständlich zu machen
4. Die ursprüngliche Aussage und Bedeutung beizubehalten
5. Den Text in gängigem Deutsch zu formatieren
6. Den Text in formloses oder formelles Deutsch zu übertragen, je nach Kontext (Standardmäßig formlos
7. unnötige Zeilenumbrüche zu entfernen, sodass ein gut leserlicher Fließtext entsteht.)

WICHTIG: Deine Ausgabe darf nur direkt den Content des transkribierten Text beinhalten. Dein kompletter Output wird weiterverarbeitet. Es dürfen keine Erkärungen drin sein.
"""

            user_prompt = f"Bitte bereinige folgenden transkribierten Text und mache ihn lesbar und verständlich:\n\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Niedrigere Temperatur für konsistentere Ergebnisse
                max_tokens=2000   # Begrenze die Antwortgröße
            )

            cleaned_text = response.choices[0].message.content.strip()
            return cleaned_text

        except UnicodeError as e:
            print(f"Unicode-Fehler bei der Textbereinigung: {e}")
            # Im Unicode-Fehlerfall geben wir den Originaltext zurück
            return text
        except Exception as e:
            print(f"Fehler bei der Textbereinigung: {e}")
            # Im Fehlerfall geben wir den Originaltext zurück, um keinen Datenverlust zu haben
            return text
