{
    "name": "Readonly Channel",
    "version": "1.0",
    "depends": ["mail"],  # Tergantung pada modul 'mail' karena modul Discuss menggunakan 'mail'
    "author": "Laila",
    "category": "Tools",
    "summary": "Add readonly feature to Discuss channels",
    "description": "Makes specific channels readonly to regular members",
    "data": [
        "views/discuss_channel_views.xml",
    ],
    "installable": True,
    "application": False,
}