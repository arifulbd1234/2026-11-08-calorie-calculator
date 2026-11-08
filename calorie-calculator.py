# Day 33 - Calorie Calculator (2026-11-08)
# What it does: estimates your daily calorie needs (BMR + activity level)
# and splits them into protein, carbs and fat targets.
# Useful for: anyone who wants to eat right - lose weight, gain weight,
# or just maintain a healthy diet without guessing portions.

def calculate_bmr(weight_kg, height_cm, age, gender):
    """Mifflin-St Jeor equation - the most widely used BMR formula."""
    gender = gender.strip().lower()
    if gender in ("male", "m", "purush"):
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    if gender in ("female", "f", "mohila"):
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    raise ValueError("Gender must be 'male' or 'female'.")


ACTIVITY = {
    "sedentary": (1.2, "Little or no exercise, desk job"),
    "light": (1.375, "Light exercise 1-3 days a week"),
    "moderate": (1.55, "Moderate exercise 3-5 days a week"),
    "active": (1.725, "Hard exercise 6-7 days a week"),
    "athlete": (1.9, "Very hard exercise, physical job or training twice a day"),
}


def daily_calories(weight_kg, height_cm, age, gender, activity="moderate"):
    """Return (bmr, maintenance calories) for the given person."""
    if weight_kg <= 0 or height_cm <= 0 or age <= 0:
        raise ValueError("Weight, height and age must be positive numbers.")
    key = activity.strip().lower()
    if key not in ACTIVITY:
        raise ValueError(f"Activity must be one of: {', '.join(ACTIVITY)}")
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)
    return round(bmr), round(bmr * ACTIVITY[key][0])


def calorie_goal(maintenance, goal="maintain"):
    """Adjust maintenance calories for a weight goal."""
    goal = goal.strip().lower()
    if goal == "lose":
        return maintenance - 500, "lose about 0.5 kg per week"
    if goal == "gain":
        return maintenance + 300, "gain weight slowly and healthily"
    if goal == "maintain":
        return maintenance, "stay at your current weight"
    raise ValueError("Goal must be 'lose', 'maintain' or 'gain'.")


def macro_split(calories):
    """Split calories into protein / carbs / fat (grams per day)."""
    protein_g = round(calories * 0.30 / 4)   # 30% protein, 4 kcal per gram
    carbs_g = round(calories * 0.40 / 4)     # 40% carbs, 4 kcal per gram
    fat_g = round(calories * 0.30 / 9)       # 30% fat, 9 kcal per gram
    return {"protein_g": protein_g, "carbs_g": carbs_g, "fat_g": fat_g}


def calorie_plan(weight_kg, height_cm, age, gender,
                 activity="moderate", goal="maintain"):
    """Full plan: BMR, daily calories for the goal, and macro targets."""
    bmr, maintenance = daily_calories(weight_kg, height_cm, age,
                                      gender, activity)
    target, note = calorie_goal(maintenance, goal)
    plan = {
        "bmr": bmr,
        "maintenance_calories": maintenance,
        "goal": goal,
        "target_calories": target,
        "note": note,
    }
    plan.update(macro_split(target))
    return plan


def show_plan(weight_kg, height_cm, age, gender,
              activity="moderate", goal="maintain"):
    """Print a readable daily calorie plan."""
    plan = calorie_plan(weight_kg, height_cm, age, gender, activity, goal)
    print(f"BMR (resting burn): {plan['bmr']} kcal/day")
    print(f"Maintenance calories: {plan['maintenance_calories']} kcal/day")
    print(f"Goal ({goal}): {plan['target_calories']} kcal/day "
          f"- {plan['note']}")
    print("Daily macros:")
    print(f"  Protein: {plan['protein_g']} g")
    print(f"  Carbs:   {plan['carbs_g']} g")
    print(f"  Fat:     {plan['fat_g']} g")


if __name__ == "__main__":
    # Example 1: office worker who wants to lose a little weight
    print("Example 1 - 30-year-old man, 75 kg, 175 cm, sedentary, lose weight:")
    show_plan(75, 175, 30, "male", "sedentary", "lose")
    print()
    # Example 2: active woman maintaining her weight
    print("Example 2 - 25-year-old woman, 60 kg, 165 cm, moderate, maintain:")
    show_plan(60, 165, 25, "female", "moderate", "maintain")
    print()
    # Example 3: young man training hard and gaining muscle
    print("Example 3 - 22-year-old man, 68 kg, 178 cm, active, gain:")
    show_plan(68, 178, 22, "male", "active", "gain")
