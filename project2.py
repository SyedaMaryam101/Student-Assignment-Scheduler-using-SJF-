import datetime
import json
import os
from collections import defaultdict

# ✅ Define your custom file path in D drive
FILE_PATH = r"D:\4th Semester\Projects\assignments.json"

class Assignment:
    def __init__(self, name, duration, deadline, status="Not Started", start_time=None, end_time=None):
        self.name = name
        self.duration = duration
        self.deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d")
        self.status = status
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.name} | {self.duration}h | Deadline: {self.deadline.date()} | Status: {self.status}"

    def to_dict(self):
        return {
            "name": self.name,
            "duration": self.duration,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "status": self.status,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S")if self.start_time else None,
            "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else None,
        }

    @staticmethod
    def from_dict(data):
        return Assignment(
            name=data["name"],
            duration=data["duration"],
            deadline=data["deadline"],
            status=data.get("status", "Not Started"),
            start_time=datetime.datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S") if data["start_time"] else None,
            end_time=datetime.datetime.strptime(data["end_time"], "%Y-%m-%d %H:%M:%S") if data["end_time"] else None,
        )

class Scheduler:
    def __init__(self):
        self.assignments = []
        self.load_assignments()

    def save_assignments(self):
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        with open(FILE_PATH, "w") as f:
            json.dump([a.to_dict() for a in self.assignments], f, indent=4)
        print(f"\n💾 Assignments saved to: {FILE_PATH}")

    def load_assignments(self):
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "r") as f:
                data = json.load(f)
                self.assignments = [Assignment.from_dict(d) for d in data]
            print(f"\n📂 Loaded existing assignments from: {FILE_PATH}")
        else:
            print(f"\n📁 No existing file found at: {FILE_PATH} (starting fresh)")

    def add_assignment(self, name, duration, deadline):
        assignment = Assignment(name, duration, deadline)
        self.assignments.append(assignment)
        self.save_assignments()

    def sort_by_sjf(self):
        self.assignments.sort(key=lambda x: x.duration)

    def show_assignments(self):
        self.sort_by_sjf()
        print("\n--- 📋 SJF Assignment List ---")
        for idx, a in enumerate(self.assignments, start=1):
            print(f"{idx}. {a}")

    def mark_complete(self, index):
        if 0 <= index < len(self.assignments):
            assignment = self.assignments[index]
            assignment.status = "Completed"
            assignment.end_time = datetime.datetime.now()
            self.save_assignments()
            print(f"✅ '{assignment.name}' marked as completed!")
        else:
            print("❌ Invalid assignment index.")

    def report(self):
        print("\n--- 📈 Completion Report ---")
        for a in self.assignments:
            if a.status == "Completed":
                actual_time = (a.end_time - a.deadline).days
                print(f"{a.name} | Completed On: {a.end_time.date()} | Deadline: {a.deadline.date()} | Days Difference: {actual_time}")
        print("Total Completed:", sum(1 for a in self.assignments if a.status == "Completed"))

    def show_weekly_calendar(self):
        print("\n📅 Weekly Assignment Calendar View:")
        week_map = defaultdict(list)
        for a in self.assignments:
            week_num = a.deadline.isocalendar()[1]
            week_map[week_num].append(a)

        for week in sorted(week_map.keys()):
            print(f"\n📆 Week {week}")
            for a in sorted(week_map[week], key=lambda x: x.deadline):
                print(f"  - {a.name} | Due: {a.deadline.strftime('%A, %Y-%m-%d')} | Status: {a.status}")

    def show_reminders(self):
        today = datetime.datetime.now().date()
        print("\n⏰ Reminders:")
        found = False
        for a in self.assignments:
            if a.status != "Completed":
                days_left = (a.deadline.date() - today).days
                if days_left == 0:
                    print(f"⚠️ TODAY: '{a.name}' is due today!")
                    found = True
                elif 0 < days_left <= 2:
                    print(f"📌 UPCOMING: '{a.name}' is due in {days_left} day(s).")
                    found = True
        if not found:
            print("🎉 No urgent deadlines today or in next 2 days.")

def main():
    scheduler = Scheduler()

    while True:
        print("\n📚 Student Assignment Scheduler (SJF)")
        print("1. Add Assignment(s)")
        print("2. Show Assignments (SJF Order)")
        print("3. Mark Assignment as Completed")
        print("4. Show Completion Report")
        print("5. Show Weekly Calendar View")
        print("6. Show Deadline Reminders")
        print("7. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            try:
                count = int(input("How many assignments do you want to add? "))
                for i in range(count):
                    print(f"\nAssignment {i + 1}:")
                    name = input("  Name: ")
                    duration = float(input("  Estimated Duration (in hours): "))
                    deadline = input("  Deadline (YYYY-MM-DD): ")
                    scheduler.add_assignment(name, duration, deadline)
                print(f"\n✅ {count} assignment(s) added successfully!")
            except ValueError:
                print("❌ Invalid input. Please enter a valid number.")

        elif choice == '2':
            scheduler.show_assignments()

        elif choice == '3':
            scheduler.show_assignments()
            try:
                idx = int(input("Enter assignment number to mark as completed: ")) - 1
                scheduler.mark_complete(idx)
            except ValueError:
                print("❌ Please enter a valid number.")

        elif choice == '4':
            scheduler.report()

        elif choice == '5':
            scheduler.show_weekly_calendar()

        elif choice == '6':
            scheduler.show_reminders()

        elif choice == '7':
            print("👋 Exiting. Stay on top of your deadlines!")
            break

        else:
            print("❗ Invalid option, try again.")

if __name__ == "__main__":
    main()