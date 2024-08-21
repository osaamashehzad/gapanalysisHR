import pandas as pd
import numpy as np
import plotly.graph_objs as go
from scipy.stats import gaussian_kde
from plotly.subplots import make_subplots



# Load the datasets
normal_df = pd.read_csv(r"C:\Users\my file path\normaldata.csv")
non_normal_df = pd.read_csv(r"C:\Users\my file path\nonnormaldata.csv")

# Function to create 3D density surface and scatter plot traces
def create_3d_plots(df, title):
    # Extract the three dimensions
    x = df['Skill Gap']
    y = df['Time Gap']
    z = df['Will Gap']
    
    # Perform kernel density estimation
    xyz = np.vstack([x, y, z])
    kde = gaussian_kde(xyz)
    
    # Create a grid for the surface plot
    xi, yi, zi = np.mgrid[1:5:50j, 1:5:50j, 1:5:50j]
    positions = np.vstack([xi.ravel(), yi.ravel(), zi.ravel()])
    density = kde(positions).reshape(xi.shape)
    
    # Colors for the surface and points
    colorscale = 'RdYlGn_r'

    # Isosurface trace
    surface_trace = go.Isosurface(
        x=xi.ravel(),
        y=yi.ravel(),
        z=zi.ravel(),
        value=density.ravel(),
        colorscale=colorscale,
        isomin=density.min(),
        isomax=density.max(),
        opacity=0.3,  # Adjusted opacity for better visibility of other surfaces
        surface_count=10,
        caps=dict(x_show=False, y_show=False, z_show=False),
        name=title + ' Density'
    )
    
    # Scatter trace for points
    scatter_trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=2,
            color='blue',  # Color of points
            opacity=0.7  # Opacity of points
        ),
        name=title + ' Data Points'
    )
    
    return surface_trace, scatter_trace

# Create the plots for both datasets
normal_surface_trace, normal_scatter_trace = create_3d_plots(normal_df, "Normal Distribution")
non_normal_surface_trace, non_normal_scatter_trace = create_3d_plots(non_normal_df, "Non-Normal Distribution")

# Create a subplot figure
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'scene'}, {'type': 'scene'}]],
    subplot_titles=("Normal Distribution", "Non-Normal Distribution")
)

# Add the traces to the subplot
fig.add_trace(normal_surface_trace, row=1, col=1)
fig.add_trace(normal_scatter_trace, row=1, col=1)
fig.add_trace(non_normal_surface_trace, row=1, col=2)
fig.add_trace(non_normal_scatter_trace, row=1, col=2)

# Update layout for better visualization
fig.update_layout(
    title_text="Gap Analysis to Drive Strategic Workforce Planning Using 3-D Surface Plots",
    scene=dict(
        xaxis_title='Skill Gap',
        yaxis_title='Time Gap',
        zaxis_title='Will Gap',
    ),
    scene2=dict(
        xaxis_title='Skill Gap',
        yaxis_title='Time Gap',
        zaxis_title='Will Gap',
    ),
    showlegend=False
)

fig.show()




