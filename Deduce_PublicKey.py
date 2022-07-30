import hashlib
import random
from Crypto.Util.number import *
from bitarray import bitarray
import mmh3

# 随机找到G点
Gx = 2
Gy = 7
n=13
# G的阶为13


a=1
b=6
#prime = getPrime(128)  # 模数prime，就是文中的p
prime=11
# 设置私钥k
d=random.randint(1,n)
k=random.randint(1,n)

# 求value在Fp域的逆——用于分数求逆
def get_inverse(value, p):
    for k in range(1, p):
        if (k * value) % p == 1:
            return k
    return -1


# 求最大公约数——用于约分化简
def get_gcd(x, k):
    if k == 0:
        return x
    else:
        return get_gcd(k, x % k)

# 计算P+Q函数
def calculate_p_q(x1, y1, x2, y2, a, b, p):
    flag = 1  # 控制符号位

    # 若P = Q，则k=[(3x1^2+a)/2y1]mod p
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a  # 计算分子
        denominator = 2 * y1  # 计算分母

    # 若P≠Q，则k=(y2-y1)/(x2-x1) mod p
    else:
        member = y2 - y1  # 分子
        denominator = x2 - x1  # 分母
        if member * denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)

    # 将分子和分母化为最简
    gcd_value = get_gcd(member, denominator)
    member = member // gcd_value
    denominator = denominator // gcd_value

    # 求分母的逆元
    inverse_value = get_inverse(denominator, p)
    k = (member * inverse_value)
    if flag == 0:
        k = -k
    k = k % p

    # 计算x3,y3
    """
        x3≡k^2-x1-x2(mod p)
        y3≡k(x1-x3)-y1(mod p)
    """
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return [x3, y3]


# 计算SHA-256加密
def hash256(m):
    return hashlib.sha256(m.encode()).hexdigest()


# 计算nP函数
def calculate_np(p_x, p_y, a, b, p, n):
    tem_x = p_x
    tem_y = p_y
    for k in range(n - 1):
        p_value = calculate_p_q(tem_x, tem_y, p_x, p_y, a, b, p)
        tem_x = p_value[0]
        tem_y = p_value[1]
    # return p_value
    return [tem_x, tem_y]

P = calculate_np(Gx, Gy, a, b, prime, d)
Px = P[0]
Py = P[1]
print("公钥为：",P)

K = calculate_np(Gx, Gy, a, b, prime, k)
Kx = K[0]
Ky = K[1]
print("x1:",Kx)
print("y1:",Ky)

m='hello'
e=hash256(m)
#计算签名r，s
r=(int(e,16)+Kx)%n
d_=get_inverse(d+1,n)
s=(d_*(k-r*d))%n
print("输出签名r为:",r,"s:",s)
signature=[r,s]


#Deduce public key from signature
def Deduce(sig,message):
    r1=sig[0]
    s1=sig[1]
    e1=hash256(message)
    kGx=(r1-int(e1,16))%n
    print("kG横坐标为:",kGx)
    for i in range(prime):
        if (i * i - (kGx * kGx * kGx + a * kGx + b)) % prime == 0:
            kGy1=i
            break

    kGy2=prime-i
    print("kG可能的纵坐标为:",kGy1,kGy2)
    sG=calculate_np(Gx, Gy, a, b, prime, s1)
    sGx=sG[0]
    sGy=sG[1]

    #计算kG-sG（有两种情况）
    k_sG1=calculate_p_q(kGx, kGy1, sGx-2*sGx, sGy-2*sGy, a, b, prime)
    k_sG1x=k_sG1[0]
    k_sG1y=k_sG1[1]

    s_r = get_inverse(s1+r1,n)
    PA1=calculate_np(k_sG1x, k_sG1y, a, b, prime, s_r)

    k_sG2 = calculate_p_q(kGx, kGy2, sGx-2*sGx, sGy-2*sGy, a, b, prime)
    k_sG2x = k_sG2[0]
    k_sG2y = k_sG2[1]
    PA2 = calculate_np(k_sG2x, k_sG2y, a, b, prime, s_r)

    return PA1,PA2

pa1,pa2=Deduce(signature,m)
print("公钥1为：",pa1)
print("公钥2为：",pa2)
