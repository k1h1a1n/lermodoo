{'name':'LERM',
 'summary': "Laboratory Enterprise Resource Management",
 'author': "Usman Shaikhnag", 
 'website': "http://www.esehat.org", 
 'category': 'Lerm', 
 'version': '13.0.1', 
 'depends':['base' , 'contacts' , 'product', 'stock'],
 'data': [
          "views/report.xml",
          'views/lab.xml',
          'data/data.xml',
          'views/test_sample.xml',
          'views/lab_sample.xml',
          'views/test_parameter.xml',
          'views/lab_contact.xml',
          'views/lab_qualification.xml',
          'views/sample_assignment.xml',
          'views/lab_notebook.xml',
          'reports/test_report_action.xml',
          'reports/test_report_templates.xml',
          'security/groups.xml',
          'security/ir.model.access.csv'
          ]
}