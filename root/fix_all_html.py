import re
import os

def fix_file(fpath, replacements):
    """Apply regex replacements to a file."""
    if not os.path.exists(fpath):
        print(f'  SKIP: {os.path.basename(fpath)}')
        return
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    original = content
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  FIXED: {os.path.basename(fpath)}')
    else:
        print(f'  OK: {os.path.basename(fpath)}')

print('=== attendance.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\attendance.html', [
    # Leave requests table - remove mock data
    (r'(<thead>\s*<tr>\s*<th>Employee</th>\s*<th>Leave Type</th>\s*<th>From</th>\s*<th>To</th>\s*<th>Days</th>\s*<th>Reason</th>\s*<th>Status</th>\s*<th>Action</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="leaves-tbody"><tr><td colspan="8" style="text-align:center;padding:40px;color:var(--text-muted);">Loading leave requests...</td></tr></tbody>'),
])

print('\n=== payroll.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\payroll.html', [
    # Payroll summary table
    (r'(<thead>\s*<tr>\s*<th>Department</th>\s*<th>Employees</th>\s*<th>Total Payroll</th>\s*<th>Allowances</th>\s*<th>Deductions</th>\s*<th>Net Pay</th>\s*<th>Status</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="payroll-summary-tbody"><tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-muted);">Loading payroll data...</td></tr></tbody>'),
    # Payslips table
    (r'(<thead>\s*<tr>\s*<th>Employee</th>\s*<th>Pay Period</th>\s*<th>Gross</th>\s*<th>Deductions</th>\s*<th>Net Pay</th>\s*<th>Status</th>\s*<th>Action</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="payslips-tbody"><tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-muted);">Loading payslips...</td></tr></tbody>'),
    # Loans table
    (r'(<thead>\s*<tr>\s*<th>Employee</th>\s*<th>Loan Type</th>\s*<th>Amount</th>\s*<th>EMI</th>\s*<th>Balance</th>\s*<th>Status</th>\s*<th>Action</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="loans-tbody"><tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-muted);">Loading loans...</td></tr></tbody>'),
    # Bonuses table
    (r'(<thead>\s*<tr>\s*<th>Employee</th>\s*<th>Bonus Type</th>\s*<th>Amount</th>\s*<th>Pay Month</th>\s*<th>Status</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="bonuses-tbody"><tr><td colspan="5" style="text-align:center;padding:40px;color:var(--text-muted);">Loading bonuses...</td></tr></tbody>'),
])

print('\n=== recruitment.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\recruitment.html', [
    # Jobs table
    (r'(<thead>\s*<tr>\s*<th>Job Title</th>\s*<th>Department</th>\s*<th>Location</th>\s*<th>Deadline</th>\s*<th>Applicants</th>\s*<th>Status</th>\s*<th>Actions</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="jobs-tbody"><tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-muted);">Loading job postings...</td></tr></tbody>'),
    # Candidates table
    (r'(<thead>\s*<tr>\s*<th>Candidate</th>\s*<th>Applied For</th>\s*<th>Source</th>\s*<th>Experience</th>\s*<th>Stage</th>\s*<th>Actions</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="candidates-tbody"><tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-muted);">Loading candidates...</td></tr></tbody>'),
])

print('\n=== onboarding.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\onboarding.html', [
    # Onboarding tasks table
    (r'(<thead>\s*<tr>\s*<th>Employee</th>\s*<th>Task</th>\s*<th>Type</th>\s*<th>Due Date</th>\s*<th>Assigned To</th>\s*<th>Status</th>\s*<th>Actions</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="onboarding-tbody"><tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-muted);">Loading onboarding tasks...</td></tr></tbody>'),
    # Exit interviews table
    (r'(<thead>\s*<tr>\s*<th>Employee</th>\s*<th>Interview Date</th>\s*<th>Reason</th>\s*<th>Rating</th>\s*<th>Status</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="exit-interviews-tbody"><tr><td colspan="5" style="text-align:center;padding:40px;color:var(--text-muted);">Loading exit interviews...</td></tr></tbody>'),
])

print('\n=== ess.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\ess.html', [
    # Expenses table
    (r'(<thead>\s*<tr>\s*<th>Category</th>\s*<th>Amount</th>\s*<th>Date</th>\s*<th>Description</th>\s*<th>Status</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="expenses-tbody"><tr><td colspan="5" style="text-align:center;padding:40px;color:var(--text-muted);">Loading expense claims...</td></tr></tbody>'),
])

print('\n=== performance.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\performance.html', [
    # Reviews table
    (r'(<thead>\s*<tr>\s*<th>Employee</th>\s*<th>Department</th>\s*<th>Period</th>\s*<th>Rating</th>\s*<th>Status</th>\s*<th>Actions</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="reviews-tbody"><tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-muted);">Loading performance reviews...</td></tr></tbody>'),
    # Goals table
    (r'(<thead>\s*<tr>\s*<th>Goal</th>\s*<th>Employee</th>\s*<th>Progress</th>\s*<th>Due Date</th>\s*<th>Status</th>\s*<th>Actions</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="goals-tbody"><tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-muted);">Loading goals...</td></tr></tbody>'),
])

