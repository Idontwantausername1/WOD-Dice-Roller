import random
from colorama import init, Fore, Style
from flask import Flask, request, jsonify

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
SPLAT_FUNCTIONS = {
    "Mage": lambda: roll_generic(get_int_input("Enter Arete rating: "), get_int_input("Enter difficulty (3-9): "), "Arete"),
    "Changeling": lambda: roll_generic(get_int_input("Enter Banality rating: "), 6, "Banality"),
    "Wraith": [lambda: roll_generic(get_int_input("Enter Pathos rating: "), 6, "Pathos"), 
               lambda: roll_generic(get_int_input("Enter Angst rating: "), 6, "Angst")],
    "Demon": [lambda: roll_generic(get_int_input("Enter Faith rating: "), 6, "Faith"), 
              lambda: roll_generic(get_int_input("Enter Torment rating: "), 6, "Torment")],
    "Mummy": [lambda: roll_generic(get_int_input("Enter Balance rating: "), 6, "Balance"), 
              lambda: roll_generic(get_int_input("Enter Sekhem rating: "), 6, "Sekhem")],
    "Hunter": [lambda: roll_generic(get_int_input("Enter Desperation dice: "), 6, "Desperation"), 
               lambda: roll_generic(get_int_input("Enter Willpower rating: "), 6, "Willpower")],
    "Kindred of the East": [lambda: roll_generic(get_int_input("Enter Chi pool: "), 6, "Chi"), 
                            lambda: roll_generic(get_int_input("Enter Dharma rating: "), 6, "Dharma")],
    "Ghoul": lambda: roll_generic(get_int_input("Enter Willpower rating: "), 6, "Frenzy"),
    "Mortal": lambda: roll_generic(get_int_input("Enter total number of dice: "), get_int_input("Enter difficulty: "), "Attribute + Skill"),
}

# 🔹 Main Game Loop
def main():
    splat = get_splat_choice()

    while True:
        if splat in SPLAT_FUNCTIONS:
            function = SPLAT_FUNCTIONS[splat]
            if isinstance(function, list):  # Handle splats with multiple rolls
                print(f"\nAvailable Rolls: {', '.join(['Pathos', 'Angst'])}" if splat == "Wraith" else 
                      f"\nAvailable Rolls: {', '.join(['Faith', 'Torment'])}" if splat == "Demon" else 
                      f"\nAvailable Rolls: {', '.join(['Balance', 'Sekhem'])}")
                choice = get_int_input("Which roll do you want to perform? (1 or 2): ", 1) - 1
                function[choice]()  
            else:
                function()  
        else:
            roll_generic(get_int_input("Enter total number of dice: "), get_int_input("Enter difficulty: "), "Attribute + Skill")

        if get_yes_no_input("\nRoll again? (y/n): ") != 'y':
            break

if __name__ == "__main__":
    main()

# 🌎 Flask API Integration
app = Flask(__name__)

@app.route('/roll', methods=['GET'])
def roll():
    """API Endpoint for rolling dice."""
    try:
        num_dice = int(request.args.get('num_dice', 1))
        difficulty = int(request.args.get('difficulty', 6))
        results = [random.randint(1, 10) for _ in range(num_dice)]
        successes = sum(1 for die in results if die >= difficulty)
        return jsonify({"results": results, "successes": successes, "difficulty": difficulty})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "WOD Dice Roller API is running!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
