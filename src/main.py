from database.database import initialize_database
from ui.main_window import MainWindow


def main() -> None:

    initialize_database()

    app = MainWindow()

    app.run()


if __name__ == "__main__":
    main()