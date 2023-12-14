from app.tasks.celery_app import celery_app


def start_celery_worker():
    argv = [
        "worker",
        "--loglevel=info",
    ]
    celery_app.worker_main(argv)


if __name__ == "__main__":
    start_celery_worker()
