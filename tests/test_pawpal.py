"""
PawPal+ - Automated Test Suite
Tests for the PawPal+ pet care management system.
"""

import pytest
from datetime import datetime, timedelta
from pawpal_system import (
    Owner, Pet, Task, Medication, Appointment, Scheduler,
    TaskType, Priority, Status
)


class TestTask:
    """Tests for the Task class."""
    
    def test_task_creation(self):
        """Test that a task is created with correct attributes."""
        now = datetime.now()
        task = Task(
            description="Test task",
            scheduled_time=now,
            task_type=TaskType.FEEDING,
            priority=Priority.HIGH
        )
        assert task.description == "Test task"
        assert task.task_type == TaskType.FEEDING
        assert task.priority == Priority.HIGH
        assert task.status == Status.PENDING
    
    def test_task_completion(self):
        """Test that marking a task complete changes its status."""
        now = datetime.now()
        task = Task(
            description="Test task",
            scheduled_time=now,
            task_type=TaskType.FEEDING
        )
        assert task.status == Status.PENDING
        task.mark_complete()
        assert task.status == Status.COMPLETED
        assert task.completed_at is not None
    
    def test_task_overdue(self):
        """Test that overdue detection works."""
        past_time = datetime.now() - timedelta(hours=1)
        task = Task(
            description="Past task",
            scheduled_time=past_time,
            task_type=TaskType.FEEDING
        )
        assert task.is_overdue() == True
    
    def test_task_not_overdue(self):
        """Test that future tasks are not overdue."""
        future_time = datetime.now() + timedelta(hours=1)
        task = Task(
            description="Future task",
            scheduled_time=future_time,
            task_type=TaskType.FEEDING
        )
        assert task.is_overdue() == False


class TestPet:
    """Tests for the Pet class."""
    
    def test_pet_creation(self):
        """Test that a pet is created with correct attributes."""
        pet = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=36, weight=30.5)
        assert pet.name == "Buddy"
        assert pet.species == "Dog"
        assert pet.breed == "Golden Retriever"
        assert pet.age == 36
        assert pet.weight == 30.5
    
    def test_add_task_to_pet(self):
        """Test that adding a task increases task count."""
        pet = Pet(name="Buddy", species="Dog")
        assert len(pet.get_tasks()) == 0
        
        now = datetime.now()
        task = Task(
            description="Test task",
            scheduled_time=now,
            task_type=TaskType.FEEDING
        )
        pet.add_task(task)
        assert len(pet.get_tasks()) == 1


class TestScheduler:
    """Tests for the Scheduler class."""
    
    def test_add_task_to_scheduler(self):
        """Test that tasks can be added to scheduler."""
        scheduler = Scheduler()
        assert len(scheduler.tasks) == 0
        
        now = datetime.now()
        task = Task(
            description="Test task",
            scheduled_time=now,
            task_type=TaskType.FEEDING
        )
        scheduler.add_task(task)
        assert len(scheduler.tasks) == 1
    
    def test_sort_by_time(self):
        """Test that tasks are sorted chronologically."""
        scheduler = Scheduler()
        
        now = datetime.now()
        task1 = Task(
            description="Task 1",
            scheduled_time=now + timedelta(hours=2),
            task_type=TaskType.FEEDING
        )
        task2 = Task(
            description="Task 2",
            scheduled_time=now + timedelta(hours=1),
            task_type=TaskType.FEEDING
        )
        task3 = Task(
            description="Task 3",
            scheduled_time=now,
            task_type=TaskType.FEEDING
        )
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        scheduler.add_task(task3)
        
        sorted_tasks = scheduler.sort_tasks_by_time()
        assert sorted_tasks[0] == task3
        assert sorted_tasks[1] == task2
        assert sorted_tasks[2] == task1
    
    def test_conflict_detection(self):
        """Test that conflicts are detected correctly."""
        scheduler = Scheduler()
        
        now = datetime.now()
        task1 = Task(
            description="Task 1",
            scheduled_time=now,
            task_type=TaskType.FEEDING
        )
        task2 = Task(
            description="Task 2",
            scheduled_time=now + timedelta(minutes=15),
            task_type=TaskType.WALKING
        )
        task3 = Task(
            description="Task 3",
            scheduled_time=now + timedelta(hours=2),
            task_type=TaskType.GROOMING
        )
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        scheduler.add_task(task3)
        
        conflicts = scheduler.detect_conflicts()
        # Tasks 1 and 2 are within 30 minutes, so they conflict
        assert len(conflicts) > 0
    
    def test_no_conflict(self):
        """Test that distant tasks don't conflict."""
        scheduler = Scheduler()
        
        now = datetime.now()
        task1 = Task(
            description="Task 1",
            scheduled_time=now,
            task_type=TaskType.FEEDING
        )
        task2 = Task(
            description="Task 2",
            scheduled_time=now + timedelta(hours=2),
            task_type=TaskType.WALKING
        )
        
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        conflicts = scheduler.detect_conflicts()
        assert len(conflicts) == 0