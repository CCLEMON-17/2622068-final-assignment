from database import init_db, save_repos
from scraper import scrape_google_repos
import sqlite3


def main():
  # Initialize database
  init_db()

  # Scrape data
  print("Scraping repositories...")
  data = scrape_google_repos()

  # Save to database
  if data:
    save_repos(data)
    print("Data saved successfully!")

  # Display data using SELECT query (Step 4)
  print("\n--- Displaying Saved Repositories ---")
  conn = sqlite3.connect("google_repos.db")
  cursor = conn.cursor()
  cursor.execute("SELECT repo_name, language, stars FROM repositories")
  for row in cursor.fetchall():
    print(f"Repo: {row[0]} | Language: {row[1]} | Stars: {row[2]}")
  conn.close()


if __name__ == "__main__":
  main()