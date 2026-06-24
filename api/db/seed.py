from datetime import date

from api.db.database import engine, SessionLocal, Base
from api.models.employee import Employee


def seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    if db.query(Employee).count() > 0:
        print("Database already has data. Skipping seed.")
        db.close()
        return

    employees = [
        Employee(name="Rohit Sharma", department="Engineering", role="Backend Engineer",
                 salary=95000, city="Mumbai", joined_on=date(2021, 3, 15)),
        Employee(name="Priya Nair", department="Engineering", role="DevOps Engineer",
                 salary=88000, city="Bangalore", joined_on=date(2020, 7, 1)),
        Employee(name="Arjun Mehta", department="Product", role="Product Manager",
                 salary=105000, city="Delhi", joined_on=date(2019, 11, 20)),
        Employee(name="Sneha Kulkarni", department="Design", role="UI/UX Designer",
                 salary=78000, city="Pune", joined_on=date(2022, 1, 10)),
        Employee(name="Vikram Iyer", department="Engineering", role="Frontend Engineer",
                 salary=82000, city="Chennai", joined_on=date(2021, 9, 5)),
        Employee(name="Meena Pillai", department="HR", role="HR Manager",
                 salary=72000, city="Hyderabad", joined_on=date(2018, 4, 22)),
        Employee(name="Aditya Joshi", department="Finance", role="Financial Analyst",
                 salary=91000, city="Mumbai", joined_on=date(2020, 2, 14)),
        Employee(name="Kavya Reddy", department="Engineering", role="Data Engineer",
                 salary=97000, city="Bangalore", joined_on=date(2022, 6, 30)),
    ]

    db.add_all(employees)
    db.commit()
    print(f"Seeded {len(employees)} employees into the database.")
    db.close()


if __name__ == "__main__":
    seed()
