import asyncio
import csv
from datetime import datetime
from pathlib import Path
from bleak import BleakClient, BleakScanner

# === UUIDs BLE
START_UUID = "abcdefab-cdef-1234-5678-abcdefabcdeb"
GSR_UUID   = "abcdefab-cdef-1234-5678-abcdefabcdea"

# === CSV file path
csv_filename = Path(__file__).resolve().parent / "ReceiverGSR.csv"
if not csv_filename.exists():
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "GSR Value (uS)"])

# === Callback
def handle_gsr(_, data):
    import struct
    conductance_uS = struct.unpack('<f', data)[0]  # BLEFloat => 4 octets little endian
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    with open(csv_filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, round(conductance_uS, 2)])

    print(f"🟢 {timestamp} | GSR: {conductance_uS:.2f} µS")

# === Main function
async def run():
    print("🔍 Recherche de l'Arduino GSR...")
    devices = await BleakScanner.discover(timeout=5)
    arduino = next((d for d in devices if d.name and "Arduino-GSR" in d.name), None)

    if not arduino:
        print("❌ Arduino 'Arduino-GSR' introuvable.")
        return

    print(f"✅ Appareil trouvé : {arduino.name} ({arduino.address})")

    async with BleakClient(arduino.address) as client:
        print("📡 Connecté. Activation des notifications BLE...")
        await client.start_notify(GSR_UUID, handle_gsr)

        print("🚀 Envoi du signal de démarrage...")
        await client.write_gatt_char(START_UUID, bytearray([1]))

        print("📬 En attente des données. Ctrl+C pour quitter.")
        while True:
            await asyncio.sleep(1)

try:
    asyncio.run(run())
except KeyboardInterrupt:
    print("\n🛑 Arrêté par l'utilisateur.")
