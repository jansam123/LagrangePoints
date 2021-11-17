import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import operator as op


def variable_setup(m1, m2, a, G):
    M = m1 + m2
    alpha = m2/M
    omega2 = G*M/a**3
    return M, alpha, omega2


def polynom_solver(alpha, a):
    all_roots = []
    p1 = [1, -(2+alpha), 1+2*alpha, -(alpha + 1), 2*(1-alpha), alpha-1]
    p2 = [1, -(2+alpha), 1+2*alpha, (1 - alpha), 2*(alpha-1), 1-alpha]
    p3 = [1, -(2+alpha), 1+2*alpha, (1 - 3*alpha), 2*(alpha-1), 1-alpha]
    p4 = [1, -(2+alpha), 1+2*alpha, (alpha - 1), 2*(1-alpha), alpha-1]
    for p, o in zip([p1, p2, p3, p4], [[op.gt, op.gt], [op.lt, op.lt], [op.gt, op.lt], [op.lt, op.gt]]):
        lim1 = a-alpha*a
        lim2 = -alpha*a
        poly = np.poly1d(p)
        P = poly(np.poly1d([1/a, alpha]))
        roots = P.roots
        real_roots = np.real(roots[np.where(np.imag(roots) == 0)])
        for r in real_roots:
            if o[0](r, lim1) and o[1](r, lim2):
                all_roots.append(r)
    return all_roots


def potential(x, y, alpha, a, omega2, M, G):
    denom1 = np.sqrt((x + alpha*a)**2 + y**2)
    denom2 = np.sqrt((x - (1 - alpha)*a)**2 + y**2)
    return -G*M*(((1-alpha)/denom1) + (alpha/denom2)) - 0.5*omega2*(x**2 + y**2)


def Lag_points(a, alpha, omega2, M, G):
    roots = polynom_solver(alpha, a)
    X_lag_points = np.array([(0.5-alpha)*a, (0.5-alpha)*a, *roots])
    y_lag = [-np.sqrt(3)*a/2, np.sqrt(3)*a/2]
    y_lag += [0 for _ in roots]
    Y_lag_points = np.array(y_lag)
    Z_lag_points = potential(
        X_lag_points, Y_lag_points, alpha, a, omega2, M, G)
    return X_lag_points, Y_lag_points, Z_lag_points


def coordinates(a, alpha, omega2, M, G):
    square = 3*a
    x = np.linspace(-square, square, 100)
    y = np.linspace(-square, square, 100)
    X, Y = np.meshgrid(x, y)
    Z = potential(X, Y, alpha, a, omega2, M, G)
    return X, Y, Z


def run_plotly(
        X, Y, Z,
        X_lag_points, Y_lag_points, Z_lag_points, zmin, zmax, show_LP=True):

    layout = go.Layout(
        title="Lagrange points",
    )

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, cmin=zmin, cmax=Z_lag_points[0], contours={
        "z": {"show": True, "start": Z_lag_points.min(), "end": Z_lag_points.max(), "size": (Z_lag_points.max()-Z_lag_points.min())/4, "color": "white"}
    }, colorscale='turbo')], layout=layout)

    if show_LP:
        fig.add_trace(go.Scatter3d(x=X_lag_points, y=Y_lag_points, z=Z_lag_points, mode='markers', marker=dict(
            size=13,
            color=[[130, 230, 240], [130, 230, 240], [
                130, 230, 240], [130, 230, 240], [130, 230, 240]],
        )))
    fig.update_layout(
        scene=dict(
            xaxis={'title': 'X', 'autorange': True},
            yaxis={'title': 'Y', 'autorange': True},
            zaxis={'title': 'V_ef', 'range': [zmin, zmax]})
    )
    fig.update_layout(scene=dict(
        xaxis=dict(
            # backgroundcolor="white",
            gridcolor="white",
            showbackground=False,
            zerolinecolor="white",),
        yaxis=dict(
            # backgroundcolor="white",
            gridcolor="white",
            showbackground=False,
            zerolinecolor="white"),
        zaxis=dict(
            # backgroundcolor="white",
            gridcolor="white",
            showbackground=False,
            zerolinecolor="white",
            ticks=""),)
    )


    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=-0.45),
        eye=dict(x=1.25, y=1.25, z=1.25)
    )

    fig.update_layout(scene_camera=camera)

    return fig


def main_plotly(m1, m2, a, G):
    M, alpha, omega2 = variable_setup(m1, m2, a, G)
    X, Y, Z = coordinates(a, alpha, omega2, M, G)
    X_lag_points, Y_lag_points, Z_lag_points = Lag_points(
        a, alpha, omega2, M, G)
    fig = run_plotly(X, Y, Z,  X_lag_points, Y_lag_points, Z_lag_points,
                     zmin=-3*alpha*G*M/a,
                     zmax=0*alpha*G*M/a,
                     )
    fig.show()


def main_contourplot(m1, m2, a, G):
    M, alpha, omega2 = variable_setup(m1, m2, a, G)
    X, Y, Z = coordinates(a, alpha, omega2, M, G)
    X_lag_points, Y_lag_points, Z_lag_points = Lag_points(
        a, alpha, omega2, M, G)

    levels = np.linspace(-4*alpha*G*M/a, Z_lag_points[0], 100)
    cp = plt.contourf(X, Y, Z, levels=levels, cmap='turbo', zorder=1)
    plt.title('Lagrange Points')
    plt.colorbar(cp)

    levels = np.array([-4.8/G])
    levels = np.sort(np.append(levels, Z_lag_points[1:]))
    cp = plt.contour(X, Y, Z, levels=levels, colors='white',
                     linestyles='solid', zorder=2)
    plt.scatter(X_lag_points, Y_lag_points, color=[[
                130/255, 230/255, 240/255]], zorder=3, s=100)
    plt.xlim(-1.5*a, 1.5*a)
    plt.ylim(-1.5*a, 1.5*a)

    plt.savefig('potential.png')


if __name__ == '__main__':
    m1 = 1
    m2 = 3
    a = 1.2
    G = 1

    m1 = 1.898e27  # 1
    m2 = 1.989e30  # 3
    a = 748.9e9  # 1.2
    G = 6.67408e-11  # 1
    main_plotly(m1, m2, a, G)
