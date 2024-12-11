def convert_temperature(conversion_type, temp):
    if conversion_type == "c_to_f":
        return (temp * 9/5) + 32
    elif conversion_type == "f_to_c":
        return (temp - 32) * 5/9
    elif conversion_type == "k_to_c":
        return temp - 273.15
    elif conversion_type == "c_to_k":
        return temp + 273.15

conversions = {
    "1": "c_to_f",
    "2": "f_to_c",
    "3": "k_to_c",
    "4": "c_to_k"
}

menu = input("""välj ett sätt att konvertera
1. celsius till fahrenheit
2. fahrenheit till celsius
3. kelvin till celsius
4. celsius till kelvin
val: """)

if menu in conversions:
    temp = float(input("Skriv in temperatur: "))
    converted_temp = convert_temperature(conversions[menu], temp)
    print(f"Konverterad temperatur: {converted_temp}")