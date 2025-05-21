class ProfileResponse:
    def __init__(self, name, email, avatar_url, bio, age, gender, location, interests, created_at):
        self.name = name
        self.email = email
        self.avatar_url = avatar_url
        self.bio = bio
        self.age = age
        self.gender = gender
        self.location = location
        self.interests = interests
        self.created_at = created_at