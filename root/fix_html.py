import re
import os

files_to_fix = [
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\attendance.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\payroll.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\recruitment.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\onboarding.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\ess.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\performance.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\training.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\talent.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\engagement.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\branding.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\compliance.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\health.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\global.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\integrations.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\reports.html',
    r'F:\DASHBOARD_APP\HR_APP-2\root\main\templates\index.html',
]

for fpath in files_to_fix:
    if not os.path.exists(fpath):
        print(f'NOT FOUND: {fpath}')
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Remove mock pagination buttons (Prev, Next, page numbers)
    content = re.sub(r'<button[^>]*btn-outline-custom[^>]*>[‹‹]?\s*Prev\s*</button>', '', content)
    content = re.sub(r'<button[^>]*btn-primary-custom[^>]*>\d+</button>', '', content)
    content = re.sub(r'<button[^>]*btn-outline-custom[^>]*>\d+</button>', '', content)
    content = re.sub(r'<button[^>]*btn-outline-custom[^>]*>Next\s*[››]?\s*</button>', '', content)
    
    # Remove mock 'Showing X of Y' text spans
    content = re.sub(
        r'<span[^>]*>Showing\s+\d+[–-]\d+\s+of\s+[\d,]+\s+\w+</span>',
        '<span class="pagination-info" style="font-size:0.75rem;color:var(--text-muted);">Loading...</span>',
        content
    )
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {os.path.basename(fpath)}')
    else:
        print(f'No changes: {os.path.basename(fpath)}')

print('\nDone!')
