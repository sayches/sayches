import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from django.conf import settings
from users.models import UserRSA


class MessagingRSA:
    @classmethod
    def create_rsa(cls, request):
        password = request.session.get('encryption_token')
        salt = settings.SECRET_KEY
        master_key = PBKDF2(password, salt, count=10000)

        def random(n):
            random.counter += 1
            return PBKDF2(master_key, "random:%d" % random.counter, dkLen=n, count=1)

        random.counter = 0
        key = RSA.generate(2048, randfunc=random)
        if not UserRSA.objects.filter(user=request.user):
            UserRSA.objects.create(
                user=request.user,
                public_pem=key.publickey().exportKey('PEM').decode()
            )
        request.session['private_pem'] = key.exportKey('PEM').decode()
        request.session.modified = True
        return key

    @classmethod
    def encrypt(cls, request, receiver, msg):
        if not request.session.get('user_public_pem'):
            sender_pem = UserRSA.objects.get(user=request.user)
            request.session['user_public_pem'] = sender_pem.public_pem
            request.session.modified = True
        sender_pem = request.session.get('user_public_pem')
        receiver_pem = UserRSA.objects.get(user=receiver).public_pem
        cipher_receiver = PKCS1_OAEP.new(key=RSA.import_key(bytes(receiver_pem, 'utf-8')))
        cipher_sender = PKCS1_OAEP.new(key=RSA.import_key(bytes(sender_pem, 'utf-8')))
        data = {
            'receiver_msg': base64.b64encode(cipher_receiver.encrypt(bytes(msg, 'utf-8'))).decode(),
            'sender_msg': base64.b64encode(cipher_sender.encrypt(bytes(msg, 'utf-8'))).decode(),
        }
        return data

    @classmethod
    def decrypt(cls, request, msg):
        if not request.session.get('private_pem'):
            cls.create_rsa(request)
        sender_pem = request.session.get('private_pem')
        cipher_sender = PKCS1_OAEP.new(key=RSA.import_key(bytes(sender_pem, 'utf-8')))
        msg = cipher_sender.decrypt(base64.b64decode(msg.encode())).decode()
        return msg
