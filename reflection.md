# PawPal+ Project Reflection

## 1. System Design

### Core User Actions

1. **Register and Manage Pets**
   - Users can add new pets with details like name, species, breed, age, weight, and special needs
   - Users can view all their pets in one place
   - Users can update pet information as needed
   - Users can remove pets that are no longer under their care

2. **Create and Schedule Tasks**
   - Users can create tasks for feeding, walking, medication, and vet appointments
   - Users can set specific dates and times for each task
   - Users can set up recurring tasks (daily, weekly, monthly)
   - Users can assign priority levels (high, medium, low) to tasks

3. **View and Complete Daily Tasks**
   - Users can see a prioritized list of all tasks scheduled for today
   - Users can view tasks sorted by urgency and time
   - Users can mark tasks as complete when finished
   - Users can identify overdue tasks that need immediate attention

**a. Initial design**

- Briefly describe your initial UML design.

My initial UML design for PawPal+ follows a modular object-oriented approach with six main classes: Owner, Pet, Task, Medication, Appointment, and Scheduler. The design uses inheritance where Medication and Appointment extend the Task base class, and aggregation where Owner contains multiple Pets, and each Pet contains multiple Tasks. The Scheduler acts as a service class that manages and organizes all tasks across the system.

- What classes did you include, and what responsibilities did you assign to each?

**Owner**: Manages user/pet owner information (name, email, phone) and maintains a collection of pets. Responsible for adding/removing pets and retrieving upcoming tasks across all pets.

**Pet**: Stores pet details (name, species, breed, age, weight, special needs) and manages its own list of tasks. Responsible for task management specific to that pet.

**Task (Base Class)**: Handles all schedulable activities with attributes like task_type, scheduled_time, priority, status, and recurrence. Responsible for marking completion, checking overdue status, and generating next occurrences for recurring tasks.

**Medication (Inherits from Task)**: Extends Task with medication-specific attributes (medication_name, dosage, frequency, administration_method). Responsible for refill tracking and administration logging.

**Appointment (Inherits from Task)**: Extends Task with veterinary-specific attributes (vet_name, clinic_address, reason). Responsible for generating preparation tasks and providing clinic directions.

**Scheduler**: Manages the collection of all tasks and handles algorithmic logic. Responsible for sorting by priority/time, detecting scheduling conflicts, and generating daily summaries.

**b. Design changes**

- Did your design change during implementation?

Yes, my design evolved during implementation as I encountered practical challenges.

- If yes, describe at least one change and why you made it.

One significant change was adding a `priority_calculation` method to the Task class that I initially planned to handle entirely within the Scheduler. During implementation, I realized that tasks needed to be aware of their own urgency based on multiple factors (time until deadline, task type importance, pet health needs). Moving this logic into the Task class made the system more maintainable and followed the Single Responsibility Principle—each task now knows how to calculate its own priority, and the Scheduler simply sorts based on that value. This change also made it easier to add new task types in the future without modifying the Scheduler.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

My scheduler considers three main constraints:
1. **Time**: Tasks are sorted chronologically to ensure daily routines flow logically.
2. **Priority**: Tasks are assigned priority levels (high, medium, low) based on urgency and pet health needs.
3. **Task Type**: Certain task types (like medications) are given higher importance than others (like grooming).

- How did you decide which constraints mattered most?

I decided that **time** and **priority** matter most because pet care often involves time-sensitive activities (medications at specific times) and critical tasks that cannot be missed. I prioritized health-related tasks over convenience tasks since pet wellbeing is the primary goal of the application.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

My scheduler prioritizes time-based sorting over priority-based sorting. This means a low-priority task scheduled for 9:00 AM will appear before a high-priority task scheduled for 3:00 PM in the daily view.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable because pet care routines are time-dependent—you can't give medication at 3:00 PM if it's supposed to be given at 9:00 AM just because it's higher priority. The scheduler ensures users follow the correct chronological order of tasks while still highlighting priority through visual cues (like color coding or labels).

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

