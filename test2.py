def yell(text):
    return text.upper()

y = yell
YY = {"yell":yell}
print(y("heyyyyyyyyyyy"))
print(YY["yell"]("helo"))