import numpy as np
import matplotlib.pyplot as plt

# ---------- 參數設定 ----------
R = 18
IMAX = 8
OCW_MIN = 7
OCW_MAX = 31
LMAX = 5

# ---------- 單次模擬(和 Step 1 相同)----------
def simulate_once(M):
    ocw = np.full(M, OCW_MIN)
    obo = np.random.randint(0, ocw + 1)
    tx_count = np.zeros(M, dtype=int)
    success = np.zeros(M, dtype=bool)

    for slot in range(IMAX):
        obo = obo - R
        ready = (obo <= 0) & (~success) & (tx_count < LMAX)
        ready_idx = np.where(ready)[0]
        if len(ready_idx) == 0:
            continue
        choice = np.random.randint(0, R, size=len(ready_idx))
        counts = np.bincount(choice, minlength=R)
        for k, sta in enumerate(ready_idx):
            ru = choice[k]
            tx_count[sta] += 1
            if counts[ru] == 1:
                success[sta] = True
            else:
                ocw[sta] = min(2 * ocw[sta] + 1, OCW_MAX)
                obo[sta] = np.random.randint(0, ocw[sta] + 1)
    return success.sum() / M

def simulate(M, num_runs):
    return np.mean([simulate_once(M) for _ in range(num_runs)])

# ---------- 主程式:比較不同 NUM_RUNS ----------
M_values = list(range(10, 201, 10))
runs_to_test = [1, 10, 100, 1000]   # 要比較的模擬次數

plt.figure()
for num_runs in runs_to_test:
    P_values = [simulate(M, num_runs) for M in M_values]
    plt.plot(M_values, P_values, marker='o', label=f"{num_runs} runs")
    print(f"done: {num_runs} runs")

plt.xlabel("M (number of STAs)")
plt.ylabel("P (access success probability)")
plt.title("Effect of Monte Carlo runs on curve stability")
plt.legend()
plt.grid(True)
plt.savefig("runs_compare.png", dpi=120)
print("\nSaved figure to runs_compare.png")