I used AI tools throughout the project in several ways:
1. **Design brainstorming**: I asked AI to help identify the main classes and their relationships for the UML diagram.
2. **Code generation**: I used AI to generate initial class structures and method implementations.
3. **Algorithm design**: I collaborated with AI to develop the sorting and conflict detection logic for the scheduler.
4. **Refactoring**: I used AI suggestions to improve code organization and follow OOP principles.
5. **Testing**: I asked AI to generate test cases and edge cases for my scheduler logic.

- What kinds of prompts or questions were most helpful?

The most helpful prompts were:
- "What classes would I need for a pet care management system and what are their responsibilities?"
- "How should I structure the inheritance relationship between Task, Medication, and Appointment?"
- "What's an efficient way to sort tasks by priority and time?"
- "How can I detect scheduling conflicts?"
- "What edge cases should I test for in a task scheduler?"

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

AI suggested creating a single monolithic Scheduler class that handled all sorting, conflict detection, and task management logic. While this would have worked, I felt it violated the Single Responsibility Principle.

- How did you evaluate or verify what the AI suggested?

I evaluated the suggestion by considering the project requirements and OOP best practices. I decided to split the responsibilities across multiple classes:
- The Task class handles its own priority calculation
- The Scheduler handles sorting and conflict detection
- The Owner and Pet classes manage their respective collections

This made the code more modular, testable, and easier to maintain. I verified my approach by implementing both versions in a small prototype and found that the modular approach was significantly easier to debug and extend.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

I tested the following behaviors:
1. **Task creation**: Ensuring tasks are created with correct attributes (type, time, priority, recurrence).
2. **Priority calculation**: Verifying that tasks correctly calculate their priority based on urgency and type.
3. **Sorting**: Testing that tasks are sorted correctly by time and priority.
4. **Conflict detection**: Verifying that overlapping tasks are correctly identified.
5. **Recurring tasks**: Testing that recurring tasks generate the next occurrence correctly.
6. **Task completion**: Ensuring tasks are marked complete and don't appear in active task lists.
7. **Pet management**: Testing adding, removing, and updating pets.

- Why were these tests important?

These tests were important because they verify the core functionality of the system. The scheduler is the heart of PawPal+, and if sorting, priority calculation, or conflict detection fails, users could miss important pet care tasks. Testing ensures reliability and builds confidence in the system.

**b. Confidence**

- How confident are you that your scheduler works correctly?

I am moderately confident (80%) that my scheduler works correctly for standard use cases. The core sorting and priority logic is solid, and I've tested most common scenarios.

- What edge cases would you test next if you had more time?

If I had more time, I would test:
1. **Concurrent tasks**: Multiple tasks scheduled at exactly the same time.
2. **Boundary conditions**: Tasks scheduled at midnight or during daylight saving time changes.
3. **Large datasets**: Performance testing with hundreds of tasks and pets.
4. **Invalid inputs**: Handling of malformed dates, missing attributes, or invalid priority values.
5. **Complex recurrences**: Weekly tasks that skip certain days or monthly tasks that handle varying month lengths.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with the clean separation of concerns in the class design. The Owner, Pet, Task, and Scheduler classes each have well-defined responsibilities, making the code readable and maintainable. I'm also proud of the priority calculation logic, which dynamically adjusts based on task type, time until deadline, and pet health needs.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would:
1. Add a database layer to persist data across sessions (currently using in-memory storage).
2. Implement a notification system to alert users when tasks are due or overdue.
3. Add more sophisticated conflict resolution (e.g., automatically suggesting alternative times).
4. Include a calendar view in the UI for better visualization of tasks across days/weeks.
5. Add user authentication to support multiple users with separate pet accounts.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

The most important thing I learned is that **AI is a powerful collaborator but not a replacement for critical thinking**. While AI can generate code and suggest designs quickly, it's essential to evaluate suggestions against project requirements, OOP principles, and real-world usability. I learned to use AI as a starting point and then refine and validate its suggestions through testing and thoughtful analysis. The best results came from an iterative process where I would ask AI for suggestions, evaluate them, implement the best ideas, and then refine further based on testing results.