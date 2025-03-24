import java.util.Scanner;

public class SecurityScanner {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter the website (e.g., example.com): ");
        String host = scanner.nextLine().trim();
        scanner.close();

        if (host.isEmpty()) {
            System.out.println("Error: No website entered.");
            return;
        }

        System.out.println("\n🔍 Scanning host: " + host);

        // Perform DNS Lookup
        NetworkingUtils.getDNSInfo(host);

        // Check for HTTPS (networking)
        NetworkingUtils.checkHTTPS("http://" + host);  // Use http:// to check for unencrypted traffic

        // Check for open admin pages (vulnerability assessment)
        NetworkingUtils.checkOpenAdminPage(host);

        // Check for exposed sensitive information (vulnerability assessment)
        NetworkingUtils.checkExposedInfo(host);
    }
}
