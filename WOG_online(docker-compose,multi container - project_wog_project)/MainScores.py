@app.route('/Scores')
def score_server():
    from sqlalchemy import create_engine, Column, Integer, String, func
    from sqlalchemy.orm import sessionmaker, declarative_base
    from alembic.config import Config
    from alembic import command
    from os import environ
    from flask import render_template

    # Alembic configuration file path (none, env.py in folder)
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location",
                                "/")
    command.upgrade(alembic_cfg, "head")

    # Initialize database engine
    engine = create_engine(f"mysql://{environ['USER_NAME']}:{environ['USER_PASSWORD']}@localhost/{environ['DB_NAME']}")

    # Declare database table
    class user_scores_table(declarative_base()):
        __tablename__ = environ['TABLE_NAME']
        id = Column(Integer, primary_key=True)
        username = Column(String)
        score = Column(Integer)
        timestamp = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Check if the value exists in the database, and update it or create it if it doesn't
    scores = session.query(user_scores_table).all
    render_template('score.html', scores)