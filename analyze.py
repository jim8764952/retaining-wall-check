import matplotlib.pyplot as plt
from math import sin, cos, tan, radians, asin, degrees, sqrt
from math import exp, pi, atan
from mpmath import cot

# R = radians

# 使用 Rankine 土壓力計算方法檢核傾倒

# 擋土牆型式
# 重力式尺寸比例
# H = 6.7      # 牆總高度(m)
# H2 = 0.7      # 底板厚度(m)
# D = 1.5     # 牆底至牆趾地表深(m)
# B = 4      # 底板總寬度(m)
# B1 = 0.7      # 牆趾寬(m)
# B2 = 0.5      # 牆頂寬(m)
# B3 = 2.6      # 牆跟寬(m)
# S1 = 0.2/6       # 牆面斜率(最少0.02)
# S2 = 0       # 牆背面斜率 0 = 垂直

# ## 地層材料
# r2 = 19     # γ2地層單位重(kN/m3)
# Phi2 = 20       # ϕ2 地層摩擦角(deg)
# c2 = 40     # c2地層凝聚力(kN/m2)
# ## 回填土
# alpha = 10       # α回填土地表傾角(deg)
# r1 = 18        # γ1回填土單位重(kN/m3)
# Phi1 = 30        # ϕ1 回填土摩擦角(deg)
# c1 = 0       # c1回填土凝聚力(kN/m2)

# ## 材料
# rc = 23.58        # γc混凝土單位重(kN/m3)


def graph(H=6.7, H2=0.7, D=1.5, B=4, B1=0.7,
          B2=0.5, B3=2.6, S1=0.2/6, S2=0, alpha=10):
    fig = plt.figure(figsize=(4, 2.5), dpi=100)

    def aver(x0, x1):
        return (x0 + x1)/2
    # 牆
    x0, y0 = [0, 0]
    x1, y1 = [B, 0]
    x2, y2 = [B, H2]
    x3, y3 = [B-B3, H2]
    x4, y4 = [x3 - (H-H2)*S2, H]
    x5, y5 = [x4 - B2, H]
    x6, y6 = [B1, H2]
    x7, y7 = [0, H2]

    conx = [x0, x1, x2, x3, x4, x5, x6, x7, x0]
    cony = [y0, y1, y2, y3, y4, y5, y6, y7, y0]
    plt.plot(conx, cony, color="black")
    # 回填土
    xs1, ys1 = [B, H+(B3 + (H-H2)*S2)*tan(radians(alpha))]
    soilx = [x4, xs1]
    soily = [y4, ys1]
    plt.plot(soilx, soily, linestyle="--")
    # 牆趾覆土
    plt.plot([-2, x6], [D, D], color="black")
    # 標註
    plt.plot([x4, B+1], [y4, y4], color="gray")
    plt.plot([x1, x1+1], [0, 0], color="gray")
    plt.plot([x1+0.8, x1+0.8], [0, H], color="gray")
    plt.text(x1+0.8+0.1, aver(0, H), "H")
    plt.text(aver(x0, x1)-0.2, 0+0.1, "B")
    plt.text(aver(x6, x7)-0.2, aver(y6, y7)+0.1, "B1")
    plt.text(aver(x4, x5)-0.2, aver(y4, y5)+0.1, "B2")
    plt.text(aver(x2, x3)-0.2, aver(y2, y3)+0.1, "B2")
    plt.plot([x2, x2+0.5], [y2, y2], color="gray")
    plt.plot([x2+0.3, x2+0.3], [0, y2], color="gray")
    plt.text(x2+0.3+0.1, aver(0, y2), "H2")
    plt.text(x6-0.3, aver(y5, y6)+0.1, "S1")
    plt.text(x3+0.3, aver(y3, y4)+0.1, "S2")
    plt.plot([-1.8, -1.8], [0, D], color="gray")
    plt.plot([-2, 0], [0, 0], color="gray")
    plt.text(-1.8+0.1, aver(0, D), "D")

    # 設定
    # plt.ylim(ymin=-7, ymax=ys1)
    plt.axis('equal')
    # plt.show()
    return fig


def Ka_R(alpha, theta, phi):  # Rankine 一般狀況主動土壓係數
    # 轉成 rad
    alpha_D, theta_D, phi_D = alpha, theta, phi  # float
    alpha_R, theta_R, phi_R = map(
        radians, [alpha, theta, phi])  # float_def->float_rad
    # 分子
    fork = (degrees(asin(sin(alpha_R) / sin(phi_R)))) - alpha_D + 2 * theta_D
    # print(f"fork -> {fork:.4f}")

    fork_R = radians(fork)
    # print(f"fork_R -> {fork_R:.4f}")

    root = 1 + (sin(phi_R))**2 - 2 * (sin(phi_R)) * (cos(fork_R))
    # print(f"root -> {root:.4f}")

    left = (cos(radians(alpha_D - theta_D)))
    # print(f"left -> {left:.4f}")

    right = sqrt(root)
    # print(f"right -> {right:.4f}")

    mole = left * right

    # 分母
    root = (sin(phi_R))**2 - (sin(alpha_R))**2
    deno = (cos(theta_R))**2 * ((cos(alpha_R)) + sqrt(root))

    return mole / deno


def Kp_R(phi):  # Rankine 一般狀況被動土壓係數
    return tan(radians(45 + phi/2))**2


