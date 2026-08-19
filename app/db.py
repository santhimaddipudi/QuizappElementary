import sqlite3
from pathlib import Path

import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    schema_path = Path(current_app.root_path) / "schema.sql"
    with schema_path.open("r", encoding="utf-8") as f:
        db.executescript(f.read())


@click.command("init-db")
@click.option("--seed/--no-seed", default=True, help="Load starter TEKS-aligned questions after creating tables.")
def init_db_command(seed):
    """Create fresh tables, wiping any existing data, and optionally seed starter questions."""
    init_db()
    click.echo("Initialized the database.")
    if seed:
        from app.seed_data import seed_database
        seed_database(get_db())
        click.echo("Seeded starter questions.")


@click.command("seed-db")
def seed_db_command():
    """Load starter TEKS-aligned questions without wiping existing tables/data."""
    from app.seed_data import seed_database
    seed_database(get_db())
    click.echo("Seeded starter questions.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
