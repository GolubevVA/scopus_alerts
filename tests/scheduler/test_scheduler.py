import asyncio
import pytest
from datetime import timedelta
from internal.scheduler.scheduler.scheduler import Scheduler
from tests.mocks import FakeSchedulerRepo as FakeRepo, FakeSchedulerJob as FakeJob, FIXED_TIME_FOR_SCHEDULER_NOW

@pytest.mark.asyncio
async def test_run_once_not_yet_due(freeze_scheduler_time):
    """
    If current time is before next_run_time, work should not be called
    and timestamp should remain unchanged.
    """
    fake_future = FIXED_TIME_FOR_SCHEDULER_NOW + timedelta(days=1)
    repo = FakeRepo(initial=None)
    job = FakeJob()
    sched = Scheduler(
        repository=repo,
        job=job,
        scheduling_interval=timedelta(days=7),
        first_run_time=fake_future
    )
    await sched._run_once()
    assert job.calls == []
    assert repo.get_timestamp() is None
    assert sched.next_run_time == fake_future

@pytest.mark.asyncio
async def test_run_once_due_and_updates(freeze_scheduler_time):
    """
    If current time >= next_run_time, work should be called,
    timestamp set, and next_run_time advanced by interval.
    """
    FIXED = FIXED_TIME_FOR_SCHEDULER_NOW
    repo = FakeRepo(initial=None)
    job = FakeJob()
    interval = timedelta(days=7)
    sched = Scheduler(repository=repo, job=job, scheduling_interval=interval)
    await sched._run_once()

    assert len(job.calls) == 1
    last_run, current_run = job.calls[0]
    assert last_run == FIXED - interval
    assert current_run == FIXED

    assert repo.get_timestamp() == FIXED
    assert sched.next_run_time == FIXED + interval

@pytest.mark.asyncio
async def test_run_and_stop_loop():
	"""
    Scheduler.run should execute one job and then await stop() to exit.
    """
	repo = FakeRepo(initial=None)
	job = FakeJob()
	interval = timedelta(seconds=1)
	sched = Scheduler(repository=repo, job=job, scheduling_interval=interval)

	task = asyncio.create_task(sched.run())
    
	await asyncio.sleep(0.1)
	assert len(job.calls) == 1

	await asyncio.sleep(1)
	assert len(job.calls) == 2

	await sched.stop()
	await task
    
	await asyncio.sleep(1)

	assert len(job.calls) == 2
