import java.io.*;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;

public class NetworkingUtils {

    private static final List<String> ADMIN_PATHS = Arrays.asList("/admin", "/dashboard", "/login", "/wp-admin");
    private static final Pattern SENSITIVE_INFO_PATTERN = Pattern.compile(
            "(api[_-]?key|password|secret|token)", Pattern.CASE_INSENSITIVE);

    public static String sendHttpRequest(String host, String path) {
        StringBuilder response = new StringBuilder();
        try (Socket socket = new Socket(host, 80)) {
            OutputStream out = socket.getOutputStream();
            PrintWriter writer = new PrintWriter(out, true);
            
            // Send HTTP request
            String request = "GET " + path + " HTTP/1.1\r\n" +
                             "Host: " + host + "\r\n" +
                             "Connection: close\r\n\r\n";
            writer.println(request);

            // Read HTTP response
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

    public static void getDNSInfo(String host) {
        try {
            InetAddress address = InetAddress.getByName(host);
            System.out.println("\n🔍 DNS Lookup for: " + host);
            System.out.println("📌 IP Address: " + address.getHostAddress());
            System.out.println("📡 Hostname: " + address.getHostName());
        } catch (UnknownHostException e) {
            System.out.println("❌ ERROR: Could not resolve DNS for " + host);
        }
    }

    public static void checkHTTPS(String url) {
        if (url.startsWith("https://")) {
            System.out.println("GOOD: The website is using HTTPS.");
        } else {
            System.out.println("WARNING: The website is not using HTTPS. Data might not be encrypted.");
            RiskAssessment.printRiskLevel(RiskLevel.HIGH);  // Unencrypted HTTP is a high risk
        }
    }

    public static void checkOpenAdminPage(String host) {
        for (String path : ADMIN_PATHS) {
            String response = sendHttpRequest(host, path);
            RiskLevel risk = RiskAssessment.assessRisk(response);
            RiskAssessment.printRiskLevel(risk);
        }
    }

    public static void checkExposedInfo(String host) {
        String response = sendHttpRequest(host, "/");
        if (SENSITIVE_INFO_PATTERN.matcher(response).find()) {
            System.out.println("WARNING: The website might be exposing sensitive information!");
            RiskAssessment.printRiskLevel(RiskLevel.HIGH);
        } else {
            System.out.println("GOOD: No sensitive info detected on the main page.");
        }
    }
}
