import pandas as pd
from collections import Counter

data = pd.read_csv("webmd.csv")

age_groups = {
    "19-24": list(range(19, 25)),
    "25-34": list(range(25, 35)),
    "35-44": list(range(35, 45)),
    "13-18": list(range(13, 19)),
    "45-54": list(range(45, 55)),
    "55-64": list(range(55, 65)),
    "0-2": list(range(0, 3)),
    "7-12": list(range(7, 13))
}

def describe_age(age: int, gender: str, drug: str = None, condition: str = None):
    """Descriptive analysis based on user's age group, gender, drug, or condition."""

    # Determine user's age group
    group = [key for key, list_ in age_groups.items() if age in list_]
    age_group = group[0]

    # Filter dataset by age group
    filtered = data[data["Age"] == age_group]

    # Filter by gender
    if gender and gender != "<Choose One>":
        filtered = filtered[filtered["Sex"] == gender]

    # Filter by drug
    if drug and drug != "<Choose One>":
        filtered = filtered[filtered["Drug"] == drug]

    # Filter by condition
    if condition and condition != "<Choose One>":
        filtered = filtered[filtered["Condition"] == condition]

    # If no results left after filtering
    if filtered.empty:
        return {
            "age_group": age_group,
            "side_effects": [],
            "sorted_reviews": {
                "Reviews": [],
                "Drugs": [],
                "Conditions": []
            }
        }

    # Extract and clean side effects
    side_effects = []
    dirty_side_effects = filtered["Sides"].dropna().to_list()

    for item in dirty_side_effects:
        for word in item.split(","):
            side_effects.append(word.strip())

    # Count top side effects
    string_counter = Counter(side_effects)
    most_common_side_effects = string_counter.most_common(10)
    top_side_effects = [s for s, c in most_common_side_effects]

    # Get top 5 most useful reviews
    sorted_reviews = filtered.nlargest(5, 'UsefulCount')
    sorted_reviews = sorted_reviews[["Reviews", "Drug", "Condition"]].reset_index(drop=True)

    return {
        "age_group": age_group,
        "side_effects": top_side_effects,
        "sorted_reviews": {
            "Reviews": sorted_reviews["Reviews"].to_list(),
            "Drugs": sorted_reviews["Drug"].to_list(),
            "Conditions": sorted_reviews["Condition"].to_list()
        }
    }