from time import sleep

from celery import shared_task


@shared_task(queue='default')
def long_time_task(loop_number: int):
    for n in range(loop_number):
        print(f'número: {n}')
        sleep(1)


@shared_task(queue='periodic')
def schedule_task():
    print('executou a tarefa agendada')
