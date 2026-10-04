import os
from datetime import datetime, timedelta
from supabase import create_client
import pywhatkit as kit
import time

# Deine Supabase Zugangsdaten
SUPABASE_URL = "https://ybghdcddwdtdfybqfxxk.supabase.co"
SUPABASE_KEY = "sb_publishable_EtE4Ouh4FBdBbLLMMnnTSA_Nehpq9WC"  # Hier deinen echten Supabase Key eintragen
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Name deiner WhatsApp-Gruppe exakt wie in WhatsApp Web
WHATSAPP_GRUPPEN_NAME = "TSV Uheim1"

def check_and_send():
    today = datetime.now().date()
    # 1,5 Wochen = 10 bis 11 Tage im Voraus
    target_date_min = today + timedelta(days=10)
    target_date_max = today + timedelta(days=11)
    
    # Spiele aus Supabase abrufen
    response = supabase.table("volleyball_spiele").select("*").gte("datum", str(target_date_min)).lte("datum", str(target_date_max)).execute()
    spiele = response.data
    
    if not spiele:
        print("Kein Spiel in den nächsten 1,5 Wochen gefunden.")
        return

    for spiel in spiele:
        gegner = spiel.get("gegner")
        datum = spiel.get("datum")
        uhrzeit = spiel.get("uhrzeit")
        ort = spiel.get("ort")
        
        # Datum für die Nachricht formatieren
        formatted_date = datetime.strptime(datum, "%Y-%m-%d").strftime("%d.%m.%Y")
        
        nachricht = (
            f"🏐 *Erinnerung: Volleyball-Spiel in ca. 1,5 Wochen!*\n\n"
            f"📅 Datum: {formatted_date}\n"
            f"⏰ Uhrzeit: {uhrzeit} Uhr\n"
            f"🆚 Gegner: {gegner}\n"
            f"📍 Ort: {ort}\n\n"
            f"Bitte gebt rechtzeitig Bescheid, wer Zeit hat! 💪"
        )
        
        print(f"Sende Nachricht für Spiel gegen {gegner}...")
        
        # WhatsApp Web steuern (öffnet Browser, tippt Nachricht, sendet ab)
        now = datetime.now()
        kit.send_what_msg_to_group(
            groupId_or_Name=WHATSAPP_GRUPPEN_NAME,
            message=nachricht,
            time_hour=now.hour,
            time_min=now.minutee + 2 if hasattr(now, 'minutee') else now.minute + 2, # Sendet in 2 Minuten
            wait_time=15,
            tab_close=True
        )
        print("Nachricht erfolgreich übergeben!")
        time.sleep(10)
if __name__ == "__main__":
    check_and_send()