"""
PawPal+ - Smart Pet Care Management System
A modular system for managing pets, tasks, and scheduling.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Tuple
from enum import Enum
import uuid


class TaskType(Enum):
    """Enumeration of possible task types."""
    FEEDING = "feeding"
    WALKING = "walking"
    MEDICATION = "medication"
    APPOINTMENT = "appointment"
    GROOMING = "grooming"


class Priority(Enum):
    """Enumeration of priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Status(Enum):
    """Enumeration of task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class Owner:
    """Represents a pet owner/user of the system."""
    
    def __init__(self, name: str, email: str, phone: str = "", address: str = ""):
        self.owner_id = str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.pets: List['Pet'] = []
    
    def add_pet(self, pet: 'Pet') -> None:
        """Add a new pet to the owner's account."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner_id = self.owner_id
    
    def remove_pet(self, pet_id: str) -> bool:
        """Remove a pet from the owner's account."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                self.pets.remove(pet)
                return True
        return False
    
    def get_pets(self) -> List['Pet']:
        """Return list of all pets."""
        return self.pets
    
    def get_upcoming_tasks(self) -> List['Task']:
        """Get all upcoming tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def update_profile(self, name: str = None, email: str = None, 
                      phone: str = None, address: str = None) -> None:
        """Update owner information."""
        if name:
            self.name = name
        if email:
            self.email = email
        if phone:
            self.phone = phone
        if address:
            self.address = address
    
    def __str__(self):
        return f"Owner({self.name}, {self.email}, {len(self.pets)} pets)"


class Pet:
    """Represents an individual pet with its characteristics."""
    
    def __init__(self, name: str, species: str, breed: str = "", 
                 age: int = 0, weight: float = 0.0, special_needs: str = ""):
        self.pet_id = str(uuid.uuid4())[:8]
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age  # in months
        self.weight = weight  # in kg
        self.special_needs = special_needs
        self.owner_id: Optional[str] = None
        self.tasks: List['Task'] = []
        self.medical_conditions: List[str] = []
    
    def add_task(self, task: 'Task') -> None:
        """Schedule a new task for the pet."""
        self.tasks.append(task)
        task.pet_id = self.pet_id
    
    def get_tasks(self) -> List['Task']:
        """Return all tasks for this pet."""
        return self.tasks
    
    def get_tasks_by_type(self, task_type: TaskType) -> List['Task']:
        """Filter tasks by type."""
        return [t for t in self.tasks if t.task_type == task_type]
    
    def get_tasks_by_date(self, date: datetime) -> List['Task']:
        """Get tasks for a specific date."""
        return [t for t in self.tasks if t.scheduled_time.date() == date.date()]
    
    def update_medical_info(self, condition: str) -> None:
        """Add a medical condition."""
        if condition not in self.medical_conditions:
            self.medical_conditions.append(condition)
    
    def __str__(self):
        return f"Pet({self.name}, {self.species}, {len(self.tasks)} tasks)"


class Task:
    """Base class for all schedulable activities."""
    
    def __init__(self, description: str, scheduled_time: datetime,
                 task_type: TaskType, priority: Priority = Priority.MEDIUM,
                 recurring: bool = False, recurrence_pattern: str = ""):
        self.task_id = str(uuid.uuid4())[:8]
        self.pet_id: Optional[str] = None
        self.task_type = task_type
        self.description = description
        self.scheduled_time = scheduled_time
        self.priority = priority
        self.status = Status.PENDING
        self.recurring = recurring
        self.recurrence_pattern = recurrence_pattern
        self.completed_at: Optional[datetime] = None
        self.notes: str = ""
    
    def mark_complete(self) -> None:
        """Mark task as completed."""
        self.status = Status.COMPLETED
        self.completed_at = datetime.now()
    
    def mark_in_progress(self) -> None:
        """Update status to in-progress."""
        self.status = Status.IN_PROGRESS
    
    def reschedule(self, new_time: datetime) -> None:
        """Change scheduled time."""
        self.scheduled_time = new_time
        self.status = Status.PENDING
    
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.status == Status.COMPLETED:
            return False
        return datetime.now() > self.scheduled_time
    
    def calculate_priority(self) -> Priority:
        """
        Calculate priority based on urgency and task type.
        Higher priority for time-sensitive tasks and health-related tasks.
        """
        now = datetime.now()
        time_delta = self.scheduled_time - now
        
        # Health-related tasks get higher priority
        health_tasks = [TaskType.MEDICATION, TaskType.APPOINTMENT]
        
        if self.task_type in health_tasks:
            if time_delta.total_seconds() < 3600:  # Within 1 hour
                return Priority.HIGH
            elif time_delta.total_seconds() < 86400:  # Within 24 hours
                return Priority.HIGH
            else:
                return Priority.MEDIUM
        
        # Non-health tasks
        if time_delta.total_seconds() < 3600:
            return Priority.HIGH
        elif time_delta.total_seconds() < 86400:
            return Priority.MEDIUM
        else:
            return Priority.LOW
    
    def generate_next_occurrence(self) -> Optional['Task']:
        """Generate the next occurrence for recurring tasks."""
        if not self.recurring or not self.recurrence_pattern:
            return None
        
        next_time = None
        if self.recurrence_pattern == "daily":
            next_time = self.scheduled_time + timedelta(days=1)
        elif self.recurrence_pattern == "weekly":
            next_time = self.scheduled_time + timedelta(weeks=1)
        elif self.recurrence_pattern == "monthly":
            # Simple monthly - add 30 days
            next_time = self.scheduled_time + timedelta(days=30)
        else:
            return None
        
        # Create new task with same properties
        new_task = Task(
            description=self.description,
            scheduled_time=next_time,
            task_type=self.task_type,
            priority=self.priority,
            recurring=self.recurring,
            recurrence_pattern=self.recurrence_pattern
        )
        new_task.notes = self.notes
        new_task.pet_id = self.pet_id
        return new_task
    
    def __str__(self):
        return f"Task({self.task_type.value}: {self.description[:30]}..., {self.priority.value})"


