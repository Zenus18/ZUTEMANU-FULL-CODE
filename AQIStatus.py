
def calculate_IAQ(score):
    IAQ_text = ""
    score = (100 - score) * 5

    if score >= 301:
        IAQ_text += "Hazardous"
        red.on()
        yellow.off()
        green.off()
        beep()
    elif 201 <= score <= 300:
        IAQ_text += "Very Unhealthy"
        red.on()
        yellow.off()
        green.off()
        beep()
    elif 176 <= score <= 200:
        IAQ_text += "Unhealthy"
        red.off()
        yellow.on()
        green.off()
        buzzer.off()
    elif 151 <= score <= 175:
        IAQ_text += "Unhealthy for Sensitive Groups"
        red.off()
        yellow.on()
        green.off()
        buzzer.off()
    elif 51 <= score <= 150:
        IAQ_text += "Moderate"
        red.off()
        yellow.off()
        green.on()
        buzzer.off()
    elif 0 <= score <= 50:
        IAQ_text += "Good"
        red.off()
        yellow.off()
        green.on()
        buzzer.off()
    return IAQ_text