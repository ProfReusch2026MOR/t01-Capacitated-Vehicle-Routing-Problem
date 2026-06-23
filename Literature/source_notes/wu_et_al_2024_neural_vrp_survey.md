# Wu et al. (2024) — Neural Combinatorial Optimization for VRPs

## Full reference

Wu, X., Wang, D., Wen, L., Xiao, Y., Wu, C., Wu, Y., Yu, C., Maskell, D. L., & Zhou, Y. (2024). *Neural Combinatorial Optimization Algorithms for Solving Vehicle Routing Problems: A Comprehensive Survey with Perspectives.*


This survey is helpful because it gives a more careful view of recent AI-based routing methods. At first glance, neural combinatorial optimization sounds like the most modern direction for vehicle routing. But the paper makes clear that these methods still have serious weaknesses, especially when they are compared with established Operations Research algorithms.

For our project, that matters because it prevents us from making the literature review sound like we should have used machine learning just because it is newer. The survey points out problems such as weak generalization, difficulty with larger instances, limited coverage of different VRP variants, and challenges in comparing neural methods fairly with classical OR approaches.

This supports our decision to keep the project focused on classical OR logic: a mathematical model, transparent input data, a solver-based approach, and a heuristic comparison. For a university project with a strict requirement for explanation and reproducibility, this is more defensible than adding an AI method that we cannot properly implement or explain.

The source also helps us frame our project limitations. We can mention that learning-based routing methods are an active research direction, but they are outside the scope of our implementation. That makes the literature review look more balanced. We are not ignoring newer AI methods; we are simply choosing a more explainable and reproducible approach for this project.

The limitation is that the paper is a survey of neural methods, not a direct solution method for our TDHVRPTW case. It should therefore be used mainly to explain why we do not base our repository on AI routing, rather than as a core modeling source.