class Medication(Task):
    """Task subclass for medication administration."""
    
    def __init__(self, description: str, scheduled_time: datetime,
                 medication_name: str, dosage: str, frequency: str,
                 administration_method: str, priority: Priority = Priority.HIGH,
                 recurring: bool = True, refill_reminder: bool = True):
        super().__init__(
            description=description,
            scheduled_time=scheduled_time,
            task_type=TaskType.MEDICATION,
            priority=priority,
            recurring=recurring,
            recurrence_pattern=frequency
        )
        self.medication_name = medication_name
        self.dosage = dosage
        self.frequency = frequency
        self.administration_method = administration_method
        self.refill_reminder = refill_reminder
        self.last_administered: Optional[datetime] = None
    
    def check_refill_needed(self) -> bool:
        """Check if medication needs refilling."""
        # Simple check - would be more sophisticated with actual inventory
        return self.refill_reminder
    
    def record_administration(self) -> None:
        """Log when medication was given."""
        self.last_administered = datetime.now()
        self.mark_complete()
    
    def __str__(self):
        return f"Medication({self.medication_name}, {self.dosage}, {self.frequency})"


class Appointment(Task):
    """Task subclass for veterinary appointments."""
    
    def __init__(self, description: str, scheduled_time: datetime,
                 vet_name: str, vet_phone: str, clinic_address: str,
                 reason: str, preparation_notes: str = "",
                 priority: Priority = Priority.MEDIUM):
        super().__init__(
            description=description,
            scheduled_time=scheduled_time,
            task_type=TaskType.APPOINTMENT,
            priority=priority,
            recurring=False,
            recurrence_pattern=""
        )
        self.vet_name = vet_name
        self.vet_phone = vet_phone
        self.clinic_address = clinic_address
        self.reason = reason
        self.preparation_notes = preparation_notes
    
    def add_preparation_task(self) -> List[Task]:
        """Generate preparation tasks for appointment."""
        prep_tasks = []
        
        # Reminder 24 hours before
        reminder_time = self.scheduled_time - timedelta(days=1)
        reminder = Task(
            description=f"Reminder: {self.description} tomorrow",
            scheduled_time=reminder_time,
            task_type=TaskType.APPOINTMENT,
            priority=Priority.MEDIUM
        )
        prep_tasks.append(reminder)
        
        # Travel prep 2 hours before
        travel_time = self.scheduled_time - timedelta(hours=2)
        travel = Task(
            description=f"Prepare for {self.description} - leave for clinic",
            scheduled_time=travel_time,
            task_type=TaskType.APPOINTMENT,
            priority=Priority.MEDIUM
        )
        prep_tasks.append(travel)
        
        return prep_tasks
    
    def get_directions(self) -> str:
        """Get clinic address/directions."""
        return f"Clinic: {self.vet_name}\nAddress: {self.clinic_address}\nPhone: {self.vet_phone}"
    
    def __str__(self):
        return f"Appointment({self.vet_name}, {self.reason})"


