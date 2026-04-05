import re
import os

def add_pagination_js(fpath, table_configs):
    """Add client-side pagination JavaScript to an HTML file."""
    if not os.path.exists(fpath):
        return
    
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Check if pagination JS already exists
    if 'function renderPagination(' in content or 'renderPagination' in content:
        print(f'  SKIP (has pagination): {os.path.basename(fpath)}')
        return
    
    # Find the closing </script> tag and insert pagination JS before it
    pagination_js = '''
    // Client-side pagination helper
    let currentPage = 1;
    const pageSize = 10;
    let allData = [];

    function renderPagination(data, tbodyId, infoId, containerId, renderRowFn) {
      allData = data || [];
      const totalPages = Math.max(1, Math.ceil(allData.length / pageSize));
      if (currentPage > totalPages) currentPage = totalPages;
      const start = (currentPage - 1) * pageSize;
      const end = Math.min(start + pageSize, allData.length);
      const pageData = allData.slice(start, end);
      
      const tbody = document.getElementById(tbodyId);
      if (tbody) {
        tbody.innerHTML = '';
        if (pageData.length === 0) {
          tbody.innerHTML = '<tr><td colspan="99" style="text-align:center;padding:40px;color:var(--text-muted);">No data found</td></tr>';
        } else {
          pageData.forEach((item, i) => {
            tbody.innerHTML += renderRowFn(item, i);
          });
        }
      }
      
      const info = document.getElementById(infoId);
      if (info) {
        info.textContent = allData.length > 0 ? `Showing ${start + 1}\u2013${end} of ${allData.length}` : 'No data found';
      }
      
      const container = document.getElementById(containerId);
      if (container) {
        let html = '';
        html += `<button class="btn-outline-custom" style="padding:5px 10px;${currentPage === 1 ? 'opacity:0.5;pointer-events:none;' : ''}" onclick="changePage('${tbodyId}','${infoId}','${containerId}',${currentPage - 1})">\u2039 Prev</button>`;
        for (let i = 1; i <= totalPages; i++) {
          if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
            html += `<button class="${i === currentPage ? 'btn-primary-custom' : 'btn-outline-custom'}" style="padding:5px 10px;" onclick="changePage('${tbodyId}','${infoId}','${containerId}',${i})">${i}</button>`;
          } else if (i === currentPage - 2 || i === currentPage + 2) {
            html += `<span style="padding:5px;color:var(--text-muted);">\u2026</span>`;
          }
        }
        html += `<button class="btn-outline-custom" style="padding:5px 10px;${currentPage === totalPages ? 'opacity:0.5;pointer-events:none;' : ''}" onclick="changePage('${tbodyId}','${infoId}','${containerId}',${currentPage + 1})">Next \u203a</button>`;
        container.innerHTML = html;
      }
    }

    function changePage(tbodyId, infoId, containerId, page) {
      currentPage = page;
      // Re-render using stored data - trigger the load function
      const loadFn = window['loadFn_' + tbodyId];
      if (loadFn) loadFn();
    }
'''
    
    # Insert before </script>
    content = content.replace('</script>', pagination_js + '\n  </script>')
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ADDED pagination: {os.path.basename(fpath)}')

# Add pagination to all HTML files
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

for f in files:
    add_pagination_js(f, [])

print('\nDone adding pagination!')
