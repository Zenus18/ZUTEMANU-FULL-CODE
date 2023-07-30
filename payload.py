def send_to_ubidots(payload):
    url = "https://industrial.api.ubidots.com/api/v1.6/devices/bme680"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": "BBFF-ha9Yzk9zFNMZL21MHBTdKSms4ffDYX"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Data berhasil diunggah ke Ubidots")
    else:
        print("Gagal mengunggah data ke Ubidots. Kode status:", response.status_code)