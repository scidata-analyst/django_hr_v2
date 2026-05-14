import re
import os

def update_file_pagination(fpath, config):
    """Update a file's JavaScript to use proper pagination."""
    if not os.path.exists(fpath):
        print(f'SKIP: {os.path.basename(fpath)}')
        return
    
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Remove duplicate pagination blocks
    content = re.sub(
        r'\n\s*// Client-side pagination helper.*?function changePage\([^)]+\) \{[^}]+\}\n',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Remove duplicate });
    content = re.sub(r'\}\);\s*\n\s*\}\);\s*\n\s*\}\s*\n\s*</script>', '});\n  </script>', content)
    
    # Add pagination info containers after each tbody
    for tbody_id in config.get('tbody_ids', []):
        if f'id="{tbody_id}"' in content or f"id='{tbody_id}'" in content:
            # Check if pagination container already exists
            info_id = tbody_id.replace('-tbody', '-pagination-info')
            container_id = tbody_id.replace('-tbody', '-pagination')
            if info_id not in content:
                # Add pagination containers after the table
                content = content.replace(
                    f'</tbody>\n              </table>',
                    f'</tbody>\n              </table>\n            </div>\n            <div style="padding:14px 20px;display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--border);flex-wrap:wrap;gap:8px;">\n              <span id="{info_id}" style="font-size:0.75rem;color:var(--text-muted);">Loading...</span>\n              <div id="{container_id}" style="display:flex;gap:4px;"></div>\n            </div>\n            <div style="overflow-x:auto;">\n              <table class="table-custom">'
                )
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'Updated: {os.path.basename(fpath)}')

# Config for each file
configs = {
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\payroll.html': {
        'tbody_ids': ['structures-tbody', 'payslips-tbody', 'loans-tbody', 'bonuses-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\recruitment.html': {
        'tbody_ids': ['jobs-tbody', 'candidates-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\onboarding.html': {
        'tbody_ids': ['onboarding-tbody', 'exit-interviews-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\core_module\templates\pages\ess.html': {
        'tbody_ids': ['expenses-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\performance.html': {
        'tbody_ids': ['reviews-tbody', 'goals-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\training.html': {
        'tbody_ids': ['courses-tbody', 'enrollments-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\talent.html': {
        'tbody_ids': ['profiles-tbody', 'succession-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\talent_growth\templates\pages\engagement.html': {
        'tbody_ids': ['surveys-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\branding.html': {
        'tbody_ids': ['branding-candidates-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\compliance.html': {
        'tbody_ids': ['policies-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\health.html': {
        'tbody_ids': ['benefits-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\global.html': {
        'tbody_ids': ['offices-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\integrations.html': {
        'tbody_ids': ['integrations-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\operation\templates\pages\reports.html': {
        'tbody_ids': ['reports-tbody']
    },
    r'F:\DASHBOARD_APP\HR_APP-2\root\main\templates\index.html': {
        'tbody_ids': ['recent-hires-tbody']
    },
}

for fpath, config in configs.items():
    update_file_pagination(fpath, config)

print('\nDone!')
