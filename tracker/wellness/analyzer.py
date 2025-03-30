class WellnessAnalyzer:
    def __init__(self, steps, sleep_hours, calories):
        self.steps = steps
        self.sleep_hours = sleep_hours
        self.calories = calories

    def activity_score(self):
        score = 0
        if self.steps >= 8000:
            score += 3
        elif self.steps >= 5000:
            score += 2
        else:
            score += 1

        if self.sleep_hours >= 7:
            score += 3
        elif self.sleep_hours >= 5:
            score += 2
        else:
            score += 1

        if 1800 <= self.calories <= 2500:
            score += 3
        else:
            score += 1

        return score

    def category(self):
        score = self.activity_score()
        if score >= 8:
            return "Excellent"
        elif score >= 6:
            return "Good"
        else:
            return "Needs Improvement"
