class RBUser:
    def __init__(self, username: str | None = None,
                 fname: str | None = None,
                 lname: str | None = None,
                 sex: str | None = None,
                 email: str | None = None,
                 phone: str | None = None):
        self.username = username
        self.fname = fname
        self.lname = lname
        self.sex = sex
        self.email = email
        self.phone = phone
        
    def to_dict(self) -> dict:
        data = {'username': self.username, 'fname': self.fname, 'lname': self.lname, 'sex': self.sex,
                'email': self.email, 'phone': self.phone}

        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data