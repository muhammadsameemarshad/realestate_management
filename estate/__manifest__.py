{
    'name':"Real-Estate Management",
    'version':'14.1.0',
    'depends':['base'],
    'sequence':'1',
    'author':"Sameem Arshad",
    'category':'Category',
    'description':"""This is a  module of Real-Estate Management for Axiom World""",
    'data': [
    'security/ir.model.access.csv',
    # 'views/estate_menu.xml',
    'views/estate_property_views.xml',
    'views/estate_property_list_view.xml',
    'views/estate_property_form_view.xml',
    'views/estate_property_search_view.xml',
    # 'views/estate_property_offer_views.xml',

],

    'installable': True,
    'auto_install': False,
    'application':  True,
}