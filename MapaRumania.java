import java.util.*;

public class MapaRumania {

    // Clase que representa un nodo en el grafo (ciudad)
    private static class Nodo {
        String ciudad;
        List<Arista> aristas = new ArrayList<>();

        Nodo(String ciudad) {
            this.ciudad = ciudad;
        }
    }

    // Clase que representa una arista en el grafo (conexión entre ciudades)
    private static class Arista {
        Nodo destino;
        double costo;

        Arista(Nodo destino, double costo) {
            this.destino = destino;
            this.costo = costo;
        }
    }

    private Map<String, Nodo> grafo = new HashMap<>();

    public MapaRumania() {
        inicializarMapa();
    }

    public void inicializarMapa() {
        // Creación de nodos
        agregarNodo("Oradea");
        agregarNodo("Zerind");
        agregarNodo("Arad");
        agregarNodo("Timisoara");
        agregarNodo("Lugoj");
        agregarNodo("Mehadia");
        agregarNodo("Dobreta");
        agregarNodo("Sibiu");
        agregarNodo("RimnicuVilcea");
        agregarNodo("Craiova");
        agregarNodo("Fagaras");
        agregarNodo("Pitesti");
        agregarNodo("Giurgiu");
        agregarNodo("Bucarest");
        agregarNodo("Neamt");
        agregarNodo("Urziceni");
        agregarNodo("Iasi");
        agregarNodo("Vaslui");
        agregarNodo("Hirsova");
        agregarNodo("Eforie");

        // Creación de enlaces bidireccionales
        agregarEnlaceBidireccional("Oradea", "Zerind", 71.0);
        agregarEnlaceBidireccional("Oradea", "Sibiu", 151.0);
        agregarEnlaceBidireccional("Zerind", "Arad", 75.0);
        agregarEnlaceBidireccional("Arad", "Timisoara", 118.0);
        agregarEnlaceBidireccional("Arad", "Sibiu", 140.0);
        agregarEnlaceBidireccional("Timisoara", "Lugoj", 111.0);
        agregarEnlaceBidireccional("Lugoj", "Mehadia", 70.0);
        agregarEnlaceBidireccional("Mehadia", "Dobreta", 75.0);
        agregarEnlaceBidireccional("Dobreta", "Craiova", 120.0);
        agregarEnlaceBidireccional("Sibiu", "Fagaras", 99.0);
        agregarEnlaceBidireccional("Sibiu", "RimnicuVilcea", 80.0);
        agregarEnlaceBidireccional("RimnicuVilcea", "Pitesti", 97.0);
        agregarEnlaceBidireccional("RimnicuVilcea", "Craiova", 146.0);
        agregarEnlaceBidireccional("Craiova", "Pitesti", 138.0);
        agregarEnlaceBidireccional("Fagaras", "Bucarest", 211.0);
        agregarEnlaceBidireccional("Pitesti", "Bucarest", 101.0);
        agregarEnlaceBidireccional("Giurgiu", "Bucarest", 90.0);
        agregarEnlaceBidireccional("Bucarest", "Urziceni", 85.0);
        agregarEnlaceBidireccional("Neamt", "Iasi", 87.0);
        agregarEnlaceBidireccional("Urziceni", "Vaslui", 142.0);
        agregarEnlaceBidireccional("Urziceni", "Hirsova", 98.0);
        agregarEnlaceBidireccional("Iasi", "Vaslui", 92.0);
        agregarEnlaceBidireccional("Hirsova", "Eforie", 86.0);
    }

    private void agregarNodo(String ciudad) {
        grafo.put(ciudad, new Nodo(ciudad));
    }

    private void agregarEnlaceBidireccional(String desde, String hasta, double costo) {
        Nodo nodoDesde = grafo.get(desde);
        Nodo nodoHasta = grafo.get(hasta);
        nodoDesde.aristas.add(new Arista(nodoHasta, costo));
        nodoHasta.aristas.add(new Arista(nodoDesde, costo));
    }

    // Búsqueda en Anchura (BFS)
    public List<String> bfs(String inicio, String objetivo) {
        Queue<Nodo> frontera = new LinkedList<>();
        Set<String> explorado = new HashSet<>();
        Map<String, String> vieneDe = new HashMap<>();

        Nodo nodoInicio = grafo.get(inicio);
        frontera.add(nodoInicio);
        vieneDe.put(inicio, null);

        while (!frontera.isEmpty()) {
            Nodo actual = frontera.poll();
            if (actual.ciudad.equals(objetivo)) {
                return reconstruirCamino(vieneDe, objetivo);
            }
            explorado.add(actual.ciudad);

            for (Arista arista : actual.aristas) {
                if (!explorado.contains(arista.destino.ciudad) && !frontera.contains(arista.destino)) {
                    frontera.add(arista.destino);
                    vieneDe.put(arista.destino.ciudad, actual.ciudad);
                }
            }
        }
        return null;
    }

