from taskiq.cli.worker.run import run_worker

from app.core.lifespan import broker


if __name__ == '__main__':
    # taskiq worker app.core.lifespan:broker --fs-discover --tasks-pattern="app/backend/routs.py"
    run_worker(broker)
