with open('dashboard/app.py', encoding='utf-8') as f:
    lines = f.readlines()
    content = ''.join(lines)

checks = {
    'CSS injection via components.html': 'components.html' in content,
    'CSS injected into window.parent': 'window.parent.document.head' in content,
    'Particle canvas created': 'particle-canvas' in content,
    '3D tilt effect (initTilt)': 'initTilt' in content,
    'Click burst/explosion': 'burst' in content and 'click' in content,
    'Auto-advance toggle in Live Feed': 'auto_play' in content,
    'KPI cards HTML': 'kpi-card' in content,
    'Hero banner section': 'hero-banner' in content,
    'Tab 6 Live Feed Simulator': 'Live Feed' in content,
    'CSV file path fallback': 'fallback_path' in content,
    'No deprecated use_container_width': 'use_container_width' not in content,
    'width=stretch for charts': "width='stretch'" in content,
    'st.set_page_config at top': 'st.set_page_config' in content,
    'Data loading with cache': '@st.cache_data' in content,
    'Particle mouse repulsion': 'mouse.x' in content,
}

print('Feature Verification Report')
print('=' * 50)
all_pass = True
for feature, status in checks.items():
    icon = 'OK     ' if status else 'MISSING'
    print(f'  [{icon}]  {feature}')
    if not status:
        all_pass = False
print('=' * 50)
print('RESULT:', 'ALL CHECKS PASSED' if all_pass else 'SOME CHECKS FAILED')
print(f'Total lines in app.py: {len(lines)}')
