from taskiq.cli.worker.run import run_worker

from app.core.lifespan import broker


if __name__ == '__main__':
    run_worker(broker)
