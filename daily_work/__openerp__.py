{ 
"name" : "Daily Work Module", 
"author" : "Techanipr", 
"version" : "1.0", 
"category" : "HR",
"depends" : ["hr_timesheet"],
"demo_xml" : [], 
"data" : ["daily_work_view.xml",
          'security/daily_work_security.xml',
        'security/ir.model.access.csv'
        ],
    'auto_install': False,
    'application': True, 
        "installable": True 
}