from elife_app.domain.models import DailyEntry


class WellnessService:

    def calculate_score(self, entry: DailyEntry) -> tuple[int, list[str]]:
        score = (
            entry.sleep_quality +
            entry.mood +
            entry.friends * 10 +
            entry.exercise * 10 +
            entry.hobbies * 10 +
            entry.meds * 10 +
            min(entry.steps // 5000, 10) +
            min(int(entry.water_intake), 10) -
            entry.stress -
            max(0, int(entry.work_hours) - 8)
        )
        score = max(0, score)

        advice = []

        if entry.stress >= 7:
            advice.append("💪 Lower your stress bestie!")
        if entry.friends == 0:
            advice.append("🌿 Touch grass with friends!")
        if entry.water_intake < 1.5:
            advice.append("💧 Hydrate queen!")
        if entry.exercise == 0:
            advice.append("🏃 Move your body!")
        if entry.mood <= 3:
            advice.append("💖 Your mood needs attention!")
        if entry.steps < 5000:
            advice.append("👟 Walk more!")
        if entry.hobbies == 0:
            advice.append("🎨 Do something fun!")
        if entry.meds == 0:
            advice.append("💊 Don't forget your meds!")

        entry.score = score
        return score, advice

    def weekly_report(self, entries):
        if not entries:
            return "No data."

        last_7 = entries[-7:]
        avg = sum(e.score for e in last_7) / len(last_7)

        return f"📊 Weekly Average Score: {avg:.1f}"
