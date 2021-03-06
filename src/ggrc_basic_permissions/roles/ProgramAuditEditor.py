scope = "Audit Implied"
description = """
  A user with the ProgramEditor role for a private program will also have this
  role in the audit context for any audit created for that program.
  """
permissions = {
    "read": [
        "Request",
        "DocumentationResponse",
        "InterviewResponse",
        "PopulationSampleResponse",
        "Audit",
        "AuditObject",
        "Meeting",
        "ObjectControl",
        "ObjectDocument",
        "ObjectObjective",
        "ObjectPerson",
        "ObjectSection",
        "Relationship",
        "Document",
        "Meeting",
        "UserRole",
        "Context",
    ],
    "create": [
        "Request",
        "DocumentationResponse",
        "InterviewResponse",
        "PopulationSampleResponse",
        "Meeting",
        "ObjectControl",
        "ObjectDocument",
        "ObjectObjective",
        "ObjectPerson",
        "ObjectSection",
        "Relationship",
        "Document",
        "Meeting",
        "Response",
        "AuditObject"
    ],
    "view_object_page": [
        "__GGRC_ALL__"
    ],
    "update": [
        {
            "terms": {
                "property_name": "status",
                "value": [
                    "Requested",
                    "Amended Request"
                ]
            },
            "type": "Request",
            "condition": "in"
        },
        {
            "terms": {
                "property_name": "assignee",
                "value": "$current_user"
            },
            "type": "Request",
            "condition": "is"
        },
        "DocumentationResponse",
        "InterviewResponse",
        "PopulationSampleResponse",
        "Audit",
        "AuditObject",
        "Meeting",
        "ObjectControl",
        "ObjectDocument",
        "ObjectObjective",
        "ObjectPerson",
        "ObjectSection",
        "Relationship",
        "Document",
        "Meeting"
    ],
    "delete": [
        "ObjectControl",
        "ObjectDocument",
        "ObjectObjective",
        "ObjectPerson",
        "ObjectSection",
        "Relationship",
        "Document",
        "Meeting",
        "AuditObject"
    ]
}
