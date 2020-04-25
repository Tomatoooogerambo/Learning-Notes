#coding=utf-8
import math
import numpy as np
import matplotlib as mb
import matplotlib.pyplot as mplt
from matplotlib.pyplot import MultipleLocator

# get the common great divisor
def gcd(x, y):
    if y == 0:
        return x
    gcd(y, x%y)

# get the inverse
def get_inverse(value, p):
    return (-1 * value) % p

# get the discrete curve points
def discrete_curve(para_a, para_b, para_p):
    points_x = []
    points_y = []
    y = 0
    #计算所有在该椭圆曲线上的离散点
    for x in range(0, para_p, 1):
        #use x=i to calculate mod P 
        value= (x**3+ para_a*x + para_b) % para_p
        while True:
            if (y**2) % para_p == value:
                points_x.append(x)
                points_y.append(y)
            y += 1
            if y > para_p:
                y = 0
                break
    return points_x, points_y

# draw the curve
def draw_discrete_curve(X, Y):
    mplt.scatter(X, Y, marker='o')
    ax = mplt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    mplt.show()

# ecc divisior (mode P)
def div_mod_P(numerator, denominator, p):
    numerator %= p
    denominator %= p

    n = 1
    #求分母的逆元
    while (n * denominator) % p != 1:
        n += 1
    
    return (numerator * n) % p

# ecc point P + Q
def ecc_add(P_x, P_y, Q_x, Q_y, a, p):
    if P_x == Q_x and P_y == Q_y:
        k = div_mod_P(3*P_x**2 + a, 2*P_y, p)
    else:
        if P_x == Q_x and P_y != Q_y:
            return float("inf"), float("inf")
        else:
            k = div_mod_P(Q_y-P_y, Q_x-P_x, p)
    
    res_x = (k**2-P_x-Q_x) % p
    res_y = (k*(P_x-res_x) - P_y) % p
    return res_x, res_y

# ecc add operation n*p
# such as 2P = P + P 
#         5P = P + P + P + P + P
def ecc_linear_multi(P_x, P_y, n, a, p):
    res_x = P_x
    res_y = P_y

    if P_x == float("inf") and P_y == float("inf"):
        res_x = float("inf")
        res_y = float("inf")
    else:
        for i in range(n):
            res_x, res_y = ecc_add(res_x, res_y, P_x, P_y, a, p)

    return res_x, res_y


#get ecc order
def get_order(G_x, G_y, a, p):
    order = 1
    inverse_y = get_inverse(G_y, p)
    while True:
        res_x, res_y = ecc_linear_multi(G_x, G_y, order, a, p)
        if res_y == inverse_y:
            return order + 2
        order += 1
    
if __name__ == "__main__":
    #构造椭圆曲线 y^2 = x^3 + ax + b (mod P)
    while True:
        a = int(input("选取参数a: "))
        b = int(input("选取参数b: "))
        p = int(input("选取参数p: "))
        if (4*a**3+27*b**2) % p == 0:
            print("can't build the curve for crypto")
        else:
            break       
    print("构建椭圆曲线函数 y^2 = x^3 + {0}x + {1} (mod {2})".format(a, b, p))

    X, Y = discrete_curve(a, b, p)
    print(X)
    print(Y)
    G_x = int(input("选取参数G点x坐标: "))
    G_y = int(input("选取参数G点y坐标: "))
    ecc_order = get_order(G_x, G_y, a, p)
    print("=======order is : ===========", ecc_order)
    # draw_discrete_curve(X, Y)

    #test add operation
    # resX, resY = ecc_add(3, 10, 9, 7, a, p)
    # print("({}, {})".format(resX, resY))

    # for i in range(23):
    #     resX, resY = ecc_linear_multi(G_x, G_y, i, a, p)
    #     print("{}G: ({}, {})".format(i+1, resX, resY))

    # get the priv_K
    priv_K = int(input("输入私钥: < {}  :".format(ecc_order)))
    
    # get the pub_K
    pub_K = ecc_linear_multi(G_x, G_y, priv_K, a, p)
    print("public infomation  is: ECC:a={} b={} p={} G({}, {}),  public_K: Q({}, {})".format(a, b, p, G_x, G_y, pub_K[0], pub_K[1]))

    #get c1= M + r*pub_K
    #get c2 = r* G
    random = int(input("输入随机数: "))
    message_X = int(input("输入要加密的明文x"))
    message_Y = int(input("输入要加密的明文y"))

    C_1_tail = ecc_linear_multi(pub_K[0], pub_K[1], random, a, p)
    print("-------------------C1_tail:({}, {}) ".format(C_1_tail[0], C_1_tail[1]))
    C_1 = ecc_add(message_X, message_Y, C_1_tail[0], C_1_tail[1], a, p)
    C_2 = ecc_linear_multi(G_x, G_y, random, a, p)
    print("cipher is C1:{} , C2:{}".format(C_1, C_2))

    print("======================start to decrypto==============")
    miners_priv_C_2 = ecc_linear_multi(C_2[0], C_2[1], priv_K, a, p)
    miners_X, miners_Y = miners_priv_C_2[0], (-1 * miners_priv_C_2[1]) % p

    print("-------------------C2*priv: ({}, {})".format(miners_priv_C_2[0], miners_priv_C_2[1]))
    print("-------------------inverse: ({}, {})".format(miners_X, miners_Y))


    res_x, res_y = ecc_add(C_1[0], C_1[1], miners_X, miners_Y, a, p)
    print("===============Alice get the message: M({}, {})".format(res_x, res_y))
    

