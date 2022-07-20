import ecdsa
import random
import hashlib

#python中有对应的椭圆曲线签名的ECDSA库，这里以椭圆曲线NIST256p为例，选取椭圆曲线中的一个点
gen = ecdsa.NIST256p.generator
order = gen.order()
privateKey = random.randrange(1,order-1)
#生成公钥和私钥对象
public_Key = ecdsa.ecdsa.Public_key(gen,gen * privateKey)
private_key = ecdsa.ecdsa.Private_key(public_Key,privateKey)
message = "shandongdaxue"
#对明文message进行哈希
Hash = int(hashlib.sha1(message.encode("utf8")).hexdigest(),16)
#生成临时密钥k
k = random.randrange(1,rank-1)
#利用私钥进行数字签名得到r，s作为签名值并输出
sig = private_key.sign(Hash,k)
r = sig.r
s = sig.s

def recover_key(digest, signature, i):
    #生成椭圆曲线curve
    curve = ecdsa.SECP256k1.curve
    #寻找椭圆曲线生成元G
    G = ecdsa.SECP256k1.generator
    #得到生成元的阶n
    order = ecdsa.SECP256k1.order
    yp = (i % 2)
    #生成椭圆曲线签名r，s
    r, s = ecdsa.util.sigdecode_string(signature, order)
    x = r + (i // 2) * order
    #构造椭圆曲线，其中a，b，p是椭圆曲线的参数和阶
    alpha = ((x * x * x) + (curve.a() * x) + curve.b()) % curve.p()
    beta = ecdsa.numbertheory.square_root_mod_prime(alpha, curve.p())
    y = beta if (beta - yp) % 2 == 0 else curve.p() - beta
    # 生成R点
    R = ecdsa.ellipticcurve.Point(curve, x, y, order)
    e = ecdsa.util.string_to_number(digest)
    # 生成Q点
    Q = ecdsa.numbertheory.inverse_mod(r, order) * (s * R + (-e % order) * G)
    # verify message
    if not ecdsa.VerifyingKey.from_public_point(Q, curve=ecdsa.SECP256k1).verify_digest(signature, digest, sigdecode=ecdsa.util.sigdecode_string):
        return None
    return ecdsa.VerifyingKey.from_public_point(Q, curve=ecdsa.SECP256k1)
