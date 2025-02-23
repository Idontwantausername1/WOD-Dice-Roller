import random
import datetime
import os
from colorama import init, Fore, Style

# Initialize colorama for Windows support
init(autoreset=True)

# 🔹 World of Darkness Splats Data
SPLATS = {
    "Vampire": {"hunger_dice": True, "success_threshold": 6},
    "Werewolf": {"hunger_dice": False, "success_threshold": 7, "rage_dice": True},
    "Mage": {"arete_roll": True},
    "Changeling": {"banality_roll": True},
    "Wraith": {"pathos_roll": True, "angst_roll": True},
    "Demon": {"faith_roll": True, "torment_roll": True},
    "Mummy": {"balance_roll": True, "sekhem_roll": True},
    "Hunter": {"desperation_roll": True, "willpower_roll": True},
    "Kindred of the East": {"chi_roll": True, "dharma_roll": True},
    "Ghoul": {"frenzy_roll": True},
    "Mortal": {"standard_roll": True},
}

# 🔹 Input Helper Functions
def get_int_input(prompt, min_value=1):
    """Safely gets an integer input above min_value."""
    while True:
        try:
            value = int(input(Fore.YELLOW + prompt + Style.RESET_ALL))
            if value >= min_value:
                return value
            print(f"{Fore.RED}⚠️ Enter a number ≥ {min_value}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}⚠️ Invalid input! Enter a number.{Style.RESET_ALL}")

def get_yes_no_input(prompt):
    """Safely gets a yes/no user response."""
    while True:
        choice = input(Fore.CYAN + prompt + Style.RESET_ALL).strip().lower()
        if choice in ['y', 'n']:
            return choice
        print(f"{Fore.RED}⚠️ Enter 'y' for Yes or 'n' for No.{Style.RESET_ALL}")

def get_splat_choice():
    """Prompts the user to choose their splat."""
    print(f"\n{Fore.BLUE}🌑 Choose Your World of Darkness Game 🌑{Style.RESET_ALL}")
    for i, splat in enumerate(SPLATS.keys(), 1):
        print(f"{i}. {splat}")

    while True:
        choice = get_int_input("Enter your selection: ", 1)
        if 1 <= choice <= len(SPLATS):
            return list(SPLATS.keys())[choice - 1]
        print(f"{Fore.RED}⚠️ Invalid choice! Select a valid option.{Style.RESET_ALL}")

# 🔹 Generalized Rolling Function
def roll_generic(num_dice, difficulty=6, roll_name="Roll"):
    """Handles all dice rolling and success tracking."""
    results = [random.randint(1, 10) for _ in range(num_dice)]
    successes = sum(1 for die in results if die >= difficulty)
    botch = results.count(1) >= len(results) // 2  # If half or more dice are 1s, it's a botch

    print(f"\n🎲 {Fore.CYAN}{roll_name} Dice: {results}{Style.RESET_ALL}")
    print(f"✅ {Fore.GREEN}Total Successes: {successes} (Difficulty: {difficulty}){Style.RESET_ALL}")

    if botch:
        print(f"{Fore.RED}❌ Botch! Severe consequences may occur!{Style.RESET_ALL}")
    elif successes > 0:
        print(f"{Fore.GREEN}✨ Success!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Failure!{Style.RESET_ALL}")

    return successes

# 🔹 Splat-Specific Rolls
def mage_arete_roll(): roll_generic(get_int_input("Enter Arete rating: "), get_int_input("Enter difficulty (3-9): "), "Arete")
def changeling_banality_roll(): roll_generic(get_int_input("Enter Banality rating: "), 6, "Banality")
def wraith_pathos_roll(): roll_generic(get_int_input("Enter Pathos rating: "), 6, "Pathos")
def wraith_angst_roll(): roll_generic(get_int_input("Enter Angst rating: "), 6, "Angst")
def demon_faith_roll(): roll_generic(get_int_input("Enter Faith rating: "), 6, "Faith")
def demon_torment_roll(): roll_generic(get_int_input("Enter Torment rating: "), 6, "Torment")
def mummy_balance_roll(): roll_generic(get_int_input("Enter Balance rating: "), 6, "Balance")
def mummy_sekhem_roll(): roll_generic(get_int_input("Enter Sekhem rating: "), 6, "Sekhem")
def hunter_desperation_roll(): roll_generic(get_int_input("Enter Desperation dice: "), 6, "Desperation")
def hunter_willpower_roll(): roll_generic(get_int_input("Enter Willpower rating: "), 6, "Willpower")
def kuei_jin_chi_roll(): roll_generic(get_int_input("Enter Chi pool (Yin + Yang): "), 6, "Chi")
def kuei_jin_dharma_roll(): roll_generic(get_int_input("Enter Dharma rating: "), 6, "Dharma")
def ghoul_frenzy_roll(): roll_generic(get_int_input("Enter Willpower rating: "), 6, "Frenzy")
def standard_roll(): roll_generic(get_int_input("Enter total number of dice: "), get_int_input("Enter difficulty: "), "Attribute + Skill")

# 🔹 Splat Function Map (For Dynamic Execution)
SPLAT_FUNCTIONS = {
    "Mage": mage_arete_roll,
    "Changeling": changeling_banality_roll,
    "Wraith": [wraith_pathos_roll, wraith_angst_roll],
    "Demon": [demon_faith_roll, demon_torment_roll],
    "Mummy": [mummy_balance_roll, mummy_sekhem_roll],
    "Hunter": [hunter_desperation_roll, hunter_willpower_roll],
    "Kindred of the East": [kuei_jin_chi_roll, kuei_jin_dharma_roll],
    "Ghoul": ghoul_frenzy_roll,
    "Mortal": standard_roll
}

# 🔹 Main Game Loop
def main():
    splat = get_splat_choice()

    while True:
        if splat in SPLAT_FUNCTIONS:
            function = SPLAT_FUNCTIONS[splat]
            if isinstance(function, list):  # If multiple rolls exist (e.g., Wraith, Demon)
                print(f"\nAvailable Rolls: {', '.join([f.__name__.replace('_', ' ').title() for f in function])}")
                choice = get_int_input("Which roll do you want to perform? (1 or 2): ", 1) - 1
                function[choice]()  
            else:
                function()  
        else:
            standard_roll()  

        if get_yes_no_input("\nRoll again? (y/n): ") != 'y':
            break

if __name__ == "__main__":
    main()

# 🌎 Flask API Integration (Add this at the BOTTOM of your script)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/roll', methods=['GET'])
def roll():
    num_dice = int(request.args.get('num_dice', 1))
    difficulty = int(request.args.get('difficulty', 6))
    results = [random.randint(1, 10) for _ in range(num_dice)]
    successes = sum(1 for die in results if die >= difficulty)
    
    return jsonify({"results": results, "successes": successes, "difficulty": difficulty})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "WOD Dice Roller API is running!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)