print('\n=== training.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\training.html', [
    # Courses table
    (r'(<thead>\s*<tr>\s*<th>Course</th>\s*<th>Category</th>\s*<th>Enrolled</th>\s*<th>Completion</th>\s*<th>Duration</th>\s*<th>Status</th>\s*<th>Actions</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="courses-tbody"><tr><td colspan="7" style="text-align:center;padding:40px;color:var(--text-muted);">Loading training courses...</td></tr></tbody>'),
    # Enrollments table
    (r'(<thead>\s*<tr>\s*<th>Employee</th>\s*<th>Course</th>\s*<th>Enrolled</th>\s*<th>Score</th>\s*<th>Status</th>\s*<th>Actions</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="enrollments-tbody"><tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-muted);">Loading enrollments...</td></tr></tbody>'),
])

print('\n=== talent.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\talent.html', [
    # Profiles table
    (r'(<thead>\s*<tr>\s*<th>Employee</th>\s*<th>Current Role</th>\s*<th>Potential</th>\s*<th>Rating</th>\s*<th>Readiness</th>\s*<th>Next Role</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="profiles-tbody"><tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-muted);">Loading talent profiles...</td></tr></tbody>'),
    # Succession table
    (r'(<thead>\s*<tr>\s*<th>Position</th>\s*<th>Department</th>\s*<th>Successor</th>\s*<th>Readiness</th>\s*<th>Target</th>\s*<th>Status</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="succession-tbody"><tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-muted);">Loading succession plans...</td></tr></tbody>'),
])

print('\n=== engagement.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\engagement.html', [
    # Surveys table
    (r'(<thead>\s*<tr>\s*<th>Survey</th>\s*<th>Start</th>\s*<th>End</th>\s*<th>Responses</th>\s*<th>Status</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="surveys-tbody"><tr><td colspan="5" style="text-align:center;padding:40px;color:var(--text-muted);">Loading surveys...</td></tr></tbody>'),
])

print('\n=== branding.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\branding.html', [
    # Candidates table
    (r'(<thead>\s*<tr>\s*<th>Candidate</th>\s*<th>Position</th>\s*<th>Source</th>\s*<th>Experience</th>\s*<th>Stage</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="branding-candidates-tbody"><tr><td colspan="5" style="text-align:center;padding:40px;color:var(--text-muted);">Loading candidates...</td></tr></tbody>'),
])

print('\n=== compliance.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\compliance.html', [
    # Policies table
    (r'(<thead>\s*<tr>\s*<th>Policy</th>\s*<th>Category</th>\s*<th>Version</th>\s*<th>Effective</th>\s*<th>Acknowledgement</th>\s*<th>Action</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="policies-tbody"><tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-muted);">Loading policies...</td></tr></tbody>'),
])

print('\n=== health.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\health.html', [
    # Benefits table
    (r'(<thead>\s*<tr>\s*<th>Plan</th>\s*<th>Type</th>\s*<th>Enrolled</th>\s*<th>Cost</th>\s*<th>Status</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="benefits-tbody"><tr><td colspan="5" style="text-align:center;padding:40px;color:var(--text-muted);">Loading benefit plans...</td></tr></tbody>'),
])

print('\n=== global.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\global.html', [
    # Offices table
    (r'(<thead>\s*<tr>\s*<th>Country</th>\s*<th>Office</th>\s*<th>Employees</th>\s*<th>Currency</th>\s*<th>Payroll</th>\s*<th>Compliance</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="offices-tbody"><tr><td colspan="6" style="text-align:center;padding:40px;color:var(--text-muted);">Loading offices...</td></tr></tbody>'),
])

print('\n=== integrations.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\integrations.html', [
    # Integrations table
    (r'(<thead>\s*<tr>\s*<th>Integration</th>\s*<th>Type</th>\s*<th>Status</th>\s*<th>Last Sync</th>\s*<th>Action</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="integrations-tbody"><tr><td colspan="5" style="text-align:center;padding:40px;color:var(--text-muted);">Loading integrations...</td></tr></tbody>'),
])

print('\n=== reports.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\reports.html', [
    # Reports table
    (r'(<thead>\s*<tr>\s*<th>Report</th>\s*<th>Type</th>\s*<th>Generated</th>\s*<th>By</th>\s*<th>Action</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="reports-tbody"><tr><td colspan="5" style="text-align:center;padding:40px;color:var(--text-muted);">Loading reports...</td></tr></tbody>'),
])

print('\n=== index.html ===')
fix_file(r'F:\DASHBOARD_APP\HR_APP-2\root\main\templates\index.html', [
    # Recent hires table
    (r'(<thead>\s*<tr>\s*<th>Employee</th>\s*<th>Department</th>\s*<th>Designation</th>\s*<th>Join Date</th>\s*<th>Status</th>\s*</tr>\s*</thead>\s*)<tbody>.*?</tbody>',
     r'\1<tbody id="recent-hires-tbody"><tr><td colspan="5" style="text-align:center;padding:40px;color:var(--text-muted);">Loading recent hires...</td></tr></tbody>'),
])

print('\nDone!')
