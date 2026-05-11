"""Main CLI application for Student Agentic AI"""

import click
import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()

from src.agents.tutor_agent import TutorAgent
from src.agents.pdf_analyzer import PDFAnalyzer
from src.agents.task_scheduler import TaskScheduler


@click.group()
def cli():
    """🎓 Student Agentic AI - Intelligent Tutor System"""
    pass


@cli.command()
@click.argument('question')
@click.option('--subject', default='General', help='Subject area')
@click.option('--difficulty', type=click.Choice(['beginner', 'intermediate', 'advanced']), default='intermediate')
def ask(question, subject, difficulty):
    """Ask a tutoring question"""
    try:
        tutor = TutorAgent()
        tutor.set_difficulty(difficulty)
        
        click.echo(f"\n📚 Asking about {subject} (Level: {difficulty})...\n")
        
        result = tutor.answer_question(question, subject)
        
        click.echo(f"✅ Answer:\n")
        click.echo(result['answer'])
        click.echo(f"\n🕐 Answered at: {result['timestamp']}\n")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
@click.argument('pdf_path')
@click.option('--subject', default='General', help='Subject of the PDF')
def upload_pdf(pdf_path, subject):
    """Upload and analyze a PDF solution book"""
    try:
        if not os.path.exists(pdf_path):
            click.echo(f"❌ File not found: {pdf_path}", err=True)
            return
        
        click.echo(f"\n📄 Uploading and indexing PDF...\n")
        
        analyzer = PDFAnalyzer()
        result = analyzer.index_pdf(pdf_path, subject)
        
        if result['status'] == 'success':
            click.echo(f"✅ PDF Successfully Indexed")
            click.echo(f"   Subject: {result['subject']}")
            click.echo(f"   Pages: {result['pages']}")
            click.echo(f"   Chunks: {result['chunks_created']}")
            click.echo(f"   Document ID: {result['document_id']}\n")
        else:
            click.echo(f"❌ Error: {result['message']}", err=True)
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
@click.argument('question')
@click.option('--doc-id', default=None, help='Specific document ID to search')
def ask_pdf(question, doc_id):
    """Ask a question and get answers from uploaded PDFs"""
    try:
        analyzer = PDFAnalyzer()
        
        click.echo(f"\n🔍 Searching PDFs...\n")
        
        result = analyzer.teach_from_solution(question, doc_id)
        
        if result['status'] == 'success':
            click.echo(f"✅ Based on {result['sources']} solution(s):\n")
            click.echo(result['explanation'])
            click.echo(f"\n📚 Sources from: {', '.join(result['source_subjects'])}\n")
        else:
            click.echo(f"⚠️  {result['message']}\n")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
@click.argument('title')
@click.argument('subject')
@click.option('--hours', type=float, default=1.0, help='Estimated hours needed')
@click.option('--days', type=int, default=7, help='Days until deadline')
@click.option('--priority', type=click.Choice(['low', 'medium', 'high', 'urgent']), default='medium')
@click.option('--description', default='', help='Task description')
def add_task(title, subject, hours, days, priority, description):
    """Add a new learning task"""
    try:
        scheduler = TaskScheduler()
        
        from datetime import datetime, timedelta
        deadline = (datetime.now() + timedelta(days=days)).isoformat()
        
        task = scheduler.add_task(
            title=title,
            subject=subject,
            duration_hours=hours,
            deadline=deadline,
            priority=priority,
            description=description
        )
        
        click.echo(f"\n✅ Task Created")
        click.echo(f"   Title: {task.title}")
        click.echo(f"   Subject: {task.subject}")
        click.echo(f"   Priority: {task.priority}")
        click.echo(f"   Hours: {task.duration_hours}")
        click.echo(f"   Deadline: {task.deadline}")
        click.echo(f"   ID: {task.id}\n")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
@click.argument('subject')
@click.option('--days', type=int, default=7, help='Number of days to schedule')
@click.option('--hours', type=float, default=2.0, help='Study hours per day')
def schedule(subject, days, hours):
    """Generate a personalized study schedule"""
    try:
        scheduler = TaskScheduler()
        
        click.echo(f"\n📅 Generating schedule for {subject}...\n")
        
        result = scheduler.generate_schedule(subject, days, hours)
        
        if result['status'] == 'success':
            click.echo(f"✅ Schedule Generated")
            click.echo(f"   Subject: {result['subject']}")
            click.echo(f"   Duration: {result['days']} days")
            click.echo(f"   Hours/Day: {result['hours_per_day']}")
            click.echo(f"   Total Hours Planned: {result['total_hours_planned']}")
            click.echo(f"   Tasks Scheduled: {result['tasks_scheduled']}\n")
            
            click.echo("📋 Schedule:")
            for item in result['schedule'][:10]:  # Show first 10 items
                click.echo(f"   {item['date']}: {item['title']} ({item['hours']}h)")
            if len(result['schedule']) > 10:
                click.echo(f"   ... and {len(result['schedule']) - 10} more items")
            click.echo()
        else:
            click.echo(f"⚠️  {result['message']}\n")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
