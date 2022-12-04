# Create your views here.
import pandas as pd
import phe
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from smpcp import CloudPlatform, CloudPlatformThird, SecureMultiPartyComputationProtocol
import app
from app import algorithm

from app.src.keypair import generate_keypair as gk
from app.src.path import PK_PATH, SK_PATH

CR = ''


@csrf_exempt
def realindex(request):
    return render(request, "realindex.html")

@csrf_exempt
def index(request):
    return render(request, "index.html")

@csrf_exempt
def example(request):
    return render(request, "example.html")

@csrf_exempt
def views(request):
    return render(request, "views.html")

@csrf_exempt
def knn(request):
    qx=int(request.POST.get('qx'))
    qy=int(request.POST.get('qy'))
    k=int(request.POST.get('k'))
    length=int(request.POST.get('length'))

    b,ans=algorithm.sknn(qx,qy,k,length)

    res=json.dumps({
        'answer':b,
        'answerpoint':ans
    })

    return JsonResponse({
        'answerstr':res
    })
    

@csrf_exempt
def generate_keypair(request):
    return JsonResponse({'kp': gk(int(request.POST.get("kl")))})


@csrf_exempt
def encryption(request):
    pk = phe.PaillierPublicKey(n=int(pd.read_pickle(PK_PATH).loc['n'][0]))

    c1 = pk.encrypt(float(request.POST.get("p1")))
    c2 = pk.encrypt(float(request.POST.get("p2")))

    return JsonResponse({'c1': str(hex(c1._EncryptedNumber__ciphertext).upper()),
                         'c2': str(hex(c2._EncryptedNumber__ciphertext)).upper()})


@csrf_exempt
def calculation(request):
    global CR

    pk = phe.PaillierPublicKey(n=int(pd.read_pickle(PK_PATH).loc['n'][0]))
    private_key = pd.read_pickle(SK_PATH)
    sk = phe.PaillierPrivateKey(p=int(private_key.loc['p'][0]),
                                public_key=pk, q=int(private_key.loc['q'][0]))

    cloud1 = CloudPlatform(public_key=pk)
    cloud2 = CloudPlatformThird(public_key=pk, secret_key=sk)
    protocol = SecureMultiPartyComputationProtocol(c1=cloud1, c2=cloud2)

    n1 = protocol.encode(pk.encrypt(float(request.POST.get("p1"))))
    n2 = pk.encrypt(float(request.POST.get("p2")))

    ptc = request.POST.get("ptc")
    if ptc == 'SM':
        cr = n1 * n2
    elif ptc == 'SDC':
        cr = n1 / n2
    elif ptc == 'SMAX':
        cr = n1.optimum(n2, 'max')
    elif ptc == 'SMIN':
        cr = n1.optimum(n2, 'min')
    elif ptc == 'Parity':
        cr = n1.parity()
    elif ptc == 'SBD':
        cr = []
        bit = []
        for v in n1.bit_dec(int(request.POST.get("p1")).bit_length()):
            cr.append(v)
            bit.append(hex(v._EncryptedNumber__ciphertext).upper())
        CR = cr
        return JsonResponse({'cr': str(bit)})
    elif ptc == 'SAND':
        cr = n1 & n2
    elif ptc == 'SBOR':
        cr = n1 | n2
    elif ptc == 'SNOT':
        cr = n1.bit_not()
    elif ptc == 'Not-And':
        cr = n1 ^ n2
    elif ptc == 'SEQ':
        cr = n1 == n2
    elif ptc == 'SNEQ':
        cr = n1 != n2
    elif ptc == 'Greater-Than':
        cr = n1 > n2
    elif ptc == 'Greater-Equal':
        cr = n1 >= n2
    elif ptc == 'SLESS':
        cr = n1 < n2
    elif ptc == 'SLEQ':
        cr = n1 <= n2
    else:

        CR = ''

        return JsonResponse({'cr': ''})

    CR = cr

    return JsonResponse({'cr': str(hex(cr._EncryptedNumber__ciphertext).upper())})


@csrf_exempt
def decryption(request):
    pk = phe.PaillierPublicKey(n=int(pd.read_pickle(PK_PATH).loc['n'][0]))
    private_key = pd.read_pickle(SK_PATH)
    sk = phe.PaillierPrivateKey(p=int(private_key.loc['p'][0]),
                                public_key=pk, q=int(private_key.loc['q'][0]))

    global CR
    if isinstance(CR, list):
        dr = []
        for v in CR:
            dr.append(sk.decrypt(v))
        return JsonResponse({'dr': str(dr)})

    dr = sk.decrypt(CR)

    return JsonResponse({'dr': str(round(dr, 10))})
