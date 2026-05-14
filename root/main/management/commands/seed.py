from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date, datetime
import random
from faker import Faker

fake = Faker('en_US')

from core_module.models.employee.employee import (
    Department, Location, Designation, Employee, Document
)
from core_module.models.attendance.attendance import (
    Shift, Attendance, LeaveRequest
)
from core_module.models.payroll.payroll import (
    SalaryStructure, Payslip, Loan, Bonus
)
from core_module.models.recruitment.recruitment import (
    JobPosting, Candidate, Interview
)
from core_module.models.onboarding.onboarding import (
    OnboardingTask, OffboardingTask, ExitInterview
)
from core_module.models.ess.ess import ExpenseClaim, Announcement

from talent_growth.models.performance.performance import PerformanceReview, PerformanceKPI, Goal
from talent_growth.models.training.training import TrainingCourse, CourseEnrollment
from talent_growth.models.talent.talent import TalentProfile, SuccessionPlan
from talent_growth.models.engagement.engagement import (
    EngagementSurvey, SurveyQuestion, SurveyResponse, Recognition
)

from operation.models.health.health import BenefitPlan, BenefitEnrollment, SafetyIncident
from operation.models.compliance.compliance import PolicyDocument, PolicyAcknowledgement, ComplianceChecklist
from operation.models.global_.global_ import Office
from operation.models.integration.integration import Integration
from operation.models.report.report import Report

from main.models.main import UserProfile, DashboardWidget, Notification


