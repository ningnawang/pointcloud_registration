from context import *

# read a mesh
V, F = gpy.read_mesh("data/bunny.obj")
# write input to results path
gpy.write_mesh("results/example_mesh_approximation/input_mesh.obj", V, F)

V_approx = meshapprox.approximate_mesh(V, F, k=500)
# write output to results path
gpy.write_mesh("results/example_mesh_approximation/output_mesh.obj", V_approx, F)

# find chamfer distance between original and approximated mesh
cd = utility.chamfer_distance(V, F, V_approx, F)
print("Chamfer distance between original and approximated mesh: %f" % cd)

# visualize both meshes using polyscope
ps.init()
ps.register_surface_mesh("original mesh", V, F)
ps.register_surface_mesh("approximated mesh", V_approx, F)
ps.show()
