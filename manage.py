from app import create_app, db
from app.seed import run_seed
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)


@app.cli.command("seed")
def seed():
    """Popula dados iniciais"""
    run_seed()


if __name__ == "__main__":
    app.run(debug=True)
