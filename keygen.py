import secrets

def generate_django_secret_key():
    secret_key = ''.join([secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    return secret_key

print(generate_django_secret_key())
