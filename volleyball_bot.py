import os
from datetime import datetime
from supabase import create_client
import pywhatkit as kit
import time

# Deine Supabase Zugangsdaten (mit deinem echten Key)
SUPABASE_URL = "https://ybghdcddwdtdfybqfxxk.supabase.co"
SUPABASE_KEY = "sb_publishable_EtE4Ouh4FBdBbLLMMnnTSA_Nehpq9WC"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Name deiner WhatsApp-Gruppe exakt wie in WhatsApp Web
WHATSAPP_GRUPPEN_NAME = "TSV Uheim1"

def test_send_next_game():
    print("Starte Testlauf: Suche nach dem nächsten verfügbaren Spiel...")
    
    # Holt sich das nächste Spiel aus der Tabelle, unabhängig vom Datum
    response = supabase.table("volleyball_spiele").select("*").limit(1).execute()
    spiele = response.data
    
    if not spiele:
        print("Keinerlei Spiele in der Tabelle 'volleyball_spiele' gefunden!")
        return

    spiel = spiele[0]
    gegner = spiel.get("gegner")
    datum = spiel.get("datum")
    uhrzeit = spiel.get("uhrzeit")
    ort = spiel.get("ort")
    
    # Datum für die Nachricht formatieren
    formatted_date = datetime.strptime(datum, "%Y-%m-%d").strftime("%d.%m.%Y")
    
    nachricht = (
        f"🧪 *[TESTLAUF] Volleyball-Erinnerung* 🧪\n\n"
        f"📅 Datum: {formatted_date}\n"
        f"⏰ Uhrzeit: {uhrzeit} Uhr\n"
        f"🆚 Gegner: {gegner}\n"
        f"📍 Ort: {ort}\n\n"
        f"Dies ist ein Test, ob die Benachrichtigung klappt! 💪"
    )
    
    print(f"Sende Test-Nachricht an {WHATSAPP_GRUPPEN_NAME} für Spiel gegen {gegner}...")
    
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
    print("Test-Nachricht erfolgreich an WhatsApp Web übergeben!")

if __name__ == "__main__":
    test_send_next_game()