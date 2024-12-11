def ask_question(question, correct_answer):
    user_answer = input(question + "\n> ")
    return user_answer, correct_answer

def check_answer(user_answer, correct_answer):
    # Dela upp det korrekta svaret i en lista
    correct_answers_list = [ans.strip().lower() for ans in correct_answer.split(",")]
    # Dela upp användarens svar i en lista
    user_answers_list = [ans.strip().lower() for ans in user_answer.split(",")]
    
    # Kontrollera om alla korrekta svar finns i användarens svar
    return all(ans in user_answers_list for ans in correct_answers_list) and len(user_answers_list) == len(correct_answers_list)

def main():
    print("Välkommen till retorikanalysprovets instuderingsfrågor!\n")

    questions = [
        ("Vad är ethos?", "Ethos är trovärdigheten hos personen som håller i talet."),
        ("Vad är pathos?", "Pathos är när talaren väcker känslor genom att t.ex. berätta personliga anekdoter."),
        ("Vad är logos?", "Logos handlar om logik och att man använder sig utav siffror och fakta för att bevisa det man står för."),
        ("Vilka typer av argument finns det? (Nämn alla)", 
         "Sakargument, känsloargument, majoritetsargument, auktoritetsargument, värdeargument."),
        ("Vilka är de vanliga falluckorna när man argumenterar? (Nämn alla)", 
         "Personangrepp, oberättigade generaliseringar, majoritetsargument, rävsaxen, oklar statistik, vaga ord, övertalningsdefinitioner, dåliga auktoritetsargument."),
        ("Redogör för den klassiska dispositionen för argumenterande tal.", 
         "Inledning, argumentation, motargument, avslutning."),
        ("Vad utmärker språket i argumenterande tal?", 
         "Det är ofta klart, övertygande och syftar till att påverka åhörarna."),
        ("Nämn några vanliga stilfigurer och deras effekt.", 
         "Allitteration, allusion, anafor, antites, besjälning, epifor, hyperbol, liknelse, metafor, retorisk fråga, stegring, upprepning.")
    ]

    for question, correct_answer in questions:
        user_answer, correct_answer = ask_question(question, correct_answer)
        if check_answer(user_answer, correct_answer):
            print("Rätt!\n")
        else:
            print(f"Fel! Rätt svar är: {correct_answer}\n")

    print("Bra jobbat! Du har gått igenom alla frågor.")

if __name__ == "__main__":
    main()