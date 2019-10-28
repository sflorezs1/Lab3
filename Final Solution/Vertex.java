public class Vertex <E> {
    private int head = 0;
    private E data;
    private Vertex[] neighbors = new Vertex[8];
    private boolean visited;
    private int level;

    public Vertex(E data) {
        this.data = data;
    }

    public Vertex(E data, int level) {
        this.data = data;
        this.level = level;
    }

    public void addNeighbor(Vertex<E> neighbor) {
        this.neighbors[this.head] = neighbor;
        this.head++;
    }

    public int neighborsSize() {
        return this.head + 1;
    }

    public E getData() {
        return data;
    }

    public void setData(E data) {
        this.data = data;
    }

    public Vertex[] getNeighbors() {
        return neighbors;
    }

    public void setNeighbors(Vertex[] neighbors) {
        this.neighbors = neighbors;
    }

    public boolean isVisited() {
        return visited;
    }

    public void setVisited(boolean visited) {
        this.visited = visited;
    }

    public int getLevel() {
        return level;
    }

    public void setLevel(int level) {
        this.level = level;
    }
}
