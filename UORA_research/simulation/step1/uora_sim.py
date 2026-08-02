import numpy as np
import matplotlib.pyplot as plt

# ---------- 參數設定 ----------
R = 18          # 每一輪可用的 RA-RU 數量
IMAX = 8        # 最多跑幾輪 (contention slots)
OCW_MIN = 7     # OCW 最小值
OCW_MAX = 31    # OCW 最大值
LMAX = 5        # 最多重傳幾次
NUM_RUNS = 500  # 同一個 M 重複跑幾次取平均 (Monte Carlo)

# ---------- 單次模擬 ----------
def simulate_once(M):
    # 每個 STA 的狀態
    ocw = np.full(M, OCW_MIN)              # 每個 STA 目前的 OCW
    obo = np.random.randint(0, ocw + 1)    # 抽 OBO 號碼牌 (0 ~ OCW)
    tx_count = np.zeros(M, dtype=int)       # 已經傳輸(嘗試)幾次
    success = np.zeros(M, dtype=bool)       # 是否已成功

    # 一輪一輪跑
    for slot in range(IMAX):
        obo = obo - R                       # 所有還沒成功的 STA，OBO 減 R

        # 找出這一輪要傳輸的 STA：OBO<=0、還沒成功、還沒超過重傳上限
        ready = (obo <= 0) & (~success) & (tx_count < LMAX)
        ready_idx = np.where(ready)[0]
        if len(ready_idx) == 0:
            continue

        # 每個 ready 的 STA 隨機挑一個 RU (0 ~ R-1)
        choice = np.random.randint(0, R, size=len(ready_idx))

        # 統計每個 RU 被幾個人選中
        counts = np.bincount(choice, minlength=R)

        for k, sta in enumerate(ready_idx):
            ru = choice[k]
            tx_count[sta] += 1
            if counts[ru] == 1:
                # 只有這個人選這個 RU → 成功
                success[sta] = True
            else:
                # 碰撞 → OCW 加倍、重抽 OBO
                ocw[sta] = min(2 * ocw[sta] + 1, OCW_MAX)
                obo[sta] = np.random.randint(0, ocw[sta] + 1)

    # 回傳這次的接入成功率
    return success.sum() / M

# ---------- 對每個 M 跑多次取平均 ----------
def simulate(M):
    results = [simulate_once(M) for _ in range(NUM_RUNS)]
    return np.mean(results)

# ---------- 主程式 ----------
M_values = list(range(10, 201, 10))   # M 從 10 到 200，每隔 10
P_values = [simulate(M) for M in M_values]

for M, P in zip(M_values, P_values):
    print(f"M={M:3d}  P={P:.3f}")

# ---------- 畫圖 ----------
plt.figure()
plt.plot(M_values, P_values, marker='o')
plt.xlabel("M (number of STAs)")
plt.ylabel("P (access success probability)")
plt.title(f"UORA Step 1 (R={R}, Imax={IMAX}, Lmax={LMAX})")
plt.grid(True)
plt.savefig("step1_result.png", dpi=120)
print("\nSaved figure to step1_result.png")
