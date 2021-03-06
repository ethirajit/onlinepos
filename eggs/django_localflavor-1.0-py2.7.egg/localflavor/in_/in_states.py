#: A list of states
STATE_CHOICES = (
    ('KA', 'Karnataka'),
    ('AP', 'Andhra Pradesh'),
    ('KL', 'Kerala'),
    ('TN', 'Tamil Nadu'),
    ('MH', 'Maharashtra'),
    ('UP', 'Uttar Pradesh'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('RJ', 'Rajasthan'),
    ('HP', 'Himachal Pradesh'),
    ('JK', 'Jammu and Kashmir'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CG', 'Chattisgarh'),
    ('HR', 'Haryana'),
    ('JH', 'Jharkhand'),
    ('MP', 'Madhya Pradesh'),
    ('MN', 'Manipur'),
    ('ML', 'Meghalaya'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OR', 'Orissa'),
    ('PB', 'Punjab'),
    ('SK', 'Sikkim'),
    ('TR', 'Tripura'),
    ('UA', 'Uttarakhand'),
    ('WB', 'West Bengal'),

    # Union Territories
    ('AN', 'Andaman and Nicobar'),
    ('CH', 'Chandigarh'),
    ('DN', 'Dadra and Nagar Haveli'),
    ('DD', 'Daman and Diu'),
    ('DL', 'Delhi'),
    ('LD', 'Lakshadweep'),
    ('PY', 'Pondicherry'),
)

#: Normalized state names
STATES_NORMALIZED = {
    'an': 'AN',
    'andaman and nicobar': 'AN',
    'andra pradesh': 'AP',
    'andrapradesh': 'AP',
    'andhrapradesh': 'AP',
    'ap': 'AP',
    'andhra pradesh': 'AP',
    'ar': 'AR',
    'arunachal pradesh': 'AR',
    'assam': 'AS',
    'as': 'AS',
    'bihar': 'BR',
    'br': 'BR',
    'cg': 'CG',
    'chattisgarh': 'CG',
    'ch': 'CH',
    'chandigarh': 'CH',
    'daman and diu': 'DD',
    'dd': 'DD',
    'dl': 'DL',
    'delhi': 'DL',
    'dn': 'DN',
    'dadra and nagar haveli': 'DN',
    'ga': 'GA',
    'goa': 'GA',
    'gj': 'GJ',
    'gujarat': 'GJ',
    'himachal pradesh': 'HP',
    'hp': 'HP',
    'hr': 'HR',
    'haryana': 'HR',
    'jharkhand': 'JH',
    'jh': 'JH',
    'jammu and kashmir': 'JK',
    'jk': 'JK',
    'karnataka': 'KA',
    'karnatka': 'KA',
    'ka': 'KA',
    'kerala': 'KL',
    'kl': 'KL',
    'ld': 'LD',
    'lakshadweep': 'LD',
    'maharastra': 'MH',
    'mh': 'MH',
    'maharashtra': 'MH',
    'meghalaya': 'ML',
    'ml': 'ML',
    'mn': 'MN',
    'manipur': 'MN',
    'madhya pradesh': 'MP',
    'mp': 'MP',
    'mizoram': 'MZ',
    'mizo': 'MZ',
    'mz': 'MZ',
    'nl': 'NL',
    'nagaland': 'NL',
    'orissa': 'OR',
    'odisa': 'OR',
    'orisa': 'OR',
    'or': 'OR',
    'pb': 'PB',
    'punjab': 'PB',
    'py': 'PY',
    'pondicherry': 'PY',
    'rajasthan': 'RJ',
    'rajastan': 'RJ',
    'rj': 'RJ',
    'sikkim': 'SK',
    'sk': 'SK',
    'tamil nadu': 'TN',
    'tn': 'TN',
    'tamilnadu': 'TN',
    'tamilnad': 'TN',
    'tr': 'TR',
    'tripura': 'TR',
    'ua': 'UA',
    'uttarakhand': 'UA',
    'up': 'UP',
    'uttar pradesh': 'UP',
    'westbengal': 'WB',
    'bengal': 'WB',
    'wb': 'WB',
    'west bengal': 'WB'
}
