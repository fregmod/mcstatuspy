import tkinter as tk
from tkinter import messagebox
from mcstatus import JavaServer
import threading
import time

print("caricamento in corso...")
time.sleep(2)
print("programma avviato. fatto da gxvby.")
time.sleep(2)


def start_monitoring(ip):
    def update():
        while True:
            try:
                server = JavaServer.lookup(ip)
                status = server.status()
                motd = status.description['text'] if isinstance(status.description, dict) else status.description
                players_online = status.players.online
                players_max = status.players.max

                if players_online > 0 and status.players.sample:
                    player_names = ", ".join([player.name for player in status.players.sample])
                else:
                    player_names = "nomi visibili con la versione premium. programma fatto da: gxvbyッ"

                result_text = f"""
🌐 Server IP: {ip}
📛 MOTD: {motd}
👥 Player: {players_online}/{players_max}
🧑 Nomi: {player_names}
                """
                output_text.set(result_text.strip())

            except Exception as e:
                output_text.set(f"❌ Errore: {e}")

            time.sleep(2)  # Attendi 2 secondi

    threading.Thread(target=update, daemon=True).start()

def on_submit():
    ip = ip_entry.get().strip()
    if not ip:
        messagebox.showwarning("Attenzione", "Inserire un IP valido, riavviare il programma per evitare bug.")
        return
    output_text.set(" Connessione al server...")
    start_monitoring(ip)


# GUI Setup
root = tk.Tk()
root.title("MC server status")
root.geometry("500x400")
root.resizable(True, True)

tk.Label(root, text="Inserisci l'IP del server:").pack(pady=5)
ip_entry = tk.Entry(root, width=40)
ip_entry.pack(pady=5)

submit_btn = tk.Button(root, text="Avvia status check", command=on_submit)
submit_btn.pack(pady=10)

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, justify="left", anchor="nw", bg="white", relief="solid", width=60, height=15, padx=10, pady=10)
output_label.pack(pady=10)

root.mainloop()