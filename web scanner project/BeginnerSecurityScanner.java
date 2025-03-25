import java.io.*;
import java.net.Socket;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Pattern;

public class BeginnerSecurityScanner {

    private static final List<String> ADMIN_PATHS = Arrays.asList("/admin", "/dashboard", "/login", "/wp-admin");
    private static final Pattern SENSITIVE_INFO_PATTERN = Pattern.compile(
            "(api[_-]?key|password|secret|token)", Pattern.CASE_INSENSITIVE);

    public static void checkHTTPS(String url) {
        if (url.startsWith("https://")) {
            System.out.println("GOOD: The website is using HTTPS.");
        } else {
            System.out.println("WARNING: The website is not using HTTPS. Data might not be encrypted.");
        }
    }

    private static String sendHttpRequest(String host, String path) {
        StringBuilder response = new StringBuilder();
        try (Socket socket = new Socket(host, 80)) {
            OutputStream out = socket.getOutputStream();
            PrintWriter writer = new PrintWriter(out, true);

            String request = "GET " + path + " HTTP/1.1\r\n" +
                             "Host: " + host + "\r\n" +
                             "Connection: close\r\n\r\n";
            writer.println(request);

            InputStream in = socket.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(in));

            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line).append("\n");
            }
        } catch (IOException e) {
            System.out.println("Error sending HTTP request: " + e.getMessage());
        }
        return response.toString();
    }

    public static void checkOpenAdminPage(String host) {
        for (String path : ADMIN_PATHS) {
            String response = sendHttpRequest(host, path);
            if (response.contains("HTTP/1.1 200 OK")) {
                System.out.println("WARNING: Admin page " + path + " is accessible without authentication!");
            } else if (response.contains("HTTP/1.1 302 Found") || response.contains("HTTP/1.1 403 Forbidden")) {
                System.out.println("WARNING: Admin page " + path + " might be exposed (Redirect or Forbidden).");
            } else {
                System.out.println("GOOD: " + path + " is secured.");
            }
        }
    }

    public static void checkExposedInfo(String host) {
        String response = sendHttpRequest(host, "/");
        if (SENSITIVE_INFO_PATTERN.matcher(response).find()) {
            System.out.println("WARNING: The website might be exposing sensitive information!");
        } else {
            System.out.println("GOOD: No sensitive info detected on the main page.");
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the website (e.g., example.com): ");
        String host = scanner.nextLine().trim();
        scanner.close();

        if (host.isEmpty()) {
            System.out.println("Error: No website entered.");
            return;
        }

        System.out.println("\nScanning host: " + host);
        checkHTTPS("http://" + host);  
        checkOpenAdminPage(host);    
        checkExposedInfo(host);       
    }
}
