import os
import urllib.parse
import webbrowser
from datetime import datetime, timedelta
from supabase import create_client
import time
import pyautogui
import pyperclip

# Sicherheitsverzögerung für PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1.0

# Deine Supabase Zugangsdaten
SUPABASE_URL = "https://ybghdcddwdtdfybqfxxk.supabase.co"
SUPABASE_KEY = "sb_publishable_EtE4Ouh4FBdBbLLMMnnTSA_Nehpq9WC"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Exakter Name deiner WhatsApp-Gruppe
WHATSAPP_GRUPPEN_NAME = "TSV Uheim1"

def check_and_send():
    today = datetime.now().date()
    target_date_max = today + timedelta(days=11)
    
    print(f"Suche Spiele im Zeitraum von {today} bis {target_date_max}...")
    
    # Spiele abrufen: Nur solche, bei denen erinnerung_gesendet FALSE ist
    response = supabase.table("volleyball_spiele") \
        .select("*") \
        .gte("datum", str(today)) \
        .lte("datum", str(target_date_max)) \
        .eq("erinnerung_gesendet", False) \
        .execute()
        
    spiele = response.data
    
    if not spiele:
        print("Keine neuen Spiele für den Versand in den nächsten 1,5 Wochen gefunden. Alles aktuell! 👍")
        return

    print(f"{len(spiele)} offene(s) Spiel(e) gefunden! Starte WhatsApp-Versand...")

    for spiel in spiele:
        gegner = spiel.get("gegner")
        datum = spiel.get("datum")
        uhrzeit = spiel.get("uhrzeit")
        ort = spiel.get("ort")
        
        formatted_date = datetime.strptime(datum, "%Y-%m-%d").strftime("%d.%m.%Y")
        
        nachricht = (
            f"🏐 *Erinnerung: Kommendes Volleyball-Spiel!*\n\n"
            f"📅 Datum: {formatted_date}\n"
            f"⏰ Uhrzeit: {uhrzeit} Uhr\n"
            f"🆚 Gegner: {gegner}\n"
            f"📍 Ort: {ort}\n\n"
            f"Bitte gebt rechtzeitig Bescheid, wer Zeit hat! 💪"
        )
        
        print(f"Sende Nachricht für Spiel gegen {gegner} am {formatted_date}...")

        # 1. WhatsApp Web öffnen
        webbrowser.open("https://web.whatsapp.com")
        print("Warte, bis WhatsApp Web geladen ist...")
        time.sleep(15)
        
        print(f"Suche nach der Gruppe '{WHATSAPP_GRUPPEN_NAME}'...")
        
        # 2. Globale Suche aufrufen (Strg + Alt + /)
        pyautogui.press('escape')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'alt', '/')
        time.sleep(1)
        
        # 3. Gruppennamen eintippen und per Enter auswählen
        pyperclip.copy(WHATSAPP_GRUPPEN_NAME)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        
        # 4. Nachricht einfügen und senden
        pyperclip.copy(nachricht)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        pyautogui.press('enter')
        
        print("Nachricht erfolgreich gesendet! Aktualisiere Datenbank...")
        
        # 5. In Supabase vermerken (über Datum & Gegner, da das garantiert zieht)
        try:
            update_response = supabase.table("volleyball_spiele") \
                .update({"erinnerung_gesendet": True}) \
                .eq("datum", datum) \
                .eq("gegner", gegner) \
                .execute()
            
            print("Datenbank erfolgreich aktualisiert!")
        except Exception as e:
            print(f"FEHLER beim Datenbank-Update: {e}")
            
        print("Nächstes Spiel (falls vorhanden)...")
        time.sleep(5)

if __name__ == "__main__":
    check_and_send()