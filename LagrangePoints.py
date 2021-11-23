import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import operator as op


def potential(x, y, alpha, a, omega2, M, G):
    denom1 = np.sqrt((x + alpha*a)**2 + y**2)
    denom2 = np.sqrt((x - (1 - alpha)*a)**2 + y**2)
    return -G*M*(((1-alpha)/denom1) + (alpha/denom2)) - 0.5*omega2*(x**2 + y**2)


def calculate_LagPoints_coordinates(a, alpha, omega2, M, G):
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
    X_lag_points = np.array([(0.5-alpha)*a, (0.5-alpha)*a, *all_roots])
    y_lag = [-np.sqrt(3)*a/2, np.sqrt(3)*a/2]
    y_lag += [0 for _ in all_roots]
    Y_lag_points = np.array(y_lag)
    Z_lag_points = potential(
        X_lag_points, Y_lag_points, alpha, a, omega2, M, G)
    return X_lag_points, Y_lag_points, Z_lag_points


class LagPlot:

    def __init__(self, m1, m2, a, G) -> None:
        self.fig = go.Figure(layout=go.Layout(title="Lagrange points"))
        self.update_variables(m1, m2, a, G)
        self.update_points()

    def update_plot(self, X, Y, Z, color_min, color_max, contour_start, contour_end, contour_size):

        contour_setup = {"z": {"show": True, "start": contour_start,
                               "end": contour_end, "size": contour_size, "color": "white"}}
        self.fig.add_trace(go.Surface(z=Z, x=X, y=Y, cmin=color_min,
                           cmax=color_max, contours=contour_setup, colorscale='turbo'))

    def add_LagPoints(self, size=13, color=[130, 230, 240]):
        marker = dict(
            size=size,
            color=[color for _ in range(4)],
        )
        self.fig.add_trace(go.Scatter3d(
            x=self.lagPoints[0], y=self.lagPoints[0], z=self.lagPoints[0], mode='markers', marker=marker))

    def set_VeffAxis(self, zmin, zmax):
        self.fig.update_layout(
            scene=dict(
                xaxis={'title': 'X', 'autorange': True},
                yaxis={'title': 'Y', 'autorange': True},
                zaxis={'title': 'V_ef', 'range': [zmin, zmax]})
        )
        self.fig.update_layout(scene=dict(
            xaxis=dict(
                gridcolor="white",
                showbackground=False,
                zerolinecolor="white",),
            yaxis=dict(
                gridcolor="white",
                showbackground=False,
                zerolinecolor="white"),
            zaxis=dict(
                gridcolor="white",
                showbackground=False,
                zerolinecolor="white",
            ),)
        )

    def set_basic_camera(self):
        camera = dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=-0.45),
            eye=dict(x=1.25, y=1.25, z=1.25)
        )
        self.fig.update_layout(scene_camera=camera)

    def update_physical_variables(self, m1, m2, a, G):
        M = m1 + m2
        alpha = m2/M
        omega2 = G*M/a**3
        self.__phys_parameters = {'m1': m1, 'a': a, 'G': G,
                                  'm2': m2, 'M': M, 'alpha': alpha, 'omega2': omega2}

    def update_LagPoints(self):
        self.lagPoints = calculate_LagPoints_coordinates(
            self.__phys_parameters['a'], self.__phys_parameters['alpha'], self.__phys_parameters['omega2'],
            self.__phys_parameters['M'], self.__phys_parameters['G'])