class Scheduler:
    """Manages task scheduling, sorting, and conflict detection."""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.conflicts: List[Tuple[Task, Task]] = []
    
    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        self.tasks.append(task)
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a task from the scheduler."""
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                return True
        return False
    
    def sort_tasks_by_priority(self) -> List[Task]:
        """Sort all tasks by priority (HIGH > MEDIUM > LOW)."""
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        return sorted(self.tasks, key=lambda t: priority_order.get(t.priority, 1))
    
    def sort_tasks_by_time(self) -> List[Task]:
        """Sort tasks chronologically."""
        return sorted(self.tasks, key=lambda t: t.scheduled_time)
    
    def sort_tasks_by_priority_and_time(self) -> List[Task]:
        """Sort by priority first, then by time."""
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        return sorted(self.tasks, key=lambda t: (priority_order.get(t.priority, 1), t.scheduled_time))
    
    def detect_conflicts(self) -> List[Tuple[Task, Task]]:
        """Identify scheduling conflicts (overlapping tasks)."""
        self.conflicts = []
        sorted_tasks = self.sort_tasks_by_time()
        
        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                task1 = sorted_tasks[i]
                task2 = sorted_tasks[j]
                
                # Check if tasks overlap (within 30 minutes)
                time1 = task1.scheduled_time
                time2 = task2.scheduled_time
                
                if abs((time1 - time2).total_seconds()) < 1800:  # 30 minutes
                    self.conflicts.append((task1, task2))
        
        return self.conflicts
    
    def resolve_conflicts(self) -> List[Task]:
        """Suggest resolutions for conflicts by prioritizing."""
        conflicts = self.detect_conflicts()
        resolved_tasks = []
        
        for task1, task2 in conflicts:
            # Keep higher priority task, postpone the other
            if task1.priority.value == task2.priority.value:
                # If same priority, keep the earlier one
                if task1.scheduled_time < task2.scheduled_time:
                    resolved_tasks.append(task1)
                    task2.reschedule(task2.scheduled_time + timedelta(hours=1))
                    resolved_tasks.append(task2)
                else:
                    resolved_tasks.append(task2)
                    task1.reschedule(task1.scheduled_time + timedelta(hours=1))
                    resolved_tasks.append(task1)
            elif task1.priority == Priority.HIGH or task2.priority == Priority.LOW:
                resolved_tasks.append(task1)
                task2.reschedule(task2.scheduled_time + timedelta(hours=1))
                resolved_tasks.append(task2)
            else:
                resolved_tasks.append(task2)
                task1.reschedule(task1.scheduled_time + timedelta(hours=1))
                resolved_tasks.append(task1)
        
        return resolved_tasks
    
    def get_tasks_for_today(self) -> List[Task]:
        """Return today's tasks sorted by priority."""
        today = datetime.now().date()
        today_tasks = [t for t in self.tasks if t.scheduled_time.date() == today]
        return sorted(today_tasks, key=lambda t: t.calculate_priority().value)
    
    def get_tasks_for_date(self, date: datetime) -> List[Task]:
        """Return tasks for specific date."""
        tasks = [t for t in self.tasks if t.scheduled_time.date() == date.date()]
        return sorted(tasks, key=lambda t: t.scheduled_time)
    
    def calculate_daily_summary(self) -> Dict:
        """Generate summary of today's activities."""
        today_tasks = self.get_tasks_for_today()
        
        summary = {
            "total_tasks": len(today_tasks),
            "by_type": {},
            "by_priority": {},
            "overdue": 0,
            "completed": 0,
            "pending": 0
        }
        
        for task in today_tasks:
            # Count by type
            type_key = task.task_type.value
            summary["by_type"][type_key] = summary["by_type"].get(type_key, 0) + 1
            
            # Count by priority
            priority_key = task.priority.value
            summary["by_priority"][priority_key] = summary["by_priority"].get(priority_key, 0) + 1
            
            # Count status
            if task.status == Status.OVERDUE or task.is_overdue():
                summary["overdue"] += 1
            elif task.status == Status.COMPLETED:
                summary["completed"] += 1
            elif task.status == Status.PENDING:
                summary["pending"] += 1
        
        return summary
    
    def suggest_optimal_schedule(self) -> List[Task]:
        """Suggest optimal order for tasks."""
        tasks = self.get_tasks_for_today()
        
        # Sort by priority (health tasks first) then time
        return sorted(tasks, key=lambda t: 
                     (0 if t.calculate_priority() == Priority.HIGH else 1,
                      t.scheduled_time))
    
    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks."""
        return [t for t in self.tasks if t.is_overdue() and t.status != Status.COMPLETED]
    
    def clear_completed_tasks(self) -> None:
        """Remove all completed tasks."""
        self.tasks = [t for t in self.tasks if t.status != Status.COMPLETED]
    
    def __str__(self):
        return f"Scheduler({len(self.tasks)} tasks, {len(self.conflicts)} conflicts)"