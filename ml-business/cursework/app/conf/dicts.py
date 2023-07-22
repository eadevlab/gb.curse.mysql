import calendar

CATEGORICAL_FEATURES_MAPS = {
    'poutcome': {'unknown':0,'failure': -1, 'other': 0, 'success': 1},
    'contact': {'unknown':0, 'cellular': 1, 'telephone': 2},
    'education': {'unknown':0, 'primary': 1, 'secondary': 2, 'tertiary': 3},
    'marital': {'unknown':0, 'married': 1, 'single': 0, 'divorced': 0},
    'job': {
        'unemployed': 0, 'services': 1, 'management': 1, 'blue-collar': 1,
        'self-employed': 1, 'technician': 1, 'entrepreneur': 1, 'admin.': 1, 'student': 0, 'housemaid': 0,'retired': 0,'unknown': 0
    },
    'month': {month.lower(): index for index, month in enumerate(calendar.month_abbr) if month},
    'default': {'no': 0, 'yes': 1},
    'housing': {'no': 0, 'yes': 1},
    'loan': {'no': 0, 'yes': 1}
}

