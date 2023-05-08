from datetime import datetime
from sqlalchemy.orm import Session
from apps.stopwatch.stopwatch_database import (
    Projekte,
    Stopwatches,
    Entrys,
    Session,
)

# List of project names inspired by Elon Musk's ideas
project_names = [
    "Tesla Model S",
    "Falcon Heavy",
    "Hyperloop",
    "Starship",
    "Neuralink",
    "The Boring Company",
    "Mars Colony",
    "SolarCity",
    "PayPal",
    "Zip2",
    "X.com",
    "GigaFactory",
    "Dragon",
    "Mars Pathfinder",
    "Jupiter",
    "Interplanetary Transport System",
    "Mars Ascent Vehicle",
    "Cybertruck",
    "Roadster",
    "Semi",
    "Model X",
    "Model Y",
    "Model 3",
    "Starlink",
    "Big Falcon Rocket",
]

# Create a session
session = Session()

# Loop through the project names and add them to the database
for name in project_names:
    project = Projekte(name=name, description=f"Project inspired by {name}")
    session.add(project)

# Commit the changes to the database
session.commit()

# Close the session
session.close()
