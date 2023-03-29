import graphviz

# Define the DOT code as a string
dot_code = '''
digraph finite_state_machine {
       rankdir=LR;
 node [shape=doublecircle] Q8;
        node [shape=point]; initial;
        node [shape = circle];
        initial->Q0;
        Q0->Q1[label=d];
        Q0->Q2[label="+"];
        Q0->Q3[label="-"];
        Q0->Q4[label="."];
        Q2->Q1[label=d];
        Q1->Q1[label=d];
        Q3->Q1[label=d];
        Q1->Q7[label=e];
        Q1->Q6[label="."];
        Q4->Q5[label=d];
        Q5->Q5[label=d];
        Q6->Q5[label=d];
        Q5->Q7[label=e];
        Q7->Q10[label="+"];
        Q7->Q9[label="-"];
        Q7->Q8[label=d];
        Q8->Q8[label=d];
        Q9->Q8[label=d];
        Q10->Q8[label=d];

}'''

# Create a Graphviz graph from the DOT code
graph = graphviz.Source(dot_code)

# Render the graph to a PNG image file
graph.render(filename='AFD', format='png')
