import os
from datetime import datetime, timedelta
from supabase import create_client
import pywhatkit as kit
import time

# Deine Supabase Zugangsdaten
SUPABASE_URL = "https://ybghdcddwdtdfybqfxxk.supabase.co"
SUPABASE_KEY = "sb_publishable_EtE4Ouh4FBdBbLLMMnnTSA_Nehpq9WC"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# WICHTIG: Trage hier den Einladungs-Code deiner WhatsApp-Gruppe ein!
# Beispiel: Wenn der Link https://chat.whatsapp.com/AB123CDEFGHijklmn lautet, 
# ist die Group-ID hier "AB123CDEFGHijklmn"
WHATSAPP_GROUP_ID = "https://chat.whatsapp.com/L99bTQi617wKaxfMmmXwTt"

def check_and_send():
    today = datetime.now().date()
    # Alle Spiele von heute bis in die nächsten 1,5 Wochen (11 Tage)
    target_date_max = today + timedelta(days=11)
    
    print(f"Suche Spiele im Zeitraum von {today} bis {target_date_max}...")
    
    # Spiele aus Supabase abrufen
    response = supabase.table("volleyball_spiele").select("*").gte("datum", str(today)).lte("datum", str(target_date_max)).execute()
    spiele = response.data
    
    if not spiele:
        print("Keine Spiele in den nächsten 1,5 Wochen gefunden.")
        return

    print(f"{len(spiele)} Spiel(e) gefunden! Starte WhatsApp-Versand...")

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

        # Erhöhe die wait_time auf 30 Sekunden, damit WhatsApp Web in Ruhe laden kann
        now = datetime.now()
        kit.sendwhatmsg_to_group(
            WHATSAPP_GROUP_ID,
            nachricht,
            now.hour,
            now.minute + 2, 
            30,             # Erhöht auf 30 Sekunden Wartezeit zum Laden
            True            # tab_close
        )
        
        # WhatsApp Web steuern (Positionsargumente: group_id, message, time_hour, time_min, wait_time, tab_close, close_time)
        now = datetime.now()
        kit.sendwhatmsg_to_group(
            WHATSAPP_GROUP_ID,
            nachricht,
            now.hour,
            now.minute + 2, # Sendet in 2 Minuten
            15,             # wait_time
            True            # tab_close
        )
        print("Nachricht erfolgreich an WhatsApp übergeben!")
        time.sleep(10)

if __name__ == "__main__":
    check_and_send()