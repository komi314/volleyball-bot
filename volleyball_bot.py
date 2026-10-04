import os
from datetime import datetime, timedelta
from supabase import create_client
import pywhatkit as kit
import time

# Deine Supabase Zugangsdaten
SUPABASE_URL = "https://ybghdcddwdtdfybqfxxk.supabase.co"
SUPABASE_KEY = "sb_publishable_EtE4Ouh4FBdBbLLMMnnTSA_Nehpq9WC"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Name deiner WhatsApp-Gruppe exakt wie in WhatsApp Web
WHATSAPP_GRUPPEN_NAME = "TSV Uheim1"

def check_and_send():
    today = datetime.now().date()
    # Alle Spiele von heute bis in 11 Tage (1,5 Wochen)
    target_date_max = today + timedelta(days=11)
    
    # Spiele aus Supabase abrufen (alles zwischen heute und in 11 Tagen)
    response = supabase.table("volleyball_spiele").select("*").gte("datum", str(today)).lte("datum", str(target_date_max)).execute()
    spiele = response.data
    
    if not spiele:
        print("Keine Spiele in den nächsten 1,5 Wochen gefunden.")
        return

    print(f"{len(spiel if 'spiel' in locals() else spiele)} Spiel(e) in den nächsten 1,5 Wochen gefunden. Starte Versand...")

    for spiel in spiele:
        gegner = spiel.get("gegner")
        datum = spiel.get("datum")
        uhrzeit = spiel.get("uhrzeit")
        ort = spiel.get("ort")
        
        # Datum für die Nachricht formatieren
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
        
        # WhatsApp Web steuern (öffnet Browser, tippt Nachricht, sendet ab)
        now = datetime.now()
        kit.send_what_msg_to_group(
            groupId_or_Name=WHATSAPP_GRUPPEN_NAME,
            message=nachricht,
            time_hour=now.hour,
            time_min=now.minute + 2, # Sendet in 2 Minuten
            wait_time=15,
            tab_close=True
        )
        print("Nachricht erfolgreich übergeben!")
        time.sleep(10)

if __name__ == "__main__":
    check_and_send()