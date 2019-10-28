import java.io.File;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

/**
 * @authors sflorezs1 && jdbuenol
 */
public class Main {
    
    private static boolean isIn(int[] forbidden, int item){
        for (int banned : forbidden) if (item == banned) return true;
        return false;
    }

    public static void main(String[] args) {
        System.out.print("Input? ");
        try {
            Scanner sc = new Scanner(new File(new Scanner(System.in).nextLine()));
            int testCases = Integer.parseInt(sc.nextLine());
            for (int i = 0; i < testCases; i++) {
                boolean found = false;
                int initial = Integer.parseInt(sc.nextLine().replaceAll(" ", ""));
                int target = Integer.parseInt(sc.nextLine().replaceAll(" ", ""));
                if(initial == target) System.out.println(0);
                int nForbidden = Integer.parseInt(sc.nextLine());
                int[] forbidden = new int[nForbidden];
                for (int j = 0; j < nForbidden; j++) forbidden[j] = Integer.parseInt(sc.nextLine().replaceAll(" ", ""));
                
                //Start graphing! ha!

                Vertex<Integer> currentVertex = new Vertex<>(initial);
                currentVertex.setLevel(0);
                Queue<Vertex<Integer>> queue = new LinkedList<>();
                queue.add(currentVertex);
                boolean[] graph = new boolean[10000];
                while(!queue.isEmpty()) {
                    currentVertex = queue.poll();
                    int currentValue = currentVertex.getData();
                    if (currentValue == target) {
                        found = true;
                        System.out.println(currentVertex.getLevel());
                        break;
                    } else {
                        int currentLevel = currentVertex.getLevel() + 1;
                        int someNeighbor = currentValue + (currentValue / 1000 == 9 ? -9000 : 1000);
                        if (!isIn(forbidden, someNeighbor) && !graph[someNeighbor]) {
                            queue.add(new Vertex<>(someNeighbor, currentLevel));
                            graph[someNeighbor] = true;
                        }
                        someNeighbor = currentValue - (currentValue / 1000 == 0 ? -9000 : 1000);
                        if (!isIn(forbidden, someNeighbor) && !graph[someNeighbor]) {
                            queue.add(new Vertex<>(someNeighbor, currentLevel));
                            graph[someNeighbor] = true;
                        }
                        someNeighbor = currentValue + ((currentValue / 100) % 10 == 9 ? -900 : 100);
                        if (!isIn(forbidden, someNeighbor) && !graph[someNeighbor]) {
                            queue.add(new Vertex<>(someNeighbor, currentLevel));
                            graph[someNeighbor] = true;
                        }
                        someNeighbor = currentValue - ((currentValue / 100) % 10 == 0 ? -900 : 100);
                        if (!isIn(forbidden, someNeighbor) && !graph[someNeighbor]) {
                            queue.add(new Vertex<>(someNeighbor, currentLevel));
                            graph[someNeighbor] = true;
                        }
                        someNeighbor = currentValue + ((currentValue / 10) % 10 == 9 ? -90 : 10);
                        if (!isIn(forbidden, someNeighbor) && !graph[someNeighbor]) {
                            queue.add(new Vertex<>(someNeighbor, currentLevel));
                            graph[someNeighbor] = true;
                        }
                        someNeighbor = currentValue - ((currentValue / 10) % 10 == 0 ? -90 : 10);
                        if (!isIn(forbidden, someNeighbor) && !graph[someNeighbor]) {
                            queue.add(new Vertex<>(someNeighbor, currentLevel));
                            graph[someNeighbor] = true;
                        }
                        someNeighbor = currentVertex.getData() + (currentValue % 10 == 9 ? -9 : 1);
                        if (!isIn(forbidden, someNeighbor) && !graph[someNeighbor]) {
                            queue.add(new Vertex<>(someNeighbor, currentLevel));
                            graph[someNeighbor] = true;
                        }
                        someNeighbor = currentVertex.getData() - (currentValue % 10 == 0 ? -9 : 1);
                        if (!isIn(forbidden, someNeighbor) && !graph[someNeighbor]) {
                            queue.add(new Vertex<>(someNeighbor, currentLevel));
                            graph[someNeighbor] = true;
                        }
                    }
                }
                if (!found) System.out.println(-1);
                if(sc.hasNext())sc.nextLine();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}