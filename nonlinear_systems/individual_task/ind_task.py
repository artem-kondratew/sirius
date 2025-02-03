import matplotlib.pyplot as plt 
import numpy as np


relay = False
compensation = False


sigma0 = np.array([[9],
                   [0]])

D = np.array([[1,  2],
              [2, -1]])

if relay:
    T = D.T
else:
    T = np.linalg.inv(D)

x, t = [sigma0, T @ sigma0], 0  # [sigma, sigma2], t

t1 = 2  # sim period
dt = 0.0001  # time step

tarr = []
uarr = []
sigmaarr  = []
sigma2arr = []
dsigmaarr = []
phiarr = []
farr = []


def rhs(t, state):

    _, sigma2 = state

    phi = np.array([[20 * np.sin(4 * t)],
                    [ 2 * np.cos(5 * t)]])

    f = np.array([[2 * np.cos(4 * t)],
                  [3 * np.sin(2 * t)]])
    
    f += np.array([[-10], [2]]) * sigma0

    # relay control with compensation
    if relay and compensation:
        norm = np.linalg.norm(phi, axis=1, ord=2)
        ro = np.diag(norm + 4)
        u = -ro @ np.sign(sigma2) - np.linalg.inv(D) @ f
    
    # relay control without compensation
    if relay and not compensation:
        norm = np.linalg.norm(np.linalg.inv(D) @ f + phi, axis=1, ord=2)
        ro = np.diag(norm + 1)
        u = -ro @ np.sign(sigma2)

    # unit control with compensation
    if not relay and compensation:
        ro = np.linalg.norm(phi, ord=2) + 1
        u = -ro / np.linalg.norm(sigma2) * sigma2 - np.linalg.inv(D) @ f

    # unit control without compensation
    if not relay and not compensation:
        ro = np.linalg.norm(np.linalg.inv(D) @ f + phi, ord=2) + 4
        u = -ro / np.linalg.norm(sigma2) * sigma2

    dsigma = D @ (u + phi + np.linalg.inv(D) @ f)
    dsigma2 = T @ D @ (u + phi + np.linalg.inv(D) @ f)
    
    uarr.append(u)
    farr.append(f)
    phiarr.append(phi)
    
    return [dsigma, dsigma2]
    

while t < t1:
    dsigma, dsigma2 = rhs(t, x)

    x[0] = x[0] + dsigma * dt
    x[1] = x[1] + dsigma2 * dt

    sigmaarr.append(x[0])
    sigma2arr.append(x[1])

    tarr.append(t)
    t += dt

sigmaarr = np.array(sigmaarr)
sigma2arr = np.array(sigma2arr)
uarr = np.array(uarr)
farr = np.array(farr)
phiarr = np.array(phiarr)

fig1, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 5), sharex=True)

title = ('Vector relay' if relay else 'Unit') + ' control ' + ('with' if compensation else 'without') + ' compensation'
fig1.suptitle(title, fontsize=14)

ax1.set_xlabel('t, s')
ax1.set_ylabel('$\\sigma_1$, $\\sigma_2$')
ax1.plot(tarr, sigmaarr[:, 0, [0]].flatten(), 'b-', label='$\\sigma_1$')
ax1.plot(tarr, sigmaarr[:, 1, [0]].flatten(), 'r-', label='$\\sigma_2$')
ax1.legend(loc='upper right')
ax1.grid(True)

ax2.set_xlabel('t, s')
ax2.set_ylabel('Est. of $\\sigma_1$, $\\sigma_2$')
ax2.plot(tarr, sigma2arr[:, 0, [0]].flatten(), 'b-', label='Est. $\\sigma_1$')
ax2.plot(tarr, sigma2arr[:, 1, [0]].flatten(), 'r-', label='Est. $\\sigma_2$')
ax2.legend(loc='upper right')
ax2.grid(True)

ax3.set_xlabel('t, s')
ax3.set_ylabel('$u_1$, $u_2$')
ax3.plot(tarr, uarr[:, 1].flatten(), 'r-', label='$u_2$')
ax3.plot(tarr, uarr[:, 0].flatten(), 'b-', label='$u_1$')
ax3.legend(loc='upper right')
ax3.grid(True)

ax4.set_xlabel('t, s')
ax4.set_ylabel('$\\phi_1$, $\\phi_2$, $f_1$, $f_2$')
ax4.plot(tarr, phiarr[:, 0].flatten(), 'b-', label='$\\phi_1$')
ax4.plot(tarr, phiarr[:, 1].flatten(), 'r-', label='$\\phi_2$')
ax4.plot(tarr, farr[:, 0].flatten(), 'g-', label='$f_1$')
ax4.plot(tarr, farr[:, 1].flatten(), 'y-', label='$f_2$')
ax4.legend(loc='upper right')
ax4.grid(True)

# plt.tight_layout()
plt.show()