    // Búsqueda en Profundidad (DFS)
    public List<String> dfs(String inicio, String objetivo) {
        Stack<Nodo> frontera = new Stack<>();
        Set<String> explorado = new HashSet<>();
        Map<String, String> vieneDe = new HashMap<>();

        Nodo nodoInicio = grafo.get(inicio);
        frontera.push(nodoInicio);
        vieneDe.put(inicio, null);

        while (!frontera.isEmpty()) {
            Nodo actual = frontera.pop();
            if (actual.ciudad.equals(objetivo)) {
                return reconstruirCamino(vieneDe, objetivo);
            }
            explorado.add(actual.ciudad);

            for (Arista arista : actual.aristas) {
                if (!explorado.contains(arista.destino.ciudad) && !frontera.contains(arista.destino)) {
                    frontera.push(arista.destino);
                    vieneDe.put(arista.destino.ciudad, actual.ciudad);
                }
            }
        }
        return null;
    }

    // Búsqueda Primero el Mejor (BPE)
    public List<String> bpe(String inicio, String objetivo, Map<String, Double> heuristica) {
        PriorityQueue<Nodo> frontera = new PriorityQueue<>(Comparator.comparingDouble(n -> heuristica.get(n.ciudad)));
        Set<String> explorado = new HashSet<>();
        Map<String, String> vieneDe = new HashMap<>();

        Nodo nodoInicio = grafo.get(inicio);
        frontera.add(nodoInicio);
        vieneDe.put(inicio, null);

        while (!frontera.isEmpty()) {
            Nodo actual = frontera.poll();
            if (actual.ciudad.equals(objetivo)) {
                return reconstruirCamino(vieneDe, objetivo);
            }
            explorado.add(actual.ciudad);

            for (Arista arista : actual.aristas) {
                if (!explorado.contains(arista.destino.ciudad) && !frontera.contains(arista.destino)) {
                    frontera.add(arista.destino);
                    vieneDe.put(arista.destino.ciudad, actual.ciudad);
                }
            }
        }
        return null;
    }

    private List<String> reconstruirCamino(Map<String, String> vieneDe, String objetivo) {
        List<String> camino = new LinkedList<>();
        for (String en = objetivo; en != null; en = vieneDe.get(en)) {
            camino.add(en);
        }
        Collections.reverse(camino);
        return camino;
    }

    public static void main(String[] args) {
        MapaRumania mapa = new MapaRumania();
        Scanner scanner = new Scanner(System.in);

        System.out.println("Ingrese la ciudad de inicio: ");
        String inicio = scanner.nextLine();

        System.out.println("Ingrese la ciudad objetivo: ");
        String objetivo = scanner.nextLine();

        // Heurística (distancias aproximadas a Bucarest)
        Map<String, Double> heuristica = new HashMap<>();
        heuristica.put("Arad", 366.0);
        heuristica.put("Bucarest", 0.0);
        heuristica.put("Craiova", 160.0);
        heuristica.put("Dobreta", 242.0);
        heuristica.put("Eforie", 161.0);
        heuristica.put("Fagaras", 176.0);
        heuristica.put("Giurgiu", 77.0);
        heuristica.put("Hirsova", 151.0);
        heuristica.put("Iasi", 226.0);
        heuristica.put("Lugoj", 244.0);
        heuristica.put("Mehadia", 241.0);
        heuristica.put("Neamt", 234.0);
        heuristica.put("Oradea", 380.0);
        heuristica.put("Pitesti", 100.0);
        heuristica.put("RimnicuVilcea", 193.0);
        heuristica.put("Sibiu", 253.0);
        heuristica.put("Timisoara", 329.0);
        heuristica.put("Urziceni", 80.0);
        heuristica.put("Vaslui", 199.0);
        heuristica.put("Zerind", 374.0);

        long inicioTiempo = System.nanoTime();
        List<String> resultadoBFS = mapa.bfs(inicio, objetivo);
        long finTiempo = System.nanoTime();
        long tiempoBFS = finTiempo - inicioTiempo;
        long memoriaBFS = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        System.out.println("Resultado BFS: " + resultadoBFS);
        System.out.println("Tiempo BFS: " + tiempoBFS + " ns");
        System.out.println("Memoria BFS: " + memoriaBFS + " bytes");

        inicioTiempo = System.nanoTime();
        List<String> resultadoDFS = mapa.dfs(inicio, objetivo);
        finTiempo = System.nanoTime();
        long tiempoDFS = finTiempo - inicioTiempo;
        long memoriaDFS = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        System.out.println("\n Resultado DFS: " + resultadoDFS);
        System.out.println("Tiempo DFS: " + tiempoDFS + " ns");
        System.out.println("Memoria DFS: " + memoriaDFS + " bytes");

        inicioTiempo = System.nanoTime();
        List<String> resultadoBPE = mapa.bpe(inicio, objetivo, heuristica);
        finTiempo = System.nanoTime();
        long tiempoBPE = finTiempo - inicioTiempo;
        long memoriaBPE = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        System.out.println("\nResultado BPE: " + resultadoBPE);
        System.out.println("Tiempo BPE: " + tiempoBPE + " ns");
        System.out.println("Memoria BPE: " + memoriaBPE + " bytes");
    }
}
