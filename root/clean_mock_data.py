import re
import os

def clean_tbody(content):
    """Find all tbody blocks that contain mock data and replace with loading placeholder."""
    # Pattern to match tbody with actual content (not just loading message)
    pattern = r'<tbody[^>]*>(.*?)</tbody>'
    
    def replace_tbody(match):
        inner = match.group(1).strip()
        # If already has loading message, keep it
        if 'Loading' in inner and 'colspan' in inner:
            return match.group(0)
        # If empty or whitespace only, add loading
        if not inner or inner.isspace():
            return '<tbody><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading...</td></tr></tbody>'
        # If has mock data (contains <tr> with actual content), replace
        if '<tr>' in inner:
            # Count cols from thead if possible, otherwise use 99
            return '<tbody><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading...</td></tr></tbody>'
        return match.group(0)
    
    return re.sub(pattern, replace_tbody, content, flags=re.DOTALL)

files = [
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

for fpath in files:
    if not os.path.exists(fpath):
        print(f'SKIP: {os.path.basename(fpath)}')
        continue
    
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    new_content = clean_tbody(content)
    
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'CLEANED: {os.path.basename(fpath)}')
    else:
        print(f'OK: {os.path.basename(fpath)}')

print('\nDone!')
