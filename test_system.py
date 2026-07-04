"""
Quick test script for PawPal+ system.
Run this to verify your implementation works.
"""

from datetime import datetime, timedelta
from pawpal_system import (
    Owner, Pet, Task, Medication, Appointment, Scheduler,
    TaskType, Priority, Status
)

def test_pawpal_system():
    """Test the main functionality of PawPal+."""
    
    print("=" * 50)
    print("🧪 Testing PawPal+ System")
    print("=" * 50)
    
    # 1. Create an owner
    print("\n📝 Creating owner...")
    owner = Owner(name="John Doe", email="john@example.com", phone="555-0123")
    print(f"✅ Owner created: {owner}")
    
    # 2. Create pets
    print("\n🐾 Creating pets...")
    pet1 = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=36, weight=30.5)
    pet2 = Pet(name="Whiskers", species="Cat", breed="Siamese", age=24, weight=4.2)
    
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    print(f"✅ Pets added: {pet1}, {pet2}")
    
    # 3. Create tasks
    print("\n📋 Creating tasks...")
    
    # Feeding task
    feed_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    feed_task = Task(
        description="Feed Buddy breakfast",
        scheduled_time=feed_time,
        task_type=TaskType.FEEDING,
        priority=Priority.MEDIUM,
        recurring=True,
        recurrence_pattern="daily"
    )
    pet1.add_task(feed_task)
    
    # Walk task
    walk_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    walk_task = Task(
        description="Walk Buddy",
        scheduled_time=walk_time,
        task_type=TaskType.WALKING,
        priority=Priority.MEDIUM,
        recurring=True,
        recurrence_pattern="daily"
    )
    pet1.add_task(walk_task)
    
    # Medication task
    med_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    med_task = Medication(
        description="Give Buddy heartworm medication",
        scheduled_time=med_time,
        medication_name="Heartgard",
        dosage="1 tablet",
        frequency="monthly",
        administration_method="oral"
    )
    pet1.add_task(med_task)
    
    # Appointment task
    appt_time = datetime.now().replace(hour=14, minute=0, second=0, microsecond=0) + timedelta(days=2)
    appt_task = Appointment(
        description="Vet checkup for Buddy",
        scheduled_time=appt_time,
        vet_name="Dr. Smith",
        vet_phone="555-0456",
        clinic_address="123 Pet Lane, Animal City",
        reason="Annual checkup",
        preparation_notes="Bring vaccination records"
    )
    pet1.add_task(appt_task)
    
    print(f"✅ Tasks created: {len(pet1.get_tasks())} tasks for Buddy")
    
    # 4. Test scheduler
    print("\n⏰ Testing scheduler...")
    scheduler = Scheduler()
    for task in pet1.get_tasks():
        scheduler.add_task(task)
    
    # Get today's tasks
    today_tasks = scheduler.get_tasks_for_today()
    print(f"✅ Today's tasks: {len(today_tasks)}")
    
    # Check for conflicts
    conflicts = scheduler.detect_conflicts()
    print(f"✅ Conflicts detected: {len(conflicts)}")
    
    # Calculate priority
    for task in today_tasks:
        calculated = task.calculate_priority()
        print(f"   - {task.description[:30]}... Priority: {calculated.value}")
    
    # 5. Test daily summary
    print("\n📊 Daily summary:")
    summary = scheduler.calculate_daily_summary()
    print(f"   Total tasks: {summary['total_tasks']}")
    print(f"   By type: {summary['by_type']}")
    print(f"   By priority: {summary['by_priority']}")
    
    # 6. Test recurring task generation
    print("\n🔄 Testing recurring tasks...")
    next_task = feed_task.generate_next_occurrence()
    if next_task:
        print(f"✅ Next feeding: {next_task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
    
    # 7. Test task completion
    print("\n✅ Testing task completion...")
    if today_tasks:
        task_to_complete = today_tasks[0]
        task_to_complete.mark_complete()
        print(f"✅ Completed: {task_to_complete.description[:30]}...")
        print(f"   Status: {task_to_complete.status.value}")
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    test_pawpal_system()