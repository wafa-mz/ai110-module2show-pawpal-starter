"""
PawPal+ - Streamlit UI
A modern web interface for the PawPal+ pet care management system.
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

from pawpal_system import (
    Owner, Pet, Task, Medication, Appointment, Scheduler,
    TaskType, Priority, Status
)

# Page configuration
st.set_page_config(
    page_title="PawPal+ Pet Care",
    page_icon="🐾",
    layout="wide"
)

# Initialize session state
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="John Doe", email="john@example.com", phone="555-0123")

if 'scheduler' not in st.session_state:
    st.session_state.scheduler = Scheduler()

if 'pet_counter' not in st.session_state:
    st.session_state.pet_counter = 0

# Title
st.title("🐾 PawPal+ Smart Pet Care")
st.subheader("Keep your furry friends happy and healthy!")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose an option:",
    ["🏠 Dashboard", "🐕 Add Pet", "📋 Add Task", "📊 View Tasks", "⏰ Scheduler"]
)

# ============================================================================
# DASHBOARD
# ============================================================================
if page == "🏠 Dashboard":
    st.header("📊 Dashboard")
    
    owner = st.session_state.owner
    scheduler = st.session_state.scheduler
    
    # Show owner info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👤 Owner", owner.name)
    with col2:
        st.metric("🐾 Pets", len(owner.get_pets()))
    with col3:
        st.metric("📋 Today's Tasks", len(scheduler.get_tasks_for_today()))
    
    # Show pets
    st.subheader("Your Pets")
    pets = owner.get_pets()
    if pets:
        for pet in pets:
            with st.expander(f"🐕 {pet.name} ({pet.species})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Breed:** {pet.breed}")
                    st.write(f"**Age:** {pet.age} months")
                with col2:
                    st.write(f"**Weight:** {pet.weight} kg")
                    st.write(f"**Special Needs:** {pet.special_needs or 'None'}")
    else:
        st.info("No pets yet. Add a pet using the sidebar!")
    
    # Today's tasks
    st.subheader("📋 Today's Tasks")
    today_tasks = scheduler.get_tasks_for_today()
    if today_tasks:
        for task in today_tasks:
            priority_color = {
                "high": "🔴",
                "medium": "🟡",
                "low": "🟢"
            }.get(task.priority.value, "⚪")
            st.write(f"{priority_color} **{task.description}** - {task.scheduled_time.strftime('%H:%M')}")
    else:
        st.info("No tasks scheduled for today!")

# ============================================================================
# ADD PET
# ============================================================================
elif page == "🐕 Add Pet":
    st.header("🐕 Add a New Pet")
    
    with st.form("add_pet_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Pet Name*", placeholder="e.g., Buddy")
            species = st.text_input("Species*", placeholder="e.g., Dog, Cat")
            breed = st.text_input("Breed", placeholder="e.g., Golden Retriever")
        with col2:
            age = st.number_input("Age (months)", min_value=0, step=1)
            weight = st.number_input("Weight (kg)", min_value=0.0, step=0.5)
            special_needs = st.text_input("Special Needs", placeholder="e.g., allergies")
        
        submitted = st.form_submit_button("Add Pet")
        
        if submitted:
            if name and species:
                pet = Pet(
                    name=name,
                    species=species,
                    breed=breed,
                    age=age,
                    weight=weight,
                    special_needs=special_needs
                )
                st.session_state.owner.add_pet(pet)
                st.session_state.pet_counter += 1
                st.success(f"✅ {name} has been added to your family!")
            else:
                st.error("Please fill in at least Name and Species.")

# ============================================================================
# ADD TASK
# ============================================================================
elif page == "📋 Add Task":
    st.header("📋 Add a New Task")
    
    owner = st.session_state.owner
    pets = owner.get_pets()
    
    if not pets:
        st.warning("You need to add a pet first!")
        st.stop()
    
    with st.form("add_task_form"):
        col1, col2 = st.columns(2)
        with col1:
            pet_names = [pet.name for pet in pets]
            selected_pet_name = st.selectbox("Select Pet", pet_names)
            selected_pet = next(p for p in pets if p.name == selected_pet_name)
            
            task_type = st.selectbox(
                "Task Type",
                ["feeding", "walking", "medication", "appointment", "grooming"]
            )
            description = st.text_input("Task Description*")
        
        with col2:
            task_date = st.date_input("Date", datetime.now())
            task_time = st.time_input("Time", datetime.now().time())
            scheduled_time = datetime.combine(task_date, task_time)
            
            priority = st.selectbox("Priority", ["high", "medium", "low"])
            priority_map = {"high": Priority.HIGH, "medium": Priority.MEDIUM, "low": Priority.LOW}
            
            recurring = st.checkbox("Recurring Task")
            recurrence_pattern = ""
            if recurring:
                recurrence_pattern = st.selectbox("Frequency", ["daily", "weekly", "monthly"])
        
        # Medication specific fields
        if task_type == "medication":
            st.subheader("💊 Medication Details")
            col1, col2 = st.columns(2)
            with col1:
                medication_name = st.text_input("Medication Name")
                dosage = st.text_input("Dosage")
            with col2:
                frequency = st.text_input("Frequency", placeholder="e.g., daily")
                admin_method = st.selectbox("Administration Method", ["oral", "injection", "topical", "other"])
        else:
            medication_name = dosage = frequency = admin_method = ""
        
        # Appointment specific fields
        if task_type == "appointment":
            st.subheader("🏥 Appointment Details")
            col1, col2 = st.columns(2)
            with col1:
                vet_name = st.text_input("Vet Name")
                vet_phone = st.text_input("Vet Phone")
            with col2:
                clinic_address = st.text_input("Clinic Address")
                reason = st.text_input("Reason for Visit")
            prep_notes = st.text_area("Preparation Notes")
        else:
            vet_name = vet_phone = clinic_address = reason = prep_notes = ""
        
        submitted = st.form_submit_button("Add Task")
        
        if submitted:
            if description:
                if task_type == "medication":
                    task = Medication(
                        description=description,
                        scheduled_time=scheduled_time,
                        medication_name=medication_name,
                        dosage=dosage,
                        frequency=frequency,
                        administration_method=admin_method,
                        priority=priority_map[priority],
                        recurring=recurring
                    )
                elif task_type == "appointment":
                    task = Appointment(
                        description=description,
                        scheduled_time=scheduled_time,
                        vet_name=vet_name,
                        vet_phone=vet_phone,
                        clinic_address=clinic_address,
                        reason=reason,
                        preparation_notes=prep_notes,
                        priority=priority_map[priority]
                    )
                else:
                    task = Task(
                        description=description,
                        scheduled_time=scheduled_time,
                        task_type=TaskType(task_type),
                        priority=priority_map[priority],
                        recurring=recurring,
                        recurrence_pattern=recurrence_pattern
                    )
                
                selected_pet.add_task(task)
                st.session_state.scheduler.add_task(task)
                st.success(f"✅ Task '{description}' added for {selected_pet_name}!")
            else:
                st.error("Please enter a task description.")

# ============================================================================
# VIEW TASKS
# ============================================================================
elif page == "📊 View Tasks":
    st.header("📊 View All Tasks")
    
    scheduler = st.session_state.scheduler
    owner = st.session_state.owner
    
    # Filter options
    filter_type = st.selectbox("Filter by:", ["All", "Today", "By Date", "By Pet", "Overdue"])
    
    tasks = []
    
    if filter_type == "All":
        tasks = scheduler.tasks
    elif filter_type == "Today":
        tasks = scheduler.get_tasks_for_today()
    elif filter_type == "By Date":
        date = st.date_input("Select Date", datetime.now())
        tasks = scheduler.get_tasks_for_date(datetime.combine(date, datetime.min.time()))
    elif filter_type == "By Pet":
        pets = owner.get_pets()
        if pets:
            pet_names = [pet.name for pet in pets]
            selected_pet_name = st.selectbox("Select Pet", pet_names)
            selected_pet = next(p for p in pets if p.name == selected_pet_name)
            tasks = selected_pet.get_tasks()
    elif filter_type == "Overdue":
        tasks = scheduler.get_overdue_tasks()
    
    if tasks:
        # Convert to DataFrame for display
        data = []
        for task in tasks:
            pet_name = "Unknown"
            for pet in owner.get_pets():
                if pet.pet_id == task.pet_id:
                    pet_name = pet.name
                    break
            
            data.append({
                "Description": task.description[:40] + "..." if len(task.description) > 40 else task.description,
                "Pet": pet_name,
                "Type": task.task_type.value,
                "Time": task.scheduled_time.strftime("%Y-%m-%d %H:%M"),
                "Priority": task.priority.value,
                "Status": task.status.value,
                "Recurring": "✅" if task.recurring else "❌"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No tasks found!")

# ============================================================================
# SCHEDULER
# ============================================================================
elif page == "⏰ Scheduler":
    st.header("⏰ Advanced Scheduler")
    
    scheduler = st.session_state.scheduler
    
    st.subheader("📊 Daily Summary")
    summary = scheduler.calculate_daily_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📋 Total Tasks", summary['total_tasks'])
    with col2:
        st.metric("⏰ Overdue", summary['overdue'])
    with col3:
        st.metric("✅ Completed", summary['completed'])
    with col4:
        st.metric("⏳ Pending", summary['pending'])
    
    # Conflict detection
    st.subheader("🔍 Conflict Detection")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        st.warning(f"⚠️ {len(conflicts)} conflicts detected!")
        for task1, task2 in conflicts:
            st.write(f"**Conflict:** '{task1.description}' and '{task2.description}' overlap!")
    else:
        st.success("✅ No conflicts detected!")
    
    # Optimal schedule
    st.subheader("📋 Optimal Schedule (Today)")
    optimal = scheduler.suggest_optimal_schedule()
    if optimal:
        for i, task in enumerate(optimal, 1):
            priority_icon = "🔴" if task.priority == Priority.HIGH else "🟡" if task.priority == Priority.MEDIUM else "🟢"
            st.write(f"{i}. {priority_icon} **{task.description}** - {task.scheduled_time.strftime('%H:%M')}")
    else:
        st.info("No tasks scheduled for today!")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("🐾 PawPal+ v1.0 | Built with ❤️")