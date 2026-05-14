import re
import os

def fix_html_file(fpath, table_configs):
    """
    Fix an HTML file by:
    1. Adding IDs to tbody elements
    2. Adding pagination container IDs
    3. Removing mock data from tbody
    4. Fixing null reference issues
    """
    if not os.path.exists(fpath):
        print(f'NOT FOUND: {fpath}')
        return False
    
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    original = content
    
    for config in table_configs:
        # Replace mock tbody content with loading placeholder
        old_tbody = config.get('old_tbody_pattern')
        new_tbody = config.get('new_tbody', '<tbody><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading...</td></tr></tbody>')
        
        if old_tbody:
            content = re.sub(old_tbody, new_tbody, content, flags=re.DOTALL)
        
        # Add pagination container if not exists
        pag_container = config.get('pagination_container')
        if pag_container and pag_container not in content:
            # Find the pagination area and replace it
            old_pag = config.get('old_pagination_pattern')
            if old_pag:
                content = re.sub(old_pag, pag_container, content, flags=re.DOTALL)
    
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {os.path.basename(fpath)}')
        return True
    else:
        print(f'No changes: {os.path.basename(fpath)}')
        return False

# Fix attendance.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\attendance.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td>\s*<div style="display:flex;align-items:center;gap:8px;">\s*<div class="avatar av-blue"[^>]*>SA</div>Sara\s*Ahme',
            'new_tbody': '<tbody id="leaves-tbody"><tr><td colspan="8" style="text-align:center;padding:40px;color:var(--text-muted);">Loading leave requests...</td></tr></tbody>',
        },
        {
            'old_pagination_pattern': r'<span[^>]*>Showing 1–\d+ of [\d,]+ employees</span>',
            'pagination_container': '<span id="leaves-pagination-info" style="font-size:0.75rem;color:var(--text-muted);">Loading...</span><div id="leaves-pagination" style="display:flex;gap:4px;"></div>',
        }
    ]
)

# Fix payroll.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\payroll.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Grade A</td>',
            'new_tbody': '<tbody id="structures-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading salary structures...</td></tr></tbody>',
        }
    ]
)

# Fix recruitment.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\recruitment.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Senior Backend Developer</td>',
            'new_tbody': '<tbody id="jobs-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading job postings...</td></tr></tbody>',
        }
    ]
)

# Fix onboarding.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\onboarding.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Kabir Hossain</td>\s*<td>Offer Letter Signed</td>',
            'new_tbody': '<tbody id="onboarding-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading onboarding tasks...</td></tr></tbody>',
        }
    ]
)

# Fix ess.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\ess.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Travel</td>',
            'new_tbody': '<tbody id="expenses-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading expense claims...</td></tr></tbody>',
        }
    ]
)

# Fix performance.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\performance.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Kabir Hossain</td>\s*<td>Engineering</td>\s*<td>Q4 2025</td>',
            'new_tbody': '<tbody id="reviews-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading performance reviews...</td></tr></tbody>',
        }
    ]
)

# Fix training.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\training.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Leadership Excellence</td>',
            'new_tbody': '<tbody id="courses-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading training courses...</td></tr></tbody>',
        }
    ]
)

# Fix talent.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\talent.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Kabir Hossain</td>\s*<td>Senior Developer</td>',
            'new_tbody': '<tbody id="profiles-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading talent profiles...</td></tr></tbody>',
        }
    ]
)

# Fix engagement.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\engagement.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Q1 2026 Employee Engagement Survey</td>',
            'new_tbody': '<tbody id="surveys-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading surveys...</td></tr></tbody>',
        }
    ]
)

# Fix branding.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\branding.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Arif Hossain</td>',
            'new_tbody': '<tbody id="branding-candidates-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading candidates...</td></tr></tbody>',
        }
    ]
)

# Fix compliance.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\compliance.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;"><i class="bi bi-file-earmark-pdf"[^>]*></i> Remote Work Policy</td>',
            'new_tbody': '<tbody id="policies-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading policies...</td></tr></tbody>',
        }
    ]
)

# Fix health.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\health.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Family Medical Insurance</td>',
            'new_tbody': '<tbody id="benefits-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading benefit plans...</td></tr></tbody>',
        }
    ]
)

# Fix global.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\global.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td><span style="font-weight:600;">Bangladesh</span></td>',
            'new_tbody': '<tbody id="offices-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading offices...</td></tr></tbody>',
        }
    ]
)

# Fix integrations.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\integrations.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Google Calendar</td>',
            'new_tbody': '<tbody id="integrations-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading integrations...</td></tr></tbody>',
        }
    ]
)

# Fix reports.html
fix_html_file(
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\reports.html',
    [
        {
            'old_tbody_pattern': r'<tbody>\s*<tr>\s*<td style="font-weight:600;">Attendance Report</td>',
            'new_tbody': '<tbody id="reports-tbody"><tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">Loading reports...</td></tr></tbody>',
        }
    ]
)

print('\nDone fixing HTML files!')
