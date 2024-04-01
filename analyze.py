# 使用 Rankine 土壓力計算方法檢核傾倒
#
import matplotlib.pyplot as plt
from math import sin, cos, tan, radians, asin, degrees, sqrt
from math import exp, pi, atan
from mpmath import cot


class analyze():
    """
    """

    def __init__(
            self, H=6.7, H2=0.7, D=1.5, B=4, B1=0.7,
            B2=0.5, B3=2.6, S1=0.2/6, S2=0, r2=19,
            Phi2=20, c2=40, r1=18, Phi1=30, c1=0,
            alpha=10, rc=23.58) -> None:

        self.H = H  # 牆總高度(m)
        self.H2 = H2  # 底板厚度(m)
        self.D = D  # 牆底至牆趾地表深(m)
        self.B = B  # 底板總寬度(m)
        self.B1 = B1  # 牆趾寬(m)
        self.B2 = B2  # 牆頂寬(m)
        self.B3 = B3  # 牆跟寬(m)
        self.S1 = S1  # 牆面斜率(最少0.02)
        self.S2 = S2  # 牆背面斜率 0 = 垂直
        self.alpha = alpha  # α回填土地表傾角(deg)

        self.r2 = r2  # γ2地層單位重(kN/m3)
        self.Phi2 = Phi2  # ϕ2 地層摩擦角(deg)
        self.c2 = c2  # c2地層凝聚力(kN/m2)

        self.r1 = r1   # γ1回填土單位重(kN/m3)
        self.Phi1 = Phi1  # ϕ1 回填土摩擦角(deg)
        self.c1 = c1  # c1回填土凝聚力(kN/m2)

        self.rc = rc  # γc混凝土單位重(kN/m3)

    def update_val(
            self, H=6.7, H2=0.7, D=1.5, B=4, B1=0.7,
            B2=0.5, B3=2.6, S1=0.2/6, S2=0, r2=19,
            Phi2=20, c2=40, r1=18, Phi1=30, c1=0,
            alpha=10, rc=23.58) -> None:

        self.H = H  # 牆總高度(m)
        self.H2 = H2  # 底板厚度(m)
        self.D = D  # 牆底至牆趾地表深(m)
        self.B = B  # 底板總寬度(m)
        self.B1 = B1  # 牆趾寬(m)
        self.B2 = B2  # 牆頂寬(m)
        self.B3 = B3  # 牆跟寬(m)
        self.S1 = S1  # 牆面斜率(最少0.02)
        self.S2 = S2  # 牆背面斜率 0 = 垂直
        self.alpha = alpha  # α回填土地表傾角(deg)

        self.r2 = r2  # γ2地層單位重(kN/m3)
        self.Phi2 = Phi2  # ϕ2 地層摩擦角(deg)
        self.c2 = c2  # c2地層凝聚力(kN/m2)

        self.r1 = r1   # γ1回填土單位重(kN/m3)
        self.Phi1 = Phi1  # ϕ1 回填土摩擦角(deg)
        self.c1 = c1  # c1回填土凝聚力(kN/m2)

        self.rc = rc  # γc混凝土單位重(kN/m3)

    def Ka_R(self, theta, phi) -> float:  # Rankine 一般狀況主動土壓係數
        # 轉成 rad
        alpha_D, theta_D, _ = self.alpha, theta, phi  # 單位:度
        alpha_R, theta_R, phi_R = map(
            radians, [self.alpha, theta, phi])  # 單位:弧度
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

    def Kp_R(self) -> float:  # Rankine 一般狀況被動土壓係數
        return tan(radians(45 + self.Phi1/2))**2

    def FS_fall(self) -> float:
        # 抗翻轉
        Ka = self.Ka_R(theta=self.alpha, phi=self.Phi1)      # Rankine 主動土壓係數
        # print(f"Ka -> {Ka:.4f}")
        # Kp = 0      # Rankine 被動土壓係數

        H1 = (tan(radians(self.alpha))) \
            * (self.B - self.B1 - self.B2 - (self.H - self.H2) * self.S1)
        Pa = 0.5 * self.r1 * (H1 + self.H)**2 * Ka   # Rankine 主動土壓力
        # print(f"Pa -> {Pa:.4f}")
        self.Pv = Pa * (sin(radians(self.alpha)))  # 垂直分量
        # print(f"Pv -> {Pv:.4f}")
        self.Ph = Pa * (cos(radians(self.alpha)))  # 水平分量
        # print(f"Ph -> {Ph:.4f}")

        # 力矩計算可以參考切分圖如何劃分 res/img.md
        self.Area = [
            (self.H-self.H2)**2 * self.S1 / 2,
            (self.H-self.H2) * self.B2, (self.H-self.H2)**2 * self.S2 / 2,
            self.B*self.H2,
            (self.B3 + (self.H-self.H2)*self.S2)**2 * tan(radians(self.alpha)) / 2,
            (self.H-self.H2)**2 * self.S2 / 2, self.B3*(self.H-self.H2)
            ]
        # 單位重
        self.Weight = [self.rc, self.rc, self.rc, self.rc, self.r1, self.r1, self.r1]
        # 力臂長
        self.Arm = [
            self.B1 + (self.H-self.H2)*self.S1 * 2 / 3,
            self.B1 + (self.H-self.H2)*self.S1 + self.B2 / 2,
            self.B1 + (self.H-self.H2)*self.S1 + self.B2 + (self.H-self.H2) * self.S2 / 3,
            self.B/2, self.B - (self.B3+(self.H-self.H2)*self.S2)/3,
            self.B1 + (self.H-self.H2)*self.S1 + self.B2 + (self.H-self.H2) * self.S2 * 2 / 3,
            self.B - (self.B3 / 2)
            ]

        Mv = self.Pv * self.B

        self.sum_MR = sum(
            [Mv]+[a*b*c for a, b, c in zip(self.Area, self.Weight, self.Arm)])  # 抗傾倒
        # print(sum_MR)
        self.sum_MO = self.Ph * (H1 + self.H) / 3  # 傾倒力矩
        # print(sum_MO)
        FS_fall = self.sum_MR/self.sum_MO     # 傾倒係數
        return FS_fall

    def FS_slide(self):
        # 抗滑動
        k1 = 2/3  # 預設
        k2 = 2/3
        Kp = self.Kp_R()
        Pp = (Kp * self.r2 * self.D**2) / 2 + (2 * self.c2 * sqrt(Kp) * self.D)  # 計算 Rankine 被動土壓力
        # print(f"Pp -> {Pp:.4f}")
        self.sum_V = sum([self.Pv]+[a*b for a, b in zip(self.Area, self.Weight)])
        # print(f"sum_V -> {sum_V:.4f}")
        FS_slide = (self.sum_V * tan(radians(k1 * self.Phi2)) + self.B * k2 * self.c2 + Pp) \
            / self.Ph
        return FS_slide

    def FS_carrying(self) -> float:
        # 承載值破壞之檢驗
        X_bar = (self.sum_MR - self.sum_MO) / self.sum_V
        e = self.B / 2 - X_bar       # 計算合力偏心值
        if e >= self.B/6:
            e_res = f"偏心量 : {e:.4f} >= B/6"
        else:
            e_res = f"偏心量 : {e:.4f} < B/6"

        print(e_res)
        q_max = self.sum_V / self.B * (1 + 6*e / self.B)
        # print(f"q_max -> {q_max:4f}")
        # q_min = sum_V / B * (1 - 6*e / B)
        # print(f"q_min -> {q_min:4f}")

        # 連續型基礎 形狀因素設為1
        Fcs = 1
        Fqs = 1
        Frs = 1
        # 承載因素
        Nq = tan(radians(45 + self.Phi2/2))**2 * exp(pi * tan(radians(self.Phi2)))
        Nc = (Nq - 1) * cot(radians(self.Phi2))
        Nr = 2 * (Nq + 1) * tan(radians(self.Phi2))

        # 深度因素
        Df = self.D
        beta = 0  # 傾斜載重角度
        if Df / self.B <= 1:
            if self.Phi2 == 0:
                Fcd = 1 + 0.4 * Df / self.B
                Fqd = 1
                Frd = 1
            else:  # >0
                Fqd = 1 + 2 * tan(radians(self.Phi2)) * \
                    (1-sin(radians(self.Phi2)))**2 * Df / self.B
                Fcd = Fqd - (1 - Fqd)/(Nc * tan(radians(self.Phi2)))
                Frd = 1
        else:  # >1
            if self.Phi2 == 0:
                Fcd = 1 + 0.4 * atan(Df / self.B)  # tan-1(r?d?)
                Fqd = 1
                Frd = 1
            else:  # >0
                Fqd = 1 + 2 * tan(radians(self.Phi2)) \
                    * (1-sin(radians(self.Phi2)))**2 * atan(Df / self.B)  # tan-1(r?d?)
                Fcd = Fqd - (1 - Fqd)/(Nc * tan(radians(self.Phi2)))
                Frd = 1

        # 傾斜因素
        Fci = (1 - beta / 90) ** 2
        Fqi = Fci
        Fri = (1 - beta / self.Phi2) ** 2

        c_part = self.c2 * Nc * Fcs * Fcd * Fci
        # print(c_part)
        q_part = self.r2 * self.D * Nq * Fqs * Fqd * Fqi
        # print(q_part)
        r_part = self.r2 / 2 * (self.B - 2*e) * Nr * Frs * Frd * Fri
        # print(r_part)
        qu = sum([c_part, q_part, r_part])
        # print(f"qu -> {float(qu):.4f}")
        return float(qu / q_max)

    def graph(self, ):
        """繪製擋土牆預覽圖"""
        fig = plt.figure(figsize=(4, 2.5), dpi=100)

        def aver(x0, x1):
            return (x0 + x1)/2
        # 牆
        x0, y0 = [0, 0]
        x1, y1 = [self.B, 0]
        x2, y2 = [self.B, self.H2]
        x3, y3 = [self.B-self.B3, self.H2]
        x4, y4 = [x3 - (self.H-self.H2)*self.S2, self.H]
        x5, y5 = [x4 - self.B2, self.H]
        x6, y6 = [self.B1, self.H2]
        x7, y7 = [0, self.H2]

        conx = [x0, x1, x2, x3, x4, x5, x6, x7, x0]
        cony = [y0, y1, y2, y3, y4, y5, y6, y7, y0]
        plt.plot(conx, cony, color="black")
        # 回填土
        xs1, ys1 = [
            self.B,
            self.H+(self.B3 + (self.H-self.H2)*self.S2)
            * tan(radians(self.alpha))
            ]
        soilx = [x4, xs1]
        soily = [y4, ys1]
        plt.plot(soilx, soily, linestyle="--")
        # 牆趾覆土
        plt.plot([-2, x6], [self.D, self.D], color="black")
        # 標註
        plt.plot([x4, self.B+1], [y4, y4], color="gray")
        plt.plot([x1, x1+1], [0, 0], color="gray")
        plt.plot([x1+0.8, x1+0.8], [0, self.H], color="gray")
        plt.text(x1+0.8+0.1, aver(0, self.H), "H")
        plt.text(aver(x0, x1)-0.2, 0+0.1, "B")
        plt.text(aver(x6, x7)-0.2, aver(y6, y7)+0.1, "B1")
        plt.text(aver(x4, x5)-0.2, aver(y4, y5)+0.1, "B2")
        plt.text(aver(x2, x3)-0.2, aver(y2, y3)+0.1, "B2")
        plt.plot([x2, x2+0.5], [y2, y2], color="gray")
        plt.plot([x2+0.3, x2+0.3], [0, y2], color="gray")
        plt.text(x2+0.3+0.1, aver(0, y2), "H2")
        plt.text(x6-0.3, aver(y5, y6)+0.1, "S1")
        plt.text(x3+0.3, aver(y3, y4)+0.1, "S2")
        plt.plot([-1.8, -1.8], [0, self.D], color="gray")
        plt.plot([-2, 0], [0, 0], color="gray")
        plt.text(-1.8+0.1, aver(0, self.D), "D")

        # 設定
        # plt.ylim(ymin=-7, ymax=ys1)
        plt.axis('equal')
        # plt.show()
        return fig


if __name__ == "__main__":
    """
    在Terminal輸出各項係數
    """
    retaining_wall = analyze()

    fall = retaining_wall.FS_fall()
    print(f"抗翻轉破壞安全係數 : {fall:.2f}")
    slide = retaining_wall.FS_slide()
    print(f"抗滑動破壞安全係數 : {slide:.2f}")
    # e_val = retaining_wall.e
    # print(f"{e_val}")
    carry = retaining_wall.FS_carrying()
    print(f"抗承載值安全係數 : {carry:.2f}")
