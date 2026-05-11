"""Smart Task Scheduler - Intelligent study scheduling and task management"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import json


@dataclass
class Task:
    """Represents a learning task."""
    id: str
    title: str
    subject: str
    description: str = ""
    priority: str = "medium"  # low, medium, high, urgent
    deadline: Optional[str] = None  # ISO format datetime
    duration_hours: float = 1.0
    estimated_hours: float = 1.0
    status: str = "pending"  # pending, in_progress, completed, blocked
    created_at: str = ""
    updated_at: str = ""
    tags: List[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()
        if self.tags is None:
            self.tags = []


class TaskScheduler:
    """Intelligent task scheduler for study planning."""
    
    PRIORITY_SCORES = {
        "low": 1,
        "medium": 5,
        "high": 10,
        "urgent": 20
    }
    
    def __init__(self):
        """Initialize task scheduler."""
        self.tasks: Dict[str, Task] = {}
        self.schedules: Dict[str, List[Dict]] = {}
        self.task_counter = 0
    
    def add_task(
        self,
        title: str,
        subject: str,
        duration_hours: float = 1.0,
        deadline: Optional[str] = None,
        priority: str = "medium",
        description: str = "",
        tags: List[str] = None
    ) -> Task:
        """Add a new task.
        
        Args:
            title: Task title
            subject: Subject area
            duration_hours: Estimated hours needed
            deadline: Deadline date/time (ISO format)
            priority: Priority level
            description: Task description
            tags: Task tags
            
        Returns:
            Created Task object
        """
        task_id = f"task_{self.task_counter}"
        self.task_counter += 1
        
        task = Task(
            id=task_id,
            title=title,
            subject=subject,
            description=description,
            priority=priority,
            deadline=deadline,
            duration_hours=duration_hours,
            estimated_hours=duration_hours,
            tags=tags or []
        )
        
        self.tasks[task_id] = task
        return task
    
    def prioritize_tasks(self, tasks: Optional[List[str]] = None) -> List[Task]:
        """Get tasks sorted by priority considering deadlines.
        
        Args:
            tasks: List of task IDs to prioritize (None = all)
            
        Returns:
            Prioritized list of tasks
        """
        task_list = [self.tasks[tid] for tid in tasks if tid in self.tasks] if tasks else list(self.tasks.values())
        
        def calculate_urgency(task: Task) -> float:
            """Calculate urgency score for a task."""
            priority_score = self.PRIORITY_SCORES.get(task.priority, 5)
            
            # Add deadline urgency
            if task.deadline:
                try:
                    deadline = datetime.fromisoformat(task.deadline)
                    time_left = (deadline - datetime.now()).total_seconds() / 3600  # hours
                    
                    if time_left <= 0:
                        return 1000  # Overdue
                    elif time_left <= 24:
                        priority_score *= 5  # Due soon
                    elif time_left <= 72:
                        priority_score *= 2  # Due in 3 days
                except:
                    pass
            
            # Adjust by duration (shorter tasks higher priority if similar priority)
            duration_factor = 1 / max(task.duration_hours, 1)
            
            return priority_score * duration_factor
        
        # Filter pending tasks
        pending_tasks = [t for t in task_list if t.status == "pending"]
        
        # Sort by urgency
        prioritized = sorted(pending_tasks, key=calculate_urgency, reverse=True)
        
        return prioritized
    
    def generate_schedule(
        self,
        subject: Optional[str] = None,
        days: int = 7,
        hours_per_day: float = 2.0
    ) -> Dict:
        """Generate optimized study schedule.
        
        Args:
            subject: Specific subject (None = all subjects)
            days: Number of days to schedule
            hours_per_day: Available study hours per day
            
        Returns:
            Generated schedule
        """
        # Get tasks for subject
        tasks = [
            t for t in self.tasks.values()
            if (subject is None or t.subject == subject) and t.status == "pending"
        ]
        
        if not tasks:
            return {
                "status": "no_tasks",
                "message": f"No pending tasks found for {subject or 'any subject'}"
            }
        
        # Prioritize tasks
        prioritized = self.prioritize_tasks([t.id for t in tasks])
        
        # Create schedule
        schedule = {}
        total_hours_available = days * hours_per_day
        current_hours = 0
        current_day = datetime.now().date()
        
        schedule_list = []
        
        for task in prioritized:
            if current_hours >= total_hours_available:
                break
            
            hours_needed = task.duration_hours
            hours_remaining = total_hours_available - current_hours
            
            if hours_needed <= hours_remaining:
                # Schedule task
                schedule_list.append({
                    "date": current_day.isoformat(),
                    "task_id": task.id,
                    "title": task.title,
                    "subject": task.subject,
                    "hours": hours_needed,
                    "priority": task.priority
                })
                current_hours += hours_needed
                
                # Move to next day if needed
                if current_hours >= hours_per_day:
                    current_day += timedelta(days=1)
                    current_hours = 0
            else:
                # Split task across days
                remaining = hours_needed
                while remaining > 0:
                    hours_for_today = min(remaining, hours_per_day - current_hours)
                    schedule_list.append({
                        "date": current_day.isoformat(),
                        "task_id": task.id,
                        "title": task.title,
                        "subject": task.subject,
                        "hours": hours_for_today,
                        "priority": task.priority
                    })
                    remaining -= hours_for_today
                    current_hours += hours_for_today
                    
                    if current_hours >= hours_per_day:
                        current_day += timedelta(days=1)
                        current_hours = 0
        
        return {
            "status": "success",
            "subject": subject or "All Subjects",
            "days": days,
            "hours_per_day": hours_per_day,
            "total_hours_planned": sum(s["hours"] for s in schedule_list),
            "tasks_scheduled": len(set(s["task_id"] for s in schedule_list)),
            "schedule": schedule_list,
            "generated_at": datetime.now().isoformat()
        }
    
    def get_today_schedule(self) -> List[Dict]:
        """Get today's study plan.
        
        Returns:
            Today's prioritized tasks
        """
        today = datetime.now().date().isoformat()
        
        # Get pending tasks
        today_tasks = [
            t for t in self.tasks.values()
            if t.status == "pending"
        ]
        
        # Prioritize them
        prioritized = self.prioritize_tasks([t.id for t in today_tasks])
        
        return [
            {
                "task_id": t.id,
                "title": t.title,
                "subject": t.subject,
                "priority": t.priority,
                "duration": t.duration_hours,
                "deadline": t.deadline
            }
            for t in prioritized
        ]
    
    def update_task_status(self, task_id: str, status: str) -> Dict:
        """Update task status.
        
        Args:
            task_id: Task ID
            status: New status
            
        Returns:
            Updated task
        """
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        
        task = self.tasks[task_id]
        task.status = status
        task.updated_at = datetime.now().isoformat()
        
        return asdict(task)
    
    def get_progress_stats(self, subject: Optional[str] = None) -> Dict:
        """Get progress statistics.
        
        Args:
            subject: Subject to get stats for (None = all)
            
        Returns:
            Statistics dictionary
        """
        tasks = [
            t for t in self.tasks.values()
            if subject is None or t.subject == subject
        ]
        
        if not tasks:
            return {"message": "No tasks found"}
        
        completed = [t for t in tasks if t.status == "completed"]
        pending = [t for t in tasks if t.status == "pending"]
        in_progress = [t for t in tasks if t.status == "in_progress"]
        
        return {
            "total_tasks": len(tasks),
            "completed": len(completed),
            "pending": len(pending),
            "in_progress": len(in_progress),
            "completion_rate": round((len(completed) / len(tasks) * 100) if tasks else 0, 2),
            "total_hours_planned": sum(t.duration_hours for t in tasks),
            "total_hours_completed": sum(t.duration_hours for t in completed),
            "subjects": list(set(t.subject for t in tasks))
        }
    
    def list_tasks(self, status: Optional[str] = None) -> List[Dict]:
        """List all tasks.
        
        Args:
            status: Filter by status (None = all)
            
        Returns:
            List of tasks
        """
        tasks = self.tasks.values()
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        return [asdict(t) for t in tasks]