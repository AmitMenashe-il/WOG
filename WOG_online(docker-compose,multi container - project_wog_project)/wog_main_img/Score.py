# add game score after winning to scores db table

def add_score(name,score):
    from sqlalchemy import create_engine, Column, Integer, String, func
    from sqlalchemy.orm import sessionmaker, declarative_base
    from alembic.config import Config
    from alembic import command
    from os import environ

    # Alembic configuration file path (none, env.py in folder)
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location",
                                "/app")
    command.upgrade(alembic_cfg, "head")

    # Initialize database engine
    engine = create_engine(f"mysql://{environ['USER_NAME']}:{environ['USER_PASSWORD']}@DB/{environ['DB_NAME']}")

    # Declare database table
    class user_scores_table(declarative_base()):
        __tablename__ = environ['TABLE_NAME']
        id = Column(Integer, primary_key=True)
        username = Column(String)
        score = Column(Integer)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

        # Check if the value exists in the database, and update it or create it if it doesn't
    value = session.query(user_scores_table).filter_by(username=name).one_or_none()
    if value is None:
        id = (session.query(func.max(user_scores_table.id)).scalar() or 0) + 1
        value = user_scores_table(id=id, username=name, score=score)
        session.add(value)
    else:
        if score > value.score:
            value.score = score
    session.commit()