class Command(BaseCommand):
    help = 'Seed database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('--employees', type=int, default=50, help='Number of employees to create')
        parser.add_argument('--full', action='store_true', help='Seed all data including performance, training, etc.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        self.clear_existing_data()

        self.create_users()
        self.create_departments()
        self.create_locations()
        self.create_designations()
        self.create_employees(options['employees'])

        self.stdout.write(self.style.SUCCESS('Basic data seeded!'))

        if options['full']:
            self.seed_full()

        self.stdout.write(self.style.SUCCESS('Seeding complete!'))

    def clear_existing_data(self):
        self.stdout.write('Clearing existing data...')
        Notification.objects.all().delete()
        DashboardWidget.objects.all().delete()
        UserProfile.objects.all().delete()
        SurveyResponse.objects.all().delete()
        CourseEnrollment.objects.all().delete()
        BenefitEnrollment.objects.all().delete()
        PolicyAcknowledgement.objects.all().delete()
        PerformanceKPI.objects.all().delete()
        Interview.objects.all().delete()
        Candidate.objects.all().delete()
        Document.objects.all().delete()
        Payslip.objects.all().delete()
        Loan.objects.all().delete()
        Bonus.objects.all().delete()
        LeaveRequest.objects.all().delete()
        Attendance.objects.all().delete()
        ExitInterview.objects.all().delete()
        OffboardingTask.objects.all().delete()
        OnboardingTask.objects.all().delete()
        ExpenseClaim.objects.all().delete()
        Announcement.objects.all().delete()
        Goal.objects.all().delete()
        PerformanceReview.objects.all().delete()
        TrainingCourse.objects.all().delete()
        TalentProfile.objects.all().delete()
        SuccessionPlan.objects.all().delete()
        EngagementSurvey.objects.all().delete()
        Recognition.objects.all().delete()
        BenefitPlan.objects.all().delete()
        SafetyIncident.objects.all().delete()
        PolicyDocument.objects.all().delete()
        ComplianceChecklist.objects.all().delete()
        Office.objects.all().delete()
        Integration.objects.all().delete()
        Report.objects.all().delete()
        SalaryStructure.objects.all().delete()
        JobPosting.objects.all().delete()
        Shift.objects.all().delete()
        Designation.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()
        Location.objects.all().delete()
        User.objects.exclude(username='admin').delete()
        self.stdout.write(self.style.SUCCESS('Existing data cleared!'))

    def create_users(self):
        self.stdout.write('Creating users...')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@hrms.com', 'admin123')

        for i in range(10):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username, f'user{i}@hrms.com', 'password123')

    def create_departments(self):
        self.stdout.write('Creating departments...')
        depts = [
            ('Human Resources', 'HR and people operations'),
            ('Engineering', 'Software development and IT'),
            ('Marketing', 'Marketing and communications'),
            ('Sales', 'Sales and business development'),
            ('Finance', 'Financial planning and accounting'),
            ('Operations', 'Operations and logistics'),
            ('Customer Support', 'Customer service and support'),
            ('Product', 'Product management and design'),
        ]
        for name, desc in depts:
            Department.objects.get_or_create(name=name, defaults={'description': desc})

    def create_locations(self):
        self.stdout.write('Creating locations...')
        locs = [
            ('Dhaka HQ', 'Dhaka', 'Bangladesh', 'headquarters'),
            ('Chittagong Office', 'Chittagong', 'Bangladesh', 'branch'),
            ('Sylhet Branch', 'Sylhet', 'Bangladesh', 'branch'),
            ('Remote Team', 'Various', 'Bangladesh', 'remote'),
        ]
        for name, city, country, ltype in locs:
            Location.objects.get_or_create(name=name, defaults={
                'city': city, 'country': country, 'location_type': ltype
            })

    def create_designations(self):
        self.stdout.write('Creating designations...')
        depts = list(Department.objects.all())
        titles = [
            ('CEO', 10), ('CTO', 9), ('CFO', 9), ('COO', 9),
            ('Director', 8), ('Senior Manager', 7), ('Manager', 6),
            ('Senior Engineer', 5), ('Engineer', 4), ('Junior Engineer', 3),
            ('Senior Associate', 4), ('Associate', 3), ('Intern', 1),
        ]
        for title, level in titles:
            for dept in depts[:3]:
                Designation.objects.get_or_create(
                    title=f'{title} - {dept.name}',
                    defaults={'department': dept, 'level': level}
                )

    def create_employees(self, count):
        self.stdout.write(f'Creating {count} employees...')
        depts = list(Department.objects.all())
        locs = list(Location.objects.all())
        desigs = list(Designation.objects.all()[:10])

        employees = []
        for i in range(count):
            first = fake.first_name_male() if random.choice([True, False]) else fake.first_name_female()
            last = fake.last_name()
            email = f'{first.lower()}.{last.lower()}{i}@company.com'

            emp = Employee(
                first_name=first,
                last_name=last,
                personal_email=email,
                work_email=f'employee{i}@company.com',
                employee_id=f'EMP{i+1:04d}',
                join_date=fake.date_between(start_date='-4y', end_date='-30d'),
                department=random.choice(depts) if depts else None,
                designation=random.choice(desigs) if desigs else None,
                office_location=random.choice(locs) if locs else None,
                employment_type=random.choice(['full_time', 'part_time', 'contract']),
                status=random.choice(['active', 'probation', 'active', 'active']),
                basic_salary=random.randint(25000, 150000),
                phone_number=fake.phone_number(),
                date_of_birth=fake.date_of_birth(minimum_age=22, maximum_age=55),
                gender=random.choice(['male', 'female', 'other']),
                current_address=fake.address(),
            )
            employees.append(emp)

        Employee.objects.bulk_create(employees)
        self.stdout.write(self.style.SUCCESS(f'Created {count} employees'))

    def seed_full(self):
        self.stdout.write(self.style.WARNING('Seeding full data...'))
        self.seed_offices()
        self.seed_shifts()
        self.seed_attendance()
        self.seed_leave_requests()
        self.seed_salary_structures()
        self.seed_payslips()
        self.seed_loans()
        self.seed_bonuses()
        self.seed_job_postings()
        self.seed_candidates()
        self.seed_interviews()
        self.seed_onboarding_tasks()
        self.seed_offboarding_tasks()
        self.seed_exit_interviews()
        self.seed_expense_claims()
        self.seed_announcements()
        self.seed_documents()
        self.seed_training_courses()
        self.seed_course_enrollments()
        self.seed_performance_reviews()
        self.seed_goals()
        self.seed_talent_profiles()
        self.seed_succession_plans()
        self.seed_engagement_surveys()
        self.seed_recognitions()
        self.seed_benefit_plans()
        self.seed_benefit_enrollments()
        self.seed_safety_incidents()
        self.seed_policies()
        self.seed_compliance_checklists()
        self.seed_integrations()
        self.seed_reports()
        self.seed_user_profiles()
        self.seed_dashboard_widgets()
        self.seed_notifications()
        self.stdout.write(self.style.SUCCESS('Full data seeded!'))

    def seed_offices(self):
        self.stdout.write('Seeding offices...')
        offices = [
            ('Dhaka Headquarters', 'Bangladesh', 'Dhaka', 'headquarters', 'House 42, Road 11, Banani', 'BDT', 'Asia/Dhaka', 'active'),
            ('London Office', 'United Kingdom', 'London', 'regional', '10 Downing Street', 'GBP', 'Europe/London', 'active'),
            ('Dubai Branch', 'UAE', 'Dubai', 'branch', 'Business Bay, Tower 3', 'AED', 'Asia/Dubai', 'active'),
            ('New York Hub', 'USA', 'New York', 'remote_hub', '350 Fifth Avenue', 'USD', 'America/New_York', 'planned'),
        ]
        employees = list(Employee.objects.all()[:4])
        for name, country, city, otype, address, currency, tz, status in offices:
            Office.objects.get_or_create(name=name, defaults={
                'country': country, 'city': city, 'office_type': otype,
                'full_address': address, 'local_currency': currency,
                'timezone': tz, 'status': status,
                'hr_contact': random.choice(employees) if employees else None,
                'capacity': random.randint(50, 500),
                'tax_law': f'{country} Tax Law',
                'labor_law': f'{country} Labor Act',
            })

    def seed_shifts(self):
        self.stdout.write('Seeding shifts...')
        shifts = [
            ('Morning Shift', 'MORN', '09:00', '18:00', 'sun_thu'),
            ('Evening Shift', 'EVEN', '14:00', '23:00', 'mon_fri'),
            ('Night Shift', 'NIGHT', '22:00', '07:00', 'rotating'),
            ('Weekend Shift', 'WKND', '08:00', '16:00', 'mon_sat'),
        ]
        for name, code, start, end, days in shifts:
            Shift.objects.get_or_create(shift_code=code, defaults={
                'shift_name': name,
                'start_time': start, 'end_time': end,
                'working_days': days,
                'break_duration': random.choice([30, 45, 60]),
                'grace_period': random.choice([10, 15, 20]),
                'overtime_eligible': random.choice([True, False]),
                'department': Department.objects.first(),
            })

    def seed_attendance(self):
        self.stdout.write('Seeding attendance...')
        employees = list(Employee.objects.all()[:30])
        shifts = list(Shift.objects.all())
        for emp in employees:
            for i in range(10):
                d = timezone.now().date() - timedelta(days=i)
                Attendance.objects.get_or_create(
                    employee=emp, date=d,
                    defaults={
                        'check_in_time': f'{random.randint(8, 10)}:{random.randint(0, 59):02d}',
                        'check_out_time': f'{random.randint(17, 20)}:{random.randint(0, 59):02d}',
                        'status': random.choice(['present', 'present', 'present', 'late', 'absent']),
                        'work_location': random.choice(['office', 'remote', 'field']),
                        'shift': random.choice(shifts) if shifts else None,
                        'overtime_hours': round(random.uniform(0, 3), 2),
                    }
                )

    def seed_leave_requests(self):
        self.stdout.write('Seeding leave requests...')
        employees = list(Employee.objects.all()[:20])
        for emp in employees:
            LeaveRequest.objects.get_or_create(
                employee=emp,
                from_date=timezone.now().date() + timedelta(days=5),
                defaults={
                    'to_date': timezone.now().date() + timedelta(days=7),
                    'leave_type': random.choice(['annual', 'sick', 'casual']),
                    'reason': fake.sentence(),
                    'status': random.choice(['pending', 'approved']),
                }
            )

    def seed_salary_structures(self):
        self.stdout.write('Seeding salary structures...')
        grades = ['A', 'B', 'C', 'D', 'E']
        for grade in grades:
            basic = random.randint(30000, 100000)
            SalaryStructure.objects.get_or_create(
                structure_name=f'Grade {grade}',
                defaults={
                    'grade_level': grade,
                    'basic_salary': basic,
                    'house_rent_percent': 30,
                    'transport_allowance': 5000,
                    'medical_allowance': 3000,
                    'food_allowance': 2000,
                    'other_allowance': 1000,
                    'income_tax_percent': round(random.uniform(5, 15), 2),
                    'provident_fund_percent': 5,
                    'insurance_premium': 1500,
                    'other_deductions': 500,
                }
            )

    def seed_payslips(self):
        self.stdout.write('Seeding payslips...')
        employees = list(Employee.objects.all()[:20])
        for emp in employees:
            Payslip.objects.get_or_create(
                employee=emp,
                pay_period=f'{timezone.now().strftime("%B")} {timezone.now().year}',
                defaults={
                    'pay_date': timezone.now().date(),
                    'basic_salary': emp.basic_salary or 50000,
                    'house_rent': 15000,
                    'transport_allowance': 5000,
                    'medical_allowance': 3000,
                    'food_allowance': 2000,
                    'other_allowance': 1000,
                    'income_tax': random.randint(2000, 8000),
                    'provident_fund': random.randint(2000, 5000),
                    'insurance_deduction': 1500,
                    'other_deductions': 500,
                }
            )

    def seed_loans(self):
        self.stdout.write('Seeding loans...')
        employees = list(Employee.objects.all()[:10])
        for emp in employees:
            Loan.objects.get_or_create(
                employee=emp,
                loan_type='personal',
                defaults={
                    'loan_amount': random.randint(50000, 500000),
                    'disbursement_date': fake.date_between(start_date='-1y', end_date='-30d'),
                    'repayment_period': random.choice([12, 24, 36]),
                    'interest_rate': round(random.uniform(5, 12), 2),
                    'status': random.choice(['active', 'pending', 'completed']),
                    'purpose_notes': fake.sentence(),
                }
            )

    def seed_bonuses(self):
        self.stdout.write('Seeding bonuses...')
        employees = list(Employee.objects.all()[:15])
        for emp in employees:
            Bonus.objects.get_or_create(
                employee=emp,
                bonus_type='festival',
                pay_month=timezone.now().date(),
                defaults={
                    'amount': random.randint(5000, 50000),
                    'status': random.choice(['pending', 'approved', 'paid']),
                    'taxable': random.choice([True, False]),
                    'remarks': fake.sentence(),
                }
            )

    def seed_job_postings(self):
        self.stdout.write('Seeding job postings...')
        jobs = [
            'Senior Software Engineer', 'Product Manager', 'UX Designer',
            'Data Analyst', 'DevOps Engineer', 'Marketing Manager',
            'Sales Executive', 'HR Coordinator', 'Finance Analyst',
        ]
        for job in jobs:
            JobPosting.objects.get_or_create(
                job_title=job,
                defaults={
                    'department': random.choice(list(Department.objects.all())),
                    'job_type': random.choice(['full_time', 'part_time', 'contract']),
                    'location': random.choice(list(Location.objects.all())),
                    'vacancies': random.randint(1, 5),
                    'salary_range_min': random.randint(30000, 60000),
                    'salary_range_max': random.randint(80000, 150000),
                    'application_deadline': fake.date_between(start_date='+30d', end_date='+90d'),
                    'experience_required': random.choice(['fresher', '1_2_years', '3_5_years', '5_10_years']),
                    'education_level': random.choice(['bachelor', 'master', 'any']),
                    'job_description': fake.paragraph(),
                    'skills_required': ', '.join(fake.words(nb=random.randint(3, 6))),
                    'status': random.choice(['active', 'draft', 'closed']),
                }
            )

    def seed_candidates(self):
        self.stdout.write('Seeding candidates...')
        jobs = list(JobPosting.objects.all()[:3])
        for job in jobs:
            for _ in range(5):
                first = fake.first_name()
                last = fake.last_name()
                Candidate.objects.get_or_create(
                    full_name=f'{first} {last}',
                    email=f'{first.lower()}.{last.lower()}@email.com',
                    applied_for=job,
                    defaults={
                        'phone': fake.phone_number(),
                        'source': random.choice(['linkedin', 'bdjobs', 'referral', 'direct']),
                        'current_stage': random.choice(['applied', 'screening', 'interview', 'offer']),
                        'experience_yrs': round(random.uniform(1, 10), 1),
                        'expected_salary': random.randint(40000, 120000),
                        'notice_period': random.choice(['Immediate', '30 days', '60 days', '90 days']),
                    }
                )

    def seed_interviews(self):
        self.stdout.write('Seeding interviews...')
        candidates = list(Candidate.objects.all()[:10])
        employees = list(Employee.objects.all()[:5])
        for cand in candidates:
            Interview.objects.get_or_create(
                candidate=cand,
                interview_type=random.choice(['phone', 'video', 'technical', 'hr']),
                scheduled_at=fake.date_time_between(start_date='-30d', end_date='+30d'),
                defaults={
                    'duration_mins': random.choice([30, 45, 60, 90]),
                    'interviewer': random.choice(employees) if employees else None,
                    'location': fake.city(),
                    'result': random.choice(['pending', 'passed', 'failed']),
                    'feedback': fake.sentence(),
                    'rating': random.randint(1, 5),
                }
            )

    def seed_onboarding_tasks(self):
        self.stdout.write('Seeding onboarding tasks...')
        employees = list(Employee.objects.all()[:10])
        task_types = ['offer_letter', 'document_verification', 'orientation', 'it_setup', 'equipment', 'training']
        for emp in employees:
            for ttype in random.sample(task_types, k=3):
                OnboardingTask.objects.get_or_create(
                    employee=emp,
                    task_type=ttype,
                    defaults={
                        'task_name': ttype.replace('_', ' ').title(),
                        'description': fake.sentence(),
                        'due_date': fake.date_between(start_date='+7d', end_date='+30d'),
                        'status': random.choice(['pending', 'in_progress', 'completed']),
                        'notes': fake.sentence(),
                    }
                )

    def seed_offboarding_tasks(self):
        self.stdout.write('Seeding offboarding tasks...')
        employees = list(Employee.objects.filter(status='resigned')[:5])
        if not employees:
            employees = list(Employee.objects.all()[:3])
        task_types = ['exit_interview', 'clearance', 'knowledge_transfer', 'equipment_return', 'access_revocation']
        for emp in employees:
            for ttype in random.sample(task_types, k=2):
                OffboardingTask.objects.get_or_create(
                    employee=emp,
                    task_type=ttype,
                    defaults={
                        'task_name': ttype.replace('_', ' ').title(),
                        'description': fake.sentence(),
                        'due_date': fake.date_between(start_date='-7d', end_date='+7d'),
                        'status': random.choice(['pending', 'in_progress', 'completed']),
                        'notes': fake.sentence(),
                    }
                )

    def seed_exit_interviews(self):
        self.stdout.write('Seeding exit interviews...')
        employees = list(Employee.objects.filter(status='resigned')[:5])
        if not employees:
            employees = list(Employee.objects.all()[:3])
        interviewers = list(Employee.objects.all()[:5])
        for emp in employees:
            ExitInterview.objects.get_or_create(
                employee=emp,
                interview_date=fake.date_between(start_date='-30d', end_date='today'),
                defaults={
                    'interviewer': random.choice(interviewers) if interviewers else None,
                    'reason_for_leaving': fake.paragraph(),
                    'feedback': fake.paragraph(),
                    'would_recommend': random.choice([True, False]),
                    'rating': random.randint(1, 5),
                }
            )

    def seed_expense_claims(self):
        self.stdout.write('Seeding expense claims...')
        employees = list(Employee.objects.all()[:15])
        for emp in employees:
            ExpenseClaim.objects.get_or_create(
                employee=emp,
                category=random.choice(['travel', 'meals', 'accommodation', 'equipment', 'communication']),
                expense_date=fake.date_between(start_date='-60d', end_date='today'),
                defaults={
                    'amount': round(random.uniform(500, 25000), 2),
                    'description': fake.sentence(),
                    'status': random.choice(['pending', 'approved', 'rejected', 'reimbursed']),
                }
            )

    def seed_announcements(self):
        self.stdout.write('Seeding announcements...')
        employees = list(Employee.objects.all()[:5])
        titles = [
            'Office Closure for Holidays', 'New Health Insurance Plan',
            'Annual Performance Review Cycle', 'Team Building Event',
            'Updated Remote Work Policy', 'Quarterly Town Hall Meeting',
            'New Learning Platform Available', 'Employee Recognition Program',
        ]
        for title in titles:
            Announcement.objects.get_or_create(
                title=title,
                defaults={
                    'content': fake.paragraph(),
                    'priority': random.choice(['low', 'medium', 'high', 'urgent']),
                    'is_pinned': random.choice([True, False]),
                    'published_by': random.choice(employees) if employees else None,
                    'expires_at': fake.date_time_between(start_date='+30d', end_date='+90d'),
                    'is_active': True,
                }
            )

    def seed_documents(self):
        self.stdout.write('Seeding documents...')
        employees = list(Employee.objects.all()[:10])
        doc_types = ['offer_letter', 'nid', 'academic_certificate', 'tax_document', 'contract']
        for emp in employees:
            for dtype in random.sample(doc_types, k=2):
                Document.objects.get_or_create(
                    employee=emp,
                    document_type=dtype,
                    defaults={
                        'title': f'{dtype.replace("_", " ").title()} - {emp.first_name}',
                        'status': random.choice(['verified', 'pending', 'missing']),
                        'notes': fake.sentence(),
                    }
                )

    def seed_training_courses(self):
        self.stdout.write('Seeding training courses...')
        courses = [
            ('Python Basics', 'technical', 20),
            ('Leadership Skills', 'leadership', 16),
            ('Workplace Safety', 'safety', 8),
            ('Communication Skills', 'soft_skills', 12),
            ('Data Privacy', 'compliance', 4),
            ('Project Management', 'management', 24),
            ('Agile Methodology', 'technical', 16),
            ('Customer Excellence', 'soft_skills', 8),
        ]
        for name, cat, hours in courses:
            TrainingCourse.objects.get_or_create(
                course_name=name,
                defaults={
                    'category': cat,
                    'duration_hours': hours,
                    'description': fake.paragraph(),
                    'instructor': fake.name(),
                    'is_mandatory': random.choice([True, False]),
                    'is_active': True,
                }
            )

    def seed_course_enrollments(self):
        self.stdout.write('Seeding course enrollments...')
        employees = list(Employee.objects.all()[:20])
        courses = list(TrainingCourse.objects.all())
        for emp in employees[:10]:
            for course in random.sample(courses, k=min(3, len(courses))):
                CourseEnrollment.objects.get_or_create(
                    employee=emp,
                    course=course,
                    defaults={
                        'status': random.choice(['enrolled', 'in_progress', 'completed', 'dropped']),
                        'score': round(random.uniform(50, 100), 2),
                        'feedback': fake.sentence(),
                    }
                )

    def seed_performance_reviews(self):
        self.stdout.write('Seeding performance reviews...')
        employees = list(Employee.objects.all()[:20])
        reviewers = list(Employee.objects.all()[:5])
        for emp in employees:
            review, created = PerformanceReview.objects.get_or_create(
                employee=emp,
                review_period='Q1 2026',
                defaults={
                    'department': emp.department,
                    'start_date': date(2026, 1, 1),
                    'end_date': date(2026, 3, 31),
                    'status': random.choice(['in_progress', 'completed']),
                    'overall_rating': round(random.uniform(3.0, 5.0), 2),
                    'reviewer': random.choice(reviewers) if reviewers else None,
                    'employee_comments': fake.sentence(),
                    'reviewer_comments': fake.sentence(),
                }
            )
            if created:
                metrics = ['Code Quality', 'Team Collaboration', 'Delivery Timeliness', 'Innovation', 'Client Satisfaction']
                for metric in random.sample(metrics, k=3):
                    PerformanceKPI.objects.create(
                        review=review,
                        metric=metric,
                        target=f'Achieve {random.randint(80, 100)}% target',
                        weight=round(random.uniform(0.5, 2.0), 2),
                        score=round(random.uniform(60, 100), 2),
                        notes=fake.sentence(),
                    )

    def seed_goals(self):
        self.stdout.write('Seeding goals...')
        employees = list(Employee.objects.all()[:15])
        goal_titles = [
            'Complete Certification', 'Launch New Feature', 'Improve Team Process',
            'Reduce Bug Rate', 'Mentor Junior Developer', 'Increase Client Satisfaction',
            'Deliver Project Alpha', 'Optimize System Performance',
        ]
        for emp in employees:
            for title in random.sample(goal_titles, k=2):
                Goal.objects.get_or_create(
                    employee=emp,
                    title=title,
                    defaults={
                        'description': fake.paragraph(),
                        'start_date': timezone.now().date(),
                        'due_date': timezone.now().date() + timedelta(days=random.randint(30, 180)),
                        'status': random.choice(['not_started', 'in_progress', 'completed']),
                        'progress': random.randint(0, 100),
                    }
                )

    def seed_talent_profiles(self):
        self.stdout.write('Seeding talent profiles...')
        employees = list(Employee.objects.all()[:15])
        for emp in employees:
            TalentProfile.objects.get_or_create(
                employee=emp,
                defaults={
                    'current_role': emp.designation.title if emp.designation else 'Employee',
                    'potential': random.choice(['high', 'medium', 'low']),
                    'performance_rating': round(random.uniform(3.0, 5.0), 2),
                    'readiness': random.choice(['ready_now', '1_year', '2_years', '3_plus_years', 'not_ready']),
                    'next_role': fake.job(),
                    'development_areas': fake.paragraph(),
                    'key_strengths': fake.paragraph(),
                    'succession_plan': random.choice([True, False]),
                }
            )

    def seed_succession_plans(self):
        self.stdout.write('Seeding succession plans...')
        depts = list(Department.objects.all())
        employees = list(Employee.objects.all())
        positions = ['CTO', 'CFO', 'VP Engineering', 'Head of Sales', 'HR Director', 'Product Lead']
        for position in positions:
            SuccessionPlan.objects.get_or_create(
                position=position,
                defaults={
                    'department': random.choice(depts) if depts else None,
                    'primary_successor': random.choice(employees) if employees else None,
                    'readiness_level': random.choice(['Ready Now', '1 Year', '2 Years']),
                    'target_date': fake.date_between(start_date='+6m', end_date='+2y'),
                    'is_active': True,
                }
            )

    def seed_engagement_surveys(self):
        self.stdout.write('Seeding engagement surveys...')
        surveys = [
            ('Q1 2026 Employee Engagement Survey', 'Quarterly engagement assessment'),
            ('Work-Life Balance Survey', 'Assessing work-life balance satisfaction'),
            ('Company Culture Survey', 'Understanding company culture perception'),
        ]
        for title, desc in surveys:
            survey, created = EngagementSurvey.objects.get_or_create(
                title=title,
                defaults={
                    'description': desc,
                    'start_date': fake.date_between(start_date='-30d', end_date='today'),
                    'end_date': fake.date_between(start_date='+30d', end_date='+60d'),
                    'is_anonymous': True,
                    'is_active': True,
                }
            )
            if created:
                questions = [
                    ('How satisfied are you with your work-life balance?', 'rating'),
                    ('Do you feel valued by your manager?', 'rating'),
                    ('How would you rate the company culture?', 'rating'),
                    ('What improvements would you suggest?', 'text'),
                    ('Which benefit do you value most?', 'multiple_choice'),
                ]
                for i, (qtext, qtype) in enumerate(questions, 1):
                    SurveyQuestion.objects.create(
                        survey=survey,
                        question_text=qtext,
                        question_type=qtype,
                        options='Health Insurance, Flexible Hours, Remote Work, Learning Budget' if qtype == 'multiple_choice' else '',
                        order=i,
                        is_required=True,
                    )

    def seed_recognitions(self):
        self.stdout.write('Seeding recognitions...')
        employees = list(Employee.objects.all()[:20])
        for _ in range(15):
            emp = random.choice(employees)
            giver = random.choice([e for e in employees if e != emp])
            Recognition.objects.create(
                employee=emp,
                recognized_by=giver,
                recognition_type=random.choice(['kudos', 'peer_award', 'innovation', 'team_player', 'leader']),
                reason=fake.paragraph(),
                points=random.choice([50, 100, 150, 200, 500]),
            )

    def seed_benefit_plans(self):
        self.stdout.write('Seeding benefit plans...')
        plans = [
            ('Basic Medical', 'medical', 2000, 'Basic health coverage for employee'),
            ('Premium Medical', 'medical', 5000, 'Comprehensive health coverage including family'),
            ('Dental Plan', 'dental', 1000, 'Dental care and orthodontics coverage'),
            ('Life Insurance', 'life_insurance', 3000, 'Life insurance with 2x annual salary coverage'),
            ('Wellness Program', 'wellness', 500, 'Gym membership and wellness activities'),
            ('Retirement Plan', 'retirement', 4000, '401k matching retirement plan'),
        ]
        for name, ptype, cost, details in plans:
            BenefitPlan.objects.get_or_create(
                plan_name=name,
                defaults={
                    'plan_type': ptype,
                    'coverage_details': details,
                    'cost_per_month': cost,
                    'employer_contribution': round(cost * 0.7, 2),
                    'is_active': True,
                }
            )

    def seed_benefit_enrollments(self):
        self.stdout.write('Seeding benefit enrollments...')
        employees = list(Employee.objects.all()[:15])
        plans = list(BenefitPlan.objects.all())
        for emp in employees[:10]:
            for plan in random.sample(plans, k=min(2, len(plans))):
                BenefitEnrollment.objects.get_or_create(
                    employee=emp,
                    plan=plan,
                    defaults={
                        'coverage_start': fake.date_between(start_date='-6m', end_date='today'),
                        'coverage_end': fake.date_between(start_date='+6m', end_date='+1y'),
                        'status': random.choice(['active', 'pending', 'cancelled']),
                        'dependent_count': random.randint(0, 4),
                    }
                )

    def seed_safety_incidents(self):
        self.stdout.write('Seeding safety incidents...')
        employees = list(Employee.objects.all()[:10])
        for _ in range(5):
            reporter = random.choice(employees)
            SafetyIncident.objects.get_or_create(
                reported_by=reporter,
                incident_date=fake.date_between(start_date='-90d', end_date='today'),
                defaults={
                    'location': fake.city(),
                    'severity': random.choice(['minor', 'moderate', 'severe', 'critical']),
                    'description': fake.paragraph(),
                    'injuries': fake.sentence() if random.choice([True, False]) else '',
                    'witnesses': ', '.join([fake.name() for _ in range(random.randint(1, 3))]),
                    'corrective_action': fake.paragraph(),
                    'status': random.choice(['reported', 'investigating', 'resolved', 'closed']),
                    'assigned_to': random.choice(employees),
                }
            )

    def seed_policies(self):
        self.stdout.write('Seeding policies...')
        policies = [
            ('Code of Conduct', 'hr', 'General workplace behavior guidelines'),
            ('Remote Work Policy', 'operations', 'Guidelines for remote work arrangements'),
            ('Data Security Policy', 'it', 'Information security and data protection'),
            ('Leave Policy', 'hr', 'Leave entitlements and procedures'),
            ('Anti-Harassment Policy', 'legal', 'Workplace harassment prevention'),
            ('IT Usage Policy', 'it', 'Proper use of company IT resources'),
        ]
        employees = list(Employee.objects.all()[:5])
        for name, cat, desc in policies:
            PolicyDocument.objects.get_or_create(
                policy_name=name,
                defaults={
                    'category': cat,
                    'version': f'{random.randint(1, 3)}.{random.randint(0, 5)}',
                    'description': desc,
                    'effective_date': fake.date_between(start_date='-1y', end_date='today'),
                    'review_date': fake.date_between(start_date='+3m', end_date='+1y'),
                    'is_mandatory': random.choice([True, False]),
                    'created_by': random.choice(employees) if employees else None,
                }
            )

    def seed_compliance_checklists(self):
        self.stdout.write('Seeding compliance checklists...')
        employees = list(Employee.objects.all()[:5])
        checklists = [
            ('Annual Tax Filing', 'legal'),
            ('Labor Law Compliance Audit', 'legal'),
            ('Fire Safety Inspection', 'safety'),
            ('Data Privacy Assessment', 'it'),
            ('HR Policy Review', 'hr'),
        ]
        for name, cat in checklists:
            ComplianceChecklist.objects.get_or_create(
                checklist_name=name,
                defaults={
                    'category': cat,
                    'description': fake.paragraph(),
                    'due_date': fake.date_between(start_date='+30d', end_date='+180d'),
                    'assigned_to': random.choice(employees) if employees else None,
                    'status': random.choice(['pending', 'in_progress', 'completed']),
                    'notes': fake.sentence(),
                }
            )

    def seed_integrations(self):
        self.stdout.write('Seeding integrations...')
        integrations = [
            ('Google Calendar', 'calendar'),
            ('Slack', 'communication'),
            ('AWS S3', 'storage'),
            ('Tableau', 'analytics'),
            ('QuickBooks', 'payroll'),
        ]
        for name, itype in integrations:
            Integration.objects.get_or_create(
                name=name,
                defaults={
                    'integration_type': itype,
                    'api_key': fake.uuid4()[:40],
                    'api_secret': fake.uuid4()[:40],
                    'webhook_url': f'https://hooks.example.com/{fake.slug()}',
                    'is_enabled': random.choice([True, False]),
                    'status': random.choice(['active', 'inactive', 'error']),
                    'settings': '{"auto_sync": true, "interval": "hourly"}',
                }
            )

    def seed_reports(self):
        self.stdout.write('Seeding reports...')
        reports = [
            ('Monthly Attendance Report', 'attendance'),
            ('Payroll Summary Q1', 'payroll'),
            ('Headcount Analysis', 'headcount'),
            ('Employee Turnover Report', 'turnover'),
            ('Performance Dashboard', 'performance'),
        ]
        employees = list(Employee.objects.all()[:5])
        for name, rtype in reports:
            Report.objects.get_or_create(
                report_name=name,
                defaults={
                    'report_type': rtype,
                    'description': fake.paragraph(),
                    'parameters': '{"start_date": "2026-01-01", "end_date": "2026-03-31"}',
                    'created_by': random.choice(employees) if employees else None,
                }
            )

    def seed_user_profiles(self):
        self.stdout.write('Seeding user profiles...')
        users = list(User.objects.all()[:10])
        employees = list(Employee.objects.all()[:10])
        used_employees = set()
        for user in users:
            available = [e for e in employees if e.id not in used_employees]
            emp = random.choice(available) if available else None
            if emp:
                used_employees.add(emp.id)
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'employee': emp,
                    'theme': random.choice(['light', 'dark']),
                    'notifications_enabled': True,
                    'email_notifications': random.choice([True, False]),
                    'language': random.choice(['en', 'bn']),
                    'timezone': random.choice(['Asia/Dhaka', 'Europe/London', 'America/New_York']),
                }
            )

    def seed_dashboard_widgets(self):
        self.stdout.write('Seeding dashboard widgets...')
        users = list(User.objects.all()[:10])
        widget_types = ['attendance_chart', 'payroll_summary', 'leave_calendar', 'headcount_stats', 'recent_hires']
        for user in users:
            for i, wtype in enumerate(random.sample(widget_types, k=3)):
                DashboardWidget.objects.get_or_create(
                    user=user,
                    widget_type=wtype,
                    position=i,
                    defaults={
                        'is_visible': True,
                        'config': {'show_legend': True, 'refresh_interval': 300},
                    }
                )

    def seed_notifications(self):
        self.stdout.write('Seeding notifications...')
        users = list(User.objects.all()[:10])
        ntypes = ['info', 'success', 'warning', 'error']
        titles = [
            'New Leave Request', 'Payroll Processed', 'Policy Updated',
            'Meeting Reminder', 'System Maintenance', 'Performance Review Due',
            'Welcome to the Team', 'Training Enrollment Confirmed',
        ]
        for user in users:
            for _ in range(3):
                Notification.objects.create(
                    user=user,
                    notification_type=random.choice(ntypes),
                    title=random.choice(titles),
                    message=fake.sentence(),
                    link=f'/dashboard/{random.choice(["attendance", "payroll", "leaves"])}',
                    is_read=random.choice([True, False]),
                )
