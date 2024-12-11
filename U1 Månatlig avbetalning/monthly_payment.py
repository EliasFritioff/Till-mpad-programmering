def calculate_monthly_payment(principal, annual_rate, years):
    monthly_rate = annual_rate / 12 / 100
    payments = years * 12
    monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -payments)
    return monthly_payment

principal = float(input("Lånebelopp: "))
annual_rate = float(input("Årsränta (%): "))
years = int(input("Löptid (år): "))

payment = calculate_monthly_payment(principal, annual_rate, years)

print(f"Din månatliga betalning är: {payment:.2f} kr")