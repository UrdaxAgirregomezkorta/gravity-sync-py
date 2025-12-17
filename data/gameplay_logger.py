import csv
import time
import os

class GameplayLogger:
    def __init__(self, filename="data/gameplay_data.csv"):
        self.filename = filename
        self.start_time = time.time()
        self.deaths = 0

        # cria pasta se não existir
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # cria ficheiro com header se não existir
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "level",
                    "time_played_sec",
                    "diamonds_collected",
                    "total_diamonds",
                    "deaths",
                    "result"
                ])

    def register_death(self):
        self.deaths += 1

    def save_run(self, level, collected, total, result):
        end_time = time.time()
        elapsed = round(end_time - self.start_time, 2)

        with open(self.filename, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                level,
                elapsed,
                collected,
                total,
                self.deaths,
                result
            ])