def today():
    """View today's study plan"""
    try:
        scheduler = TaskScheduler()
        
        today_tasks = scheduler.get_today_schedule()
        
        if today_tasks:
            click.echo(f"\n📅 Today's Study Plan\n")
            for i, task in enumerate(today_tasks, 1):
                click.echo(f"{i}. {task['title']} ({task['subject']})")
                click.echo(f"   Priority: {task['priority']} | Duration: {task['duration']}h")
                if task['deadline']:
                    click.echo(f"   Deadline: {task['deadline']}")
            click.echo()
        else:
            click.echo(f"\n✅ No tasks scheduled for today!\n")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
@click.option('--subject', default=None, help='Filter by subject')
def progress(subject):
    """View learning progress and statistics"""
    try:
        scheduler = TaskScheduler()
        
        stats = scheduler.get_progress_stats(subject)
        
        click.echo(f"\n📊 Progress Statistics\n")
        if 'message' in stats:
            click.echo(f"ℹ️  {stats['message']}\n")
        else:
            click.echo(f"Total Tasks: {stats['total_tasks']}")
            click.echo(f"Completed: {stats['completed']}")
            click.echo(f"Pending: {stats['pending']}")
            click.echo(f"In Progress: {stats['in_progress']}")
            click.echo(f"Completion Rate: {stats['completion_rate']}%")
            click.echo(f"Total Hours Planned: {stats['total_hours_planned']}h")
            click.echo(f"Total Hours Completed: {stats['total_hours_completed']}h")
            click.echo(f"Subjects: {', '.join(stats['subjects'])}\n")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
def tasks():
    """List all tasks"""
    try:
        scheduler = TaskScheduler()
        
        all_tasks = scheduler.list_tasks()
        
        if all_tasks:
            click.echo(f"\n📝 All Tasks\n")
            for task in all_tasks:
                status_icon = "⏳" if task['status'] == 'pending' else "✅" if task['status'] == 'completed' else "🔄"
                click.echo(f"{status_icon} {task['title']} ({task['subject']})")
                click.echo(f"   Priority: {task['priority']} | Status: {task['status']}")
            click.echo()
        else:
            click.echo(f"\n✅ No tasks yet!\n")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


@cli.command()
def interactive():
    """Start interactive tutoring session"""
    click.echo("\n🎓 Welcome to Student Agentic AI!\n")
    click.echo("This is your AI tutor. I can help you learn, manage tasks, and create study schedules.\n")
    
    tutor = TutorAgent()
    scheduler = TaskScheduler()
    
    while True:
        try:
            mode = click.prompt(
                "\nWhat would you like to do?",
                type=click.Choice(['ask', 'schedule', 'tasks', 'today', 'progress', 'exit']),
                default='ask'
            )
            
            if mode == 'exit':
                click.echo("\n👋 Goodbye! Keep learning!\n")
                break
            elif mode == 'ask':
                question = click.prompt("What's your question?")
                subject = click.prompt("Subject (press Enter for General)", default='General')
                difficulty = click.prompt(
                    "Difficulty level",
                    type=click.Choice(['beginner', 'intermediate', 'advanced']),
                    default='intermediate'
                )
                tutor.set_difficulty(difficulty)
                result = tutor.answer_question(question, subject)
                click.echo(f"\n{result['answer']}\n")
            
            elif mode == 'tasks':
                all_tasks = scheduler.list_tasks()
                if all_tasks:
                    click.echo(f"\nYour Tasks:")
                    for task in all_tasks:
                        click.echo(f"  • {task['title']} ({task['subject']}) - {task['status']}")
                else:
                    click.echo(f"\nNo tasks yet!")
            
            elif mode == 'schedule':
                subject = click.prompt("Which subject?")
                days = click.prompt("Days to schedule", type=int, default=7)
                hours = click.prompt("Hours per day", type=float, default=2.0)
                result = scheduler.generate_schedule(subject, days, hours)
                if result['status'] == 'success':
                    click.echo(f"\nSchedule created for {result['tasks_scheduled']} tasks!")
                else:
                    click.echo(f"\n{result['message']}")
            
            elif mode == 'today':
                today_tasks = scheduler.get_today_schedule()
                if today_tasks:
                    click.echo(f"\nToday's Tasks:")
                    for task in today_tasks:
                        click.echo(f"  • {task['title']} ({task['subject']})")
                else:
                    click.echo(f"\nNo tasks for today!")
            
            elif mode == 'progress':
                stats = scheduler.get_progress_stats()
                click.echo(f"\nCompletion Rate: {stats['completion_rate']}%")
                click.echo(f"Tasks Completed: {stats['completed']}/{stats['total_tasks']}")
        
        except click.Abort:
            click.echo("\n👋 Goodbye!\n")
            break
        except Exception as e:
            click.echo(f"\n❌ Error: {str(e)}\n")


if __name__ == '__main__':
    cli()