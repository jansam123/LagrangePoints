from dash import dcc
from dash import html


def getText():
    first_part = dcc.Markdown("""
    # Lagrange points

    Simple interactive webpage displaying Lagrange points and effective potential of two massive objects.
    The effective potential is given by
    """)
    second_part = dcc.Markdown("""
    where M = m1 + m2 is the sum of masses, a is the distance between masses, alpha = m2/M, G is gravitational contatnt and x, y are coordinates.
    The angular frequency omega is given by Kepler's law
    """)
    middle_part = dcc.Markdown("""
    Coordinates of Lagrange points L4 and L5 are given by 
    """)
    second_middle_part = dcc.Markdown("""
    y coordinates of Lagrange points L1, L2 and L3 are all y = 0 and x coordinates as a solutions to equation

    """)
    third_part = dcc.Markdown("""
    This potential includes gravitational force between masses and centrifugal force. 
    In reality there is also Coriolis force present, but it isn't easily visualized that's why we didn't inculde it.
    The effect of Coriolis force makes points L4 and L5 stable.

    Website is motivated by assigment ([link, in Czech](assets/ukol.pdf)) as a part of Theoretical Mechanics course taught by prof. Jiří Podolský at MFF, Charles University, Prague (see [MFF CUNI website](https://www.mff.cuni.cz/en) and [course website, in Czech](http://utf.mff.cuni.cz/vyuka/OFY003/OFY003.htm)).


    Source code available at https://github.com/jansam123/LagrangePoints.
    Deployed website available at https://lagrange-points.herokuapp.com.

    ____

    **Author**: Samuel Jankovych
    **Email**: samueljankovych@gmail.com
    
    """)

    Veff = html.Img(src="./assets/images/Veff.jpg", width="700")
    Kepler = html.Img(src = "./assets/images/kepler.jpg", width = "100")
    Lx = html.Img(src="./assets/images/Lx.jpg", width="400")
    Ly = html.Img(src="./assets/images/Ly.jpg", width="200")

    return first_part, Veff, second_part, Kepler, middle_part, Ly, second_middle_part, Lx, third_part
