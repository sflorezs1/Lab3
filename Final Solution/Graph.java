public class Graph <E> {

    //ATTRIBUTES
    private Vertex[] vertices;

    //METHODS
    public Graph(){ vertices = new Vertex[10000]; }

    public void addVertex(Vertex vertex, int idx){ vertices[idx] = vertex; }

    public Vertex getVertex(int idx){ return vertices[idx]; }
}