def main(H=6.7, H2=0.7, D=1.5, B=4, B1=0.7,
         B2=0.5, B3=2.6, S1=0.2/6, S2=0, r2=19,
         Phi2=20, c2=40, r1=18, Phi1=30, c1=0,
         alpha=10, rc=23.58):
    # graph()

    # 抗翻轉
    Ka = Ka_R(alpha=alpha, theta=S2, phi=Phi1)      # Rankine 主動土壓係數
    # print(f"Ka -> {Ka:.4f}")
    # Kp = 0      # Rankine 被動土壓係數

    H1 = (tan(radians(alpha))) * (B - B1 - B2 - (H - H2) * S1)
    Pa = 0.5 * r1 * (H1 + H)**2 * Ka   # Rankine 主動土壓力
    # print(f"Pa -> {Pa:.4f}")
    Pv = Pa * (sin(radians(alpha)))  # 垂直分量
    # print(f"Pv -> {Pv:.4f}")
    Ph = Pa * (cos(radians(alpha)))  # 水平分量
    # print(f"Ph -> {Ph:.4f}")

    Area = [(H-H2)**2 * S1 / 2, (H-H2) * B2, (H-H2)**2 * S2 / 2, B*H2,
            (B3 + (H-H2)*S2)**2 * tan(radians(alpha)) / 2, (H-H2)**2 * S2 / 2, B3*(H-H2)]

    Weight = [rc, rc, rc, rc, r1, r1, r1]

    Arm = [B1 + (H-H2)*S1 * 2 / 3, B1 + (H-H2)*S1 + B2 / 2, B1 + (H-H2)*S1 + B2 + (H-H2) * S2 / 3,
           B/2, B - (B3+(H-H2)*S2)/3, B1 + (H-H2)*S1 + B2 + (H-H2) * S2 * 2 / 3, B - (B3 / 2)]

    Mv = Pv * B

    sum_MR = sum(
        [Mv]+[a*b*c for a, b, c in zip(Area, Weight, Arm)])        # 抗傾倒
    # print(sum_MR)
    sum_MO = Ph * (H1 + H) / 3      # 傾倒力矩
    # print(sum_MO)
    FS_fall = sum_MR/sum_MO     # 傾倒係數
    print(f"抗翻轉破壞安全係數 {FS_fall:.2f}")

    # 抗滑動
    k1 = 2/3  # 預設
    k2 = 2/3
    Kp = Kp_R(phi=Phi2)
    Pp = (Kp * r2 * D**2) / 2 + (2 * c2 * sqrt(Kp) * D)       # Rankine 被動土壓力
    # print(f"Pp -> {Pp:.4f}")
    sum_V = sum([Pv]+[a*b for a, b in zip(Area, Weight)])
    # print(f"sum_V -> {sum_V:.4f}")
    FS_slide = (sum_V * tan(radians(k1 * Phi2)) + B * k2 * c2 + Pp) / Ph
    print(f"抗滑動破壞安全係數 {FS_slide:.2f}")

    # 承載值破壞之檢驗
    X_bar = (sum_MR - sum_MO) / sum_V
    e = B / 2 - X_bar       # 合力偏心值
    if e >= B/6:
        e_res = f"偏心量 : {e:.4f} >= B/6"
    else:
        e_res = f"偏心量 : {e:.4f} < B/6"

    print(e_res)
    q_max = sum_V / B * (1 + 6*e / B)
    # print(f"q_max -> {q_max:4f}")
    q_min = sum_V / B * (1 - 6*e / B)
    # print(f"q_min -> {q_min:4f}")

    # 連續型基礎 形狀因素設為1
    Fcs = 1
    Fqs = 1
    Frs = 1
    # 承載因素
    Nq = tan(radians(45 + Phi2/2))**2 * exp(pi * tan(radians(Phi2)))
    Nc = (Nq - 1) * cot(radians(Phi2))
    Nr = 2 * (Nq + 1) * tan(radians(Phi2))

    # 深度因素
    Df = D
    beta = 0  # 傾斜載重角度
    if Df / B <= 1:
        if Phi2 == 0:
            Fcd = 1 + 0.4 * Df / B
            Fqd = 1
            Frd = 1
        else:  # >0
            Fqd = 1 + 2 * tan(radians(Phi2)) * \
                (1-sin(radians(Phi2)))**2 * Df / B
            Fcd = Fqd - (1 - Fqd)/(Nc * tan(radians(Phi2)))
            Frd = 1
    else:  # >1
        if Phi2 == 0:
            Fcd = 1 + 0.4 * atan(Df / B)  # tan-1(r?d?)
            Fqd = 1
            Frd = 1
        else:  # >0
            Fqd = 1 + 2 * tan(radians(Phi2)) * (1-sin(radians(Phi2))
                                                )**2 * atan(Df / B)  # tan-1(r?d?)
            Fcd = Fqd - (1 - Fqd)/(Nc * tan(radians(Phi2)))
            Frd = 1
    # 傾斜因素
    Fci = (1 - beta / 90) ** 2
    Fqi = Fci
    Fri = (1 - beta / Phi2) ** 2

    c_part = c2 * Nc * Fcs * Fcd * Fci
    # print(c_part)
    q_part = r2 * D * Nq * Fqs * Fqd * Fqi
    # print(q_part)
    r_part = r2 / 2 * (B - 2*e) * Nr * Frs * Frd * Fri
    # print(r_part)
    qu = sum([c_part, q_part, r_part])
    # print(f"qu -> {float(qu):.4f}")
    print(f"抗承載值安全係數 {float(qu/q_max):.2f}")
    return (
        f"抗翻轉破壞安全係數 : {FS_fall:.2f} \n"
        f"抗滑動破壞安全係數 : {FS_slide:.2f} \n"
        f"{e_res} \n"
        f"抗承載值安全係數 : {float(qu/q_max):.2f} \n")


def test(**args):
    print()


if __name__ == "__main__":
    main()
