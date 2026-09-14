{
    'name': 'AA Gantt — Project Tasks',
    'version': '19.0.1.4',
    'summary': 'Wires aa_gantt onto all Project task menus (Enterprise-style planned dates)',
    'author': 'Aldo A.',
    'category': 'Project',
    'depends': ['project', 'aa_gantt'],
    'data': [
        'views/project_task_gantt_view.xml',
        'views/project_task_form_dates.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
    'installable': True,
    'application': False,
    'license': 'OPL-1',
    'price': 0,
    'currency': 'USD',
}
