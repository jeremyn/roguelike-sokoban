# Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import os
import sqlite3


class ScoreTracker(object):
    def __init__(self, db_file_name, level_file_name, level_name):
        self.file_name = os.path.basename(level_file_name)
        self.level_name = level_name

        self.conn = sqlite3.connect(db_file_name)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(
                """
                  CREATE TABLE scores (
                    file_name text,
                    level_name text,
                    score integer,
                    PRIMARY KEY (file_name, level_name)
                  )
                """
            )
        except sqlite3.OperationalError:
            # Database/table already exists
            pass

    def get_best_score(self):
        self.cursor.execute(
            """
              SELECT score
              FROM scores
              WHERE file_name=:file_name AND level_name=:level_name
            """,
            {
                "file_name": self.file_name,
                "level_name": self.level_name,
            },
        )
        try:
            best_score = self.cursor.fetchone()[0]
        except TypeError:
            best_score = None
        return best_score

    def update_best_score(self, score):
        args = {
            "file_name": self.file_name,
            "level_name": self.level_name,
            "score": score,
        }
        current_best_score = self.get_best_score()
        if current_best_score is None:
            self.cursor.execute(
                """
                  INSERT INTO scores
                  (file_name, level_name, score)
                  VALUES (:file_name, :level_name, :score)
                """,
                args,
            )
            self.conn.commit()
        else:
            if score < current_best_score:
                self.cursor.execute(
                    """
                      UPDATE scores
                      SET score=:score
                      WHERE file_name=:file_name AND level_name=:level_name
                    """,
                    args,
                )
                self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
